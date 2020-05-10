# dobot_magician_utilities
 Utility programs for the dobot magician robotic arm, written in python. Useful for setting up experiments
 
## Contents

- Introduction
- Installation
- Guidance on use

## Introduction

This code toolbox provides scripts to: 

1. Setup experiments on the dobot magician arm including
   1. Homing the robot arm
   2. Collecting robot poses using the button on the robot arm
   3. Displaying alarms
   4. Clearing alarms


## Installation

This code is bundelled as a python package. A setup file is included and so dependent libraries should install with the package. Please note some are ommitted on purpose because they are not available using pip.

To install the package on Windows, OS X or Linux, clone the repository and run the setup script from the repository root directory:

```sh
python setup.py install
```

To use with a virtual environment

(1) create a virtual environment (e.g. using conda). 
(2) Then run the following command in the local directory of dobot_magician_utilities setup.py: 

```sh
pip install -e . 
```

## Installation (part 2) of .dll for use with dobot magician arm: 

For both windows and linux you should *not* need to do anything with the dll. This is packaged with cri_dobot which is a prequisite. If you get an error message relating to the dll library (or are using mac) try the steps below. Please reach out for help if this isn't working!

To use the dobot dll (which is a prerequisite) follow these instructions 
- [A] use the correct DLL from dobot (64 bit or 32 bit), and
- [B] put the dll in either 
  - \cri_dobot\dobotMagician\dll_files
  - or the system root directory, for example on windows this is (%SystemRoot%\system32)

You can find the dll at (https://www.dobot.cc/downloadcenter/dobot-magician.html) - Look for Development Protocol -> 'DobotDemovX.X.zip' - Ensure you extract the correct DLL for your system (windows/linux/mac) (x64/x32)

## Installation (part 3) 

Scripts in this package use the cri, and cri_dobot and libraries. You must have all these python packages installed (e.g. in your venv). You can find them here:

- https://github.com/jlloyd237/cri
- https://github.com/meisben/cri_dobot

## Usage

- For examples of basic usage and to test the python package is working run 'utilities\utilities.py'
- To move the arm to a new position see the script 'utilities\move_to_pose.py'

## Bug list

(1) TCP

Dobot magician has a Tool Center Point (TCP) bug which means that it always assumed it's tool center point values (x,y,z) are 0,0,0. For this reason the tool center point is not currently used with the dobot magician in production code. It is yet to be determined whether this functionality will be replicated in future versions of the cri_dobot wrapper. A question has been opened on this topic in the dobot magician forums.

