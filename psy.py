# Staircase Class

class staircase:
    
    # TODO implementing the different up/down size

    def __init__(self, start_value, nup, ndown, min_value, max_value, ntrials, step_up, step_down):
        self.start_value = start_value
        self.nup = nup,
        self.ndown = ndown,
        self.min_value = min_value
        self.max_value = max_value
        self.ntrials = ntrials
        self.step_up = step_up
        self.step_down = step_down
        self.current_value = start_value
        self.trial_value = [None for x in range(ntrials)]
        self.trial_list = [x + 1 for x in range(ntrials)]
        self.reversal = [None for x in range(ntrials)]
        self.nreversals = 0
        self.response = [None for x in range(ntrials)]
        self.trial_index = -1 # counter and index for assignment
        self.trial_count = 0 # counter for trials
    
    def next_value(self):
        return self.current_value
    
    def update_staircase(self, response):
        self.trial_index += 1
        self.trial_count += 1
        self.response[self.trial_index] = response
        self.trial_value[self.trial_index] = self.current_value
        
        if response == 1:
            if (self.current_value - self.step_down) >= self.min_value:
                self.current_value = self.current_value - self.step_down
            else:
                self.current_value = self.min_value
        else:
            if (self.current_value + self.step_up) <= self.max_value:
                self.current_value = self.current_value + self.step_up
            else:
                 self.current_value = self.max_value
        return(self)

    def find_reversals(self):

        for resp in range(len(self.response) - 1):
            if self.response[resp] != self.response[resp + 1]:
                self.reversal[resp + 1] = 1

        for rev in range(len(self.reversal)):
            if self.reversal[rev] != 1:
                self.reversal[rev] = 0
        return(self)
    
    def analyze_staircase(self, nreversals = "all"):
        rev_vec = []
        for i in range(len(self.reversal)):
            if self.reversal[i] == 1:
                rev_vec.append(self.trial_value[i])
                self.nreversals += 1

        if nreversals == "all": 
            rev_vec_threshold = rev_vec[2:]  # select all but not first 2 reversals
        else:
            rev_vec_threshold = rev_vec[-nreversals:] # select n reversals starting from the end

        
        if not rev_vec_threshold:
            return("Your staircase has no sufficient reversals to analyze!")
        else:
            threshold = sum(rev_vec_threshold) / len(rev_vec_threshold)

        return(threshold)