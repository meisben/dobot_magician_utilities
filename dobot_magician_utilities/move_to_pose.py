# -*- coding: utf-8 -*-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Program Purpose: Useful to find a starting position for dobot magican robot arm experiments

# Author: Ben Money-Coomes (ben.money@gmail.com)
# (note anyone is welcome to contribute, intial author is noted only to facilitate questions)

# **Version control**

# v0.0.1    fully functional
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ------------------------------------------#
# Imports                                   #
# ------------------------------------------#

import time
import numpy as np

from cri.robot import AsyncRobot
from cri_dobot.robot import SyncDobot
from cri_dobot.controller import dobotMagicianController

# ------------------------------------------#
# Start of main program                     #
# ------------------------------------------#

np.set_printoptions(precision=2, suppress=True)


def main():
    base_frame = (0, 0, 0, 0, 0, 0)
    # base frame: x->front, y->right, z->up
    work_frame = (132, -8, 37, 0, 0, 0)

    # (129, -8, 33, 0, 0, 0) for sliding
    # (132, -8, 37, 0, 0, 0) for tapping

    with AsyncRobot(SyncDobot(dobotMagicianController())) as robot:

        # Set TCP, linear speed,  angular speed and coordinate frame
        # note that it is advisable not to use a Tool Center Point due to the dobot magician bug explained in the readme
        robot.tcp = (0, 0, 0, 0, 0, 0)
        robot.linear_speed = 100
        robot.angular_speed = 100

        # Set base frame for storing home position
        robot.coord_frame = base_frame

        # Set safe home position
        print("Setting home position")
        robot.sync_robot.set_home_params((200, 0, 80, 0, 0, 0))

        # Return to work frame
        robot.coord_frame = work_frame

        # Move to safe position of work frame
        print("Moving to safe position ...")
        robot.move_linear((0, 0, 30, 0, 0, 0))

        # Move to origin of work frame
        print("Moving to origin of work frame ...")
        robot.move_linear((0, 0, 0, 0, 0, 0))

        print("Final pose in work frame: {}".format(robot.pose))


if __name__ == '__main__':
    main()
