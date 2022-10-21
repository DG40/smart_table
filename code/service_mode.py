import time
from test_on_off_sensors import ShiftRegister
from rpi_ws281x import *
import useful_box


class ServiceMode:
    def __init__(self):
        self.players = False

    def play(self, strip):  # Need get from sensors
        useful_box.clear_leds(strip)
        useful_box.soft_up_brightness(strip)
        time.sleep(1)

        while True:
            useful_box.data_processing(useful_box.BUF_SERVICE)

            for i in range(8):
                for j in range(8):
                    if useful_box.dry_data[i][j] == 1:
                        color = 200, 200, 200, 200
                    else:
                        color = 0, 0, 0, 0
                    useful_box.color_cell(strip, i, j, color)
            strip.show()

    def led_grid(self, strip):
        for i in range(2, 6):
            for j in range(2, 6):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(180, 0, 0, 0))
        for i in range(2, 6):
            for j in range(10, 14):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(0, 180, 0, 0))
        for i in range(10, 14):
            for j in range(2, 6):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(0, 0, 180, 0))
        for i in range(10, 14):
            for j in range(10, 14):
                strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(125, 0, 125, 0))
        strip.show()

    def play_raw(self, strip):  # Need get from sensors
        useful_box.clear_leds(strip)
        self.led_grid(strip)
        useful_box.soft_up_brightness(strip)

        print(useful_box.ANSI_YELLOW + 'Choose CHECKING OPTION please' + useful_box.ANSI_RESET)

        while True:

            useful_box.data_processing(useful_box.BUF_SERVICE)

            vote_on_off = 0
            vote_light = 0
            vote_leds = 0
            vote_sensors = 0

            active_cells = 0

            useful_box.data_processing(useful_box.BUF_SELECT_GAME)
            time.sleep(0.01)

            for i in range(8):
                for j in range(8):
                    if useful_box.dry_data[i][j] == 1:
                        active_cells += 1
                        if i < 3 and j < 3:
                            vote_on_off += 1
                        elif i < 3 and j >= 5:
                            vote_light += 1
                        elif i >= 5 and j < 3:
                            vote_leds += 1
                        elif i >= 5 and j >= 3:
                            vote_sensors += 1

            if active_cells >= useful_box.EXIT_COUNT_SERVICE:
                useful_box.soft_down_brightness(strip)
                useful_box.clear_leds(strip)
                break
            elif vote_on_off >= 3:
                self.check_sensors(strip)
            elif vote_light >= 3:
                self.check_light(strip)
            elif vote_leds >= 3:
                self.check_leds(strip)
            elif vote_sensors >= 3:
                self.check_sensors_simple(strip)

    def check_sensors(self, strip):  # RED - on/off sensors
        on_off_cells = ((3, 3), (3, 4), (4, 3), (4, 4))

        useful_box.soft_down_brightness(strip)
        useful_box.clear_leds(strip)
        useful_box.soft_up_brightness(strip)

        shift = ShiftRegister()
        flag_off = False
        flag_after = False

        time.sleep(1)
           
        while True:
            useful_box.data_processing(useful_box.BUF_SERVICE)
            active_cells = 0
            exit_cells = 0
            for i in range(8):
                for j in range(8):
                    if useful_box.dry_data[i][j] == 1:
                        if (i, j) in on_off_cells:
                            active_cells += 1
                        else:
                            exit_cells += 1
                        color = (255, 255, 255, 255)
                    else:
                        c = useful_box.raw_data[i][j]
                        color = (c, c, c, c)
                    useful_box.color_cell(strip, i, j, color)
            
            if not flag_off and not flag_after and active_cells >= useful_box.SWITCH_COUNT_SERVICE:
                print(useful_box.ANSI_YELLOW + 'SWITCH ON' + useful_box.ANSI_RESET)
                flag_off = True
                tic = time.perf_counter()
                shift.switch(True)
                useful_box.soft_down_brightness(strip)
                useful_box.color_leds(strip, (30, 30, 0, 0))
                useful_box.soft_up_brightness(strip)
                time.sleep(1)
                useful_box.soft_down_brightness(strip)
                useful_box.clear_leds(strip)
                useful_box.soft_up_brightness(strip)
            elif not flag_off and not flag_after and exit_cells >= useful_box.EXIT_COUNT_SERVICE:
                useful_box.soft_down_brightness(strip)
                useful_box.clear_leds(strip)
                self.led_grid(strip)
                useful_box.soft_up_brightness(strip)
                time.sleep(1)
                break
            else:
                strip.show()

            if flag_off:
                toc = time.perf_counter()
                if toc - tic > 10:
                    shift.switch(False)
                    print(useful_box.ANSI_YELLOW + 'SWITCH OFF' + useful_box.ANSI_RESET)
                    tic = time.perf_counter()
                    flag_off = False
                    flag_after = True
            elif flag_after:
                toc = time.perf_counter()
                if toc - tic > 10:
                    flag_after = False
            
    def check_leds(self, strip):  # BLUE - leds
        useful_box.soft_down_brightness(strip)
        useful_box.clear_leds(strip)
        useful_box.soft_up_brightness(strip)
        flag_exit = False
        flag_tic_toc = False
        r, g, b, w = (0, 0, 0, 0)
        colormode = 1
        while True:
            if colormode == 0:
                r, g, b, w = (255, 255, 255, 255)
            elif colormode == 1:
                r, g, b, w = (255, 0, 0, 0)
            elif colormode == 2:
                r, g, b, w = (0, 255, 0, 0)
            elif colormode == 3:
                r, g, b, w = (0, 0, 255, 0)
            elif colormode == 4:
                r, g, b, w = (0, 0, 0, 255)

            if not flag_tic_toc:
                for i in range(16):
                    for j in range(16):
                        if useful_box.check_exit():
                            useful_box.soft_down_brightness(strip)
                            useful_box.clear_leds(strip)
                            self.led_grid(strip)
                            useful_box.soft_up_brightness(strip)
                            time.sleep(1)
                            flag_exit = True
                            break
                        else:
                            strip.setPixelColor(useful_box.LEDS_ORDER[i][j], Color(r, g, b, w))
                            strip.show()
                    if flag_exit:
                        break
                if flag_exit:
                    break

                tic = time.perf_counter()
                flag_tic_toc = True

            else:
                if useful_box.check_exit():
                    useful_box.soft_down_brightness(strip)
                    useful_box.clear_leds(strip)
                    self.led_grid(strip)
                    useful_box.soft_up_brightness(strip)
                    time.sleep(1)
                    break
                toc = time.perf_counter()
                if toc - tic > 5:
                    flag_tic_toc = False
                    useful_box.soft_down_brightness(strip)
                    useful_box.clear_leds(strip)
                    useful_box.soft_up_brightness(strip)

                    if colormode < 4:
                        colormode += 1
                    else:
                        colormode = 1

    def check_light(self, strip):  # GREEN - bright (luminance)
        useful_box.clear_leds(strip)
        time.sleep(1)
        from luxmeters import BH1750
        from luxmeters import create_lum_sensors
        from luxmeters import light_level
        sensor_1, sensor_2 = create_lum_sensors()
        while True:
            if useful_box.check_exit():
                useful_box.soft_down_brightness(strip)
                useful_box.clear_leds(strip)
                self.led_grid(strip)
                useful_box.soft_up_brightness(strip)
                time.sleep(1)
                break
            else:
                levels = list(light_level(sensor_1, sensor_2))
                for i in range(len(levels)):
                    if levels[i] > 1000:
                        levels[i] = 1000
                level = sum(levels) // 4
                if level > 255:
                    level = 255
                for i in range(2):
                    useful_box.color_cell(strip, 3, 3 + i, (0, 0, 0, level))
                    useful_box.color_cell(strip, 4, 3 + i, (0, 0, 0, level))
                strip.show()
                print(levels, level)

    def check_sensors_simple(self, strip):  # PURPLE - check sensors
        useful_box.soft_down_brightness(strip)
        useful_box.clear_leds(strip)
        useful_box.soft_up_brightness(strip)
        time.sleep(1)
        while True:
            useful_box.data_processing(useful_box.BUF_SERVICE)
            exit_cells = 0
            for i in range(8):
                for j in range(8):
                    if useful_box.dry_data[i][j] == 1:
                        exit_cells += 1
                        color = (255, 255, 255, 255)
                    else:
                        c = useful_box.raw_data[i][j]
                        color = (c, c, c, c)
                    useful_box.color_cell(strip, i, j, color)
            if exit_cells >= useful_box.EXIT_COUNT_SERVICE:
                useful_box.soft_down_brightness(strip)
                useful_box.clear_leds(strip)
                self.led_grid(strip)
                useful_box.soft_up_brightness(strip)
                time.sleep(1)
                break
            else:
                strip.show()
