import RPi.GPIO as GPIO
import time
from rpi_lcd import LCD

lcd=LCD()


GPIO.setmode(GPIO.BOARD)
led=7
GPIO.setup(led,GPIO.OUT)
push=11
GPIO.setup(push,GPIO.IN)
print("Ingrese la tarea")
test=input()
while 1:
	
	lcd.text(test,1)
	lec_push= GPIO.input(push)
	if lec_push == 0:
		GPIO.output(led,True)
		print("Se cumplio la tarea")
	else:
		GPIO.output(led,False)
		print ("No se ha hecho la tarea")
	time.sleep(0.1)
			
