# -*- coding: utf-8 -*-

"""
Modules
"""

from psychopy import core, visual, gui, monitors, event, data # psychopy stuff
from psychopy.hardware import keyboard
import numpy as np
import utils
import time
import random

"""
Functions
"""

def set_ori(trials, diff):
    """
    Assign the correct orientation for a given difference (diff)
    in degrees
    """
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

def ask(kb, obj, msg = None, keyList=None, quit = 'escape', before = '', after = '', hold = False, simulate = False, rtRange = [200, 2000], obs = None):
    """
    Display a msg and wait for keyboard (kb) response.
    Return the pressed key and the reaction time. Can append a before/after string. If hold = True no text is used. Useful for asking for a response while the stimulus is on the screen.
    """
    keyList_sim = keyList.copy() # keylist without escape for simulation
    keyList.append(quit)
    
    if hold:
        obj.draw()
    else:
        obj.text = msg
        obj.draw()
    
    win.callOnFlip(kb.clock.reset) # clock to stimulus flip
    win.flip()
    
    # select the first (only) response
    if simulate:
        keypress = utils.simKeys(keyList_sim, rtRange, obs)
        core.wait(keypress.rt)
        key_name = keypress.name
        key_rt = keypress.rt
    else:
        key = kb.waitKeys(keyList = keyList, waitRelease = True)[0]
        key_name = key.name
        key_rt = key.rt
    
    return before + key_name + after, key_rt

# Kill switch for Psychopy3 
esc_key = 'escape'

def quit():
    """Close everything and exit nicely (ending the experiment)
    """
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

# Stimulus parameters
GABOR_SF = 3.7  # 4 cycles per degree visual angle
GABOR_SIZE = 3.4  # in degrees visual angle
FIX_HEIGHT = 0.8  # Text height of fixation cross

# Timings
FRAMES_FIX = 30  # in frames. ~ 500 ms on 120 Hz
FRAMES_STIM = 2  # in frames. ~ 33 ms on 120
FRAMES_MASK = 21  # in frames. ~ 350 ms on 120 Hz
FRAMES_TARGET_RESP = 60 # in frames ~1 s on 120 hz
ITI = 1

# Condition parameterss
PRAC_TRIALS = 5 # number of practice trials
REPETITIONS = 7  # number of trials per condition
POSITIONS = 0
ORIS = [15, 45, 75, 105, 135, 165] # orientations
NTRIALS_BREAK = 50  # Number of trials between breaks
NTRIALS_PRAC = 10 # number of practice trials

# Questions and messages
MESSAGE_POS = [0, 0]  # [x, y]
MESSAGE_HEIGHT = 1  # Height of the text, still in degrees visual angle

# Keys
KEYS_QUIT = ['escape']  # Keys that quits the experiment
PAS_RESP = {'1': 'pas1', '2': 'pas2', '3':'pas3', '4': 'pas4'} # pas keys
VIS_RESP = {'pas1': 0, 'pas2': 1, 'pas3': 1, 'pas4': 1} # keys for staircase from PAS RESP
TEST_RESP = {'f': 'change', 'j': 'same'} # keys for the change detection task

"""
Text Messages
"""

INSTR_WELCOME = """
    Benvenutə in questo esperimento!
    
    Premi la barra spaziatrice per continuare!
"""
    
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
    
PAS_RESPONSE = """
1 = "I did not see the stimulus"
2 = "I saw only a brief glimpse of the stimulus"
3 = "I almost saw the stimulus"
4 = "I clearly saw the stimulus"
"""

END_INSTRUCT = """
    Thank you for the participation!
    Just few seconds, I'm saving images for the main experiment! :)
"""

TXT_BREAK = """
Puoi prenderti una pausa!
Premi la barra spaziatrice per continuare l'esperimento!
"""

print('the physical diameter of the gabor patch should be', utils.deg2cm(GABOR_SIZE, MON_DISTANCE), 'cm')
print('the physical size of the fixation cross should be', utils.deg2cm(FIX_HEIGHT, MON_DISTANCE), 'cm')

"""
 SHOW DIALOGUE AND INITIATE PSYCHOPY STIMULI
 This is computationally heavy stuff. Thus we do it in the beginning of our experiment
"""

V = {'subject':'', 'age':'', 'gender':['male', 'female'], 'simulate':[False, True]}
#V = {'subject':'', 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()

V['simulate'] = utils.str2bool(V['simulate']) # force to boolean from the gui

dirs = utils.make_dirs()

"""
Create Condition Dictionary
Each element of the dictonary will be combined using itertools.product() in order to have all the combinations.
"""

cond = {
    "subject": V['subject'],
    "age": V['age'],
    "gender": V["gender"],
    "memory_ori": ORIS,
    'test_ori': [0],
    "type": ["change", "same"],
    "trial_type": ["valid", "catch"],
    "which_change": ["clock", "anti"],
    "trial": range(1, REPETITIONS + 1),
    "quest": range(3),
    "pas": [''],
    "pas_rt": [0],
    "vis": [0],
    "test_key": [''],
    "test": [''],
    "test_rt": [0],
    "contrast": [0]
}

trials, nvalid, ncatch = utils.create_conditions(cond, prop_catch=2/3) # create the combinations. prop_catch is the proportions of catch trials to create
trials = random.sample(trials, len(trials)) # shuffling order
trials = set_ori(trials, diff = 50) # add the test orientations

