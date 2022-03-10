from psychopy import core, visual, gui, monitors, event # psychopy stuff
from psychopy.hardware import keyboard
import numpy as np
import itertools
import modules.utils as utils
import os

# Monitor parameters
MON_DISTANCE = 60  # Distance between subject's eyes and monitor
MON_WIDTH = 51  # Width of your monitor in cm
MON_SIZE = [1920, 1080]  # Pixel-dimensions of your monitor
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
VIS_RESP = {'pas1': 0, 'pas2': 1, 'pas3': 1, 'pas4': 1} # keys for staircase

# Create psychopy window
background_color = [0,0,0] # ~grey

my_monitor = monitors.Monitor('testMonitor', width=MON_WIDTH, distance=MON_DISTANCE)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_SIZE)

win = visual.Window(monitor=my_monitor, units='deg', fullscr=True, allowGUI=False, color=background_color)  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!
objects_color = "white"

gabor = visual.GratingStim(win, mask='gauss', sf=GABOR_SF, size=GABOR_SIZE, pos = (0,0))  # A gabor patch. Again, units are inherited.
gabor_anti = visual.GratingStim(win, mask='gauss', sf=GABOR_SF, size=GABOR_SIZE, pos = (-5,0))  # A gabor patch. Again, units are inherited.
gabor_clock = visual.GratingStim(win, mask='gauss', sf=GABOR_SF, size=GABOR_SIZE, pos = (5,0))  # A gabor patch. Again, units are inherited.

def crop_images(folder, ext, x, y, width, height):
    from PIL import Image
    import glob
    import os

    imlist = glob.glob(os.path.join(folder, '*.' + ext))
    
    for im in range(len(imlist)):
        temp = Image.open(imlist[im]) # read the image
        temp_crop = temp.crop((x, y, x + width, y + height)) # crop
        temp_crop.save(imlist[im]) # save

kb = keyboard.Keyboard() # init the keyboard

ORI = [15, 45, 75, 105, 135, 165]
step = 50

"""
# memory
for ori in ORI:
    gabor.ori = ori
    gabor.draw()
    win.getMovieFrame('back')
    win.saveMovieFrames('gabor/memory/' + 'ori_' + str(gabor.ori) + '.jpg')
    win.clearBuffer()

# clock
for ori in ORI:
    gabor.ori = ori + 50
    gabor.draw()
    win.getMovieFrame('back')
    win.saveMovieFrames('gabor/clock/' + 'ori_' + str(gabor.ori) + '.jpg')
    win.clearBuffer()
    
# anticlock
for ori in ORI:
    if ori < step:
        gabor.ori = 360 - abs(ori - step)
    else:
        gabor.ori = ori - step
    gabor.draw()
    win.getMovieFrame('back')
    win.saveMovieFrames('gabor/anticlock/' + 'ori_' + str(gabor.ori) + '.jpg')
    win.clearBuffer()
"""

for ori in ORI:
    gabor.ori = ori
    gabor_clock.ori = ori + step
    if ori < step:
        gabor_anti.ori = 360 - abs(ori - step)
    else:
        gabor_anti.ori = ori - step
    
    gabor.draw()
    gabor_anti.draw()
    gabor_clock.draw()
    win.flip()
    kb.waitKeys()

"""
crop_images("gabor/memory", "jpg",  x = 883, y = 463, height = 154, width = 154)
crop_images("gabor/anticlock/", "jpg",  x = 883, y = 463, height = 154, width = 154)
crop_images("gabor/clock/", "jpg",  x = 883, y = 463, height = 154, width = 154)
"""