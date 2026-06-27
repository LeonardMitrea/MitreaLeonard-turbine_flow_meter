import machine

from machine import Pin
from machine import Timer
from time import sleep_ms

DIGIT_EN   = Pin(0,Pin.OUT)
DIGIT_SEL0 = Pin(2,Pin.OUT)
DIGIT_SEL1 = Pin(3,Pin.OUT)
DIGIT_SEL2 = Pin(4,Pin.OUT)

A = Pin(15,Pin.OUT)
B = Pin(13,Pin.OUT)
C = Pin(19,Pin.OUT)
D = Pin(17,Pin.OUT)
E = Pin(16,Pin.OUT)
F = Pin(14,Pin.OUT)
G = Pin(20,Pin.OUT)
P = Pin(18,Pin.OUT)

SENSOR = Pin(21,Pin.IN)
pulse_cnt = 0
def sensor_irq ():
    global pulse_cnt
    pulse_cnt += 1
SENSOR.irq(handler = lambda h:sensor_irq() , trigger = Pin.IRQ_RISING)

DIGIT_EN.value(True)
DIGIT_SEL0.value(False)
DIGIT_SEL1.value(False)
DIGIT_SEL2.value(False)

A.value(False)
B.value(False)
C.value(False)
D.value(False)
E.value(False)
F.value(False)
G.value(False)
P.value(False)

delay_ms = 200

digit2seg = [0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F]
point2seg = 0x80

digit_cnt = 0
char_cnt = 0
def drive_number(number):
    
    global char_cnt
    global digit_cnt
    
    point = False
    digit_value = 0x00
    str_num = str(number)
    
    if char_cnt < len(str_num) and str_num[char_cnt] == '.':
        char_cnt += 1
    
    if char_cnt < len(str_num):
        DIGIT_EN.value(True)
        DIGIT_SEL0.value((digit_cnt) & 0x01)
        DIGIT_SEL1.value((digit_cnt) & 0x02)
        DIGIT_SEL2.value((digit_cnt) & 0x04)
    
        if char_cnt + 1 < len(str_num) and str_num[char_cnt+1] == '.':
            point = True
        else:
            point = False

        digit_value = digit2seg[ord(str_num[char_cnt])-ord('0')]
        
        A.value(digit_value & 0x01)
        B.value(digit_value & 0x02)
        C.value(digit_value & 0x04)
        D.value(digit_value & 0x08)
        E.value(digit_value & 0x10)
        F.value(digit_value & 0x20)
        G.value(digit_value & 0x40)
        P.value(point)
        
        DIGIT_EN.value(False)
        
    digit_cnt += 1
    char_cnt  += 1
    if char_cnt >= len(str_num) and digit_cnt < 8:
        digit_cnt = 0
        char_cnt = 0


tim_frq = 1000
display_tim = machine.Timer(-1)
display_tim.init(mode=Timer.PERIODIC, freq=tim_frq, callback=lambda t:drive_number(number))

number = 0.0
value_calib = 2.7
sample_frequency = 5 # Hz
def sample(timer):
    global number
    global pulse_cnt
    number = round(pulse_cnt / value_calib, 3)
    pulse_cnt = 0

num_tim = machine.Timer(-1)
num_tim.init(mode=Timer.PERIODIC, freq=sample_frequency, callback=sample)

while True :
    pass