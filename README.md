# pathfinding
LiDAR test data and python scripts to test pathfinding algorithms

## Directory structure

- `testdata/`: Test samples of LiDAR data frames.
- `media/`: Images of the test setups.
- `basic/`: Basic follow-the-gap algorithm, and output figures.

## Test Setups

- Scan0: Baseline with somewhat empty space ahead of the LiDAR
<div align="center">
  <image src="media/scan0-rear.jpg", style="width: 50%;">
  <image src="media/scan0-top.jpg", style="width: 41%;">
</div>

- Scan1: Nearly identical to Scan0, with a small obstacle approximately 1m ahead at 20° clockwise from center
<div align="center">
  <image src="media/scan1-rear.jpg", style="width: 46%;">
  <image src="media/scan1-top.jpg", style="width: 46%;">
</div>

## Dependencies

- Python 3 (tested with 3.9.4)
- matplotlib (tested with 3.4.1)
- numpy (tested with 1.20.2)
- pandas (tested with 1.2.3)

## Basic follow-the-gap

Executing the basic algorithm on scan0: `./basic/plot.py testdata/scan0.txt`

- The blue line shows the LiDAR scan frame.
- The orange line shows the filtered range based on the safety radius around the vehicle (represented by the red area).
- The green line shows the selected path.

Output for scan0.txt (left) and scan1.txt (right)
<div align="center">
  <image src="basic/scan0.png", style="width: 40%;">
  <image src="basic/scan1.png", style="width: 40%;">
</div>
