import os
import re
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from scipy.signal import find_peaks


matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

directories = ["traces_222603_074559_coldboot"]
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


def plot_trace(x_values, y_values):
    plt.plot(x_values, y_values, linewidth=0.5)
    # plt.ylim(80, 170)


def align_peaks(traces):
    original = traces[0]

    for ti in range(1, len(traces)):
        for i, x_val in enumerate(original["x"][traces[ti]["peaks"]]):
            peak_index = traces[ti]["peaks"][i]
            traces[ti]["x"][peak_index] = x_val

    return traces


# crpenabled_all_dicts = read_path_list(crpenabled_paths)
# crpdisabled_all_dicts = read_path_list(crpdisabled_paths)
# max_len = min(len(crpenabled_all_dicts), len(crpdisabled_all_dicts))

# crpenabled_all_traces = [{"x": np.arange(0, len(d["Data"])/d["Samplerate"], 1.0/d["Samplerate"])[:len(d["Data"])], "y": np.array(d["Data"])} for d in crpenabled_all_dicts]
# crpdisabled_all_traces = [{"x": np.arange(0, len(d["Data"])/d["Samplerate"], 1.0/d["Samplerate"])[:len(d["Data"])], "y": np.array(d["Data"])} for d in crpdisabled_all_dicts]


# crpenabled_mean = {
#     "x": crpenabled_all_traces[0]["x"],
#     "y": np.mean(np.array([
#         d["y"] for d in crpenabled_all_traces[:max_len]
#     ]), axis=0),
# }

# crpdisabled_mean = {
#     "x": crpdisabled_all_traces[0]["x"],
#     "y": np.mean(np.array([
#         d["y"] for d in crpdisabled_all_traces[:max_len] if len(d["y"]) == 300000
#     ]), axis=0),
# }


# diff_trace = {
#     "x": crpdisabled_mean["x"] * 1000,
#     "y": np.subtract(crpdisabled_mean["y"], crpenabled_mean["y"]) * 15,
# }

# pickle.dump(diff_trace, open("diff_trace_coldboot_cached.pkl", "wb"))
# pickle.dump(crpdisabled_all_traces[0], open("crpdisabled_coldboot_cached.pkl", "wb"))
# pickle.dump(crpenabled_all_traces[0], open("crpenabled_coldboot_cached.pkl", "wb"))
# exit()

diff_trace = read_path_list(["diff_trace_coldboot_cached.pkl"])[0]
crpdisabled_all_traces = read_path_list(["crpdisabled_coldboot_cached.pkl"])
crpenabled_all_traces = read_path_list(["crpenabled_coldboot_cached.pkl"])

plot_trace(crpdisabled_all_traces[0]["x"] * 1000, crpdisabled_all_traces[0]["y"] + 50)
plot_trace(crpenabled_all_traces[0]["x"] * 1000, crpenabled_all_traces[0]["y"])

# plot_trace(crpdisabled_mean["x"] * 1000, crpdisabled_mean["y"])
# plot_trace(crpenabled_mean["x"] * 1000, crpenabled_mean["y"])


plot_trace(diff_trace["x"], diff_trace["y"])

plt.xlabel("Time (ms)")
plt.yticks([])

plt.savefig("coldboot_comparison.pgf")
