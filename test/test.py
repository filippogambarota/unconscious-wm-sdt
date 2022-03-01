class csv_writer:
    def __init__(self, subject='', folder='', colnames = []):
        import time
        # Generate self.save_file and self.writer
        self.save_file = '%s%s_(%s).csv' % (folder + "/", subject, time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()))
        self.colnames = colnames
        self._setup_file()
    def _setup_file(self):
        import csv
        self._file = open(self.save_file, 'a')
        self.writer = csv.DictWriter(self._file, fieldnames=self.colnames)
        self.writer.writeheader()
    def write(self, trial):
        self.writer.writerow(trial)

trial = {
    "col1": 1,
    "col2": 2,
    "col3": 3,
    "col4": 4}



writer = csv_writer(subject = "prova", folder = '.', colnames=trial.keys())

for i in range(1000):
    writer.write(trial)