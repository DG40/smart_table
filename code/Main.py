if __name__ == '__main__':
    import time
    from select_game import SelectedGame
    import useful_box
    from useful_box import LED_COUNT as LED_COUNT
    from useful_box import LED_PIN as LED_PIN
    from useful_box import LED_FREQ_HZ as LED_FREQ_HZ
    from useful_box import LED_DMA as LED_DMA
    from useful_box import LED_INVERT as LED_INVERT
    from useful_box import LED_BRIGHTNESS as LED_BRIGHTNESS
    from useful_box import LED_CHANNEL as LED_CHANNEL
    from useful_box import LED_STRIP as LED_STRIP

    from rpi_ws281x import *
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL,
                              LED_STRIP)
    strip.begin()
    useful_box.clear_leds(strip)
    selected_game = SelectedGame()

    while True:
        strip.setBrightness(0)
        useful_box.clear_leds(strip)
        useful_box.color_leds_start(strip)
        useful_box.soft_up_brightness(strip)
        print(useful_box.ANSI_GREEN + 'Choose GAME please' + useful_box.ANSI_RESET)
        time.sleep(1)
        white_level = 0
        flag_toggle_white = True
        game_number = -1
        while game_number == -1:
            vote_checkers, vote_tik_tak_toe, vote_reversi = (0, 0, 0)
            active_cells = 0
            useful_box.color_leds_wait(strip, white_level)
            if flag_toggle_white:
                white_level += 1
            else:
                white_level -= 1
            if white_level in (0, 100):
                flag_toggle_white = not flag_toggle_white
            useful_box.data_processing(useful_box.BUF_SELECT_GAME)
            for i in range(8):
                for j in range(8):
                    if useful_box.cells[i][j] == 1:
                        active_cells += 1
                    if useful_box.dry_data[i][j] == 1:
                        if i < 3 and j < 3:
                            vote_checkers += 1
                        elif i < 3 and j >= 3:
                            vote_tik_tak_toe += 1
                        elif i >= 3 and j < 3:
                            vote_reversi += 1
            if active_cells >= useful_box.EXIT_COUNT:
                game_number = 0  # Service Mode
                break
            elif vote_checkers >= 2:
                game_number = 1  # Checkers
            elif vote_tik_tak_toe >= 2:
                game_number = 2  # Tik Tak Toe
            elif vote_reversi >= 2:
                game_number = 3  # Reversi
        selected_game.choice_the_game(game_number)
        selected_game.start_the_game(strip)
