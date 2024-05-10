"""

"""

import os
import pydicom

from .ct_slice import CTSlice


class CTImage:

    def __init__(self):

        self.number_of_slices = None
        self.slices = []

    def load_data(self, data_path: str):
        """
        This function will receive path of folder containing dicom data and will populate CTImage Object
        """

        for image_path in os.listdir(data_path):
            image_path = os.path.join(data_path, image_path)

            image = pydicom.dcmread(image_path)

            self.slices.append(CTSlice(image))

        self.number_of_slices = len(self.slices)


