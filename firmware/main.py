from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules.encoder import EncoderHandler
import board
import neopixel

keyboard = KMKKeyboard()

keyboard.direct_pins = [board.GP27, board.GP28, board.GP29, board.GP6, board.GP7, board.GP0]

keyboard.keymap = [
    [KC.F13, KC.F14, KC.F15, KC.F16, KC.F17, KC.F18],
]

enc = EncoderHandler()
enc.pins = (
    (board.GP9, board.GP8, KC.VOLD, KC.VOLU),
    (board.GP11, board.GP10, KC.NO, KC.NO)
)
keyboard.modules.append(enc)

NUM_PIXELS = 12
pixels = neopixel.NeoPixel(board.GP26, NUM_PIXELS, brightness=0.2, auto_write=False)
volume = 50
brightness = 0.2

def show_volume(level):
    lit = int((level / 100) * NUM_PIXELS)
    for i in range(NUM_PIXELS):
        pixels[i] = (0, 50, 0) if i < lit else (0, 0, 0)
    pixels.show()

old_update = enc.update

def update_encoders():
    global volume, brightness
    old_update()
    if enc.encoders[0].delta != 0:
        volume += enc.encoders[0].delta * 2
        volume = max(0, min(100, volume))
        show_volume(volume)
        enc.encoders[0].delta = 0
    if enc.encoders[1].delta != 0:
        brightness += enc.encoders[1].delta * 0.05
        brightness = max(0.05, min(1.0, brightness))
        pixels.brightness = brightness
        pixels.show()
        enc.encoders[1].delta = 0

enc.update = update_encoders

show_volume(volume)
keyboard.go()
