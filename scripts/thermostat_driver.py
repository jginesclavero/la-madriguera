#!/usr/bin/env python
import RPi.GPIO as GPIO    #Importamos la libreria RPi.GPIO
import time                #Importamos time para poder usar time.sleep
import rospy
from geometry_msgs.msg import Twist

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + " %d received", data.data

def step():

if __name__ == '__main__':
    try:
         rospy.init_node('thermostat_driver', anonymous=False)
         rospy.Subscriber('/thermostat/turn', Twist, callback)
         rate = rospy.Rate(10)

         GPIO.setmode(GPIO.BOARD)   #Ponemos la Raspberry en modo BOARD
         GPIO.setup(21,GPIO.OUT)    #Ponemos el pin 21 como salida
         p = GPIO.PWM(21,50)        #Ponemos el pin 21 en modo PWM y enviamos 50 pulsos por segundo
         p.start(7.5)               #Enviamos un pulso del 7.5% para centrar el servo

         while not rospy.is_shutdown():
            p.ChangeDutyCycle(10.5)    #Enviamos un pulso del 10.5% para girar el servo hacia la izquierda
            time.sleep(0.5)           #pausa de medio segundo
            p.ChangeDutyCycle(0.5)   #Enviamos un pulso del 0.5% para girar el servo hacia la derecha
            time.sleep(0.5)           #pausa de medio segundo
            p.ChangeDutyCycle(5.5)    #Enviamos un pulso del 5.5% para centrar el servo de nuevo
            time.sleep(0.5)           #pausa de medio segundo
            #rate.sleep()

    except rospy.ROSInterruptException:         #Si el usuario pulsa CONTROL+C entonces...
        p.stop()                      #Detenemos el servo
        GPIO.cleanup()                #Limpiamos los pines GPIO de la Raspberry y cerramos el script
