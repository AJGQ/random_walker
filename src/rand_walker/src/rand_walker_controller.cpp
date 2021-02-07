#define _USE_MATH_DEFINES
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <geometry_msgs/Twist.h>
#include <ros/ros.h>
#include <std_msgs/Empty.h>
#include "rand_walker/BumperEvent.h"
#include "rand_walker/CliffEvent.h"
#include "rand_walker/Led.h"
#include "rand_walker/WheelDropEvent.h"

#define BUMPING (bumper_left_pressed || bumper_center_pressed || bumper_right_pressed)
#define HANGING (cliff_left_detected || cliff_center_detected || cliff_right_detected)
#define DROPING (wheel_drop_left_detected || wheel_drop_right_detected)
#define RAND01  ((double)std::rand() / (double)RAND_MAX)

bool change_direction = false;
bool stop = false;
bool bumper_left_pressed = false;
bool bumper_center_pressed = false;
bool bumper_right_pressed = false;
bool cliff_left_detected = false;
bool cliff_center_detected = false;
bool cliff_right_detected = false;
bool wheel_drop_left_detected = false;
bool wheel_drop_right_detected = false;
bool led_bumper_on = false;
bool led_cliff_on = false;
bool led_wheel_drop_on = false;
bool turning = false;
int turning_direction = 1;

ros::Subscriber bumper_event_subscriber, cliff_event_subscriber, wheel_drop_event_subscriber;
ros::Publisher cmd_vel_publisher, led1_publisher, led2_publisher;
double vel_lin;
double vel_ang;
ros::Duration turning_duration;
ros::Time turning_start;

void detect_wheel_drop(const rand_walker::WheelDropEventConstPtr msg){
    // DROPPED || RAISED
    bool wheel_dropped = msg->state == rand_walker::WheelDropEvent::DROPPED;

    switch(msg->wheel){
        case rand_walker::WheelDropEvent::LEFT: wheel_drop_left_detected = wheel_dropped; break;
        case rand_walker::WheelDropEvent::RIGHT: wheel_drop_right_detected = wheel_dropped; break;
    }
}

void detect_bumper(const rand_walker::BumperEventConstPtr msg){
    // PRESSED || RELEASED
    bool bumped = msg->state == rand_walker::BumperEvent::PRESSED;
    change_direction = bumped ? true : change_direction;

    switch (msg->bumper) {
        case rand_walker::BumperEvent::LEFT:    bumper_left_pressed    = bumped; break;
        case rand_walker::BumperEvent::CENTER:  bumper_center_pressed  = bumped; break;
        case rand_walker::BumperEvent::RIGHT:   bumper_right_pressed   = bumped; break;
    }
}

void detect_cliff(const rand_walker::CliffEventConstPtr msg){
    // CLIFF || FLOOR
    bool hanging = msg->state == rand_walker::CliffEvent::CLIFF;
    change_direction = hanging ? true : change_direction;

    switch (msg->sensor) {
        case rand_walker::CliffEvent::LEFT:   cliff_left_detected    = hanging; break;
        case rand_walker::CliffEvent::CENTER: cliff_center_detected  = hanging; break;
        case rand_walker::CliffEvent::RIGHT:  cliff_right_detected   = hanging; break;
    }
}

void bumperEventCB(const rand_walker::BumperEventConstPtr msg) {
    detect_bumper(msg);

    if (!led_bumper_on && BUMPING)
    {
      rand_walker::LedPtr led_msg_ptr;
      led_msg_ptr.reset(new rand_walker::Led());
      led_msg_ptr->value = rand_walker::Led::ORANGE;
      led1_publisher.publish(led_msg_ptr);
      
      led_bumper_on = true;
    }
    else if (led_bumper_on && !BUMPING)
    {
      rand_walker::LedPtr led_msg_ptr;
      led_msg_ptr.reset(new rand_walker::Led());
      led_msg_ptr->value = rand_walker::Led::BLACK;
      led1_publisher.publish(led_msg_ptr);

      led_bumper_on = false;
    }
    if (change_direction)
    {
      ROS_INFO_STREAM("Bumper pressed. Changing direction.");
    }
};

