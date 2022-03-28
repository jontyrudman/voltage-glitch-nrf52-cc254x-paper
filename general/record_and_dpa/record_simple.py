import time

import DS1074Z
import matplotlib.pyplot as plt
import numpy as np
import pickle

DSO = DS1074Z.DS1074Z("USB0::6833::1230::DS1ZC223704302::0::INSTR")

DSO.stop()
start = time.time()
data = DSO.get_data_bytes(DS1074Z.CHANNEL_1, 3000000)
end = time.time()

pickle.dump(data, open(f"crp_enabled_ch1_coldboot_20220323.pkl", "wb"))

print(f"Took {end - start} seconds.")
