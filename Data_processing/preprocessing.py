# %%
import json
import time
import datetime
import numpy as np
import os
import glob
import matplotlib as plt
import pandas as pd


class Preprocessing:

    def __init__(self,csv_path, json_path):
        self.df = pd.read_csv(csv_path)
        self.region = json_path.split('/')[1][:2]
        self.csv_path = csv_path
        self.json_path = json_path

    def process_region_data(self):
        print(self.region)
        # Add new columns:
        self._add_category_string(self.json_path)
        self._add_tagged_column()
        self._add_region_column()
        return self.df

    def _add_category_string(self, json_path):
        category_file = open(json_path)
        category_file = json.load(category_file)
        category_list = [0 for i in range(0, 45)]
        for elem in category_file['items']:
            category_list[int(elem['id'])] = elem['snippet']['title']
        # generate column that fits category from dataframe
        category_text_column = []
        for item in self.df['categoryId']:
            category_text_column.append(category_list[item])
        # add categories to dataframe
        self.df['category_text'] = category_text_column

    def _add_tagged_column(self):
        tagged = []
        for tag in self.df['tags']:
            if tag == "[None]":
                tagged.append(False)
            else:
                tagged.append(True)
        self.df['tagged'] = tagged

    def _add_region_column(self):
        region_column = []
        for i in range(self.df.shape[0]):
            region_column.append(self.region)
        self.df['region'] = region_column
