import os
from datetime import datetime
from time import sleep
import random
import pickle
import subprocess

import DS1074Z
import matplotlib.pyplot as plt
import numpy as np


def read_info_page():
    output = subprocess.check_output(
        ["cc-tool", "-f", "-i", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def disable_crp():
    output = subprocess.check_output(
        ["cc-tool", "--erase", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def enable_crp():
    output = subprocess.check_output(
        ["cc-tool", "--lock", "debug", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def collect_traces(count):
    # Create output folder
    folder_name = f"traces_{datetime.today().strftime('%y%d%m_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)

    disable_crp() # Erase first
    enabled_str = "disabled"

    for trace in range(count):
        print("Trace " + str(trace))

        choice = random.randint(0, 1)

        if choice:
            disable_crp()
            enabled_str = "disabled"
        else:
            enable_crp()
            enabled_str = "enabled"

        sleep(0.5)
        DSO.single()
        sleep(0.5)

        read_info_page()

        data = DSO.get_data(DS1074Z.CHANNEL_1)

        print("Got " + str(len(data["Data"])) + f" samples with CRP {enabled_str}")

        output_file_path = os.path.join(folder_name, f"trace{trace}_crp{enabled_str}")
        pickle.dump(data, open(f"{output_file_path}.pkl", "wb"))
        save_trace(data["Samplerate"], data["Data"], f"{output_file_path}.svg")


def plot_trace(samplerate, data):
    plt.cla()
    plt.clf()
    y_values = data
    x_values = np.arange(0, len(y_values)/samplerate, 1.0/samplerate)[:len(y_values)]

    plt.plot(x_values, y_values)
    plt.ylim(-1, 4)
    plt.show()


def save_trace(samplerate, data, fname):
    plt.cla()
    plt.clf()
    y_values = data
    x_values = np.arange(0, len(y_values)/samplerate, 1.0/samplerate)[:len(y_values)]

    plt.plot(x_values, y_values)
    plt.ylim(-1, 4)
    plt.savefig(fname, format="svg")


def main():
    global DSO
    DSO = DS1074Z.DS1074Z("USB0::6833::1230::DS1ZC223704302::0::INSTR")
    collect_traces(150)


if __name__ == "__main__":
    main()
