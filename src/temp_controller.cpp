#include "ros/ros.h"
#include <std_msgs/Int64.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/Twist.h>
#include <math.h>

class TempController
{
public:
	TempController(): n_()
	{
		set_temp_sub_ = n_.subscribe("/thermostat/set_temperature", 1, &TempController::setTempCallback, this); //cambar a srv
    power_temp_sub_ = n_.subscribe("/thermostat/switch", 1, &TempController::switchCallback, this);
    cmd_pub_ = n_.advertise<geometry_msgs::Twist>("/thermostat/turn", 1);
    heating = false;
	}

	void setTempCallback(const std_msgs::Int64::ConstPtr& msg)
	{
    if (heating)
    {
      float temp = msg->data;
      if (temp < 10)
        temp = 0.1;
      else if (temp > 17 && temp < 20)
        temp = temp + 2;
      else if (temp > 20)
        temp = temp + 4;
        
      ROS_INFO("Temp (C): [%f]", temp);
      geometry_msgs::Twist turn_msg;
      turn_msg.angular.x = M_PI / (40/temp);
      cmd_pub_.publish(turn_msg);
    }
    else
    {
      ROS_ERROR("Power on the heating first");
    }
	}

  void switchCallback(const std_msgs::Bool::ConstPtr& msg)
	{
    heating = true;
		ROS_INFO("Switch : [%i]", msg->data);
	}

private:
	ros::NodeHandle n_;
	ros::Subscriber set_temp_sub_, power_temp_sub_;
  ros::Publisher cmd_pub_;
  bool heating;
};

int main(int argc, char **argv)
{

   ros::init(argc, argv, "temp_controller");
   ros::NodeHandle n;

   TempController temp_controller;
   ros::spin();
   return 0;

 }
