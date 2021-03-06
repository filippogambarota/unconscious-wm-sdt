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

def ask(kb, obj = None, msg = None, keyList=None, quit = 'escape', before = '', after = '', hold = False, simulate = False, rtRange = [200, 2000], obs = None, pos = (0,0)):
    """
    Display a msg and wait for keyboard (kb) response.
    Return the pressed key and the reaction time. Can append a before/after string. If hold = True no text is used. Useful for asking for a response while the stimulus is on the screen.
    """
    keyList_sim = keyList.copy() # keylist without escape for simulation
    keyList.append(quit)
    
    if not hold:
        obj.pos = pos
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

def feedback(pas_resp):
    if pas_resp == "1":
        FEEDBACK = FEEDBACK_POSITIVE.format(pas_resp)
    else:
        FEEDBACK = FEEDBACK_NEGATIVE.format(pas_resp)
    
    text.text = FEEDBACK
    text.draw()
    win.flip()
    core.wait(FEEDBACK_DUR)

# Kill switch for Psychopy3 
esc_key = 'escape'

def quit():
    """Close everything and exit nicely (ending the experiment)
    """
    
    objects_to_save = {
        "subjects": V['subject'],
        "trials": trials,
        "quest_list": quest_list,
        "duration_experiment": time.time() - start_experiment # timer for the experiment
    }
    
    utils.save_objects(dirs["session"], V["subject"], objects_to_save)
    
    win.close()
    core.quit()
    

# call globalKeys so that whenever user presses escape, quit function called
event.globalKeys.add(key=esc_key, func=quit)

"""
SET VARIABLES
"""

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 32.5  # Width of your monitor in cm
MON_SIZE = [1024, 768]  # Pixel-dimensions of your monitor

# Stimulus parameters
GABOR_SF = 3.7  # 4 cycles per degree visual angle
GABOR_SIZE = 3.4  # in degrees visual angle
FIX_HEIGHT = 0.8  # Text height of fixation cross

# position of the memory gabor
GABOR_MEMORY_POS = {"tl":(-GABOR_SIZE, GABOR_SIZE),
                    "tr":(GABOR_SIZE, GABOR_SIZE),
                    "bl":(-GABOR_SIZE, -GABOR_SIZE),
                    "br":(GABOR_SIZE, -GABOR_SIZE)}
# Timings
FRAMES_FIX = 43  # in frames. ~ 500 ms on 85 Hz
FRAMES_STIM = 3  # in frames. ~ 33 ms on 85 Hz
FRAMES_MASK = 30  # in frames. ~ 350 ms on 85 Hz
FRAMES_TARGET_RESP = 85 # in frames ~1 s on 120 hz
ITI = 1.5 # in seconds, use core.wait
FEEDBACK_DUR = 1.5

# Condition parameterss
REPETITIONS = 5  # number of trials per condition
POSITIONS = 0
ORIS = [15, 45, 75, 105, 135, 165] # orientations TODO check if other oris
NTRIALS_BREAK = 50  # Number of trials between breaks
NTRIALS_PRAC = 5 # number of practice trials

# Questions and messages
MESSAGE_POS = [0, 0]  # [x, y]
MESSAGE_HEIGHT = 1  # Height of the text, still in degrees visual angle

# Keys
KEYS_QUIT = ['escape']  # Keys that quits the experiment
PAS_RESP = {'1': 'pas1', '2': 'pas2', '3':'pas3', '4': 'pas4'} # pas keys
VIS_RESP = {'pas1': 0, 'pas2': 1, 'pas3': 1, 'pas4': 1} # keys for staircase from PAS RESP
TEST_RESP = {'f': 'same', 'j': 'change'} # keys for the change detection task

"""
Text Messages
"""

INSTR_WELCOME = """
    Benvenutə in questo esperimento!
    
    Premi la barra spaziatrice per continuare!
"""

INSTR_GENERAL = """
    In questo esperimento vedrai una croce di fissazione, seguita da uno stimolo visivo presentato molto velocemente sempre al centro che dovrai cercare di memorizzare. Dopo un breve intervallo (circa 1 secondo) comparirà un altro stimolo visivo. Il tuo compito è confrontare il primo stimolo con il secondo e poi riportare la tua esperienza visiva del primo stimolo.
    
    Premi la barra spaziatrice per continuare le istruzioni
"""
    
INSTR_GABOR = """
    Gli stimoli che useremo si chiamano Gabor patch. Sono delle griglie circolari in bianco e nero, che possono essere ruotate con diversi orientamenti. Ecco un esempio:
"""

