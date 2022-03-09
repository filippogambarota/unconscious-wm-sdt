from fileinput import filename
import pickle
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/session/s45_session.pkl')

with open(filename, "rb") as file:
    backup = pickle.load(file)