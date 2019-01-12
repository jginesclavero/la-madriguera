#!/usr/bin/env python
import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import rospy
from geometry_msgs.msg import Twist

pin = 0

def callback(data):
    global pin
    wave = (10 / (math.pi / data.angular.x)) + 0.5
    pin.ChangeDutyCycle(wave)   #Enviamos un pulso del 10.5% para girar el servo hacia la izquierda

if __name__ == '__main__':
    global pin
    try:
        rospy.init_node('thermostat_driver', anonymous=False)
        rospy.Subscriber('/thermostat/turn', Twist, callback)
        GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
        GPIO.setup(21,GPIO.OUT)    #Ponemos el pin 21 como salida
        pin = GPIO.PWM(21,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
        pin.start(7.5)               #Enviamos un pulso del 7.5% para centrar el servo
        rospy.spin()

    except rospy.ROSInterruptException:         #Si el usuario pulsa CONTROL+C entonces...
        p.stop()                      #Detenemos el servo
        GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
