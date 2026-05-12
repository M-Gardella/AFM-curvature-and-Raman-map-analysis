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

"""Curvature analysis from AFM image"""

# %% IMPORT

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

# %% DEF

def analyze_afm_surface(csv_path, pixel_size_nm, sigma):
    # 1. Load data
    # skiprows=0 if file has no header, otherwise use 1 or more
    data = np.genfromtxt(csv_path, delimiter=',')
    
    # 2. Conversion to µm and smoothing (curvature amplifies noise)
    z_µm = data / 1000.0
    pixel_size_µm = pixel_size_nm / 1000.0
    z_smooth = gaussian_filter(z_µm, sigma=sigma)
    
    # 3. Calculate gradients and second derivatives
    dz_dx, dz_dy = np.gradient(z_smooth, pixel_size_µm)
    d2z_dx2, d2z_dxdy = np.gradient(dz_dx, pixel_size_µm)
    _, d2z_dy2 = np.gradient(dz_dy, pixel_size_µm)
    
    # 4. Calculate average curvature (H)
    num = (1 + dz_dy**2) * d2z_dx2 - 2 * dz_dx * dz_dy * d2z_dxdy + (1 + dz_dx**2) * d2z_dy2
    den = 2 * (1 + dz_dx**2 + dz_dy**2)**(1.5)
    curvature = num / den
    
    # 5. Calculate curvature radius (R = 1/H)
    # Avoid dividing by zero where surface is flat
    with np.errstate(divide='ignore', invalid='ignore'):
        radius = 1.0 / curvature
        # Replace infinite values with NaN for the statistics
        radius[np.isinf(radius)] = np.nan 

    return data, curvature, radius

# %% DATA LOAD

# --- Configuration parameters ---
FILE_CSV = 'file-path'  # Replace with you file name (must be a .csv file)
NM_PER_PIXEL = 97.7  # Replace with your spacial resolution
SIGMA_SMOOTH = 5    # Change depending on your graphical output


# %% PLOTTING

try:
    z_map, curv_map, rad_map = analyze_afm_surface(FILE_CSV, NM_PER_PIXEL, SIGMA_SMOOTH)

    x_scan_µm = z_map.shape[1] * NM_PER_PIXEL / 1000
    y_scan_µm = z_map.shape[0] * NM_PER_PIXEL / 1000
    # Define the extent: [left, right, bottom, top]
    extent = [0, x_scan_µm, 0, y_scan_µm]

    # Calculate view limitations based on percentiles (2% - 98%)
    # Avoid noise to dominate the color scale
    v_min, v_max = np.nanpercentile(curv_map, [2, 98])

# --- FIGURE 1: Topography ---
    plt.figure(figsize=(8, 6))
    plt.imshow(z_map, cmap='afmhot', extent=extent)
    plt.title("Topography (nm)", fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xlabel("x (µm)", fontsize=20)
    plt.ylabel("y (µm)", fontsize=20)
    plt.colorbar(shrink=0.7).ax.tick_params(labelsize=16)
    plt.tight_layout()

    # --- FIGURE 2: Curvature ---
    plt.figure(figsize=(8, 6))
    plt.imshow(curv_map, cmap='RdBu_r', extent=extent, vmin=v_min, vmax=v_max)
    plt.title("Local Curvature (µm⁻¹)", fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xlabel("x (µm)", fontsize=20)
    plt.ylabel("y (µm)", fontsize=20)
    plt.colorbar(shrink=0.7).ax.tick_params(labelsize=16)
    plt.tight_layout()

    # --- FIGURE 3: Curvature radius ---
    plt.figure(figsize=(8, 6))
    plt.imshow(rad_map, cmap='RdBu_r', extent=extent, vmin=-50, vmax=50) # arbitrary cut-off at ±50µm
    plt.title("Curvature Radius (µm)", fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xlabel("x (µm)", fontsize=20)
    plt.ylabel("y (µm)", fontsize=20)
    plt.colorbar(shrink=0.7).ax.tick_params(labelsize=16)
    plt.tight_layout()

    # Shows all windows at the same time
    plt.show()

except Exception as e:
    print(f"Error during the execution: {e}")
    
# %% CURVATURE HISTOGRAM


# 1. Transform matrix into a 1D array and remove invalid values
curv_values = curv_map.flatten()
curv_values = curv_values[~np.isnan(curv_values)] # remove NaN
curv_values = curv_values[~np.isinf(curv_values)] # remove infinite values

# 2. Define hystogram limits (exclude extremal 1% tails)
h_min, h_max = np.percentile(curv_values, [1, 99])

# 3. Plot creation
plt.figure(figsize=(10, 6))

# Create hystogram
# bins=100 to have good resolution, range to exclude outliers
n, bins, patches = plt.hist(curv_values, bins=100, range=(h_min, h_max), 
                            color='skyblue', edgecolor='black', alpha=0.7)

# 4. Add statistic lines
mean_curv = np.mean(curv_values)
median_curv = np.median(curv_values)

plt.axvline(mean_curv, color='red', linestyle='dashed', linewidth=2, label=f'Mean: {mean_curv:.4f}')
plt.axvline(median_curv, color='green', linestyle='dotted', linewidth=2, label=f'Median: {median_curv:.4f}')

# Formattazione
plt.title("Local curvature dispersion")
plt.xlabel("Curvature (µm⁻¹)")
plt.ylabel("Frequency (n° pixel)")
plt.grid(axis='y', alpha=0.3)
plt.legend()

plt.show()

# 5. Quick print of numerical outputs
print(f"--- Curvature statistics (µm⁻¹) ---")
print(f"Mean value:   {mean_curv:.6f}")
print(f"Std deviation: {np.std(curv_values):.6f}")
print(f"Max value (99° perc): {h_max:.6f}")