INSTR_MASKING = """
    La prima Gabor sarà presentata molto velocemente e seguita da un'altro stimolo formato da rumore visivo bianco e nero. Dovrai focalizzarti solo sulla Gabor e sul suo orientamento, il secondo stimolo non è rilevante.
    
    Essendo presentata velocemente, alcune volte sarà più difficile vederla e altre volte non vedrai proprio niente. Non ti preoccupare è totalmente normale.
"""

# TODO counterbalance between f and j
INSTR_MEMORY_PROBE = """
    Il tuo compito è quello di focalizzarti sulla prima Gabor e sul suo orientamento e cercare di mantenerla in memoria. Anche se non hai visto chiaramente la Gabor non ti preoccupare, cerca di mantenerla in memoria comunque.
    
    Dopo un breve intervallo, comparirà sempre al centro un'altra Gabor che potrà avere un orientamento UGUALE o DIVERSO rispetto a quello che hai visto in precedenza. Il tuo compito è rispondere più accuratamente possibile se l'orientamento è uguale o diverso. Se non hai visto la Gabor non ti preoccupare, tenta comunque di dare la risposta, anche se dovessi rispondere casualmente.
    
    Premi "F" se l'orientamento è UGUALE
    Premi "J" se l'orientamento è DIVERSO
"""

INSTR_PAS = """
    Infine ti sarà chiesto di riportare la tua ESPERIENZA VISIVA rispetto l'ORIENTAMENTO della prima Gabor (quella presentata velocemente). Ricorda che in questa domanda non ci sono risposte giuste o sbagliate. Siamo solo interessati a comprendere la tua esperienza il più accuratamente possibile.
    
    Puoi usare queste opzioni di risposta:
    
    1 = Non ho visto l'orientamento
    2 = Ho la sensazione di aver visto l'orientamento
    3 = Ho visto abbastanza chiaramente l'orientamento
    4 = Ho visto chiaramente l'orientamento
"""

INSTR_FEEDBACK = """
    Alcune volte ci saranno dei trial senza nessuno stimolo. Dopo che avrai dato la risposta di visibilità a questi trial ti sarà dato un feedback in funzione che tu dica di aver visto qualcosa oppure no. Questo serve soltanto affinchè tu possa adattare al meglio le tue risposte. 
"""

FEEDBACK_POSITIVE = """
    Ottimo! non c'era la Gabor e hai risposto {}
"""

FEEDBACK_NEGATIVE = """
    Attenzione! non c'era la Gabor e hai risposto {}
"""
    
INSTR_START_EXPERIMENT = """
    La pratica è finita!
    
    Se vuoi possiamo fare qualche altro trial di prova.
    
    Premi P per fare ancora un pochino di pratica
    Premi la barra spaziatrice per cominciare l'esperimento
"""

PRAC_INSTRUCTIONS = """
    Prima di cominciare l'esperimento facciamo qualche trial di prova.

    Premi la barra spaziatrice per cominciare
"""
    
PAS_RESPONSE = """
    1 = Non ho visto l'orientamento
    2 = Ho la sensazione di aver visto l'orientamento
    3 = Ho visto abbastanza chiaramente l'orientamento
    4 = Ho visto chiaramente l'orientamento
"""

