import pydicom

from .segmentaiton_slice import SegmentationSlice


class SegmentationImage:

    number_of_segmentations = 4

    def __init__(self):

        self.number_of_slices = None
        self.slices = []

    def load_data(self, image_path: str):
        """

        """

        segmentation = pydicom.dcmread(image_path)
        frames = segmentation.PerFrameFunctionalGroupsSequence
        number_of_frames_in_ct_image = len(frames)//self.number_of_segmentations

        for i in range(number_of_frames_in_ct_image):
            segments = []

            sop_instance_uid = frames[i].DerivationImageSequence[0].SourceImageSequence[0] \
                .ReferencedSOPInstanceUID
            image_position_patient = frames[i].PlanePositionSequence[0].ImagePositionPatient

            for j in range(self.number_of_segmentations):
                segments.append(frames[number_of_frames_in_ct_image * j + i])

            self.slices.append(SegmentationSlice(sop_instance_uid, image_position_patient, segments))

        self.number_of_slices = len(self.slices)





