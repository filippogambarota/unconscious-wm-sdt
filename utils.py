import os
import csv
import time
import math
import numpy as np
import itertools
import random
import shelve
import pickle
from scipy import stats

def make_dirs():
    dirs = {
        "csv": os.path.join(os.path.curdir, "data", "csv"),
        "session": os.path.join(os.path.curdir, "data", "session")
    }
    return dirs

# TODO check if the with open statment is too slow
class csv_writer:
    def __init__(self, cond, subject='', folder=''):
        # Generate self.save_file and self.writer
        filename = '{}_({}).csv'
        current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        subject_path = os.path.join(folder, str(subject))
        self.save_file = filename.format(subject_path, current_time)
        self.colnames = list(cond.keys())
        self._setup_file()
    def _setup_file(self):
        with open(self.save_file, 'w', newline='') as file: # w for creating
            self.writer = csv.DictWriter(file, fieldnames = self.colnames)
            self.writer.writeheader()
    def write(self, trial):
        with open(self.save_file, 'a', newline='') as file: # a for appending
            self.writer = csv.DictWriter(file, fieldnames = self.colnames)
            self.writer.writerow(trial)
            
class csv_writer_old:
    def __init__(self, cond, subject='', folder=''):
        # Generate self.save_file and self.writer
        filename = '{}_({}).csv'
        current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        subject_path = os.path.join(folder, str(subject))
        self.save_file = filename.format(subject_path, current_time)
        self.colnames = list(cond.keys())
        self._setup_file()
    def _setup_file(self):
        self._file = open(self.save_file, "a", newline='')
        self.writer = csv.DictWriter(self._file, fieldnames = self.colnames)
        self.writer.writeheader()
    def write(self, trial):
        self.writer.writerow(trial)
        
def deg2cm(angle, distance):
    """
    Returns the size of a stimulus in cm given:
        :distance: ... to monitor in cm
        :angle: ... that stimulus extends as seen from the eye

    Use this function to verify whether your stimuli are the expected size.
    (there's an equivalent in psychopy.tools.monitorunittools.deg2cm)
    """
    return math.tan(math.radians(angle)) * distance  # trigonometry

def getActualFrameRate(frames=1000):
    """
    Measures the actual framerate of your monitor. It's not always as clean as
    you'd think. Prints various useful information.
        :frames: number of frames to do test on.
    """
    from psychopy import visual, core

    # Set stimuli up
    durations = []
    clock = core.Clock()
    win = visual.Window(color='pink')

    # Show a brief instruction / warning
    visual.TextStim(win, text='Now wait and \ndon\'t do anything', color='black').draw()
    win.flip()
    core.wait(1.5)

    # blank screen and synchronize clock to vertical blanks
    win.flip()
    clock.reset()

    # Run the test!
    for i in range(frames):
        win.flip()
        durations += [clock.getTime()]
        clock.reset()

    win.close()

    # Print summary
    print('average frame duration was', round(np.average(durations) * 1000, 3), 'ms (SD', round(np.std(durations), 5), ') ms')
    print('corresponding to a framerate of', round(1 / np.average(durations), 3), 'Hz')
    print('60 frames on your monitor takes', round(np.average(durations) * 60 * 1000, 3), 'ms')
    print('shortest duration was ', round(min(durations) * 1000, 3), 'ms and longest duration was ', round(max(durations) * 1000, 3), 'ms')
    
# Backup session thanks to https://medium.com/swlh/python-for-datascientist-quick-backup-for-everything-6d201a7e935d

def is_picklable(obj):
    try:
        pickle.dumps(obj)
    except Exception:
        return False
    return True

def backup_session(folder, subject):
    filename = "s" + str(subject) + "_" + "session.pkl"
    backup = os.path.join(folder, filename)
    
    bk = shelve.open(backup,'n')
    for k in dir():
        try:
            bk[k] = globals()[k]
        except Exception:
            pass
    bk.close()
    
    # to restore
    #bk_restore = shelve.open('./your_bk_shelve.pkl')
    #for k in bk_restore:
    #    globals()[k] = bk_restore[k]
    #bk_restore.close()

def save_objects(folder, subject, dict_to_save):
    
    filename = "s" + str(subject) + "_" + "session.pkl"
    backup = os.path.join(folder, filename)
    
    with open(backup, "wb") as backup_file:
        pickle.dump(dict_to_save, backup_file)
        
def restore_objects(dict_to_restore):
    import pickle
    import os
    
    with open(dict_to_restore, "rb") as backup_file:
        restored_file = pickle.load(backup_file)
    return restored_file

def create_conditions(cond, prop_catch = 2/3):
    
    """
    Create conditions. Equivalent to R expand.grid() or in python creating multiple for loops and combining into a dictionary
    """
    tup_list = list(itertools.product(*cond.values()))
    trial_list = [{key:value for value, key in zip(tup, cond)} for tup in tup_list]
    valid_list = [d for d in trial_list if d["trial_type"] == "valid"] # subset valid
    catch_list = [d for d in trial_list if d["trial_type"] == "catch"] # subset catch
    ncatch = int(len(catch_list)*prop_catch) # number of catch
    idx = random.sample(range(len(valid_list)), ncatch) # random index
    catch_list = [catch_list[i] for i in idx] # subset list
    return valid_list + catch_list, len(valid_list), ncatch # combine and return

# String to boolean for GUI (thanks to https://stackoverflow.com/a/715468/9032257)

def str2bool(v):
  return str(v).lower() in ("yes", "true", "t", "1")

class simKeys:
    '''
    an object to simulate key presses
    
    keyList: a list of keys to watch
    name: randomly selected from keyList
    rtRange: [min RT, max RT] where min and max RT are sepecified in ms
    rt: randomly selected from rtRange
    thanks to Becca https://discourse.psychopy.org/t/auto-response-script-in-psychopy/19349
        
    '''
    def __init__(self, keyList, rtRange, obs):
        keyList = [x for x in keyList if x != 'escape']
        if obs is not None:
            self.name = obs.get_resp() # get response based on observer
        else:
            self.name=np.random.choice(keyList)
        self.rt = np.random.choice(np.linspace(rtRange[0], rtRange[1])/1000)
        
class psy_observer:
    def __init__(self, threshold, slope, guess, lapses):
        self.threshold = threshold
        self.slope = slope
        self.guess = guess
        self.lapses = lapses
        self.xi = 0
    def get_resp(self):
        pi = self.guess + (1 - self.guess - self.lapses) * stats.norm.cdf(self.xi, self.threshold, self.slope)
        ri = np.random.binomial(1, pi, 1)[0] # get 01 according to
        if ri == 1:
            ri = np.random.choice([2,3,4])
        else:
            ri = 1
        return str(ri)