END_EXPERIMENT = """
    L'esperimento è finito!
    
    Grazie per aver partecipato! :)
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

V = {'subject':'', 'age':'', 'gender':['male', 'female'], 'simulate':[False, True], 'maindir': [True, False]}
#V = {'subject':'', 'age':'', 'gender':['male', 'female']}
if not gui.DlgFromDict(V, order=['subject', 'age', 'gender']).OK:
    core.quit()

V['simulate'] = utils.str2bool(V['simulate']) # force to boolean from the gui
V['maindir'] = utils.str2bool(V['maindir']) # force to boolean from the gui

dirs = utils.get_dirs(simulate=V['simulate'], maindir = V['maindir']) # get dirs according to simulation or real

"""
Create Condition Dictionary
Each element of the dictonary will be combined using itertools.product() in order to have all the combinations.
"""

cond = {
    "subject": [V['subject']],
    "age": [V['age']],
    "gender": [V["gender"]],
    "ntrial": [0],
    "memory_ori": ORIS,
    'test_ori': [0],
    "type": ["change", "same"],
    "trial_type": ["valid", "catch"],
    "which_change": ["clock", "anti"],
    #"memory_pos": ['0'],
    "trial": range(1, REPETITIONS + 1),
    "quest": range(3),
    "pas": [''],
    "pas_rt": [0],
    "vis": [0],
    "test_key": [''],
    "test": [''],
    "test_rt": [0],
    "contrast": [0],
    "fix_dur": [0],
    "target_dur": [0],
    "mask_dur": [0],
    "retention_dur": [0],
    "trial_dur": [0]
}

trials, nvalid, ncatch = utils.create_conditions(cond, prop_catch=1/3) # create the combinations. prop_catch is the proportions of catch trials to create
trials = random.sample(trials, len(trials)) # shuffling order
trials = set_ori(trials, diff = 50) # add the test orientations

# Create psychopy window
background_color = [0,0,0] # ~ grey

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color=background_color)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!
objects_color = "white"
win.mouseVisible = False # hide mouse

# Init the trial-by-trial saving function
writer = utils.csv_writer(cond, V["subject"], dirs["csv"])

"""
OBJECTS
"""

fix = visual.TextStim(win, '+', height=FIX_HEIGHT)  # Fixation cross is just the character "+". Units are inherited from Window when not explicitly specified.

gabor_prac = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0))  # A gabor patch. Again, units are inherited.

gabor_memory = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0))  # A gabor patch. Again, units are inherited.

gabor_test = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0), contrast = 1)  # A gabor patch. Again, units are inherited.

mask = visual.GratingStim(win, size=GABOR_SIZE, interpolate=False, autoLog=False, mask="circle", pos = (0, 0)) # mask for the backward masking. The texture is generated trial-by-trial

mask_prac = visual.GratingStim(win, size=GABOR_SIZE, interpolate=False, autoLog=False, mask="circle", pos = (0, 0)) # mask for the backward masking. The texture is generated trial-by-trial

text = visual.TextStim(win, pos=MESSAGE_POS, height=MESSAGE_HEIGHT, wrapWidth=30)  # Message / question stimulus. Will be used to display instructions and questions.

black_screen = visual.Rect(win, size = (MON_SIZE), units = "pix", fillColor = "black")

kb = keyboard.Keyboard() # init the keyboard

# Timing

clock_stim = core.Clock() # clock for the target
clock_trial = core.Clock() # clock for the trial

"""
Quest
Here we create the quest staircases with parameters. Each staircase will run for ntrials/nstaircase trials
"""

obs = utils.psy_observer(0.5, 0.2, 0, 0) # init ideal observer for simulation
fa_rate = 0 # TODO check fa value
lapse_rate = 0.01

# TODO set better values for other parameters

quest0 = data.QuestHandler(0.2, 0.2, beta = 3.5,
    pThreshold = 0.50, gamma = fa_rate, delta = lapse_rate,
    minVal=0, maxVal=1,
    ntrials = round(nvalid/3))

quest1 = data.QuestHandler(0.2, 0.2, beta = 3.5,
    pThreshold = 0.65, gamma = fa_rate, delta = lapse_rate,
    minVal=0, maxVal=1,
    ntrials = round(nvalid/3))

quest2 = data.QuestHandler(0.2, 0.2, beta = 3.5,
    pThreshold = 0.80, gamma = fa_rate, delta = lapse_rate,
    minVal = 0, maxVal = 1,
    ntrials = round(nvalid/3))

quest_list = [quest0, quest1, quest2] # list of QUEST in order to randomize the presentation. TODO check if better using the multistairhandler

"""
Experiment
"""

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
        
        # Check if catch and set contrast to 0, else take the QUEST
        
        if trial["trial_type"] == "catch":
            contrast_trial = 0
        else:
            if isPrac:
                contrast_trial = random.uniform(0, 1)
            else:
                contrast_trial = quest_list[quest_trial]._nextIntensity # suggest contrast
        
        obs.xi = contrast_trial # add contrast to observer
        gabor_memory.contrast = contrast_trial # assign contrast to memory
        gabor_memory.ori = trial['memory_ori'] # assign ori to memory
        gabor_pos_trial = random.choice(list(GABOR_MEMORY_POS.keys())) # get random position
        #gabor_memory.pos = GABOR_MEMORY_POS[gabor_pos_trial] # set the random position
        gabor_test.ori = trial['test_ori'] # assign ori to test
        mask.tex = np.random.rand(256, 256) * 2.0 - 1 # create numpy array for the mask 
        #mask.pos = GABOR_MEMORY_POS[gabor_pos_trial] # position of the mask
        # -- STARTING TRIAL
        clock_trial.reset()
        
        # Fixation
        clock_stim.reset()
        for frame in range(FRAMES_FIX):
            fix.draw()
            win.flip()
        fix_dur = clock_stim.getTime() 
        
        # Gabor
        clock_stim.reset()
        for frame in range(FRAMES_STIM):
            gabor_memory.draw()
            win.flip()
        target_dur = clock_stim.getTime()    

        # Mask
        clock_stim.reset()
        for frame in range(FRAMES_MASK):
            mask.draw()
            win.flip()
        mask_dur = clock_stim.getTime()
        
        # Retention
        clock_stim.reset()
        for frame in range(FRAMES_TARGET_RESP):
            fix.draw()
            win.flip()
        retention_dur = clock_stim.getTime()
        
        # Test
        gabor_test.draw() # drawing gabor for holding
        test_resp, test_rt = ask(kb, keyList = list(TEST_RESP.keys()), hold = True, simulate=V['simulate'])
        
        # PAS
        pas_resp, pas_rt = ask(kb, text, PAS_RESPONSE, list(PAS_RESP.keys()), simulate=V['simulate'], obs=obs) # pas
        
        if trial["trial_type"] == "catch" or contrast_trial == 0:
            win.flip()
            feedback(pas_resp)
        
        # ITI
        black_screen.draw() # avoid after-effects
        win.flip() # blank screen
        core.wait(ITI)
        
        trial_dur = clock_trial.getTime()
        
        # --- END TRIAL
        
        # Update QUEST
        vis_resp = VIS_RESP[PAS_RESP[str(pas_resp)]] # coverting to 0-1
        
        if trial[ "trial_type"] == "valid" and not isPrac: # update only if valid and not prac
            quest_list[quest_trial].addResponse(vis_resp) # updating
        
        #-- Update Dict
        
        trial['contrast'] = contrast_trial
        trial['test_key'] = test_resp
        trial['test'] = TEST_RESP[test_resp]
        trial['test_rt'] = test_rt
        trial['pas'] = pas_resp
        trial['pas_rt'] = pas_rt
        trial['vis'] = vis_resp
        trial['ntrial'] = i + 1 # setting the correct trial number
        # timing
        #trial['memory_pos'] = GABOR_MEMORY_POS[gabor_pos_trial],
        trial['target_dur'] = target_dur
        trial['mask_dur'] = mask_dur
        trial['retention_dur'] = retention_dur
        trial['fix_dur'] = fix_dur
        trial['trial_dur'] = trial_dur

        # Saving Data
        if not isPrac:
            writer.write(trial)

"""
Actual Experiment Running
"""

start_experiment = time.time() # timer for the overall experiment

# Welcome
ask(kb, text, INSTR_WELCOME, ['space'], simulate=V['simulate'])

# Instructions
ask(kb, text, INSTR_GENERAL, ['space'], simulate=V['simulate'])

# Demo Gabor
gabor_prac.ori = 45
gabor_prac.pos = (-8, -5)
gabor_prac.draw()
gabor_prac.ori = 0
gabor_prac.pos = (0, -5)
gabor_prac.draw()
gabor_prac.ori = 90
gabor_prac.pos = (8, -5)
gabor_prac.draw()

ask(kb, text, INSTR_GABOR, ['space'], simulate=V['simulate'], pos = (0, 5))

# Demo Masking

mask_prac.tex = np.random.rand(256, 256) * 2.0 - 1 # create numpy array for
mask_prac.pos = (5, -5)
gabor_prac.ori = 45
gabor_prac.pos = (-5, -5)
mask_prac.draw()
gabor_prac.draw()

ask(kb, text, INSTR_MASKING, ['space'], simulate=V['simulate'], pos = (0, 5))

# Probe
ask(kb, text, INSTR_MEMORY_PROBE, ['space'], simulate=V['simulate'])

# PAS
ask(kb, text, INSTR_PAS, ['space'], simulate=V['simulate'])

# Feedback
ask(kb, text, INSTR_FEEDBACK, ['space'], simulate=V['simulate'])

# Practice
ask(kb, text, PRAC_INSTRUCTIONS, ['space'], simulate=V['simulate'])

experiment(trials, ntrials = NTRIALS_PRAC, isPrac=True)

# checking for more practice

again_prac = True

while again_prac:
    prac_key, prac_key_rt = ask(kb, text, INSTR_START_EXPERIMENT, ['space', 'p'], simulate=V['simulate'])
    if prac_key == "p":
        experiment(trials, ntrials = NTRIALS_PRAC, isPrac=True)
    else:
        again_prac = False
    

# Experiment
experiment(trials)

# END
ask(kb, text, END_EXPERIMENT, ['space'], simulate=V['simulate'])

duration_experiment = time.time() - start_experiment # timer for the experiment

# Backup Data

objects_to_save = {
    "subjects": V['subject'],
    "trials": trials,
    "quest_list": quest_list,
    "duration_experiment": duration_experiment
}

utils.save_objects(dirs["session"], V["subject"], objects_to_save)