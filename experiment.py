# -*- coding: utf-8 -*-

"""
Modules
"""

from psychopy import core, visual, gui, monitors, event # psychopy stuff
from psychopy.hardware import keyboard
import numpy as np
import itertools
import utils
import os

"""
Functions
"""

# Assingn the correct orientation

def set_ori(trials, diff):
    for trial in trials:
        ori = trial['memory_ori']
        if trial['type'] == 'change':
            if trial['which_change'] == "clock":
                trial['test_ori'] = ori + diff
            else:
                if ori < diff:
                    trial['test_ori'] = 360 - abs(ori - diff)
                else:
                    trial['test_ori'] = ori - diff
        else:
            trial['test_ori'] = ori
    return trials

# Keyboard Response

def ask(kb, txtstim, msg, keyList=None, quit = 'escape'):
    """
    Display a msg and wait for keyboard (kb) response.
    Return the pressed key and the reaction time
    """
    keyList.append(quit)
    txtstim.text = msg
    txtstim.draw()
    win.callOnFlip(kb.clock.reset) # clock to stimulus flip
    win.flip()
    
    # select the first (only) response
    key = kb.waitKeys(keyList = keyList, waitRelease = True)[0]
    
    return key.name, key.rt

# Kill switch for Psychopy3 

esc_key= 'escape'

def quit():
    """ quit programme"""
    print ('User exited')
    win.close()
    core.quit()

# call globalKeys so that whenever user presses escape, quit function called
event.globalKeys.add(key=esc_key, func=quit)

"""
SET VARIABLES
"""

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 51  # Width of your monitor in cm
MON_SIZE = [600, 600]  # Pixel-dimensions of your monitor
SAVE_FOLDER = 'data'  # Log is saved to this folder. The folder is created if it does not exist.

# Stimulus parameters
GABOR_SF = 3.7  # 4 cycles per degree visual angle
GABOR_SIZE = 3.4  # in degrees visual angle
FIX_HEIGHT = 0.8  # Text height of fixation cross

# Timings
FRAMES_FIX = 60  # in frames. ~ 500 ms on 120 Hz
FRAMES_CUE = 60  # in frames. ~ 500 ms on 120 Hz
FRAMES_STIM = 4  # in frames. ~ 33 ms on 120
FRAMES_MASK = 42  # in frames. ~ 350 ms on 120 Hz
FRAMES_TARGET_RESP = 180 # in frames ~1 s on 120 hz
ITI = 1

# Condition parameterss
PRAC_TRIALS = 5 # number of practice trials
REPETITIONS = 7  # number of trials per condition
NCATCH = 0 # number of catch trials
POSITIONS = 0
ORIS = [15, 45, 75, 105, 135, 165]
PAUSE_INTERVAL = 200  # Number of trials between breaks

# Questions and messages
MESSAGE_POS = [0, 0]  # [x, y]
MESSAGE_HEIGHT = 1  # Height of the text, still in degrees visual angle
TEXT_BREAK = 'Press any key to continue...'  # text of regular break
KEYS_QUIT = ['escape']  # Keys that quits the experiment
VIS_RESP = {'pas1': 0, 'pas2': 1, 'pas3': 1, 'pas4': 1} # keys for staircase, this is useful for getting the key for the staircase from the response

INSTR_WELCOME = """
    Welcome to this experiment!
    The experiment is composed of two parts. 
    During first part (~10 min) we will the find the best stimuli to use in the main experiment (second part).

    Press the spacebar to continue! """
    
    
INSTR_GABOR = """
    In this first part you need to report the visibility of briefly presented stimuli. 
    These stimuli called gabor patches (or gratings) are simple shapes where the orientation is the main feature.
    The stimulus will be briefly presented and followed by an irrelevant stimulus (mask).
    Press the spacebar to continue!"""

INSTR_FIX_RESP = """
    The experiment trial start with a fixation cross followed by 2 arrows that indicate the left or the right side of the screen.
    You need to focus your attention on the cued side and report the visibility of the stimulus.
    You can use the mouse clicking on the white square associated with these alternatives:

    - I did not see the stimulus
    - I saw only a brief glimpse of the stimulus
    - I almost saw the stimulus
    - I clearly saw the stimulus
    
    Press the spacebar to continue """
    
INSTR_EXPERIENCE = """
    IMPORTANT: Remember that there are no correct or wrong responses. 
    We are interested in understanding your personal experience so choose the response that match your experience as much as possible.
    
    Press the spacebar to continue """

INSTR_ATTENTION = """
    During the entire experiment, try to keep the eyes on the fixation cross. When you see the stimuli focus your attention on the cued side without moving your gaze.
    Before starting we are going to see some example of stimuli do some practice trials.
    
    Press the spacebar to continue """

INSTR_EXAMPLE_GABOR = """
    You are gonna see stimuli like this:

    Press the spacebar to continue """
    
INSTR_START_EXPERIMENT = """
    The practice is finished!
    
    Press the spacebar to start the main experiment!
"""

EXP_INTRODUCTION_FINAL = """
    
    Please remember that there are no correct or wrong responses, 
    
    simply try to report your subjective experience as much as possible.

    Press the spacebar to continue """

PRAC_INSTRUCTIONS = """
    You are gonna do some practice trials.

    Press the spacebar to continue """

PAS1 = "I did not see the stimulus"
PAS2 = "I saw only a brief glimpse of the stimulus"
PAS3 = "I almost saw the stimulus"
PAS4 = "I clearly saw the stimulus"

END_INSTRUCT = """
    Thank you for the participation!
    Just few seconds, I'm saving images for the main experiment! :)"""

"""
print('the physical diameter of the gabor patch should be', ppc.deg2cm(GABOR_SIZE, MON_DISTANCE), 'cm')
print('the physical size of the fixation cross should be', ppc.deg2cm(FIX_HEIGHT, MON_DISTANCE), 'cm')
"""

"""
 SHOW DIALOGUE AND INITIATE PSYCHOPY STIMULI
 This is computationally heavy stuff. Thus we do it in the beginning of our experiment
"""

# Intro-dialogue. Get subject-id and other variables.
# Save input variables in "V" dictionary (V for "variables")
V = {'subject':'', 'age':'', 'gender':['male', 'female']}

#V = {'subject':'', 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()

"""
Create Condition Dictionary
"""

cond = {
    "subject": V['subject'],
    "age": V['age'],
    "gender": V["gender"],
    "ori": ORIS,
    "type": ["change", "same"],
    "trial_type": ["valid", "catch"],
    "which_change": ["clock", "anti"],
    "trial": range(1, REPETITIONS + 1),
    "quest": range(3),
    "pas": [''],
    "pas_rt": [''],
    "contrast": ['']
}

trials = utils.create_conditions(cond, prop_catch=2/3)

# Create psychopy window
background_color = [0,0,0] # ~grey

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color=background_color)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!
objects_color = "white"

# Init the trial-by-trial saving function
writer = utils.csv_writer(str(V['subject']), folder = '.')  # writer.write(trial) will write individual trials with low latency

subj_folder = os.path.join()

stim_text = visual.TextStim(win, pos=MESSAGE_POS, height=MESSAGE_HEIGHT, wrapWidth=40)  # Message / question stimulus. Will be used to display instructions and questions.

kb = keyboard.Keyboard() # init the keyboard

for trial in trials:
    pas, pas_rt = ask(kb, stim_text, "Tioca", ["left", "right"])
    print(pas)
    print(pas_rt)
    win.flip()
