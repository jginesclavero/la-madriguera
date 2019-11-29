#!/usr/bin/env python
import wiringpi
import rospy
import math
from std_srvs.srv import SetBool,SetBoolResponse

def callback(req):
  io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
  # establecemos el modo de operacion del pin, en este caso es de salida
  # hay que utilizar la nomenclatura de Wiring pi, es MUY IMPORTANTE
  io.pinMode(17, io.OUTPUT)
  if req.data:
    io.digitalWrite(17, io.HIGH)
  else:
    io.digitalWrite(17, io.LOW)

  return SetBoolResponse()

if __name__ == '__main__':
  try:
    rospy.init_node('thermostat_driver', anonymous=False)
    s = rospy.Service('/thermostat/power_on', SetBool, callback)
    rospy.spin()
  except rospy.ROSInterruptException:
    pass
