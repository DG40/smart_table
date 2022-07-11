import time
from variables import *
from rpi_ws281x import *


class DevOp:
    def __init__(self):
        self.players = False

    def play(self, strip):  # Need get from sensors
        ClearLeds(strip)
        Soft_up_brightness(strip)
        time.sleep(1)

        while True:

            DataProcessing(buf_developer)

            for i in range(8):
                for j in range(8):
                    if DryData[i][j] == 1:
                        r, g, b, w = 200, 200, 200, 200
                        strip.setPixelColor(order[i * 2][j * 2], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2 + 1][j * 2], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2][j * 2 + 1], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(r, g, b, w))
                    else:
                        r, g, b, w = 0, 0, 0, 0
                        strip.setPixelColor(order[i * 2][j * 2], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2 + 1][j * 2], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2][j * 2 + 1], Color(r, g, b, w))
                        strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(r, g, b, w))
            strip.show()

    def playRaw(self, strip):  # (need get from sensors)
        ClearLeds(strip)
        Soft_up_brightness(strip)
        time.sleep(1)
        while True:
            DataProcessing(buf_developer)
            time.sleep(0.01)
            active_cells = 0
            for i in range(8):
                for j in range(8):
                    if DryData[i][j] == 1:
                        active_cells += 1
                    if RawData[i][j] < 255:
                        r = RawData[i][j]
                        g = RawData[i][j]
                        b = RawData[i][j]
                        w = RawData[i][j]
                    else:
                        r = 255
                        g = 255
                        b = 255
                        w = 255
                    strip.setPixelColor(order[i * 2][j * 2], Color(r, g, b, w))
                    strip.setPixelColor(order[i * 2 + 1][j * 2], Color(r, g, b, w))
                    strip.setPixelColor(order[i * 2][j * 2 + 1], Color(r, g, b, w))
                    strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(r, g, b, w))
            print(active_cells)
            if active_cells >= switch_count_developer:
                Soft_down_brightness(strip)
                break
            else:
                strip.show()
