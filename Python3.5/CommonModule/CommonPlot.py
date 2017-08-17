#/home/wdcai/anaconda3/bin/

import os
import sys
import seaborn as sns
from math import pi
import matplotlib.pyplot as plt

def RadarPlot(vec_values, vec_names, y_tick_values, y_tick_names, area_color, ofname_fig):

  N = len(vec_names)

  x_as = [n / float(N) * 2 * pi for n in range(N)]

  # Because our chart will be circular we need to append a copy of the first 
  # value of each list at the end of each list with data
  vec_values += vec_values[:1]
  x_as += x_as[:1]
  
  # Set figure size
  plt.figure(figsize=(5,4))

  # Set color of axes
  plt.rc('axes', linewidth=1, edgecolor="#888888")

  # Create polar plot
  ax = plt.subplot(111, polar=True)

  # Set clockwise rotation. That is:
  ax.set_theta_offset(pi / 2)
  ax.set_theta_direction(-1)

  # Set position of y-labels
  ax.set_rlabel_position(0)

  # Set color and linestyle of grid
  ax.xaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)
  ax.yaxis.grid(True, color="#888888", linestyle='solid', linewidth=0.5)

  # Set number of radial axes and remove labels
  plt.xticks(x_as[:-1], [])

  # Set yticks
  plt.yticks(y_tick_values, y_tick_names)

  # Plot data
  ax.plot(x_as, vec_values, linewidth=2, linestyle='solid', zorder=3)

  # Fill area
  ax.fill(x_as, vec_values, area_color, alpha=0.3)

  # Set axes limits
  ylim_min = min(y_tick_values)
  ylim_max = max(y_tick_values)
  plt.ylim(ylim_min, ylim_max)

  # Draw ytick labels to make sure they fit properly
  for i in range(N):
    angle_rad = i / float(N) * 2 * pi

    if angle_rad == 0:
      ha, distance_ax = "center", (1 + (y_tick_values[-1]-y_tick_values[-2])/4)
    elif 0 < angle_rad < pi:
      ha, distance_ax = "left", 1
    elif angle_rad == pi:
      ha, distance_ax = "center", 1
    else:
      ha, distance_ax = "right", 1
    
    ax.text(angle_rad, y_tick_values[-2] + distance_ax, vec_names[i], size=14, horizontalalignment=ha, verticalalignment="center")

  # Show polar plot
  plt.savefig(ofname_fig, dpi=1000)
  plt.show()
