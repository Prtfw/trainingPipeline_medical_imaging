""" Class for dataset wrapper with next_batch
    Most of this code is adapted from Tensorflow:
    https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/learn/python/learn/datasets/mnist.py
"""

import numpy as np

class DataSet:
    '''makes batchable dataset'''
    def __init__(self,
                 images,
                 labels):
        self._images = np.asarray(images)
        self._labels = np.asarray(labels)
        self._epochs_completed = 0
        self._index_in_epoch = 0
        self._num_examples = len(labels)
    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size, shuffle=True):
        """Return the next `batch_size` examples from this data set."""
        start = self._index_in_epoch
        # Shuffle for the first epoch
        if self._epochs_completed == 0 and start == 0 and shuffle:
            perm0 = np.arange(self._num_examples)
            np.random.shuffle(perm0)
#             print(self.images,perm0,[1,2,3][perm0])
            self._images = self.images[perm0]
            self._labels = self.labels[perm0]
        # Go to the next epoch
        if start + batch_size > self._num_examples:
          # Finished epoch
            self._epochs_completed += 1
            # Get the rest examples in this epoch
            rest_num_examples = self._num_examples - start
            images_rest_part = self._images[start:self._num_examples]
            labels_rest_part = self._labels[start:self._num_examples]
            # Shuffle the data
            if shuffle:
                perm = np.arange(self._num_examples)
                np.random.shuffle(perm)
                self._images = self.images[perm]
                self._labels = self.labels[perm]
              # Start next epoch
                start = 0
                self._index_in_epoch = batch_size - rest_num_examples|0
                end = self._index_in_epoch
                images_new_part = self._images[start:end]
                labels_new_part = self._labels[start:end]
                return np.concatenate((images_rest_part, images_new_part), axis=0), np.concatenate(
                    (labels_rest_part, labels_new_part), axis=0)
        else:
            self._index_in_epoch += batch_size
            end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]
