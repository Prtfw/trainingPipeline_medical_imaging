import unittest
import dataset_wrapper

class TestStringMethods(unittest.TestCase):

    def test_get_files_in_path(self):
        path, filenames = dataset_wrapper.get_files_in_path(dataset_wrapper.DATA_PATH +
                                                    '/contourfiles/SC-HF-I-6/i-contours')
        expectedfn = ['IM-0001-0149-icontour-manual.txt',
                      'IM-0001-0119-icontour-manual.txt', 'IM-0001-0039-icontour-manual.txt',
                      'IM-0001-0069-icontour-manual.txt', 'IM-0001-0099-icontour-manual.txt',
                      'IM-0001-0159-icontour-manual.txt', 'IM-0001-0109-icontour-manual.txt',
                      'IM-0001-0089-icontour-manual.txt', 'IM-0001-0029-icontour-manual.txt',
                      'IM-0001-0079-icontour-manual.txt', 'IM-0001-0049-icontour-manual.txt',
                      'IM-0001-0019-icontour-manual.txt', 'IM-0001-0219-icontour-manual.txt',
                      'IM-0001-0199-icontour-manual.txt', 'IM-0001-0139-icontour-manual.txt',
                      'IM-0001-0169-icontour-manual.txt', 'IM-0001-0059-icontour-manual.txt',
                      'IM-0001-0009-icontour-manual.txt', 'IM-0001-0129-icontour-manual.txt',
                      'IM-0001-0179-icontour-manual.txt', 'IM-0001-0189-icontour-manual.txt',
                      'IM-0001-0209-icontour-manual.txt']
        self.assertTrue(filenames == expectedfn)
    def test_match_dicom_path(self):
        test_path = dataset_wrapper.DATA_PATH +'/contourfiles/SC-HF-I-6/i-contours\
        /IM-0001-0139-icontour-manual.txt'
        dicom_folder, dicom_name = dataset_wrapper.match_dicom_path(test_path)
        self.assertTrue(dicom_folder == 'SC-HF-I-6')
        self.assertTrue(dicom_name == '139.dcm')
        dicom_folder, dicom_name = dataset_wrapper.match_dicom_path('______')
        self.assertTrue(dicom_folder is None)
        self.assertTrue(dicom_name is None)


if __name__ == '__main__':
    unittest.main()
