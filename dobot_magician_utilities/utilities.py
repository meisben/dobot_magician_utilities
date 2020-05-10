
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Program Purposes:
#   (1) Home the robot
#   (2) Get multiple poses from the dobot magician arm using the button on the arm
#   (3) Display alarms
#   (4) Clear alarms

# Initial Author: Ben Money-Coomes (ben.money@gmail.com)
# (note anyone is welcome to contribute, intial author is noted only to facilitate questions)

# **Version control**

# v1.3  Update to readability and to add settings
# v1.4 (April 26th 2020) - Added ability to clear dobot magician alarms

# NOTE: The name of this program was formerly 'getPoseFromHandHoldMode, it has changed to utilities.py in future commits due to the extended purpose of the program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# ------------------------------------------#
# Imports                                   #
# ------------------------------------------#

# Import the dobot dll
from cri_dobot.dobotMagician.dll_files import DobotDllType as dType
import time  # For sleeping
import pandas as pd  # For manipulating poses from HHT mode
import os  # For saving files and making directory


# Load Dll
# Load the dobot magician dll to allow it to be used (note dll must be placed in same folder)
api = dType.load()

# ------------------------------------------#
# Variables                                 #
# ------------------------------------------#

# Error terms
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}  # a dictionary of error terms as defined a C++ enum in 'DobotType.h file'

# Define datapath
os.environ['DATAPATH'] = r'P:\University Robotics\(14) Dissertation\4 Code\Results'

# Verbose mode
setTCP = False  # if this bool is set to True then the Tool Center Point for the dobot magician is set. Recommended to set as false due to the bug explained in dobot_toolbox readme file
verbose = False  # if this bool is set to True then additional information is printed

# ------------------------------------------#
# Helper functions                          #
# ------------------------------------------#


def inputNumber(message):
    """ Get an input number from user. Prompt is str @message
    """
    while True:
        try:
            userInput = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return userInput
            break


def yes_or_no(question):
    """ Get a y/n answer from the user
    """
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False

# ------------------------------------------#
# Start of main program                     #
# ------------------------------------------#


print("")
print("========================")
print("")
print("Hello! This program will:")
print("")
print(" 1. Home the dobot magician robot")
print(" 2. Collect poses using Hand Hold Teaching mode (HHT)")
print("")
print(" The settings for this program are currently: verbose = {}, setTCP = {}. The default for these settings is 'False'".format(verbose, setTCP))
print("")
print(" Let's begin...")
print("")
print("========================")
print("")

# Connect Dobot
# Try and connect to dobot with automatic search, returns enumerate type
state = dType.ConnectDobot(api, "", 115200)[0]
print("Returned value from ConnectDobot command: {}".format(state))  # print result
print("Connect status meaning:", CON_STR[state])

