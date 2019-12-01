#!/usr/bin/env python
import time
import datetime               
import rospy
from std_srvs.srv import SetBool,SetBoolRequest
from std_msgs.msg import Float32
import requests
import enum

class States(enum.Enum):
   ARTICUNO = 1
   PSYDUCK = 2
   CHARMANDER = 3

class HeatingController:
  def __init__(self):
    rospy.Subscriber('/ds18b20/temperature', Float32, self.callback)
    self.temperature_ = 0.0
    self.target_temp_ = 18.0
    self.min_temp_ = self.target_temp_ - 0.5
    self.max_temp_ = self.target_temp_ + 0.5
    self.state_ = States.PSYDUCK

  def callback(self, data):
    self.temperature_ = data.data

  def sleeping_mode(self):
    if datetime.datetime.now().time().hour == 23 and datetime.datetime.now().time().minute == 00:
      url = 'http://la-madriguera-iot.herokuapp.com/heating-system/setStatus?status=0'
      requests.get(url=url)

  def check_status(self):
    try:
      url = 'http://la-madriguera-iot.herokuapp.com/heating-system/getStatus'
      resp = requests.get(url=url)
      data = resp.json()
      temp = data[0]['temp']
      print "Temp ------------"
      print temp
      if data[0]['status'] == 1:
        return True, temp
      else:
        return False, temp
    except requests.exceptions.ConnectionError, e:
      print "Service call failed: %s"%e

  def update_heating_status(self, status):
    power_on_srv = rospy.ServiceProxy('/thermostat/power_on', SetBool)
    resp = power_on_srv(status)

  def step(self):
    self.sleeping_mode()
    general_status, self.target_temp_ = self.check_status()
    if general_status:
      if self.state_ == States.ARTICUNO:
        self.update_heating_status(True)
        if self.temperature_ >= self.min_temp_:
          self.state_ = States.PSYDUCK
      elif self.state_ == States.PSYDUCK:
        if self.temperature_ < self.min_temp_:
          self.state_ = States.ARTICUNO
        elif self.temperature_ >= self.max_temp_:
          self.state_ = States.CHARMANDER
      else:
        self.update_heating_status(False)
        self.state_ = States.PSYDUCK
    else:
      self.update_heating_status(general_status)

if __name__ == '__main__':
  try:
    rospy.init_node('thermostat_getStatus', anonymous=False)
    rate = rospy.Rate(0.2)
    controller = HeatingController()
    while not rospy.is_shutdown():
      controller.step()
      rate.sleep()
  except rospy.ROSInterruptException:
    pass