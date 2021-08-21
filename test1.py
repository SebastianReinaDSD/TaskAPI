import RPi.GPIO as GPIO
import time
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

str_pad = " " * 16
my_string = input()
tam_text= len(my_string)
my_long_string = str_pad + my_string
my_long_string2 = my_string+str_pad
print(my_string)
print(tam_text)
while 1:

    if (tam_text>16):
        for i in range (0, len(my_long_string)):
            lcd_text = my_long_string[i:(i+16)]
            mylcd.lcd_display_string(lcd_text,1)
            time.sleep(0.4)
            mylcd.lcd_display_string(str_pad,1)
    else:
        mylcd.lcd_display_string(my_long_string2,1)