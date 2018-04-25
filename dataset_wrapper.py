""" returns dataset object with callable next_batch() """

import os
import csv

import parsing
import visualize
import batching

DATA_PATH = './final_data'
LINKFILE_PATH = '/Users/mengningshang/Desktop/Dev_Env/medseg/final_data/link.csv'

def get_file_pairs(_path_to_link):
    '''parse link file'''
    contour_files = []
    dicom_files = []
    _pair_dict = {}
    with open(_path_to_link) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            contour_files.append(row[1])
            dicom_files.append(row[0])
            _pair_dict[row[1]] = row[0]
    # slice off header on link file
    return contour_files[1:], dicom_files[1:], _pair_dict


def get_files_in_path(_path):
    '''returns list of file from path (recursive)'''
    for (dirpath, dirnames, filenames) in os.walk(_path):
        return dirpath, filenames

def match_dicom_path(_path_to_contour):
    '''adapter to find the right dicom img path given contour name'''
    # TODO: handle errors better, this break if filename formatting is off
    path_arr = _path_to_contour.split('/')
    try:
        filename = (path_arr[-1]).split('-')[-3].lstrip('0')+'.dcm'
        folder = path_arr[-3]
    except IndexError:
        print("unable to parse, check filename: "+_path_to_contour)
        return None, None
    return folder, filename

def make_data(dic, cont):
    '''returns data as DataSet object'''
    new_data_set = batching.DataSet(dic, cont)
    return new_data_set


def batch_wrapper(_linkfile_path, contour_type='o'):
    '''main function to call, returns DataSet Obeject'''
    all_path2contours = []
    contour_files, _, pairs = get_file_pairs(_linkfile_path)
    contour_paths = ['./final_data/contourfiles/'+ x +'/'+ contour_type +'-contours' for x in contour_files]

    for _path in contour_paths:
        path2contours, contours_avail = get_files_in_path(_path)
        all_path2contours.extend([path2contours + '/' + x for x in contours_avail])

    # fix: memoize for scalability
    dicoms = [parsing.parse_dicom_file(DATA_PATH + '/dicoms/' + pairs[match_dicom_path(x)[0]]
                                       + '/' + match_dicom_path(x)[1]) for x in all_path2contours]
    contours = [{'mask': parsing.poly_to_mask(parsing.parse_contour_file(x), 256, 256),
                 'file_path': x.split('/')[-3:]}
                for x in all_path2contours]
    return make_data(dicoms, contours)


batch3=batch_wrapper(LINKFILE_PATH).next_batch(50)
'''
visualize.plot_overlay(batch3[0][10], batch3[1][10], batch3[1][10]['file_path'])  # quick visual check
'''
# print(batch3[1][10])
