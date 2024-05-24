# Medical Imaging Project

## Project Overview

This project involves handling DICOM medical images, where the goal is to load, visualize, and perform coregistration of these images. Using Python and various libraries, the project tackles tasks from basic DICOM operations to more complex image processing techniques.

## Objectives

- **DICOM Loading and Visualization**
  - Load and visualize DICOM images from the HCC-TACE-Seg dataset.
  - Manage and rearrange image data based on specific DICOM headers.
  - Create animations to visualize Maximum Intensity Projections of the imaging data.

- **3D Rigid Coregistration**
  - Implement 3D rigid coregistration of medical images.
  - Focus on visualizing specific anatomical regions post-coregistration.

## Installation

To set up the project environment, follow these steps:

```bash
git clone https://github.com/ulhaqi12/medical-imaging-project
cd medical-imaging-project
pip install -r requirements.txt
```

## Usage

- Run the Jupyter notebooks `part1.ipynb` and `part2.ipynb` for step-by-step instructions and to execute the code.
- Use utilities provided in `utils.py` for additional functionalities.

## Dataset

- Part 1: Download the dataset from [HCC-TACE-Seg dataset](link-to-dataset). I tested the code on HCC_13 because that was assigned to me in the project.

### Important Scripts and Notebooks

- `ct_image.py`, `ct_slice.py`: Modules for handling CT image and slice operations.
- `mapping.py`, `segmentation_image.py`: Handle mapping between CT Image and Segmentation Image.
- `part1.ipynb`, `part2.ipynb`: Jupyter notebooks illustrating the project workflow.

## Coregistration

Detailed steps for image coregistration are provided in `part2.ipynb`. This includes landmark definition and similarity measure implementations without external libraries.

## Contributions

This project is part of a course requirement for Medical Image Processing at UIB, Spain. Contributions are welcomed once repository is public.


## Contact

For any queries, contact [Ikram Ul Haq](https://github.com/ulhaqi12)

## Acknowledgments

Special Thanks to [Prof. Pedro Bibiloni Serrano](https://www.uib.es/es/personal/ABjI3MDA5NA/) for teaching the course and his guidelines throughout the project.