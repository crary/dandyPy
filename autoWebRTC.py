import uinput 
import time

## Set WebRtc capture time in seconds
capTime = '35'
device = uinput.Device([uinput.KEY_ENTER, uinput.KEY_LEFTSHIFT, uinput.KEY_DOWN, uinput.KEY_TAB, uinput.KEY_C, uinput.KEY_H, \
uinput.KEY_R, uinput.KEY_O, uinput.KEY_M, uinput.KEY_E, uinput.KEY_SEMICOLON, uinput.KEY_SLASH, uinput.KEY_W, uinput.KEY_B, \
uinput.KEY_MINUS, uinput.KEY_I, uinput.KEY_O, uinput.KEY_T, uinput.KEY_N, uinput.KEY_A, uinput.KEY_L, uinput.KEY_S, uinput.KEY_LEFTCTRL])

time.sleep(1)
device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_T])
time.sleep(2)
device.emit_click(uinput.KEY_C)
device.emit_click(uinput.KEY_H)
device.emit_click(uinput.KEY_R)
device.emit_click(uinput.KEY_O)
device.emit_click(uinput.KEY_M)
device.emit_click(uinput.KEY_E)
device.emit_click(uinput.KEY_SEMICOLON)
device.emit_click(uinput.KEY_SLASH)
device.emit_click(uinput.KEY_SLASH)
device.emit_click(uinput.KEY_W)
device.emit_click(uinput.KEY_E)
device.emit_click(uinput.KEY_B)
device.emit_click(uinput.KEY_R)
device.emit_click(uinput.KEY_T)
device.emit_click(uinput.KEY_C)
device.emit_click(uinput.KEY_MINUS)
device.emit_click(uinput.KEY_I)
device.emit_click(uinput.KEY_N)
device.emit_click(uinput.KEY_T)
device.emit_click(uinput.KEY_E)
device.emit_click(uinput.KEY_R)
device.emit_click(uinput.KEY_N)
device.emit_click(uinput.KEY_A)
device.emit_click(uinput.KEY_L)
device.emit_click(uinput.KEY_S)
time.sleep(1)
device.emit_click(uinput.KEY_ENTER)
time.sleep(1)
device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_TAB])

time.sleep(capTime)
device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_TAB])
time.sleep(1)
device.emit_click(uinput.KEY_TAB)
time.sleep(1)
device.emit_click(uinput.KEY_ENTER)
time.sleep(1)
device.emit_click(uinput.KEY_TAB)
time.sleep(1)
device.emit_click(uinput.KEY_ENTER)
time.sleep(1)
device.emit_combo([uinput.KEY_LEFTCTRL, uinput.KEY_W])