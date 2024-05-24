"""
File hosts the code for data structure that stores one CT Image.

Author(s): Ikram Ul Haq(ulhaqi12)
"""

import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np
import scipy

from .ct_slice import CTSlice


def MIP_sagittal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the maximum intensity projection on the sagittal orientation. """
    # Your code here:
    #   See `np.max(...)`
    # ...
    return np.max(img_dcm, axis=2)


def MIP_coronal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the maximum intensity projection on the sagittal orientation. """
    # Your code here:
    #   See `np.max(...)`
    # ...
    return np.max(img_dcm, axis=1)


def MIP_axial_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the maximum intensity projection on the sagittal orientation. """
    # Your code here:
    #   See `np.max(...)`
    # ...
    return np.max(img_dcm, axis=0)


class CTImage:

    def __init__(self):

        self.number_of_slices = None
        self.slices = []
        self.pixel_array = None
        self.transformed = None

    def load_data(self, data_path: str):
        """
        This function will receive path of folder containing dicom data and will populate CTImage Object
        """

        for image_path in os.listdir(data_path):
            image_path = os.path.join(data_path, image_path)

            image = pydicom.dcmread(image_path)

            self.slices.append(CTSlice(image))

        self.number_of_slices = len(self.slices)

    def make_3d_array(self):
        """

        """

        self.slices = sorted(self.slices, key=lambda x: x.slice_location)
        slices_array = [slice_.data for slice_ in self.slices]

        self.pixel_array = np.array(slices_array)

    def is_same_acquisition(self):
        """
        Check if image belong to same acquisition
        """
        return False if len(list(set([a.acquisition_number for a in self.slices]))) > 1 else True

    def rescale_image(self, original_spacing, target_spacing=[1.0, 1.0, 1.0]):
        """
        rescale all three dimensions based on the pixel spacing
        """
        scaling_factors = [os / ts for os, ts in zip(original_spacing, target_spacing)]
        rescaled_image = scipy.ndimage.zoom(self.pixel_array, scaling_factors, order=1)
        self.pixel_array = rescaled_image

    def crop_image(self, target_shape):
        """
        crop image to the target size
        """
        start_indices = [(i - t) // 2 for i, t in zip(self.pixel_array.shape, target_shape)]
        end_indices = [start + t for start, t in zip(start_indices, target_shape)]
        cropped_image = self.pixel_array[:, start_indices[1]:end_indices[1],
                        start_indices[2]:end_indices[2]]
        self.pixel_array = cropped_image

    def interpolate_slices(self, target_slices):
        """
        zoom in for making slices of input similar to the reference.
        """
        current_slices = self.pixel_array.shape[0]
        zoom_factor = target_slices / current_slices
        zoom_factors = [zoom_factor, 1, 1]  # Only increase the number of slices, keep other dimensions the same
        interpolated_image = scipy.ndimage.zoom(self.pixel_array, zoom_factors, order=1)  # Linear interpolation
        self.pixel_array = interpolated_image


    def visualize_all_projections_mip(self):
        """

        """

        coronal_plane = MIP_coronal_plane(self.pixel_array)
        sagittal_plane = MIP_sagittal_plane(self.pixel_array)
        axial_plane = MIP_axial_plane(self.pixel_array)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Axial slice
        axes[0].imshow(coronal_plane, cmap='gray')
        axes[0].set_title(f"MIP Coronal")
        axes[0].axis('off')

        # Sagittal slice
        axes[1].imshow(sagittal_plane, cmap='gray')
        axes[1].set_title(f"MIP Sagittal")
        axes[1].axis('off')

        # # Coronal slice
        axes[2].imshow(axial_plane, cmap='gray')
        axes[2].set_title(f"MIP Axial")
        axes[2].axis('off')

        plt.tight_layout()
        plt.show()

    def visualize_slices(self, axial_idx, sagittal_idx, coronal_idx, aspect=1):
        """
        Plot axial, sagittal, and coronal CT slices.

        Parameters:
            image (numpy.ndarray): The 3D image array.
            axial_idx (int): The index of the axial slice to be displayed.
            sagittal_idx (int): The index of the sagittal slice to be displayed.
            coronal_idx (int): The index of the coronal slice to be displayed.
        """

        # Ensure indices are within the image dimensions
        axial_idx = np.clip(axial_idx, 0, self.pixel_array.shape[0] - 1)
        sagittal_idx = np.clip(sagittal_idx, 0, self.pixel_array.shape[1] - 1)
        coronal_idx = np.clip(coronal_idx, 0, self.pixel_array.shape[2] - 1)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Axial slice
        axes[0].imshow(self.pixel_array[axial_idx, :, :], cmap='gray')
        axes[0].set_title(f"Axial Slice at index {axial_idx}")
        axes[0].axis('off')

        # Sagittal slice
        axes[1].imshow(self.pixel_array[:, sagittal_idx, :], cmap='gray', aspect=aspect)
        axes[1].set_title(f"Sagittal Slice at index {sagittal_idx}")
        axes[1].axis('off')

        # Coronal slice
        axes[2].imshow(self.pixel_array[:, :, coronal_idx], cmap='gray', aspect=aspect)
        axes[2].set_title(f"Coronal Slice at index {coronal_idx}")
        axes[2].axis('off')

        plt.tight_layout()
        plt.show()