# If connection is successful
if (state == dType.DobotConnect.DobotConnect_NoError):  # If we managed to connect to the dobot

    # Then run this code

    # Stop to Execute Command Queue
    dType.SetQueuedCmdStopExec(api)  # Stop running commands in command queue

    # Get current pose
    # Get the pose (x,y,z,r, joint1,joint2,joint3,joint4)
    pose = dType.GetPose(api)
    print("Current Robot Pose: {} in format [x(mm),y(mm),z(mm),r(deg),joint1(deg),joint2(deg),joint3(deg),joint4(deg)]".format(
        pose))  # Print result

    # Clean Command Queue
    dType.SetQueuedCmdClear(api)  # Clear queue
    currentIndex = dType.GetQueuedCmdCurrentIndex(
        api)[0]  # Get the current command index
    if (verbose):
        print("CurrentCommandIndex: {}".format(currentIndex))

    # Async Motion Params Setting
    dType.SetHOMEParams(api, 180, 0, 80, 0, isQueued=1)  # Set home position
    # Set the velocity and acceleration of the joint co-ordinate axis in the format given in DobotDllType.py
    dType.SetPTPJointParams(api, 200, 200, 200, 200,
                            200, 200, 200, 200, isQueued=1)
    # Set the velocity ratio and acceleration ratio in PTP mode (i guess the amount of time it accelerates to define the velocity profile?)
    dType.SetPTPCommonParams(api, 100, 100, isQueued=1)

    # Check if homing is required
    print("")
    homeRobot = yes_or_no("Do you want to home the robot? ")

    # ---- These commands are only used to check the TCP of the robot arm. Please note it is advised not to use this functionality due to the bug outlined in the readme

    if(setTCP == True):

        # Find TCP current values and print these
        [x, y, z] = dType.GetEndEffectorParams(api)
        # print("TCP = x: {}, y: {}, z: {}".format(x,y,z))

        # Set TCP (If necessary)
        # tcp end position specified as x,y,z distance
        lastIndex = dType.SetEndEffectorParams(api, 0, 0, 0, isQueued=0)[0]

        # Find TCP adjusted values and print these (If necessary)
        [x, y, z] = dType.GetEndEffectorParams(api)
        # print("TCP = x: {}, y: {}, z: {}".format(x,y,z))

        # Create TCP dataframe for saving to .csv
        TCP = [[x, y, z]]
        dfTCP = pd.DataFrame(TCP, columns=['x', 'y', 'z'])

    # -----

    # Execute commands up to homing function
    dType.SetQueuedCmdStartExec(api)  # Start running commands in command queue

    # Queue homing function if homing is desired
    if homeRobot:
        # Execute the homing function. Note temp is not used by Dobot. Returned value is the last index -> "queuedCmdIndex: If this command is added to the queue, queuedCmdIndex indicates the index of this command in the queue. Otherwise, it is invalid."
        lastIndex = dType.SetHOMECmd(api, temp=0, isQueued=1)[0]
        if (verbose):
            print("retVal for homing command: {}".format(
                lastIndex))  # print command queue value

        # Loop gets current index, and waits for the command queue to finish
        while lastIndex > dType.GetQueuedCmdCurrentIndex(api)[0]:
            dType.dSleep(100)
    # Check if poses should be collected
    print("")
    collectPoses = yes_or_no("Do you want to collect robot poses? ")

    if collectPoses:

        # ---Find Current values for relevant 'HHT' (Hand hold teach functions)---

        if(verbose == True):

            retVal = dType.GetHHTTrigMode(api)
            print("retVal for GetHHTTrigMode ", retVal)

            retVal = dType.GetHHTTrigOutputEnabled(api)
            print("retVal for GetHHTTrigOutputEnabled ", retVal)

            retVal = dType.GetHHTTrigOutput(api)
            print("retVal for GetHHTTrigOutput ", retVal)

        # --- Get arm poses for 5 positions
        # First initialise space for storing data
        isTriggered = False
        poseList = []
        timeDuration = inputNumber(
            "Please input duration for pose capture in seconds ")  # seconds
        print("Duration of pose capture = ", timeDuration)
        startTime = time.time()
        timeElapsed = False
        counter = 0  # for recording poses counted

        # Loop to find arm poses
        print("Start collecting arm poses now using HHT mode...")
        print("A pose is captured each time you release the dobot arm padlock button on link 2...")

        while(not timeElapsed):
            isTriggered = dType.GetHHTTrigOutput(api)
            if isTriggered == True:
                # Get the pose [x,y,z,r, joint1,joint2,joint3,joint4]
                pose = dType.GetPose(api)
                poseList.append(pose)
                counter += 1
                print("Successfully collected pose {}".format(counter))

            currentTime = time.time()
            if (currentTime - startTime) >= timeDuration:
                timeElapsed = True

        # Print output poses
        print("Arm poses collection using HHT mode finished ...")
        print("Collected poseList = ", poseList)
        print("")

        dfPose = pd.DataFrame(
            poseList, columns=['x', 'y', 'z', 'r', 'joint1', 'joint2', 'joint3', 'joint4'])

        # Create directory:
        print("")
        print("Collected poses will be saved to a .csv file at the following datapath:")
        print("Datapath = ", os.environ['DATAPATH'])
        print("")
        folderPath = os.path.join(
            os.environ['DATAPATH'], "HHT_Poses", time.strftime('%m%d%H%M'))
        os.makedirs(folderPath)

        # Create file (Poses)
        resultsPath = folderPath + '/poses.csv'
        dfPose.to_csv(resultsPath)

        # Create file (TCP)
        resultsPath = folderPath + '/TCP.csv'
        if(setTCP == True):
            dfTCP.to_csv(resultsPath)

    # Check if user wants to print current alarms
    print("")
    printAlarms = yes_or_no(
        "Do you want to print any dobot magician alarms to the terminal? ")

    # Queue print alarms if desired
    if printAlarms:
        alarms = dType.GetAlarmsState(api)  # Get the alarms
        alarmsState = alarms[0]
        lenAlarms = alarms[1]
        print("alarms Length = {} items".format(lenAlarms))
        print("alarmsState: {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} ".format(alarmsState[0], alarmsState[1], alarmsState[2], alarmsState[3], alarmsState[
              4], alarmsState[5], alarmsState[6], alarmsState[7], alarmsState[8], alarmsState[9], alarmsState[10], alarmsState[11], alarmsState[12], alarmsState[13], alarmsState[14], alarmsState[15]))
        print(
            "[HOLD] Waiting for dobot reply to email to find out what these alarms mean")

    # Check if homing is required
    print("")
    clearAlarms = yes_or_no("Do you want to clear any dobot magician alarms? ")

    # Queue clear alarms if desired
    if clearAlarms:
        lastIndex = dType.ClearAllAlarmsState(api)  # Clear the alarms
        if (verbose):
            print("retVal for clear alarms command: {}".format(
                lastIndex))  # print command queue value

# Disconnect Dobot
dType.DisconnectDobot(api)  # Disconnect the Dobot
print("Dobot disconnected !")
