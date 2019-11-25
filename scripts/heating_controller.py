#!/usr/bin/env python
import time
import datetime               
import rospy
from std_srvs.srv import SetBool,SetBoolRequest
import requests

sleeping = False

def sleeping_mode():
  global sleeping
  if datetime.datetime.now().time().hour == 23 and not sleeping:
    url = 'http://la-madriguera-iot.herokuapp.com/heating-system/setStatus?status=0'
    requests.get(url=url)
    sleeping = True
  else:
    sleeping = False

def update_heating_status():
  sleeping_mode()
  try:
    status = False
    url = 'http://la-madriguera-iot.herokuapp.com/heating-system/getStatus'
    resp = requests.get(url=url)
    data = resp.json()
    if data[0]['status'] == 1:
      status = True
    #power_on_srv = rospy.ServiceProxy('/thermostat/power_on', SetBool)
    #resp = power_on_srv(status)
    return
  except rospy.ServiceException, e:
    print "Service call failed: %s"%e

if __name__ == '__main__':
  try:
    rospy.init_node('thermostat_getStatus', anonymous=False)
    rate = rospy.Rate(0.2)
    #rospy.wait_for_service('/thermostat/power_on')
    while not rospy.is_shutdown():
      update_heating_status()
      rate.sleep()
  except rospy.ROSInterruptException:
    pass