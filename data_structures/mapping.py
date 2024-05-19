import numpy as np
import matplotlib.pyplot as plt

from .ct_image import CTImage
from .segmentation_image import SegmentationImage


class CTMapping:

    def __init__(self, ct_image: CTImage, segmentation_image: SegmentationImage):
        self.image = None
        self.segmentation_image_combined = None
        self.segmentations = []
        self.ct_image = ct_image
        self.segmentation_image = segmentation_image
        self.mappings = []

    def do_mapping(self):

        for ct_slice in self.ct_image.slices:
            for segment_slice in self.segmentation_image.slices:
                if ct_slice.sop_instance_uid == segment_slice.sop_instance_uid:
                    self.mappings.append((ct_slice, segment_slice))

        self.mappings = sorted(self.mappings, key=lambda x: x[0].slice_location)

        ct_image_slices = []
        for ct_slice, segment_slice in self.mappings:
            ct_image_slices.append(ct_slice.data)

        self.image = np.array(ct_image_slices)

        for i in range(SegmentationImage.number_of_segmentations):
            segmentation_image_slices = []
            for ct_slice, segment_slice in self.mappings:
                segmentation_image_slices.append(segment_slice.segmentation_slices[i])

            self.segmentations.append(np.array(segmentation_image_slices))

        self.combine_segmentations()

    def plot_histogram(self, bins=256):
        """Plot histogram of the 3D image intensities."""
        plt.figure(figsize=(10, 6))
        plt.hist(self.image.flatten(), bins=bins)
        plt.title('Histogram of Pixel Intensities')
        plt.xlabel('Pixel Intensity')
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.show()

    import numpy as np
    import matplotlib.pyplot as plt

    def sigmoid_windowing(self, window_center, window_width):
        """Apply sigmoid windowing to the 3D image to enhance contrast."""
        # Sigmoid function parameters
        L = 255  # Maximum pixel intensity for an 8-bit image
        a = 10  # Control the steepness of the sigmoid, adjust based on desired contrast

        # Sigmoid transformation formula
        x = (self.image - window_center) * (a / window_width)  # Scaled distance from window center
        windowed_img = L / (1 + np.exp(-x))

        self.image = windowed_img.astype(np.uint8)

    def correct_orientation(self):

        self.image = np.flip(self.image, axis=0)
        self.segmentation_image_combined = np.flip(self.segmentation_image_combined, axis=0)

    def plot_image_slice(self, slice_index, axis=0):
        """
        Plots a single slice from a 3D numpy array.

        Parameters:
        - data: 3D numpy array
        - slice_index: index of the slice to be plotted
        - axis: axis along which to take the slice (0, 1, or 2)
        """
        if axis == 0:
            slice_data = self.image[slice_index, :, :]
        elif axis == 1:
            slice_data = self.image[:, slice_index, :]
        elif axis == 2:
            slice_data = self.image[:, :, slice_index]
        else:
            raise ValueError("Axis must be 0, 1, or 2.")

        plt.imshow(slice_data, cmap='gray')
        plt.colorbar()
        plt.title(f'Slice {slice_index} along axis {axis}')
        plt.show()

    def plot_image_slice_with_segments(self, slice_index, axis=0):
        """
        Plots a single slice from multiple 3D numpy arrays in a 2x3 subplot layout.

        Parameters:
        - datas: list of 3D numpy arrays
        - slice_index: index of the slice to be plotted
        - axis: axis along which to take the slice (0, 1, or 2)
        """
        fig, axs = plt.subplots(2, 3, figsize=(15, 10))  # Set up a 2x3 subplot grid

        all_figures = [self.image] + self.segmentations

        for i, data in enumerate(all_figures):
            ax = axs[i // 3, i % 3]  # Determine subplot location
            if axis == 0:
                slice_data = data[slice_index, :, :]
            elif axis == 1:
                slice_data = data[:, slice_index, :]
            elif axis == 2:
                slice_data = data[:, :, slice_index]
            else:
                raise ValueError("Axis must be 0, 1, or 2.")

            if i == 0:
                ax.imshow(slice_data, cmap='gray')
                ax.set_title(f'Slice {slice_index} of Image {i + 1}')
            else:
                ax.imshow(slice_data, cmap='jet')
                ax.set_title(f'Slice {slice_index} of Segmentation {i}')

            ax.axis('off')  # Hide axes ticks

        # Hide the last subplot as it's unused
        axs[1, 2].axis('off')

        plt.tight_layout()
        plt.show()

    def combine_segmentations(self, weights=None):
        """
        Computes a weighted sum of the entire 3D volumes from a list of 4 3D arrays based on given weights.

        Parameters:
        - segmentation_arrays: list of 4 3D numpy arrays.
        - weights: list of floats, weights for each array. Default is [0.2, 0.4, 0.6, 0.9].

        Returns:
        - A 3D numpy array representing the weighted sum of the entire volumes.
        """
        if weights is None:
            weights = [0.2, 0.4, 0.6, 0.9]  # Default weights

        if len(self.segmentations) != 4 or len(weights) != 4:
            raise ValueError("There must be exactly four segmentation arrays and four weights.")

        # Initialize the result volume with a float type to accommodate weighted values
        result_volume = np.zeros_like(self.segmentations[0], dtype=np.float64)

        # Compute the weighted sum of the volumes
        for seg_array, weight in zip(self.segmentations, weights):
            result_volume += weight * seg_array

        self.segmentation_image_combined = result_volume
