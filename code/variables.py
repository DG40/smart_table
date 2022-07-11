from rpi_ws281x import *
import RPi.GPIO as GPIO

# Auxiliary variables (text color in terminal):
ansi_black = "\u001b[30m"
ansi_red = "\u001b[31m"
ansi_green = "\u001b[32m"
ansi_yellow = "\u001b[33m"
ansi_blue = "\u001b[34m"
ansi_magenta = "\u001b[35m"
ansi_cyan = "\u001b[36m"
ansi_white = "\u001b[37m"
ansi_reset = "\u001b[0m"

# Pins for changing sensor selection:
S0_pin = 26
S1_pin = 19
S2_pin = 13
E_pin = 21

# ZIP for  surveying sensors:
S_0 = [0, 1, 0, 1, 1, 1, 0, 0]
S_1 = [1, 0, 0, 1, 0, 1, 1, 0]
S_2 = [0, 0, 0, 0, 1, 1, 1, 1]

# Output pins of multiplexers:
M1 = 22
M2 = 16
M3 = 5
M4 = 6
M5 = 25
M6 = 24
M7 = 17
M8 = 27
M = [M1, M2, M3, M4, M5, M6, M7, M8]

# Setup GPIO on Raspberry Pi:
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

GPIO.setup(S0_pin, GPIO.OUT)
GPIO.setup(S1_pin, GPIO.OUT)
GPIO.setup(S2_pin, GPIO.OUT)
GPIO.setup(E_pin, GPIO.OUT)

GPIO.output(E_pin, False)


# FOR TIK-TAK-TOE GAME:
cell_1 = [[1, 1], [1, 2], [2, 1], [2, 2]]
cell_2 = [[1, 3], [1, 4], [2, 3], [2, 4]]
cell_3 = [[1, 5], [1, 6], [2, 5], [2, 6]]
cell_4 = [[3, 1], [3, 2], [4, 1], [4, 2]]
cell_5 = [[3, 3], [3, 4], [4, 3], [4, 4]]
cell_6 = [[3, 5], [3, 6], [4, 5], [4, 6]]
cell_7 = [[5, 1], [5, 2], [6, 1], [6, 2]]
cell_8 = [[5, 3], [5, 4], [6, 3], [6, 4]]
cell_9 = [[5, 5], [5, 6], [6, 5], [6, 6]]
cells_TikTak = [cell_1, cell_2, cell_3, cell_4, cell_5, cell_6, cell_7, cell_8, cell_9]


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
LED_PIN = 12  # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 650000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
LED_STRIP = ws.SK6812W_STRIP

order = [
    [56, 55, 40, 39, 24, 23, 8, 7, 248, 247, 232, 231, 216, 215, 200, 199],
    [57, 54, 41, 38, 25, 22, 9, 6, 249, 246, 233, 230, 217, 214, 201, 198],
    [58, 53, 42, 37, 26, 21, 10, 5, 250, 245, 234, 229, 218, 213, 202, 197],
    [59, 52, 43, 36, 27, 20, 11, 4, 251, 244, 235, 228, 219, 212, 203, 196],
    [60, 51, 44, 35, 28, 19, 12, 3, 252, 243, 236, 227, 220, 211, 204, 195],
    [61, 50, 45, 34, 29, 18, 13, 2, 253, 242, 237, 226, 221, 210, 205, 194],
    [62, 49, 46, 33, 30, 17, 14, 1, 254, 241, 238, 225, 222, 209, 206, 193],
    [63, 48, 47, 32, 31, 16, 15, 0, 255, 240, 239, 224, 223, 208, 207, 192],
    [64, 79, 80, 95, 96, 111, 112, 127, 128, 143, 144, 159, 160, 175, 176, 191],
    [65, 78, 81, 94, 97, 110, 113, 126, 129, 142, 145, 158, 161, 174, 177, 190],
    [66, 77, 82, 93, 98, 109, 114, 125, 130, 141, 146, 157, 162, 173, 178, 189],
    [67, 76, 83, 92, 99, 108, 115, 124, 131, 140, 147, 156, 163, 172, 179, 188],
    [68, 75, 84, 91, 100, 107, 116, 123, 132, 139, 148, 155, 164, 171, 180, 187],
    [69, 74, 85, 90, 101, 106, 117, 122, 133, 138, 149, 154, 165, 170, 181, 186],
    [70, 73, 86, 89, 102, 105, 118, 121, 134, 137, 150, 153, 166, 169, 182, 185],
    [71, 72, 87, 88, 103, 104, 119, 120, 135, 136, 151, 152, 167, 168, 183, 184]
]

