""" visualizes dicoms and contours """
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

COLORS = [(0, 0, 1, c) for c in np.linspace(0, 1, 100)]
CMAPBLUE = mcolors.LinearSegmentedColormap.from_list('mycmap', COLORS, N=5)

def plot_overlay(_dicom, _mask, _name=''):
    '''quick code to overlay mask on dicom'''
    dicom = plt.imshow(_dicom['pixel_data'], cmap=plt.cm.bone)
    mask = plt.imshow(_mask['mask'], alpha=.4, cmap=CMAPBLUE)
    if _name:
        plt.title(_name)
    plt.show()
