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
        ["cc-tool", "--erase", "--log", "-f", "-w", "../blink_state.hex", "-v"],
        stderr=subprocess.STDOUT
    )
    return output


def enable_crp():
    output = subprocess.check_output(
        ["cc-tool", "--lock", "debug", "--log"],
        stderr=subprocess.STDOUT
    )
    return output


def enable_dac():
    output = subprocess.check_output(
        ["python", os.path.expanduser("~/giant-revB/python/turn_dac_on.py")],
        stderr=subprocess.STDOUT
    )
    return output


def disable_dac():
    output = subprocess.check_output(
        ["python", os.path.expanduser("~/giant-revB/python/turn_dac_off.py")],
        stderr=subprocess.STDOUT
    )
    return output


def collect_traces(count):
    # Create output folder
    folder_name = f"traces_{datetime.today().strftime('%y%d%m_%H%M%S')}"
    os.makedirs(folder_name, exist_ok=True)

    enable_dac()
    disable_crp() # Erase first
    enabled_str = "disabled"

    for trace in range(count):
        enable_dac()
        print("Trace " + str(trace))

        choice = random.randint(0, 1)

        if choice:
            disable_crp()
            enabled_str = "disabled"
        else:
            enable_crp()
            enabled_str = "enabled"

        disable_dac()
        sleep(0.5)
        DSO.single()
        sleep(0.5)

        enable_dac()

        data = DSO.get_data_bytes(DS1074Z.CHANNEL_1, 300000)

        print("Got " + str(len(data["Data"])) + f" samples with CRP {enabled_str}")

        output_file_path = os.path.join(folder_name, f"trace{trace}_crp{enabled_str}")
        pickle.dump(data, open(f"{output_file_path}.pkl", "wb"))
        # save_trace(data["Samplerate"], data["Data"], f"{output_file_path}.svg")


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
    collect_traces(1500)


if __name__ == "__main__":
    main()
