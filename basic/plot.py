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
    "range": np.asarray(json.loads(raw_frame[13].removeprefix('ranges: '))),
    "intensity": np.asarray(json.loads(raw_frame[14].removeprefix('intensities: ')))})

safety = 0.500 / 2.0

# NOTE: if performance is a consideration, make the selection as soon as some `d` is found with filtered ranges remaining at `d`.

filtered = data.copy()
for d in sorted({d for d in data['range']}, reverse=True):
  for (_, row) in data[data['range'] == d].iterrows():
    t, r = row['angle'], row['range']
    dt = np.arctan(safety / r)
    filt = ((t - dt) <= data['angle']) & (data['angle'] <= (t + dt))
    neighbors = data[filt]
    filtered.loc[filt, 'range'] = min(neighbors['range'])

# select the path with near max filtered range, closest to 0°
max_filtered_range = filtered['range'].max()
fudge_factor = 0.1
paths = filtered[
    ((max_filtered_range - fudge_factor) <= filtered['range']) &
    (filtered['range'] <= (max_filtered_range + fudge_factor))]
selection = paths[paths['angle'].abs() == paths['angle'].abs().min()]
print(selection)

# TODO: stop if max filtered range is below some threshold, maybe TTC

plt.rcParams.update({'font.size': 26})
fig = plt.figure()
ax = fig.add_subplot(111, projection='polar')
ax.plot(
  filtered['angle'], data['range'],
  linewidth=2.5)
ax.plot(
  filtered['angle'], filtered['range'],
  linewidth=2.5)
plt.polar(
  [0.0, selection['angle'].iloc[0]], [0.0, selection['range'].iloc[0]],
  linewidth=5.0)

axis = fig.axes[0]
axis.fill_between(np.linspace(0.0, 2*np.pi,100), np.ones(100) * safety, color='r')
axis.set_theta_zero_location('N')
axis.set_rmin(0)
axis.set_rmax(5)

plt.show()
