# ==============================================================================
# RESEARCH CODE DISCLAIMER
# This script was developed for academic research purposes to analyze AFM and 
# Raman data. It is provided "as is" without warranty of any kind. 
# The authors are not responsible for any data misinterpretation or 
# consequential damages resulting from the use of this software.
# 
# Developed by: M-Gardella
# Environment: Python 3.x / Spyder IDE
# ==============================================================================

"""Raman map analysis"""

# %% IMPORT

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import MultipleLocator

# %% DEF

def load_swapped_axes_map(filename):
    # Load data: Col0=X, Col1=Y, Col2=Peak_Pos
    data = np.loadtxt(filename)
    x_raw, y_raw, z_raw = data[:, 0], data[:, 1], data[:, 2]
    
    # Find the unique values to define the grid
    u_x = np.unique(x_raw)
    u_y = np.unique(y_raw)
    
    # Create an empty matrix with inverted dimensions
    # Rows = number of unique X, Columns = number of unique Y
    z_matrix = np.zeros((len(u_x), len(u_y)))
    
    # Fill the matrix by mapping X on rows and Y on columns
    for i in range(len(z_raw)):
        # Find the corresponding index on grid
        ix = np.where(u_x == x_raw[i])[0][0]
        iy = np.where(u_y == y_raw[i])[0][0]
        z_matrix[ix, iy] = z_raw[i]
    
    # Return u_y as new x-axis and u_x as new y-axis (or vice versa)
    return u_y, u_x, z_matrix, z_raw

# %% MAPS LOADING

# --- Files Configuration ---
# Working with PtTe2 I am interested in A and E vibrational modes
file_mode_E = 'file-path'  # Replace with your file name
file_mode_A = 'file-path'  # Replace with your file name

# --- Execution ---
# Load PtTe2 E-mode and A-mode
x_new, y_new, map_E, flat_E = load_swapped_axes_map(file_mode_E)
_, _, map_A, flat_A = load_swapped_axes_map(file_mode_A)

# --- Plotting ---
fig, ax = plt.subplots(1, 2, figsize=(18, 5))

# Correct spatial extent for the plot
# extent = [x_new.min(), x_new.max(), y_new.max(), y_new.min()]
# x_new.min()=-7279.05, x_new.max()=-7243.05
# y_new.max()=-10824.8, y_new.min()=-10845.8

# I first correct this extent to have x- and y-axis starting from a relative 0 
# instead of having Raman stage absolute values
# extent = [7279.05+x_new.min(), 7279.05+x_new.max(), -10824.8-y_new.max(), -10824.8-y_new.min()]

# I further correct the extent for graphical reasons: Raman maps was acquired
# using 3µm steps, so each pixel will have 3µm size and I want the ticks 
# centered in the pixels. I add +/-1.5µm at the min/max values 
extent = [-1.5+7279.05+x_new.min(), 7279.05+x_new.max()+1.5, -1.5-10824.8-y_new.max(), -10824.8-y_new.min()+1.5]

# E-mode Map
im1 = ax[0].imshow(map_E, extent=extent, cmap='viridis')
ax[0].set_title('E-mode Map', fontsize=20)
ax[0].set_xlabel('x (µm)', fontsize=20)
ax[0].set_ylabel('y (µm)', fontsize=20)
ax[0].xaxis.set_major_locator(MultipleLocator(6))
ax[0].yaxis.set_major_locator(MultipleLocator(6))
ax[0].tick_params(axis='both', which='major', labelsize=16)
fig.colorbar(im1, ax=ax[0]).ax.tick_params(labelsize=14)

# A-mode Map
im2 = ax[1].imshow(map_A, extent=extent, cmap='magma')
ax[1].set_title('A-mode Map', fontsize=20)
ax[1].set_xlabel('x (µm)', fontsize=20)
ax[1].set_ylabel('y (µm)', fontsize=20)
ax[1].xaxis.set_major_locator(MultipleLocator(6))
ax[1].yaxis.set_major_locator(MultipleLocator(6))
ax[1].tick_params(axis='both', which='major', labelsize=16)
fig.colorbar(im2, ax=ax[1]).ax.tick_params(labelsize=14)

plt.tight_layout()
plt.show()

# Scatter Plot 
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(flat_E, flat_A, alpha=0.6, s=60, color='darkcyan', edgecolors='white', linewidth=0.5)
ax.set_xlabel('E-mode Position (cm$^{-1}$)', fontsize=20)
ax.set_ylabel('A-mode Position (cm$^{-1}$)', fontsize=20)
ax.set_title('Scatter Plot: Strain Analysis', fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=14)
ax.grid(True, alpha=0.3)

# Optional: Linear fit to highlight strain trend
m, b = np.polyfit(flat_E, flat_A, 1)
ax.plot(flat_E, m*flat_E + b, color='red', label=f'Fit: slope={m:.2f}')
ax.legend(fontsize=18)

plt.tight_layout()
plt.show()

# %% REGIONS OF INTEREST (ROIs) SELECTION 

