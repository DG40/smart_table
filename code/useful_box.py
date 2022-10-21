import os
import time
from rpi_ws281x import *
import RPi.GPIO as GPIO

ANSI_BLACK = "\u001b[30m"
ANSI_RED = "\u001b[31m"
ANSI_GREEN = "\u001b[32m"
ANSI_YELLOW = "\u001b[33m"
ANSI_BLUE = "\u001b[34m"
ANSI_MAGENTA = "\u001b[35m"
ANSI_CYAN = "\u001b[36m"
ANSI_WHITE = "\u001b[37m"
ANSI_RESET = "\u001b[0m"

# SENSORS

S0_PIN = 26
S1_PIN = 19
S2_PIN = 13
E_PIN = 21

S_0 = (0, 1, 0, 1, 1, 1, 0, 0)
S_1 = (1, 0, 0, 1, 0, 1, 1, 0)
S_2 = (0, 0, 0, 0, 1, 1, 1, 1)

M1 = 22
M2 = 11
M3 = 5
M4 = 6
M5 = 25
M6 = 24
M7 = 17
M8 = 27

M = (M1, M2, M3, M4, M5, M6, M7, M8)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(M1, GPIO.IN)
GPIO.setup(M2, GPIO.IN)
GPIO.setup(M3, GPIO.IN)
GPIO.setup(M4, GPIO.IN)
GPIO.setup(M5, GPIO.IN)
GPIO.setup(M6, GPIO.IN)
GPIO.setup(M7, GPIO.IN)
GPIO.setup(M8, GPIO.IN)

GPIO.setup(S0_PIN, GPIO.OUT)
GPIO.setup(S1_PIN, GPIO.OUT)
GPIO.setup(S2_PIN, GPIO.OUT)
GPIO.setup(E_PIN, GPIO.OUT)

GPIO.output(E_PIN, False)

# SENSORS DATA

cells = [  # Cells[0-7][0-7]
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]
]

raw_data = [  # [0-7][0-7]
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

dry_data = [  # [0-7][0-7]
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]
]

BUF_CHECKERS = 70
BUF_TIK_TAK_TOE = 1
BUF_REVERSI = 1600
BUF_SELECT_GAME = 100
EXIT_COUNT = 9

BUF_SERVICE = 100
EXIT_COUNT_SERVICE = 7
SWITCH_COUNT_SERVICE = 4

FLAG_EXIT = False

def read_cells(buf):
    for j in range(len(S_0)):
        GPIO.output(S0_PIN, S_0[j])
        GPIO.output(S1_PIN, S_1[j])
        GPIO.output(S2_PIN, S_2[j])
        for i in range(len(M)):
            cells[i][j] = GPIO.input(M[i])
            if cells[i][j] == 1 and raw_data[i][j] < buf:
                raw_data[i][j] += 1
                if raw_data[i][j] == buf:
                    dry_data[i][j] = 1
                else:
                    dry_data[i][j] = 0
            else:
                raw_data[i][j] = 0


def data_processing(buf):
    for j in range(len(S_0)):
        GPIO.output(S0_PIN, S_0[j])
        GPIO.output(S1_PIN, S_1[j])
        GPIO.output(S2_PIN, S_2[j])
        for i in range(len(M)):
            cells[i][j] = GPIO.input(M[i])
            if cells[i][j] == 1:
                if raw_data[i][j] < buf:
                    raw_data[i][j] += 1
                elif raw_data[i][j] == buf:
                    dry_data[i][j] = 1
            else:
                raw_data[i][j] = 0
                dry_data[i][j] = 0


def print_data():
    print('  ', 0, 1, 2, 3, 4, 5, 6, 7, sep='')
    print('  ', '--------', sep='')
    for i in range(len(M)):
        print(i, '|', sep='', end='')
        for j in range(len(S_0)):
            print(ANSI_YELLOW + str(dry_data[i][j]) + ANSI_RESET, end='')
        print()
    print()


def print_active_cells():
    os.system('clear')
    print('  ', 0, 1, 2, 3, 4, 5, 6, 7, sep='')
    print('  ', '--------', sep='')
    for i in range(len(M)):
        print(i, '|', sep='', end='')
        for j in range(len(S_0)):
            print(ANSI_YELLOW + str(1 if raw_data[i][j] else 0) + ANSI_RESET, end='')
        print()
    print()


def check_exit():
    data_processing(BUF_SERVICE)
    active_cells = 0
    for i in range(8):
        for j in range(8):
            if dry_data[i][j] == 1:
                active_cells += 1
    if active_cells >= SWITCH_COUNT_SERVICE:
        return True


# FOR TIK-TAK-TOE GAME:
CELL_1 = ((1, 1), (1, 2), (2, 1), (2, 2))
CELL_2 = ((1, 3), (1, 4), (2, 3), (2, 4))
CELL_3 = ((1, 5), (1, 6), (2, 5), (2, 6))
CELL_4 = ((3, 1), (3, 2), (4, 1), (4, 2))
CELL_5 = ((3, 3), (3, 4), (4, 3), (4, 4))
CELL_6 = ((3, 5), (3, 6), (4, 5), (4, 6))
CELL_7 = ((5, 1), (5, 2), (6, 1), (6, 2))
CELL_8 = ((5, 3), (5, 4), (6, 3), (6, 4))
CELL_9 = ((5, 5), (5, 6), (6, 5), (6, 6))
CELLS_TIK_TAK = (CELL_1, CELL_2, CELL_3, CELL_4, CELL_5, CELL_6, CELL_7, CELL_8, CELL_9)

