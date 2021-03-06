import emoji
import pandas as pd
from os import listdir, mkdir
import os
import json
import numpy as np
from emoji import EMOJI_UNICODE

from os.path import exists

def find_csv_filenames(path_to_dir="Dataset/", suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


def create_list_of_country_codes(filenames):
    country_codes = []
    for filename in filenames:
        country_codes.append(filename[:filename.find("_")])
    return country_codes


def did_use_caps(title):
    words = title.split()
    for word in words:
        if word.isupper() == True:
            return True
    return False


def did_use_parenthesis_or_square_brackets(title):
    found_parenthesis_pair = False
    found_square_brackets_pair = False

    for index in range(0, len(title)):
        if found_parenthesis_pair or found_square_brackets_pair:
            break;
        if title[index] == "(":
            for new_index in range(index+1, len(title)):
                if title[new_index] == ")":
                    found_parenthesis_pair = True;
                    break;
        if title[index] == "[":
            for new_index in range(index + 1, len(title)):
                if title[new_index] == "]":
                    found_square_brackets_pair = True;
                    break;
    return found_parenthesis_pair or found_square_brackets_pair;

def did_use_emojis(title):
    for index in range(0, len(title)):
        char = title[index]
        if emoji.is_emoji(char):
            return True
    return False

def create_totals_file(country, number_of_titles_with_parenthesis_or_squarebracket_usage, number_of_titles_with_caps_usage, number_of_titles_with_emoji_usage, number_of_videos_in_the_period):
    header_for_totals = {'number_of_titles_with_parenthesis_or_squarebracket_usage': [number_of_titles_with_parenthesis_or_squarebracket_usage],
                         'number_of_titles_with_caps_usage': [number_of_titles_with_caps_usage],
                         'number_of_titles_with_emoji_usage': [number_of_titles_with_emoji_usage],
                         'total_number_of_titles': [number_of_videos_in_the_period]}

    df = pd.DataFrame(header_for_totals)
    file = 'Dataset/Titledata/' + country + '/' + country +'_title_totals.csv'
    file_exists = exists(file)
    if file_exists:
        os.remove(file)
    df.to_csv(file)
    print("Created totals file for " + country)


def calculate_total_numbers_for_each_country_and_write_to_file():
    # Create list of csv filenames in the "Dataset"-folder
    filenames = find_csv_filenames()

    # Create list of country codes
    country_codes = create_list_of_country_codes(filenames)

    total_number_of_parenthesis_or_square_bracket_usage = 0
    total_number_of_caps_usage = 0
    total_number_of_emoji_usage = 0
    total_number_of_videos_in_the_period = 0

    for country in country_codes:
        titles = pd.read_csv('Dataset/' + country + '_youtube_trending_data.csv', usecols=[1])

        for index, row in titles.iterrows():
            # print(row['title'], row['trending_date'])
            title = row['title']
            total_number_of_videos_in_the_period = total_number_of_videos_in_the_period + 1
            if did_use_parenthesis_or_square_brackets(title):
                total_number_of_parenthesis_or_square_bracket_usage = total_number_of_parenthesis_or_square_bracket_usage + 1
            if did_use_caps(title):
                total_number_of_caps_usage = total_number_of_caps_usage + 1
            if did_use_emojis(title):
                total_number_of_emoji_usage = total_number_of_emoji_usage + 1

        create_totals_file(country, total_number_of_parenthesis_or_square_bracket_usage, total_number_of_caps_usage,
                           total_number_of_emoji_usage, total_number_of_videos_in_the_period)

        total_number_of_parenthesis_or_square_bracket_usage = 0
        total_number_of_caps_usage = 0
        total_number_of_emoji_usage = 0
        total_number_of_videos_in_the_period = 0

def create_totals_perday_file(country, array_of_dates, array_of_number_of_titles_with_parenthesis_or_squarebracket_usage, array_of_number_of_titles_with_caps_usage, array_of_number_of_titles_with_emoji_usage, array_of_number_of_videos_on_the_day):
    header_for_totals = {'date': array_of_dates,
                         'number_of_titles_with_parenthesis_or_squarebracket_usage': array_of_number_of_titles_with_parenthesis_or_squarebracket_usage,
                         'number_of_titles_with_caps_usage': array_of_number_of_titles_with_caps_usage,
                         'number_of_titles_with_emoji_usage': array_of_number_of_titles_with_emoji_usage,
                         'total_number_of_titles': array_of_number_of_videos_on_the_day}

    df = pd.DataFrame(header_for_totals)
    file = 'Dataset/Titledata/' + country + '/' + country +'_allcategories_totals_per_day.csv'
    file_exists = exists(file)
    if file_exists:
        os.remove(file)
    df.to_csv(file)
    print("Created per day file for " + country)


def create_totals_per_category_perday_file(country, category, array_of_dates, array_of_number_of_titles_with_parenthesis_or_squarebracket_usage, array_of_number_of_titles_with_caps_usage, array_of_number_of_titles_with_emoji_usage, array_of_number_of_videos_on_the_day):
    header_for_totals = {'date': array_of_dates,
                         'number_of_titles_with_parenthesis_or_squarebracket_usage': array_of_number_of_titles_with_parenthesis_or_squarebracket_usage,
                         'number_of_titles_with_caps_usage': array_of_number_of_titles_with_caps_usage,
                         'number_of_titles_with_emoji_usage': array_of_number_of_titles_with_emoji_usage,
                         'total_number_of_titles': array_of_number_of_videos_on_the_day}

    df = pd.DataFrame(header_for_totals)
    file = 'Dataset/Titledata/' + country + '/' + country + '_category' + category + '_totals_per_day.csv'
    file_exists = exists(file)
    if file_exists:
        os.remove(file)
    df.to_csv(file)
    print("Created per day file for " + country + ", category: " + category)

def create_categories_file(country, category_dict):
    category_IDs = []
    category_names = []
    for (key, value) in category_dict.items():
        category_IDs.append(key)
        category_names.append(value)

    header_for_categories_file = {'category_IDs': category_IDs, 'category_names': category_names}

    df = pd.DataFrame(header_for_categories_file)
    file = 'Dataset/Titledata/' + country + '/' + country + '_category_list.csv'
    file_exists = exists(file)
    if file_exists:
        os.remove(file)
    df.to_csv(file)
    print("Created category list file for " + country)


def calculate_perday_numbers_for_each_country_and_write_to_file():
    # Create list of csv filenames in the "Dataset"-folder
    filenames = find_csv_filenames()

    # Create list of country codes
    country_codes = create_list_of_country_codes(filenames)

    array_of_dates = []
    array_of_number_of_titles_with_parenthesis_or_squarebracket_usage = []
    array_of_number_of_titles_with_caps_usage = []
    array_of_number_of_titles_with_emoji_usage = []
    array_of_number_of_videos_on_the_day = []

    perday_number_of_parenthesis_or_square_bracket_usage = 0
    perday_number_of_caps_usage = 0
    perday_number_of_emoji_usage = 0
    total_number_of_videos_perday= 0

    for country in country_codes:
        titles_and_trending_dates = pd.read_csv('Dataset/' + country + '_youtube_trending_data.csv', usecols=[1,6])
        titles_and_trending_dates.sort_values('trending_date')

        current_date = ""

        for index, row in titles_and_trending_dates.iterrows():
            title = row['title']
            if current_date != row['trending_date']:
                if current_date != "":
                    array_of_dates.append(current_date)
                    array_of_number_of_titles_with_parenthesis_or_squarebracket_usage.append(perday_number_of_parenthesis_or_square_bracket_usage)
                    array_of_number_of_titles_with_caps_usage.append(perday_number_of_caps_usage)
                    array_of_number_of_titles_with_emoji_usage.append(perday_number_of_emoji_usage)
                    array_of_number_of_videos_on_the_day.append(total_number_of_videos_perday)
                current_date = row['trending_date']
                perday_number_of_parenthesis_or_square_bracket_usage = 0
                perday_number_of_caps_usage = 0
                perday_number_of_emoji_usage = 0
                total_number_of_videos_perday = 0

                total_number_of_videos_perday = total_number_of_videos_perday + 1
                if did_use_parenthesis_or_square_brackets(title):
                    perday_number_of_parenthesis_or_square_bracket_usage = perday_number_of_parenthesis_or_square_bracket_usage + 1
                if did_use_caps(title):
                    perday_number_of_caps_usage = perday_number_of_caps_usage + 1
                if did_use_emojis(title):
                    perday_number_of_emoji_usage = perday_number_of_emoji_usage + 1
            else:
                total_number_of_videos_perday = total_number_of_videos_perday + 1
                if did_use_parenthesis_or_square_brackets(title):
                    perday_number_of_parenthesis_or_square_bracket_usage = perday_number_of_parenthesis_or_square_bracket_usage + 1
                if did_use_caps(title):
                    perday_number_of_caps_usage = perday_number_of_caps_usage + 1
                if did_use_emojis(title):
                    perday_number_of_emoji_usage = perday_number_of_emoji_usage + 1

        create_totals_perday_file(country, array_of_dates, array_of_number_of_titles_with_parenthesis_or_squarebracket_usage,
                           array_of_number_of_titles_with_caps_usage, array_of_number_of_titles_with_emoji_usage,
                           array_of_number_of_videos_on_the_day)

        perday_number_of_parenthesis_or_square_bracket_usage = 0
        perday_number_of_caps_usage = 0
        perday_number_of_emoji_usage = 0
        total_number_of_videos_perday = 0

        array_of_dates = []
        array_of_number_of_titles_with_parenthesis_or_squarebracket_usage = []
        array_of_number_of_titles_with_caps_usage = []
        array_of_number_of_titles_with_emoji_usage = []
        array_of_number_of_videos_on_the_day = []

def calculate_perday_numbers_for_each_country_and_each_category_and_write_to_file():
    # Create list of csv filenames in the "Dataset"-folder
    filenames = find_csv_filenames()

    # Create list of country codes
    country_codes = create_list_of_country_codes(filenames)

    array_of_dates = []
    array_of_number_of_titles_with_parenthesis_or_squarebracket_usage = []
    array_of_number_of_titles_with_caps_usage = []
    array_of_number_of_titles_with_emoji_usage = []
    array_of_number_of_videos_on_the_day = []

    perday_number_of_parenthesis_or_square_bracket_usage = 0
    perday_number_of_caps_usage = 0
    perday_number_of_emoji_usage = 0
    total_number_of_videos_perday= 0

    for country in country_codes:
        titles_and_categories_and_trending_dates = pd.read_csv('Dataset/' + country + '_youtube_trending_data.csv', usecols=[1, 5, 6])
        titles_and_categories_and_trending_dates.sort_values('trending_date')
        categories = np.asarray(titles_and_categories_and_trending_dates.categoryId.unique()).copy()
        categories.sort()

        category_file = json.load(open('Dataset/' + country + '_category_id.json'))
        category_dict = {}

        for elem in category_file['items']:
            category_dict[int(elem['id'])] = elem['snippet']['title']

        create_categories_file(country, category_dict)

        for category in categories:
            current_date = ""

            for index, row in titles_and_categories_and_trending_dates.iterrows():
                title = row['title']
                if category == row['categoryId']:
                    if current_date != row['trending_date']:
                        if current_date != "":
                            array_of_dates.append(current_date)
                            array_of_number_of_titles_with_parenthesis_or_squarebracket_usage.append(perday_number_of_parenthesis_or_square_bracket_usage)
                            array_of_number_of_titles_with_caps_usage.append(perday_number_of_caps_usage)
                            array_of_number_of_titles_with_emoji_usage.append(perday_number_of_emoji_usage)
                            array_of_number_of_videos_on_the_day.append(total_number_of_videos_perday)
                        current_date = row['trending_date']
                        perday_number_of_parenthesis_or_square_bracket_usage = 0
                        perday_number_of_caps_usage = 0
                        perday_number_of_emoji_usage = 0
                        total_number_of_videos_perday = 0

                        total_number_of_videos_perday = total_number_of_videos_perday + 1
                        if did_use_parenthesis_or_square_brackets(title):
                            perday_number_of_parenthesis_or_square_bracket_usage = perday_number_of_parenthesis_or_square_bracket_usage + 1
                        if did_use_caps(title):
                            perday_number_of_caps_usage = perday_number_of_caps_usage + 1
                        if did_use_emojis(title):
                            perday_number_of_emoji_usage = perday_number_of_emoji_usage + 1
                    else:
                        total_number_of_videos_perday = total_number_of_videos_perday + 1
                        if did_use_parenthesis_or_square_brackets(title):
                            perday_number_of_parenthesis_or_square_bracket_usage = perday_number_of_parenthesis_or_square_bracket_usage + 1
                        if did_use_caps(title):
                            perday_number_of_caps_usage = perday_number_of_caps_usage + 1
                        if did_use_emojis(title):
                            perday_number_of_emoji_usage = perday_number_of_emoji_usage + 1

            create_totals_per_category_perday_file(country, str(category), array_of_dates, array_of_number_of_titles_with_parenthesis_or_squarebracket_usage,
                               array_of_number_of_titles_with_caps_usage, array_of_number_of_titles_with_emoji_usage,
                               array_of_number_of_videos_on_the_day)

            perday_number_of_parenthesis_or_square_bracket_usage = 0
            perday_number_of_caps_usage = 0
            perday_number_of_emoji_usage = 0
            total_number_of_videos_perday = 0

            array_of_dates = []
            array_of_number_of_titles_with_parenthesis_or_squarebracket_usage = []
            array_of_number_of_titles_with_caps_usage = []
            array_of_number_of_titles_with_emoji_usage = []
            array_of_number_of_videos_on_the_day = []

#Make a directory "Titledata" in the "Dataset"-folder
try:
    mkdir("Dataset/Titledata")
    print("Created a folder called 'Titledata' in the 'Dataset' folder.")
except OSError as error:
    print(error)

#Make a directory for each country in the "Titledata"-folder
try:
    country_codes = create_list_of_country_codes(find_csv_filenames())
    for country in country_codes:
        mkdir("Dataset/Titledata/" + country)
except OSError as error:
    print(error)

#calculate_total_numbers_for_each_country_and_write_to_file()

#calculate_perday_numbers_for_each_country_and_write_to_file()

calculate_perday_numbers_for_each_country_and_each_category_and_write_to_file()