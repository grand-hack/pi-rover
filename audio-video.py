#
# Usage: python3 record_and_play.py -m MEETING_URL
#
import sys
sys.path.append('TurboPi')
import argparse
import threading
import time

from daily import *
import cv2
import pyaudio
import HiwonderSDK.mecanum as mecanum

VIDEO_FPS = 10
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
SAMPLE_RATE = 48000
NUM_CHANNELS = 1
AUDIO_OUT_CHUNKS = 256 # safe number of samples to read/write. restart process if audio is scratchy.

chassis = mecanum.MecanumChassis()

class PyAudioApp(EventHandler):
    def __init__(self, sample_rate, num_channels):
        self.__app_quit = False        
        self.__sample_rate = sample_rate
        self.__num_channels = num_channels

        # Video capture initialization
        self.__camera = Daily.create_camera_device(
            "my-camera", width=VIDEO_WIDTH, height=VIDEO_HEIGHT, color_format="RGB"
        )
        self.__capcam = cv2.VideoCapture(0)
        if not self.__capcam.isOpened():
            raise RuntimeError("Error: Could not open camera")
        self.__capcam.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH) 
        self.__capcam.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
        
        # Start video capture thread
        self.__video_thread = threading.Thread(target=self.capture_video_stream)
        self.__video_thread.daemon = True  # Thread will close when main program exits
        self.__video_thread.start()

        # We configure the microphone as non-blocking so we don't block PyAudio
        # when we write the frames.
        self.__virtual_mic = Daily.create_microphone_device(
            "my-mic", sample_rate=sample_rate, channels=num_channels, non_blocking=True
        )

        # In contrast, we configure the speaker as blocking. In this case, we
        # read audio from the speaker and synchronously write to PyAudio's
        # output stream.
        self.__virtual_speaker = Daily.create_speaker_device(
            "my-speaker",
            sample_rate=sample_rate,
            channels=num_channels,
        )
        Daily.select_speaker_device("my-speaker")

        self.__pyaudio = pyaudio.PyAudio()
        self.__input_stream = self.__pyaudio.open(
            # input_device_index=2,
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            input=True,
            stream_callback=self.on_input_stream,
        )
        self.__output_stream = self.__pyaudio.open(
            output_device_index=0,
            format=pyaudio.paInt16, channels=num_channels, rate=sample_rate, output=True,
            frames_per_buffer=AUDIO_OUT_CHUNKS
        )

        self.__client = CallClient(self)

        self.__client.update_subscription_profiles(
            {"base": {"camera": "unsubscribed", "microphone": "subscribed"}}
        )

        self.__thread = threading.Thread(target=self.send_audio_stream)
        self.__thread.start()

    def on_joined(self, data, error):
        if error:
            print(f"Unable to join meeting: {error}")
            self.__app_quit = True

    def capture_video_stream(self):
        frame_delay = 1/VIDEO_FPS
        frame_count = 0
        
        while not self.__app_quit:
            start_time = time.time()
            
            ret, frame = self.__capcam.read()
            if not ret:
                print("Error: Can't receive frame")
                continue
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.__camera.write_frame(rgb_frame.tobytes())
            frame_count += 1                          
            while (time.time() - start_time) < frame_delay:
                time.sleep(0.001)

    def run(self, meeting_url):
        self.__client.join(
            meeting_url,
            client_settings={
                "inputs": {
                    "camera": {"isEnabled": True, "settings": {"deviceId": "my-camera"}},
                    "microphone": {
                        "settings": {
                            "deviceId": "my-mic",
                            "customConstraints": {
                                "autoGainControl": {"exact": True},
                                "noiseSuppression": {"exact": True},
                                "echoCancellation": {"exact": True},
                            },
                        },
                    },
                },
                "publishing": {
                    "microphone": {
                        "isPublishing": True,
                        "sendSettings": {
                            "channelConfig": "stereo" if self.__num_channels == 2 else "mono",
                        },
                    },
                    "camera": { "isPublishing": True }
                },
            },
            completion=self.on_joined,
        )
        # self.__thread.join()

    def leave(self):
        self.__app_quit = True
        self.__client.leave()
        self.__client.release()
        # This is not very pretty (taken from PyAudio docs).
        while self.__input_stream.is_active():
            time.sleep(0.1)
        self.__input_stream.close()
        self.__pyaudio.terminate()

    def on_input_stream(self, in_data, frame_count, time_info, status):
        if self.__app_quit:
            return None, pyaudio.paAbort
        # If the microphone hasn't started yet `write_frames` this will return
        # 0. In that case, we just tell PyAudio to continue.
        self.__virtual_mic.write_frames(in_data)
        return None, pyaudio.paContinue

    def send_audio_stream(self):
        num_frames = AUDIO_OUT_CHUNKS
        while not self.__app_quit:
            audio = self.__virtual_speaker.read_frames(num_frames)
            if audio:
                self.__output_stream.write(audio)
            else:
                time.sleep(0)
        self.__output_stream.close()

    # Daily event handlers
    def on_participant_joined(self, participant):
        print("PARTICIPANT JOINED", participant)

    def on_app_message(self, message, sender):
        print("APP MESSAGE", message)
        cmd = message["message"]
        if cmd == 'move':
            chassis.set_velocity(50,90,0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--meeting", required=True, help="Meeting URL")
    parser.add_argument(
        "-c", "--channels", type=int, default=NUM_CHANNELS, help="Number of channels"
    )
    parser.add_argument("-r", "--rate", type=int, default=SAMPLE_RATE, help="Sample rate")
    args = parser.parse_args()

    Daily.init()

    app = PyAudioApp(args.rate, args.channels)

    try:
        app.run(args.meeting)
        print("post RUN")
        time.sleep(300)
    except KeyboardInterrupt:
        print("Ctrl-C detected. Exiting!")
    finally:
        chassis.set_velocity(0,0,0)
        app.leave()


if __name__ == "__main__":
    main()