# Create psychopy window
background_color = [0,0,0] # ~ grey

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color=background_color)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!
objects_color = "white"

# Init the trial-by-trial saving function
writer = utils.csv_writer(cond, V["subject"], dirs["csv"])

"""
OBJECTS
"""

fix = visual.TextStim(win, '+', height=FIX_HEIGHT)  # Fixation cross is just the character "+". Units are inherited from Window when not explicitly specified.
gabor_memory = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0))  # A gabor patch. Again, units are inherited.

gabor_test = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0), contrast = 1)  # A gabor patch. Again, units are inherited.

mask = visual.GratingStim(win, size=GABOR_SIZE, interpolate=False, autoLog=False, mask="circle", pos = (0, 0)) # mask for the backward masking. The texture is generated trial-by-trial

text = visual.TextStim(win, pos=MESSAGE_POS, height=MESSAGE_HEIGHT, wrapWidth=40)  # Message / question stimulus. Will be used to display instructions and questions.

kb = keyboard.Keyboard() # init the keyboard

"""
Quest
Here we create the quest staircases with parameters. Each staircase will run for ntrials/nstaircase trials
"""

obs = utils.psy_observer(0.5, 0.2, 0, 0) # init ideal observer for simulation

quest_50 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.5, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = round(nvalid/3))

quest_70 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.7, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = round(nvalid/3))

quest_80 = data.QuestHandler(0.5, 0.2, beta = 3.5,
    pThreshold=0.8, gamma=0, delta = 0,
    minVal=0, maxVal=1,
    ntrials = round(nvalid/3))

quest_list = [quest_50, quest_70, quest_80] # list of QUEST in order to randomize the presentation. TODO check if better using the multistairhandler

"""
Experiment
"""
start_experiment = time.time() # timer for the overall experiment

def experiment(trials, ntrials = None, isPrac = False):
    """
    This function run the experiment or a subset of trials (for the practice). If the isPrac argument is True, a subset of random trials (ntrials) will be selected and used in the practice.
    """
    
    if isPrac:
        prac_idx = random.sample(range(len(trials)), ntrials) # random index
        trials = [trials[i] for i in prac_idx] # select only practice trials

    # Start Experiment

    for i in range(len(trials)):
        
        # Check for break
        if i % NTRIALS_BREAK == 0 and i != 0:
            ask(kb, text, TXT_BREAK, ["space"], simulate=V['simulate'])
        
        # Init trial
        trial = trials[i] # get current dictionary
        quest_trial = trial['quest'] # get index quest
        contrast_trial = quest_list[quest_trial]._nextIntensity # suggest contrast
        obs.xi = contrast_trial # add contrast to observer
        gabor_memory.contrast = contrast_trial # assign contrast to memory
        gabor_memory.ori = trial['memory_ori'] # assign ori to memory
        gabor_test.ori = trial['test_ori'] # assign ori to test
        mask.tex = np.random.rand(256, 256) * 2.0 - 1 # create numpy array for the mask 
        
        # -- STARTING TRIAL
        
        # Fixation
        for frame in range(FRAMES_FIX):
            fix.draw()
            win.flip()
            
        # Gabor
        for frame in range(FRAMES_STIM):
            gabor_memory.draw()
            win.flip()
            
        # Mask
        for frame in range(FRAMES_MASK):
            mask.draw()
            win.flip()
            
        # Retention
        for frame in range(FRAMES_TARGET_RESP):
            fix.draw()
            win.flip()
            
        # Test
        test_resp, test_rt = ask(kb, gabor_test, keyList = list(TEST_RESP.keys()), hold = True, simulate=V['simulate'])
        
        # PAS
        pas_resp, pas_rt = ask(kb, text, PAS_RESPONSE, list(PAS_RESP.keys()), simulate=V['simulate'], obs=obs) # pas
        
        # ITI
        win.flip() # blank screen
        core.wait(ITI)
        
        # --- END TRIAL
        
        # Update QUEST
        vis_resp = VIS_RESP[PAS_RESP[str(pas_resp)]] # coverting to 0-1
        
        if trial[ "trial_type"] == "valid": # update only if not catch
            quest_list[quest_trial].addResponse(vis_resp) # updating
        
        # Update Dict
        trial['contrast'] = contrast_trial
        trial['test_key'] = test_resp
        trial['test'] = TEST_RESP[test_resp]
        trial['test_rt'] = test_rt
        trial['pas'] = pas_resp
        trial['pas_rt'] = pas_rt
        trial['vis'] = vis_resp

        # Saving Data
        if not isPrac:
            writer.write(trial)

duration_experiment = time.time() - start_experiment # timer for the experiment

"""
Actual Experiment Running
"""

# Welcome
ask(kb, text, INSTR_WELCOME, ['space'], simulate=V['simulate'])

# TODO add instructions

# Practice
ask(kb, text, PRAC_INSTRUCTIONS, ['space'], simulate=V['simulate'])
experiment(trials, ntrials = NTRIALS_PRAC, isPrac=True)

# Experiment
ask(kb, text, INSTR_START_EXPERIMENT, ['space'], simulate=V['simulate'])
experiment(trials)

# Backup Data

objects_to_save = {
    "subjects": V['subject'],
    "trials": trials,
    "quest_list": quest_list,
    "duration_experiment": duration_experiment
}

utils.save_objects(dirs["session"], V["subject"], objects_to_save)