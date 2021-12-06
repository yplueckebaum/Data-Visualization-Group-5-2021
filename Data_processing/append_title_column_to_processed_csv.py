import pandas as pd
import emoji

df = pd.read_csv("../processed_dataset.csv")
titles = pd.read_csv("../processed_dataset.csv", usecols=[2])

did_use_parenthesis_or_square_brackets_array = []
did_use_caps_array = []
did_use_emojis_array = []

print("Started")

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


for index, row in titles.iterrows():
    title = row['title']
    did_use_parenthesis_or_square_brackets_array.append(did_use_parenthesis_or_square_brackets(title))
    did_use_caps_array.append(did_use_caps(title))
    did_use_emojis_array.append(did_use_emojis(title))

df["did_use_parens"] = did_use_parenthesis_or_square_brackets_array
df["did_use_caps"] = did_use_caps_array
df["did_use_emojis"] = did_use_emojis_array

df.to_csv("../processed_dataset.csv")

print("Finished")