import os
import re
import pickle
import numpy as np
import matplotlib.pyplot as plt

# directories = ["traces_220303_210951", "traces_220303_212329"]
directories = ["traces_220503_115041"]
combined_file_list = [os.path.join(d, p) for d in directories for p in os.listdir(d)]

crpenabled_paths = [
    x for x in combined_file_list
    if re.match(".*/trace[0-9]+_crpenabled.pkl", x)
]

crpdisabled_paths = [
    x for x in combined_file_list
    if re.match(".*/trace[0-9]+_crpdisabled.pkl", x)
]


def read_path_list(path_list):
    contents_list = []
    for p in path_list:
        contents_list.append(pickle.load(open(p, "rb")))
    return contents_list

crpenabled_all_dicts = read_path_list(crpenabled_paths)
crpdisabled_all_dicts = read_path_list(crpdisabled_paths)
max_len = min(len(crpenabled_all_dicts), len(crpdisabled_all_dicts))
crpenabled_mean = {
    "Samplerate": crpenabled_all_dicts[0]["Samplerate"],
    "Data": np.mean(np.array([
        d["Data"] for d in crpenabled_all_dicts[:max_len]
    ]), axis=0),
}
crpdisabled_mean = {
    "Samplerate": crpdisabled_all_dicts[0]["Samplerate"],
    "Data": np.mean(np.array([
        d["Data"] for d in crpdisabled_all_dicts[:max_len]
    ]), axis=0),
}

def plot_trace(samplerate, data):
    y_values = data
    x_values = np.arange(0, len(y_values)/samplerate, 1.0/samplerate)[:len(y_values)]

    plt.plot(x_values, y_values, linewidth=0.5)
    plt.ylim(-1, 4)


plot_trace(crpdisabled_mean["Samplerate"], crpdisabled_mean["Data"])
plot_trace(crpenabled_mean["Samplerate"], crpenabled_mean["Data"])

diff_trace = {
    "Samplerate": crpdisabled_mean["Samplerate"],
    "Data": np.subtract(crpdisabled_mean["Data"], crpenabled_mean["Data"]) * 15,
}

plot_trace(diff_trace["Samplerate"], diff_trace["Data"])
plt.show()
