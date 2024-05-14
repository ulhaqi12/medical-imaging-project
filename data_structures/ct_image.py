"""

"""

import os
import pydicom
import matplotlib.pyplot as plt
import numpy as np

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

    def visualize_all_projections_mip(self):
        """

        """

        coronal_plane = MIP_coronal_plane(self.pixel_array)
        sagittal_plane = MIP_sagittal_plane(self.pixel_array)
        axial_plane = MIP_axial_plane(self.pixel_array)

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # Axial slice
        axes[0].imshow(coronal_plane, cmap='gray', aspect=2)
        axes[0].set_title(f"MIP Coronal")
        axes[0].axis('off')

        # Sagittal slice
        axes[1].imshow(sagittal_plane, cmap='gray', aspect=2)
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

