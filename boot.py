# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Altavista', 'sunstone1901')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
webrepl.start()
gc.collect()
