import time
from rpi_ws281x import *
from table import Table
from variables import *

if __name__ == '__main__':

    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                              LED_STRIP)
    strip.begin()

    for i in range(16):
        for j in range(16):
            strip.setPixelColor(order[i][j], Color(0, 0, 0, 0))
    strip.show()

    obj_table = Table()

    while True:
        strip.setBrightness(0)
        ClearLeds(strip)
        obj_table.ColoringTable_Start(strip)
        Soft_up_brightness(strip)
        time.sleep(1)
        print(ansi_green + 'Choose GAME please' + ansi_reset)
        game_number = -1
        k = 0  # - counter for soft pulses of LED's light
        flag = False

        while game_number == -1:

            DataProcessing(buf_developer)
            time.sleep(0.01)
            active_cells = 0

            obj_table.ColoringTable_Wait(strip, k)

            if not flag:
                k += 1
            else:
                k -= 1

            if k == 0 or k == 50:  # 50 - picked up empirically for soft pulses of LED's light
                flag = not flag

            vote_Checkers = 0
            vote_TikTakToe = 0
            active_cells = 0

            DataProcessing(buf_selectgame)
            time.sleep(0.01)  # - for prettier LEDs effect

            for i in range(8):
                for j in range(8):
                    if Cells[i][j] == 1:
                        active_cells += 1
                    if DryData[i][j] == 1:
                        if j < 3:
                            vote_Checkers += 1
                        else:
                            vote_TikTakToe += 1

            print(vote_TikTakToe)
            if active_cells >= switch_count:
                game_number = 0  # Developer Mode
                break
            elif vote_Checkers >= 4:
                game_number = 1  # Checkers
            elif vote_TikTakToe >= 4:
                game_number = 2  # TikTakToe

        obj_table.select_game(game_number)  # Need get from sensors
        obj_table.start_game(strip)
