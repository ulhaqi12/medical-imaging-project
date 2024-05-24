"""
File that contain utility functions for the project (mostly copied from labs/activities in the course)

Author(s): Ikram Ul Haq (ulhaqi12)
"""

import pydicom
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy


def load_and_print_info(dicom_path):
    dicom_file = pydicom.dcmread(dicom_path)
    print("DICOM Header Information:")
    print(dicom_file)
    print("\n")


def median_sagittal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the median sagittal plane of the CT image provided. """
    return img_dcm[:, :, img_dcm.shape[1]//2]    # Why //2?


def median_coronal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the median sagittal plane of the CT image provided. """
    return img_dcm[:, img_dcm.shape[2]//2, :]


def MIP_sagittal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the maximum intensity projection on the sagittal orientation. """
    # Your code here:
    #   See `np.max(...)`
    # ...
    return np.max(img_dcm, axis=2)


def AIP_sagittal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the average intensity projection on the sagittal orientation. """
    # Your code here:
    #   See `np.mean(...)`
    # ...
    return np.mean(img_dcm, axis=2)


def MIP_coronal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the maximum intensity projection on the coronal orientation. """
    # Your code here:
    # ...
    return np.max(img_dcm, axis=1)


def AIP_coronal_plane(img_dcm: np.ndarray) -> np.ndarray:
    """ Compute the average intensity projection on the coronal orientation. """
    # Your code here:
    # ...
    return np.mean(img_dcm, axis=1)


def rotate_on_axial_plane(img_dcm: np.ndarray, angle_in_degrees: float) -> np.ndarray:
    """ Rotate the image on the axial plane. """
    # Your code here:
    #   See `scipy.ndimage.rotate(...)`
    # ...
    return scipy.ndimage.rotate(img_dcm, angle_in_degrees, axes=(1, 2), reshape=False, order=0)


def apply_cmap(img: np.ndarray, cmap_name: str = 'bone') -> np.ndarray:
    """ Apply a colormap to a 2D image. """
    cmap_function = matplotlib.colormaps[cmap_name]
    return cmap_function(img)


# def visualize_alpha_fusion(img: np.ndarray, mask: np.ndarray, alpha: float = 0.25, aspect=1, visualize=False):
#     """ Visualize both image and mask in the same plot. """
#     img_sagittal_cmapped = apply_cmap(img, cmap_name='bone')    # Why 'bone'?
#     mask_bone_cmapped = apply_cmap(mask, cmap_name='prism')     # Why 'prism'?
#     mask_bone_cmapped = mask_bone_cmapped * mask[..., np.newaxis].astype('bool')
#
#     result = img_sagittal_cmapped * (1-alpha) + mask_bone_cmapped * alpha
#     if visualize:
#         plt.imshow(result, aspect=aspect)
#         plt.title(f'Segmentation with alpha {alpha}')
#         plt.show()
#     else:
#         return result


def visualize_alpha_fusion(img: np.ndarray, mask: np.ndarray, alpha: float = 0.25, aspect=1, visualize=False):
    """Visualize both image and mask in the same plot."""
    img_sagittal_cmapped = apply_cmap(img, cmap_name='bone')
    mask_bone_cmapped = apply_cmap(mask, cmap_name='prism')

    # Create a boolean array where mask is present
    mask_present = mask.astype(bool)

    # Applying (1-alpha) only where mask is present, and alpha blending where mask is present
    img_sagittal_cmapped[mask_present] *= (1 - alpha)
    result = img_sagittal_cmapped + mask_bone_cmapped * alpha * mask_present[..., np.newaxis]

    if visualize:
        plt.imshow(result, aspect=aspect)
        plt.title(f'Segmentation with alpha {alpha}')
        plt.show()
    else:
        return result

def visualize_slices(image, axial_idx, sagittal_idx, coronal_idx, aspect=1):
    """
    Plot axial, sagittal, and coronal CT slices.

    Parameters:
        image (numpy.ndarray): The 3D image array.
        axial_idx (int): The index of the axial slice to be displayed.
        sagittal_idx (int): The index of the sagittal slice to be displayed.
        coronal_idx (int): The index of the coronal slice to be displayed.
    """

    # Ensure indices are within the image dimensions
    axial_idx = np.clip(axial_idx, 0, image.shape[0] - 1)
    sagittal_idx = np.clip(sagittal_idx, 0, image.shape[1] - 1)
    coronal_idx = np.clip(coronal_idx, 0, image.shape[2] - 1)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Axial slice
    axes[0].imshow(image[axial_idx, :, :], cmap='gray')
    axes[0].set_title(f"Axial Slice at index {axial_idx}")
    axes[0].axis('off')

    # Sagittal slice
    axes[1].imshow(image[:, sagittal_idx, :], cmap='gray', aspect=aspect)
    axes[1].set_title(f"Sagittal Slice at index {sagittal_idx}")
    axes[1].axis('off')

    # Coronal slice
    axes[2].imshow(image[:, :, coronal_idx], cmap='gray', aspect=aspect)
    axes[2].set_title(f"Coronal Slice at index {coronal_idx}")
    axes[2].axis('off')

    plt.tight_layout()
    plt.show()

