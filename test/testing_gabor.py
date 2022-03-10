import random
from psychopy import core, visual, gui, monitors, event, data # psychopy stuff
from psychopy.hardware import keyboard

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 51  # Width of your monitor in cm
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor

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
ORIS = [15, 45, 75, 105, 135, 165] # orientations TODO check if other oris
NTRIALS_BREAK = 50  # Number of trials between breaks
NTRIALS_PRAC = 10 # number of practice trials

# Questions and messages
MESSAGE_POS = [0, 0]  # [x, y]
MESSAGE_HEIGHT = 1  # Height of the text, still in degrees visual angle

# Create psychopy window
background_color = [0,0,0] # ~ grey

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color=background_color)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!
objects_color = "white"
win.mouseVisible = False # hide mouse

gabor_center = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (0, 0), contrast = 1)  # A gabor patch. Again, units are inherited.
gabor_left = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (-8, 0), contrast = 1)  # A gabor patch. Again, units are inherited.
gabor_right = visual.GratingStim(win, mask='gauss', sf = GABOR_SF, size = GABOR_SIZE, pos = (8, 0), contrast = 1)  # A gabor patch. Again, units are inherited.

text = visual.TextStim(win, pos=MESSAGE_POS, height=MESSAGE_HEIGHT, wrapWidth=30)  # Message / question stimulus. Will be used to display instructions and questions.


ORIS = [15, 45, 75, 105, 135, 165] # orientations TODO check if other oris
kb = keyboard.Keyboard() # init the keyboard
    
for i in range(10):
    ori = random.choice(list(range(0, 180)))
    # hard
    text.text = "HARD 30 degree"
    text.pos = (-8, 9)
    text.draw()
    diff = 30
    gabor_center.pos = (0, 5)
    gabor_left.pos = (-8, 5)
    gabor_right.pos = (8, 5)
    gabor_center.ori = ori
    gabor_center.draw()
    if ori < diff:
        gabor_left.ori = 180  - abs(ori - diff)
    else:
        gabor_left.ori = ori - diff
    gabor_right.ori = ori + diff
    gabor_center.draw()
    gabor_right.draw()
    gabor_left.draw()
    
    # easy
    text.text = "EASY 50 degree"
    text.pos = (-8, -9)
    text.draw()
    diff = 50
    gabor_center.pos = (0, -5)
    gabor_left.pos = (-8, -5)
    gabor_right.pos = (8, -5)
    gabor_center.ori = ori
    gabor_center.draw()
    if ori < diff:
        gabor_left.ori = 180 - abs(ori - diff)
    else:
        gabor_left.ori = ori - diff
    gabor_right.ori = ori + diff
    gabor_center.draw()
    gabor_right.draw()
    gabor_left.draw()
    
    win.flip()
    kb.waitKeys(keyList = ["space"], waitRelease = True)   
    
   
    