# Modify x- and y- indexes here to select your ROIs 
# f : flat region    
row_start_f, row_end_f = 0, 4    # y-axis range (indexes) 
col_start_f, col_end_f = 9, 13   # x-axis range (indexes)
# w : wrinkle region
row_start_w, row_end_w = 2, 6    # y-axis range (indexes)
col_start_w, col_end_w = 4, 8    # x-axis range (indexes)

# ROI data extraction
sub_map_E_f = map_E[row_start_f:row_end_f, col_start_f:col_end_f]
sub_map_A_f = map_A[row_start_f:row_end_f, col_start_f:col_end_f]
sub_E_f = sub_map_E_f.flatten()
sub_A_f = sub_map_A_f.flatten()

sub_map_E_w = map_E[row_start_w:row_end_w, col_start_w:col_end_w]
sub_map_A_w = map_A[row_start_w:row_end_w, col_start_w:col_end_w]
sub_E_w = sub_map_E_w.flatten()
sub_A_w = sub_map_A_w.flatten()

# Calculate the spatial coordinates of the rectangles for the ROIs
# same x and y corrections used for extent, also considering the 3µm step
# x_new.min()=-7279.05, x_new.max()=-7243.05
# y_new.max()=-10824.8, y_new.min()=-10845.8
rect_x_f = -1.5+7279.05+x_new[col_start_f]
rect_y_f = 1.5-10824.8-y_new[row_start_f]
rect_w_f = x_new[col_end_f-1] - x_new[col_start_f] + 3
rect_h_f = y_new[row_start_f] - y_new[row_end_f-1] - 3

rect_x_w = -1.5+7279.05+x_new[col_start_w]
rect_y_w = 1.5-10824.8-y_new[row_start_w]
rect_w_w = x_new[col_end_w-1] - x_new[col_start_w] + 3
rect_h_w = y_new[row_start_w] - y_new[row_end_w-1] - 3

# --- PLOTTING ---
fig = plt.figure(figsize=(18, 6))

# 1. Complete E-mode map with highlighted ROIs
ax1 = plt.subplot(1, 2, 1)
im1 = ax1.imshow(map_E, extent=extent, cmap='viridis')
ax1.tick_params(axis='both', which='major', labelsize=16)
ax1.set_xlabel('x (µm)', fontsize=20)
ax1.set_ylabel('y (µm)', fontsize=20)
ax1.set_title('E-mode Map with ROIs', fontsize=20)
ax1.xaxis.set_major_locator(MultipleLocator(6))
ax1.yaxis.set_major_locator(MultipleLocator(6))
plt.colorbar(im1, ax=ax1).ax.tick_params(labelsize=14)
# Add rectangles for ROIs
rect_f = patches.Rectangle((rect_x_f, rect_y_f), rect_w_f, rect_h_f, linewidth=4, edgecolor='blue', facecolor='none', linestyle='--')
rect_w = patches.Rectangle((rect_x_w, rect_y_w), rect_w_w, rect_h_w, linewidth=4, edgecolor='red', facecolor='none', linestyle='--')
ax1.add_patch(rect_f)
ax1.add_patch(rect_w)

# 2. ROI zoom (E-mode)
#ax2 = plt.subplot(2, 2, 2)
#im2 = ax2.imshow(sub_map_E_flat, origin='lower', cmap='viridis')
#ax2.set_title(f'Zoom ROI ({sub_map_E_flat.shape[0]}x{sub_map_E_flat.shape[1]} punti)')
#plt.colorbar(im2, ax=ax2)

# 3. Total dispersion plot (gray dots) and ROIs dispersions (blue and red dots)
ax3 = plt.subplot(1, 2, 2)
ax3.scatter(flat_E, flat_A, alpha=0.8, s=70, color='gray', label='all')
ax3.scatter(sub_E_f, sub_A_f, alpha=0.8, s=70, color='blue', edgecolors='black', label='flat')
ax3.scatter(sub_E_w, sub_A_w, alpha=0.8, s=70, color='red', edgecolors='black', label='wrinkle')
# I manually add a reference point for unstrained material (exfoliated flake)
ax3.scatter(111.1, 157.2, alpha=0.8, s=180, marker='x', linewidths=5, color='green', edgecolors='black', label='flake')

# Linear fit only for ROI points
#if len(sub_flat_E) > 1:
#    m, b = np.polyfit(sub_flat_E, sub_flat_A, 1)
#    ax3.plot(sub_flat_E, m*sub_flat_E + b, color='red', lw=2, label=f'Fit Locale (Slope: {m:.2f})')

ax3.tick_params(axis='both', which='major', labelsize=16)
ax3.set_xlabel('E-mode (cm$^{-1}$)', fontsize=20)
ax3.set_ylabel('A-mode (cm$^{-1}$)', fontsize=20)
ax3.set_title('Scatter Plot: Strain Analysis', fontsize=20)
ax3.legend(fontsize=18)
ax3.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Numerical output
#print(f"ROI analysis completed:")
#print(f"Local slope (Strain coupling): {m:.2f}")
#print(f"E-mode average shift: {np.mean(sub_flat_E):.2f} cm^-1")
