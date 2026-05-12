# AFM & Raman Data Analysis Toolkit

This repository contains a suite of Python scripts developed for the analysis of morphological surface properties extracted from **Atomic Force Microscopy image** (local curvature and curvature radius) and of vibrational properties retrieved from **Raman Spectroscopy maps** (strain, mode shifting).

The analysis is extremely case-specific, based on the data included in the scientific research paper for which I developed these scripts, but it can be quite easily generalized to some extent.

> **Development Note:** This code was developed and optimized through a collaborative interaction with **Gemini (Google AI)**, integrating experimental physics domain expertise with AI-assisted programming techniques.
> 
> **Citation:** If you use this code in your research, please cite the following paper (to be updated with Journal and DOI after publication):
*M.Gardella et al., "Thermally Engineered CVD for Controlling Crystal Orientation and Strain in Large‑Area PtTe₂ Layers"*

---

## 🛠️ Features

### 1. Curvature Analysis (`AFM_curvature_analysis.py`)
This script processes AFM topographic maps (.csv format) to extract quantitative morphological data.
* **Gaussian Smoothing:** Implements noise reduction to prevent derivative artifacts during curvature calculation.
* **Surface Curvature ($H$):** Calculates the mean curvature using second-order partial derivatives of the surface.
* **Radius of Curvature ($R$):** Computes the local radius ($R = 1/H$) and handles flat-surface singularities.
* **Statistical Analysis:** Generates histograms of curvature distribution, including mean, median, and standard deviation.

### 2. Raman Mapping & Strain Study (`Raman_map_analysis.py`)
A dedicated tool for processing Raman maps (works on .txt files containing peaks position shift).
* **Coordinate Transformation:** Converts raw list-format data (X, Y, Peak Position) into 2D matrices for spatial visualization.
* **Spatial Calibration:** Corrects stage absolute coordinates to relative microns, ensuring pixels are centered according to the step size (e.g., 3µm).
* **ROI Analysis:** Allows the selection of specific Regions of Interest (e.g., "wrinkles" vs "flat regions") to compare local vibrational properties.
* **Strain Correlation:** Features scatter plots with linear fitting to analyze the coupling between different Raman modes.

---

## 🚀 Technical Stack
* **Language:** Python 3.x
* **Core Libraries:**
    * `NumPy`: Multi-dimensional array handling and numerical operations.
    * `Matplotlib`: Publication-quality heatmaps and scatter plots.
    * `SciPy`: Image processing (Gaussian filters) and gradient calculations.

## 📊 Visualizations
The scripts produce several high-impact plots:
1. **Topography Maps:** Surface height in nanometers.
2. **Curvature Maps:** Local surface curvature in $\mu m^{-1}$.
3. **Correlation Plots:** E-mode vs A-mode dispersion for strain analysis.
4. **ROI Overlays:** Spatial maps with highlighted regions of interest using `matplotlib.patches`.

---

## ⚠️ Disclaimer
This code was developed for academic research purposes. It is provided "as is" without warranty of any kind. The authors are not responsible for any data misinterpretation or consequential damages resulting from the use of this software.

---
**Developed by:** [M-Gardella]  
**Environment:** Optimized for Spyder IDE / Python 3.x

## License
This project is licensed under the **MIT License** - see the LICENSE file for details.
