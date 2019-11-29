#!/usr/bin/env python
import time
import datetime               
import rospy
from std_srvs.srv import SetBool,SetBoolRequest
from std_msgs.msg import Float32
import requests

class HeatingController:
  def __init__(self):
    rospy.Subscriber('/ds18b20/temperature', Float32, self.callback)
    self.temperature_ = 0.0
    self.sleeping_ = False

  def callback(self, data):
    self.temperature_ = data.data

  def sleeping_mode(self):
    if datetime.datetime.now().time().hour == 23 and not self.sleeping_:
      url = 'http://la-madriguera-iot.herokuapp.com/heating-system/setStatus?status=0'
      requests.get(url=url)
      self.sleeping_ = True
    else:
      self.sleeping_ = False

  def update_heating_status(self):
    self.sleeping_mode()
    try:
      status = False
      url = 'http://la-madriguera-iot.herokuapp.com/heating-system/getStatus'
      resp = requests.get(url=url)
      data = resp.json()
      if data[0]['status'] == 1 and self.temperature_ < 19.0:
        status = True
      power_on_srv = rospy.ServiceProxy('/thermostat/power_on', SetBool)
      resp = power_on_srv(status)
      return
    except rospy.ServiceException, e:
      print "Service call failed: %s"%e

if __name__ == '__main__':
  try:
    rospy.init_node('thermostat_getStatus', anonymous=False)
    rate = rospy.Rate(0.2)
    controller = HeatingController()
    while not rospy.is_shutdown():
      controller.update_heating_status()
      rate.sleep()
  except rospy.ROSInterruptException:
    pass