"""
File contains the code of data structure to store on slice of segmentation image.

Authors(s): Ikram Ul Haq(ulhaqi12)
"""


class SegmentationSlice:

    def __init__(self, sop_instance_uid, image_position_patient, segmentation_slices):

        self.sop_instance_uid = sop_instance_uid
        self.image_position_patient = image_position_patient
        self.segmentation_slices = segmentation_slices

