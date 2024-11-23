from smbus2 import SMBus


class LEDController:
    def __init__(self):
        self.i2c_addr = 0x77
        self.i2c = 1

    def set_led(self, index: int, rgb: tuple[int, int, int]):
        try:
            start_reg = 3 if index == 0 else 6
            with SMBus(self.i2c) as bus:
                bus.write_byte_data(self.i2c_addr, start_reg, rgb[0])
                bus.write_byte_data(self.i2c_addr, start_reg + 1, rgb[1])
                bus.write_byte_data(self.i2c_addr, start_reg + 2, rgb[2])
        except Exception as e:
            print(f"Error setting LED: {e}")


leds = LEDController()


def set_eye_color(left: tuple[int, int, int], right: tuple[int, int, int]):
    leds.set_led(0, left)
    leds.set_led(1, right)