void cliffEventCB(const rand_walker::CliffEventConstPtr msg)
{
    detect_cliff(msg);

    if (!led_cliff_on && HANGING) {
        rand_walker::LedPtr led_msg_ptr;
        led_msg_ptr.reset(new rand_walker::Led());
        led_msg_ptr->value = rand_walker::Led::ORANGE;
        led2_publisher.publish(led_msg_ptr);

        led_cliff_on = true;
    }
    else if (led_cliff_on && !HANGING) {
        rand_walker::LedPtr led_msg_ptr;
        led_msg_ptr.reset(new rand_walker::Led());
        led_msg_ptr->value = rand_walker::Led::BLACK;
        led2_publisher.publish(led_msg_ptr);

        led_cliff_on = false;
    }

    if (change_direction) {
        ROS_INFO_STREAM("Cliff detected. Changing direction.");
    }
};

void wheelDropEventCB(const rand_walker::WheelDropEventConstPtr msg) {
    detect_wheel_drop(msg);

    if (!led_wheel_drop_on && DROPING) {
        rand_walker::LedPtr led_msg_ptr;
        led_msg_ptr.reset(new rand_walker::Led());
        led_msg_ptr->value = rand_walker::Led::RED;
        led1_publisher.publish(led_msg_ptr);
        led2_publisher.publish(led_msg_ptr);

        stop = true;
        led_wheel_drop_on = true;
    }
    else if (led_wheel_drop_on && !DROPING) {
        rand_walker::LedPtr led_msg_ptr;
        led_msg_ptr.reset(new rand_walker::Led());
        led_msg_ptr->value = rand_walker::Led::BLACK;
        led1_publisher.publish(led_msg_ptr);
        led2_publisher.publish(led_msg_ptr);

        stop = false;
        led_wheel_drop_on = false;
    }

    if (change_direction) {
        ROS_INFO_STREAM("Wheel(s) dropped. Stopping.");
    }
};

void loop_body(){
    // Velocity commands
    geometry_msgs::TwistPtr cmd_vel_msg_ptr;
    cmd_vel_msg_ptr.reset(new geometry_msgs::Twist());

    if(stop){
        cmd_vel_publisher.publish(cmd_vel_msg_ptr); // will be all zero when initialised
        return;
    }

    if(change_direction){
        change_direction = false;

        // calculate a random turning angle (-180 ... +180) based on the set angular velocity
        // time for turning 180 degrees in seconds = M_PI / angular velocity
        turning_duration = ros::Duration(RAND01 * (M_PI / vel_ang));
        // randomly chosen turning direction
        turning_direction = RAND01 >= 0.5 ? 1 : -1;

        turning_start = ros::Time::now();
        turning = true;
        ROS_INFO_STREAM(
            "Will rotate " << turning_direction * turning_duration.toSec() * vel_ang / M_PI * 180
            << " degrees."
            );
    }

    if(turning){
        if((ros::Time::now() - turning_start) < turning_duration){
            cmd_vel_msg_ptr->angular.z = turning_direction * vel_ang;
            cmd_vel_publisher.publish(cmd_vel_msg_ptr);
        }
        else{
            turning = false;
        }
    }
    else{
        cmd_vel_msg_ptr->linear.x = vel_lin;
        cmd_vel_publisher.publish(cmd_vel_msg_ptr);
    }
};

void init(ros::NodeHandle nh){

    bumper_event_subscriber = nh.subscribe("events/bumper", 10, &bumperEventCB);
    cliff_event_subscriber = nh.subscribe("events/cliff", 10, &cliffEventCB);
    wheel_drop_event_subscriber = nh.subscribe("events/wheel_drop", 10, &wheelDropEventCB);

    cmd_vel_publisher = nh.advertise<geometry_msgs::Twist>("commands/velocity", 10);
    led1_publisher = nh.advertise<rand_walker::Led>("commands/led1", 10);
    led2_publisher = nh.advertise<rand_walker::Led> ("commands/led2", 10);

    nh.param("linear_velocity", vel_lin, 0.5);
    nh.param("angular_velocity", vel_ang, 0.1);

    ROS_INFO_STREAM(
        "Velocity parameters: linear velocity = " << vel_lin << 
        ", angular velocity = " << vel_ang
        );

    std::srand(std::time(0));
}

int main(int argc, char** argv){
    ros::init(argc, argv, "controller");
    ros::NodeHandle nh;
    ros::Rate loop_rate = 10; //Hz

    init(nh);

    while(ros::ok()){
        loop_body();
        ros::spin();
        loop_rate.sleep();
    }

    return 0;
}