# SENSORS DATA:

Cells = [  # Cells[0-7][0-7]
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]
]

RawData = [  # RawData[0-7][0-7]
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

DryData = [  # DryData[0-7][0-7]
    [1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]
]

# Variables for touchpad response adjustment:
buf_checkers = 70
buf_tiktaktoe = 1
buf_selectgame = 60
switch_count = 8 # (q-ty of activated cells for changing mode between games)

buf_developer = 160
switch_count_developer = 8 # (q-ty of activated cells for changing mode to "developer_mode")


def ReadCells(buf):
    for j in range(len(S_0)):
        GPIO.output(S0_pin, S_0[j])
        GPIO.output(S1_pin, S_1[j])
        GPIO.output(S2_pin, S_2[j])
        for i in range(len(M)):
            Cells[i][j] = GPIO.input(M[i])
            if Cells[i][j] == 1 and RawData[i][j] < buf:
                RawData[i][j] += 1
                if RawData[i][j] == buf:
                    DryData[i][j] = 1
                else:
                    DryData[i][j] = 0
            else:
                RawData[i][j] = 0


def DataProcessing(buf):
    for j in range(len(S_0)):
        GPIO.output(S0_pin, S_0[j])
        GPIO.output(S1_pin, S_1[j])
        GPIO.output(S2_pin, S_2[j])
        for i in range(len(M)):
            Cells[i][j] = GPIO.input(M[i])
            if Cells[i][j] == 1:
                if RawData[i][j] < buf:
                    RawData[i][j] += 1
                elif RawData[i][j] == buf:
                    DryData[i][j] = 1
            else:
                RawData[i][j] = 0
                DryData[i][j] = 0


def PrintData():
    print('  ', 0, 1, 2, 3, 4, 5, 6, 7, sep='')
    print('  ', '--------', sep='')
    for i in range(len(M)):
        print(i, '|', sep='', end='')
        for j in range(len(S_0)):
            print(ansi_yellow + str(DryData[i][j]) + ansi_reset, end='')
        print()
    print()


def PrintLeds(strip):
    PrintData()
    for i in range(8):
        for j in range(8):
            if DryData[i][j] == 1:
                strip.setPixelColor(order[i * 2][j * 2], Color(0, 0, 255, 255))
                strip.setPixelColor(order[i * 2 + 1][j * 2], Color(0, 0, 255, 255))
                strip.setPixelColor(order[i * 2][j * 2 + 1], Color(0, 0, 255, 255))
                strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(0, 0, 255, 255))
            else:
                strip.setPixelColor(order[i * 2][j * 2], Color(0, 0, 0, 0))
                strip.setPixelColor(order[i * 2 + 1][j * 2], Color(0, 0, 0, 0))
                strip.setPixelColor(order[i * 2][j * 2 + 1], Color(0, 0, 0, 0))
                strip.setPixelColor(order[i * 2 + 1][j * 2 + 1], Color(0, 0, 0, 0))
    strip.show()


def Soft_brightness(strip):
    i = 255
    while i > 50:
        strip.setBrightness(i)
        strip.show()
        i -= 5
    while i <= 255:
        strip.setBrightness(i)
        strip.show()
        i += 5


def Soft_down_brightness(strip):
    i = 255
    while i >= 0:
        strip.setBrightness(i)
        strip.show()
        i -= 5


def Soft_up_brightness(strip):
    i = 0
    while i <= 255:
        strip.setBrightness(i)
        strip.show()
        i += 15


def ClearLeds(strip):
    for i in range(16):
        for j in range(16):
            strip.setPixelColor(order[i][j], Color(0, 0, 0, 0))
    strip.show()
