import ast
import pickle
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np


def plot_trace(samplerate, data, x_offset=0, y_offset=0):
    y_values = np.array(data) + y_offset
    x_values = np.array(np.arange(0, len(y_values)/samplerate, 1.0/samplerate)[:len(y_values)]) + x_offset

    plt.plot(x_values, y_values)
    plt.ylim(-20, 20)

trace0 = pickle.load(open("traces_221503_124326/trace0_crpdisabled.pkl", "rb"))
trace1 = pickle.load(open("traces_221503_112303/trace0_crpenabled.pkl", "rb"))

plot_trace(trace0["Samplerate"], trace0["Data"], 0, -trace0["Data"][0] + 15)
plot_trace(trace1["Samplerate"], trace1["Data"], 0.000000790, -trace0["Data"][0] - 15)
plt.show()