# FOR CHECKERS GAME
battlefield = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

# LEDS DATA
LED_COUNT = 256  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 650000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812W_STRIP
LEDS_ORDER = (
    (56, 55, 40, 39, 24, 23, 8, 7, 248, 247, 232, 231, 216, 215, 200, 199),
    (57, 54, 41, 38, 25, 22, 9, 6, 249, 246, 233, 230, 217, 214, 201, 198),
    (58, 53, 42, 37, 26, 21, 10, 5, 250, 245, 234, 229, 218, 213, 202, 197),
    (59, 52, 43, 36, 27, 20, 11, 4, 251, 244, 235, 228, 219, 212, 203, 196),
    (60, 51, 44, 35, 28, 19, 12, 3, 252, 243, 236, 227, 220, 211, 204, 195),
    (61, 50, 45, 34, 29, 18, 13, 2, 253, 242, 237, 226, 221, 210, 205, 194),
    (62, 49, 46, 33, 30, 17, 14, 1, 254, 241, 238, 225, 222, 209, 206, 193),
    (63, 48, 47, 32, 31, 16, 15, 0, 255, 240, 239, 224, 223, 208, 207, 192),
    (64, 79, 80, 95, 96, 111, 112, 127, 128, 143, 144, 159, 160, 175, 176, 191),
    (65, 78, 81, 94, 97, 110, 113, 126, 129, 142, 145, 158, 161, 174, 177, 190),
    (66, 77, 82, 93, 98, 109, 114, 125, 130, 141, 146, 157, 162, 173, 178, 189),
    (67, 76, 83, 92, 99, 108, 115, 124, 131, 140, 147, 156, 163, 172, 179, 188),
    (68, 75, 84, 91, 100, 107, 116, 123, 132, 139, 148, 155, 164, 171, 180, 187),
    (69, 74, 85, 90, 101, 106, 117, 122, 133, 138, 149, 154, 165, 170, 181, 186),
    (70, 73, 86, 89, 102, 105, 118, 121, 134, 137, 150, 153, 166, 169, 182, 185),
    (71, 72, 87, 88, 103, 104, 119, 120, 135, 136, 151, 152, 167, 168, 183, 184)
)


# LEDS FUNCTIONS

def print_leds(strip):
    print_data()
    for i in range(8):
        for j in range(8):
            if dry_data[i][j] == 1:
                color = (0, 0, 255, 255)
            else:
                color = (0, 0, 0, 0)
            color_cell(strip, i, j, color)
    strip.show()


def soft_brightness(strip):
    i = 255
    while i > 50:
        strip.setBrightness(i)
        strip.show()
        i -= 5
    while i <= 255:
        strip.setBrightness(i)
        strip.show()
        i += 5


def soft_down_brightness(strip):
    i = 255
    while i >= 0:
        strip.setBrightness(i)
        strip.show()
        i -= 5


def soft_up_brightness(strip):
    i = 0
    while i <= 255:
        strip.setBrightness(i)
        strip.show()
        i += 15


def color_leds(strip, color, cells_pause: float = 0, rows_pause: float = 0):
    r, g, b, w = color[0], color[1], color[2], color[3]
    for i in range(16):
        for j in range(16):
            strip.setPixelColor(LEDS_ORDER[i][j], Color(r, g, b, w))
            if cells_pause:
                strip.show()
                time.sleep(cells_pause)
        if rows_pause:
            strip.show()
            time.sleep(rows_pause)
    if not cells_pause and not rows_pause:
        strip.show()


def clear_leds(strip):
    color_leds(strip, (0, 0, 0, 0))


def slide_leds(strip, color):
    color_leds(strip, color, rows_pause=0.02)


def color_cell(strip, x, y, color):
    r, g, b, w = color
    for i in range(2):
        for j in range(2):
            strip.setPixelColor(LEDS_ORDER[x * 2 + i][y * 2 + j], Color(r, g, b, w))


def color_leds_start(strip):
    for i in range(16):
        for j in range(16):
            if i < 8 and j < 8:
                r, g, b, w = 0, 0, 255, 0
            elif i < 8 and j >= 8:
                r, g, b, w = 255, 0, 0, 0
            elif i >= 8 and j < 8:
                r, g, b, w = 255, 255, 0, 0
            else:
                r, g, b, w = 0, 0, 0, 80
            strip.setPixelColor(LEDS_ORDER[i][j], Color(r, g, b, w))
    strip.show()


def color_leds_wait(strip, white_level):
    for i in range(16):
        for j in range(16):
            if i < 8 and j < 8:
                r, g, b, w = 0, 0, 255, white_level
            elif i < 8 and j >= 8:
                r, g, b, w = 255, 0, 0, white_level
            elif i >= 8 and j < 8:
                r, g, b, w = 255, 255, 0, white_level
            else:
                r, g, b, w = 0, 0, 0, 70 + (50 - white_level) // 3

            strip.setPixelColor(LEDS_ORDER[i][j], Color(r, g, b, w))

    strip.show()


def color_leds_error(strip):
    color_leds(strip, (255, 0, 0, 0))
    time.sleep(0.15)
    color_leds(strip, (50, 0, 0, 0))
    time.sleep(0.15)
    color_leds(strip, (255, 0, 0, 0))
    time.sleep(0.3)

def draw_endgame(strip):
    print('end')
    r, g, b, w = 0, 0, 0, 0
    for i in range(16):
        for j in range(16):
            strip.setPixelColor(LEDS_ORDER[15 - i][j], Color(r, g, b, w))
        time.sleep(0.05)
        strip.show()
    time.sleep(1)
