import numpy as np

from .ct_image import CTImage
from .segmentation_image import SegmentationImage


class CTMapping:

    def __init__(self, ct_image: CTImage, segmentation_image: SegmentationImage):
        self.image = None
        self.segmentation = None
        self.ct_image =ct_image
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
