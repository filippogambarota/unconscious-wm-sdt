class csv_writer:
    def __init__(self, subject='', base_folder = '', folder='', colnames = []):
        import time
        import os
        # Generate self.save_file and self.writer
        filename = '{}{}_({}).csv'
        current_time = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())
        subject_path = os.path.join(base_folder, folder, str(subject))
        self.save_file = filename.format(subject_path, subject, current_time)
        print(self.save_file)
        self.colnames = colnames
        self._setup_file()
    def _setup_file(self):
        import csv
        self._file = open(self.save_file, 'a')
        self.writer = csv.DictWriter(self._file, fieldnames=self.colnames)
        self.writer.writeheader()
    def write(self, trial):
        self.writer.writerow(trial)
        
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
    import numpy as np
    print('average frame duration was', round(np.average(durations) * 1000, 3), 'ms (SD', round(np.std(durations), 5), ') ms')
    print('corresponding to a framerate of', round(1 / np.average(durations), 3), 'Hz')
    print('60 frames on your monitor takes', round(np.average(durations) * 60 * 1000, 3), 'ms')
    print('shortest duration was ', round(min(durations) * 1000, 3), 'ms and longest duration was ', round(max(durations) * 1000, 3), 'ms')
    
# Backup session thanks to https://medium.com/swlh/python-for-datascientist-quick-backup-for-everything-6d201a7e935d

def is_picklable(obj):
    import pickle

    try:
        pickle.dumps(obj)
    except Exception:
        return False
    return True

def backup_session(folder, subject):
    import shelve
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
    import pickle
    import os
    
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
    import itertools
    import random
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
    return valid_list + catch_list # combine and return