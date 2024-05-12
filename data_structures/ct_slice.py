"""
File contains the definition of Class CTSlice that will handle slides of CT Scan Image.

Author(s): Ikram Ul Haq (ulhaqi12)
"""


class CTSlice:
    """
    Class to maintain important headers and data of one slice
    """

    def __init__(self, image_slice):
        self.sop_instance_uid = image_slice.SOPInstanceUID
        self.slice_thickness = image_slice.SliceThickness
        self.image_position_patient = image_slice.ImagePositionPatient
        self.series_number = image_slice.SeriesNumber
        self.acquisition_number = image_slice.AcquisitionNumber
        self.instance_number = image_slice.InstanceNumber
        self.slice_location = image_slice.SliceLocation
        self.number_of_rows = image_slice.Rows
        self.number_of_columns = image_slice.Columns
        self.pixel_spacing = image_slice.PixelSpacing

        self.data = image_slice.pixel_array




