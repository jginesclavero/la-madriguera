#!/usr/bin/env python
version = "v1.0"
import sys
import rospy
from std_msgs.msg import Float32

class Ds18b20Node:
  def __init__(self):
    try:
      self.serialnum_ = (sys.argv[1])
    except:
      print ("Usage: 'ds18b20_driver.py {serialnumber of the ds18b20 -- ls /sys/bus/w1/devices}'")
      sys.exit()
    self.pub_ = rospy.Publisher('/ds18b20/temperature', Float32, queue_size=1)
    self.temperature_ = 0.0

  def getTemp(self):
    for i in range(5):
      filename = "/sys/bus/w1/devices/" + self.serialnum_ + "/w1_slave"
      tfile = open(filename)
      text = tfile.read()
      tfile.close()
      secondline = text.split("\n")[1]
      temperaturedata = secondline.split(" ")[9]
      self.temperature_ = float(temperaturedata[2:])
      self.temperature_ = self.temperature_ / 1000
      self.pub_.publish(self.temperature_)
      firstline = text
      ccrrcc = firstline.split(" ")[11]
      ccrrcc = (ccrrcc[:3]) #take only first 3 characters
      if ccrrcc == 'YES':
        break
      else:
        print ' Oops '

if __name__ == '__main__':
  rospy.init_node('ds18b20_node', anonymous=True)
  rate = rospy.Rate(1)
  try:
    driver = Ds18b20Node()
    while not rospy.is_shutdown():
      driver.getTemp()
      rate.sleep()
  except rospy.ROSInterruptException:
    pass