import micropython, array
from micropython import const
from machine import Timer, Pin
import time
import random
micropython.alloc_emergency_exception_buf(100)

class BoundsException(Exception):
    pass

rly = Pin(0,Pin.OUT)

def RelayTimerCallback(t):
    global rly
    if rly.value() == 1:
        rly.value(0)        # turn off relay
    relayTimer.deinit()
    

button_pressed = False
press_time = time.ticks_ms()
min_press_time = 500
max_press_time = 2000

def pin_isr(Pin):
    global button_pressed, press_time
    button_pressed = True
    press_time = time.ticks_ms()

button = Pin(14, Pin.IN, Pin.PULL_UP)
button.irq(handler=pin_isr,trigger=Pin.IRQ_FALLING)

relayTimer = Timer(-1) 

print("starting up")

# the main loop
while True:
    # check for button press, else goto sleep
    if button_pressed is True:
        button_pressed = False    
        # do a debounce
        time.sleep_ms(20)
        now = time.ticks_ms()
        print("isr latency:" + str(now-press_time))
        if button.value() == 0 and rly.value() == 0:
            rly.value(1)    # turn on relay
            # wait until button is released or held beyond max_press_time
            loop = 0
            while button.value() == 0 and (now - press_time < max_press_time):
                time.sleep_us(50)
                now = time.ticks_ms()
                loop += 1
                #print("button hold loop count:" + str(loop))
            ontime = max(min_press_time,(now - press_time)) * 20.0
            #print("start of press:" + str(now/1000.0))
            #print("end of press:" + str(press_time/1000.0))
            print("button pressed time:" + str((now - press_time)/1000.0))
            print("ontime:" + str(ontime))
            relayTimer.init(period=(int(ontime)), mode=Timer.ONE_SHOT, callback=RelayTimerCallback)
        elif rly.value() == 1:
            print("reinit of timer at:" + str(time.ticks_ms()/1000.0))
            relayTimer.init(period=(15 * 1000), mode=Timer.ONE_SHOT, callback=RelayTimerCallback)
    
    time.sleep(.1)
        

