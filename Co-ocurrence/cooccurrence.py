#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import math
import csv
import scipy
from scipy.sparse import load_npz
from scipy.sparse import dok_matrix
from scipy.sparse import save_npz


class CoOccurrence:
    #dtype must have higher max than
    def __init__(self):
        self.df = None
        self.data_len = None
        self.unique_tags = None
        self.number_of_tags = None
        self.tags_dict = None
        self.tags_dict_inverse = None
        self.dtype_co_occurrence = None
        self.tags_occurrence_dict = None
        self.co_occurrence_dok = None

    def _generate_unique_tags(self):
        unique_tags = []
        for index, row in self.df.iterrows():
            if row['tagged']:
                for tag in row['tags'].split("|"):
                    unique_tags.append(tag)
        return list(set(unique_tags))

    # generates co-occurrence matrix and tag occurrence vector
    # WILL DELETE CURRENT MATRIX
    def generate_occurrences(self,dtype_co_occurrence: np.dtype, export: bool = True, export_path: str = ".",csv_path: str = "."):
        if self.co_occurrence_dok is not None and self.tags_occurrence_dict is not None:
            self.co_occurrence_dok.clear()
            self.tags_occurrence_dict.clear()
        # THIS SETS LEN TO ZERO

        self.df = pd.read_csv(csv_path+"/processed_dataset.csv")
        self.data_len = self.df.shape[0]
        print(self.data_len)
        self.unique_tags = self._generate_unique_tags()
        self.number_of_tags = len(self.unique_tags)
        self.tags_dict = {self.unique_tags[i]: i for i in range(0, len(self.unique_tags))}
        self.tags_dict_inverse = {v: k for k, v in self.tags_dict.items()}
        self.dtype_co_occurrence = dtype_co_occurrence
        self.tags_occurrence_dict = {self.unique_tags[i]: 0 for i in range(0, len(self.unique_tags))}
        assert np.issubdtype(self.dtype_co_occurrence, np.integer)
        assert np.iinfo(self.dtype_co_occurrence).max > self.data_len
        self.co_occurrence_dok = dok_matrix((len(self.unique_tags), len(self.unique_tags)),
                                            dtype=self.dtype_co_occurrence)
        # error
        # todo either init again(unnecessary init) or build function that catches the exception(unclean exception
        #  handling) However only tags that do not exist should give an error so this is the current version :P

        for index, row in self.df.iterrows():
            if index % 10000 == 0:
                print(f"{int(round(index / self.data_len,2) * 100)}%")
            if bool(row['tagged']):
                for tag1 in row['tags'].split("|"):
                    self.tags_occurrence_dict[tag1] += 1
                    for tag2 in row['tags'].split("|"):
                        # increase dict entry(matrix is symmetric so half the entries are useless
                        self.co_occurrence_dok[self.tags_dict[tag1], self.tags_dict[tag2]] += 1
        if export:
            coo_co_occurrence_matrix = self.co_occurrence_dok.tocoo(copy=True)  # check stackoverflow
            save_npz(export_path + '/co-occurrence_matrix.npz', coo_co_occurrence_matrix)

            # convert to df and export
            occurrence_df = pd.DataFrame.from_dict(self.tags_occurrence_dict, orient='index').to_csv(
                export_path + "/tag_occurrence.csv")
            assert type(self.co_occurrence_dok) == scipy.sparse.dok.dok_matrix  # todo?

        return self.co_occurrence_dok, self.tags_occurrence_dict

    # imports
    def import_occurrences(self, co_occurrence_path: str = ".", occurrence_path: str = "."):
        tags_occurrence_df = pd.read_csv(occurrence_path + "/tag_occurrence.csv", index_col=0)
        self.tags_occurrence_dict = tags_occurrence_df.T.to_dict(orient='records')[0]
        # todo write tests

        coo_co_occurrence_matrix = load_npz(co_occurrence_path + "/co-occurrence_matrix.npz")
        self.co_occurrence_dok = coo_co_occurrence_matrix.todok(
            copy=False)  # dont need to flood memory when loading? todo stackoverflow check

        return  self.co_occurrence_dok,self.tags_occurrence_dict

