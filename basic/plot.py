#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import sys

if len(sys.argv) < 2:
  print(f"Usage: {sys.argv[0]} logfile")
  exit(1)

log_file = sys.argv[1]
raw_frames = []
with open(log_file) as f:
  raw_frames = [e for e in f.read().split("---") if e.strip() != ""]

raw_frame = raw_frames[0].split("\n")
angle_bounds = (
  float(raw_frame[6].removeprefix('angle_min: ')),
  float(raw_frame[7].removeprefix('angle_max: ')),
  float(raw_frame[8].removeprefix('angle_increment: ')))
range_bounds = (
  float(raw_frame[11].removeprefix('range_min: ')),
  float(raw_frame[12].removeprefix('range_max: ')))
data = pd.DataFrame(
  { "angle": np.arange(*angle_bounds),
    "intensity": np.asarray(json.loads(raw_frame[14].removeprefix('intensities: '))),
    "range": np.asarray(json.loads(raw_frame[13].removeprefix('ranges: '))),
  })

safety = 0.500 / 2.0

ranges = [float(f) for f in data['range']]
angles = [float(f) for f in data['angle']]
filtered = ranges.copy()
for i in range(len(angles)):
  r = min(ranges[i], 10.0)
  t = np.arctan2(safety, r)
  d_idx = int(np.ceil(t / angle_bounds[2]))
  lower = max(0, i - d_idx)
  upper = min(len(ranges), i + d_idx)
  local_min = min([ranges[i] for i in range(lower, upper)])
  for j in range(lower, upper):
    if filtered[j] > local_min: filtered[j] = local_min

data['filtered'] = filtered

# select the path with near max filtered range, closest to 0°
max_filtered_range = max(filtered)
fudge_factor = 0.1
paths = data[
    ((max_filtered_range - fudge_factor) <= data['filtered']) &
    (data['filtered'] <= (max_filtered_range + fudge_factor))]
paths = data[
    ((max_filtered_range - fudge_factor) <= data['filtered']) &
    (data['filtered'] <= (max_filtered_range + fudge_factor))]
selection = paths[paths['angle'].abs() == paths['angle'].abs().min()]
print(selection)

plt.rcParams.update({'font.size': 26})
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.plot(
  data['angle'], data['range'],
  linewidth=2.5)
ax.plot(
  data['angle'], data['filtered'],
  linewidth=2.5)
ax.plot(
  [0.0, selection['angle'].iloc[0]], [0.0, selection['filtered'].iloc[0]],
  linewidth=5.0)

axis = fig.axes[0]
axis.fill_between(np.linspace(0.0, 2*np.pi,100), np.ones(100) * safety, color='r')
axis.set_theta_zero_location('N')
axis.set_rmin(0)
axis.set_rmax(5)

plt.show()
