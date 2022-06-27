# For using a membrane keypad (4x4) with i2c lcd on  Raspberry Pi 4B to run a calculator

# A module to control Raspberry Pi GPIO channels
# use the following command: pip install RPi.GPIO

# Define lcd (Need to install rpi_lcd on Raspberry pi)
# First Command: wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/lcd_i2c.py
# Second Command: sudo pip3 install rpi_lcd

import RPi.GPIO as GPIO
import time
import math
import pytz
from rpi_lcd import LCD
from datetime import datetime
from subprocess import check_output

# Get date and time
today = datetime.today()
today_1 = datetime.now().strftime('%b %d  %H:%M:%S')
current_date = today.strftime("%d/%B/%Y") # use %m instead of %B for month format in numbers
current_time = today.strftime("%H:%M:%S")
dt_string = today.strftime("%d/%B/%Y %H:%M:%S")

# Instal pytz for time zones using : sudo pip install pytz
# Time zone for America / New york
tz_NY = pytz.timezone('America/New_York')
datetime_NY = datetime.now(tz_NY)
# Time zone for London / UK
tz_London = pytz.timezone('Europe/London')
datetime_London = datetime.now(tz_London)


# Define lcd (Need to install rpi_lcd on Raspberry pi)
# First Command: wget https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/lcd_i2c.py
# Second Command: sudo pip3 install rpi_lcd
lcd = LCD()

# Define variable to get IP address
def get_ip():
    cmd = "hostname -I | cut -d\' \' -f1"
    return check_output(cmd, shell=True).decode("utf-8").strip()

IP = get_ip()


# Define variables
number = ["0","1","2","3","4","5","6","7","8","9"]
operator = ["+", "-", "*", "/"]
num1 = ""
num2 = ""
op = ""
Key = ""
k = 0

# Used to scroll text in lcd
str_pad = " " * 16
my_long_string = "Starting PI Calculator"
my_long_string = str_pad + my_long_string

# These are the GPIO pin numbers where the
# lines of the keypad matrix are connected
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Calculation function
def arithmetics(num1, op, num2):
    if(op == "+"):
        val = str(int(num1)+int(num2))
    if(op == "-"):
        val = str(int(num1)-int(num2))
    if(op == "*"):    
        val = str(int(num1)*int(num2))
    if(op == "/"):    
        val = str(float(num1)/float(num2))
    return val

# Read and create inputs from keypad  
def print_key(Key):
    
    global number
    global operator
    global num1
    global num2
    global val
    global op
    global k
    global today_1
    
    if Key in number: # check if the pressed key is a number
        num2 += Key
        if(num1 != ""):
                if k<1:
                    val = num1 + op + num2
                    lcd.text(val, 2)
                else:
                    val = num1 +op+ num2
                lcd.text(val, 2)
        else:
                lcd.text(num2, 2)

    elif Key in operator: # check if the key pressed is operation
        if (num1 == "") and (num2 == ""):
            lcd.text(Key, 2)
            op = ""
        elif (num1 != "") and (num2 != ""):
            val = arithmetics(num1, op, num2)
            num1 = val
            val = num1 + Key
            op = Key
            num2 = ""
            k = 1
            lcd.text(val, 2)
        elif (num1 == ""):
            num1 = num2
            num2 = ""
            op = Key
            val = num1 + op
            lcd.text(val, 2)
        else:
            val = num1 + Key
            op = Key
            lcd.text(val, 2)

    elif Key == "CE": # check when clear is pressed
        num1 = ""
        num2 = ""
        op = ""
        k = 0
        Key = ""
        today_1 = datetime.now().strftime('%b %d  %H:%M:%S')
        lcd.clear()
        lcd.text("PI Calculator", 1)
        lcd.text("CE", 2)
        time.sleep(0.5)
        lcd.clear
        lcd.text(str(today_1), 1)
        lcd.text(("IP:" +str(IP)), 2)
        time.sleep(3)
        lcd.clear() 
        
        
    elif Key == "=": # check when equal sign is pressed
        k = 0
        val = arithmetics(num1, op, num2)
        answer = num1 + op + num2 + "="
        answer_1 = "=" + val
        lcd.text(answer_1, 2)
        num1 = ""
        num2 = ""
        op = ""
        Key = ""

            
            
# reads the columns and appends the value, that corresponds
# to the button, to a variable  
def readLine(line, characters):    
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        print_key(characters[0])
    if(GPIO.input(C2) == 1):
        print_key(characters[1])             
    if(GPIO.input(C3) == 1):
        print_key(characters[2])             
    if(GPIO.input(C4) == 1):
        print_key(characters[3])           
    GPIO.output(line, GPIO.LOW)

# Scroll text on lcd once
for i in range (0, len(my_long_string)):
    lcd_text = my_long_string[i:(i+16)]
    lcd.text(lcd_text,1)
    time.sleep(0.15)
    lcd.text(str_pad,1)


try:
    while True:

            lcd.text("PI Calculator", 1) # Use to show fix text not scrolling
            readLine(L1, ["1","2","3","+"]) 
            readLine(L2, ["4","5","6","-"])
            readLine(L3, ["7","8","9","*"])
            readLine(L4, ["CE","0","=","/"])
            time.sleep(0.05)


except KeyboardInterrupt:
    print("\nApplication stopped!")
finally:
    lcd.clear()
    GPIO.cleanup()
    
    
    
