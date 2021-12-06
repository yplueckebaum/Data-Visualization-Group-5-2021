#!/usr/bin/env python
# coding: utf-8
import pickle

import networkx as nx
import pandas as pd
import numpy as np
import scipy
#import community as community_louvain
from networkx import from_scipy_sparse_matrix
from scipy.sparse import load_npz
from scipy.sparse import dok_matrix
from scipy.sparse import save_npz


class CoOccurrence:
    # dtype must have higher max than
    def __init__(self):
        self.df = pd.DataFrame()
        self.data_len = None
        self.unique_tags = None
        self.number_of_tags = None
        self.tags_dict = None
        self.tags_dict_inverse = None
        self.dtype_co_occurrence = None
        self.tags_occurrence_dict = None
        self.co_occurrence_dok = None
        self.tag_graph = None
        self.partition = None

    def setup(self,debugging,df_from_dashboard, csv_path: str = "."):
        #self.df = pd.read_csv(csv_path + "/processed_dataset.csv", engine="python", error_bad_lines=False) #try to to do this.iloc[:50]
        if debugging:
            self.df = df_from_dashboard.iloc[:100]
        else:
            self.df = df_from_dashboard
        self.data_len = self.df.shape[0]
        unique_tags = []
        for index, row in self.df.iterrows():
            if row['tagged']:
                for tag in row['tags'].split("|"):
                    unique_tags.append(tag.lower())
        self.unique_tags = list(set(unique_tags))
        self.number_of_tags = len(self.unique_tags)
        self.tags_dict = {self.unique_tags[i]: i for i in range(0, len(self.unique_tags))}
        self.tags_dict_inverse = {v: k for k, v in self.tags_dict.items()}

    # generates co-occurrence matrix and tag occurrence vector
    # WILL DELETE CURRENT MATRIX
    def generate_occurrences(self, dtype_co_occurrence: np.dtype,
                             csv_path: str = "."):
        if self.co_occurrence_dok is not None and self.tags_occurrence_dict is not None:
            self.co_occurrence_dok.clear()
            self.tags_occurrence_dict.clear()
        # THIS SETS LEN TO ZERO
        if self.df.empty:
            self.setup(csv_path)
        self.dtype_co_occurrence = dtype_co_occurrence
        self.tags_occurrence_dict = {self.unique_tags[i]: 0 for i in range(0, len(self.unique_tags))}
        assert np.issubdtype(self.dtype_co_occurrence, np.integer)
        assert np.iinfo(self.dtype_co_occurrence).max > self.data_len
        self.co_occurrence_dok = dok_matrix((len(self.unique_tags), len(self.unique_tags)),
                                            dtype=self.dtype_co_occurrence)

        for index, row in self.df.iterrows():
            if index % 10000 == 0:
                print(f"{int(round(index / self.data_len, 2) * 100)}%")
            if bool(row['tagged']):
                for tag1 in row['tags'].split("|"):
                    self.tags_occurrence_dict[tag1] += 1
                    for tag2 in row['tags'].split("|"):
                        # increase dict entry(matrix is symmetric so half the entries are useless
                        self.co_occurrence_dok[self.tags_dict[tag1], self.tags_dict[tag2]] += 1

        return self.co_occurrence_dok, self.tags_occurrence_dict

    def generate_graph(self):
        self.tag_graph = from_scipy_sparse_matrix(self.co_occurrence_dok, parallel_edges=False,
                                                  create_using=nx.Graph)

    def generate_partition(self):
        self.partition = community_louvain.generate_dendrogram(self.tag_graph, weight='weight')

    # imports
    def import_occurrences_old(self, co_occurrence_path: str = ".", occurrence_path: str = ".", name=""):
        tags_occurrence_df = pd.read_csv(occurrence_path + "/tag_occurrence.csv", index_col=0)
        self.tags_occurrence_dict = tags_occurrence_df.T.to_dict(orient='records')[0]

        coo_co_occurrence_matrix = load_npz(co_occurrence_path + "/co-occurrence_matrix.npz")
        self.co_occurrence_dok = coo_co_occurrence_matrix.todok(
            copy=False)  # dont need to flood memory when loading? todo stackoverflow check

        return self.co_occurrence_dok, self.tags_occurrence_dict

    def import_occurrences(self, co_occurrence_path: str = ".", occurrence_path: str = ".",
                           co_occurrence_name="co-occurrence", occurrence_name="occurrence"):
        coo_co_occurrence_matrix = load_npz(co_occurrence_path + "/" + co_occurrence_name + ".npz")
        self.co_occurrence_dok = coo_co_occurrence_matrix.todok(
            copy=False)

        with open(occurrence_path + "/" + occurrence_name + '.pickle', 'rb') as handle:
            self.tags_occurrence_dict = pickle.load(handle)

    def export_occurrences(self, co_occurrence_path: str = ".", occurrence_path: str = ".",
                           co_occurrence_name="co-occurrence", occurrence_name="occurrence"):
        save_npz(co_occurrence_path + '/' + co_occurrence_name + ".npz", self.co_occurrence_dok.tocoo(copy=True))

        with open(occurrence_path + "/" + occurrence_name + '.pickle', 'wb') as handle:
            pickle.dump(self.tags_occurrence_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_network(self, path=".", name="network", ):
        with open(path + "/" + name + '.pickle', 'rb') as handle:
            self.tag_graph = pickle.load(handle)

    def export_network(self, path=".", name="network"):
        with open(path + "/" + name + '.pickle', 'wb') as handle:
            pickle.dump(self.tag_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_partition(self, path=".", name="partition"):
        with open(path + "/" + name + '.pickle', 'rb') as handle:
            self.partition = pickle.load(handle)

    def export_partition(self, path=".", name="partition"):
        with open(path + "/" + name + '.pickle', 'wb') as handle:
            pickle.dump(self.partition, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_tag_dict(self, path=".", name="partition"):
        with open(path + "/" + name + '.pickle', 'rb') as handle:
            self.tags_dict = pickle.load(handle)

    def export_tag_dict(self, path=".", name="tag_dict"):
        with open(path + "/" + name + '.pickle', 'wb') as handle:
            pickle.dump(self.tags_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_tag_dict_inv(self, path=".", name="tag_dict_inv"):
        with open(path + "/" + name + '.pickle', 'rb') as handle:
            self.tags_occurrence_dict = pickle.load(handle)

    def export_tag_dict_inv(self, path=".", name="tag_dict_inv"):
        with open(path + "/" + name + '.pickle', 'wb') as handle:
            pickle.dump(self.tags_dict_inverse, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def import_tag_graph(self, path=".", name="tag_graph"):
        with open(path + "/" + name + '.pickle', 'rb') as handle:
            self.tag_graph = pickle.load(handle)

    def export_tag_graph(self, path=".", name="tag_graph"):
        with open(path + "/" + name + '.pickle', 'wb') as handle:
            pickle.dump(self.tag_graph, handle, protocol=pickle.HIGHEST_PROTOCOL)
