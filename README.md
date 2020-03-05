# Pinyin English Names
Find English names that can be read in Chinese pinyin.

# Data Source
Data files are in ```input_files``` folder.
- ```NationalNames.csv``` is part of the US baby names dataset.
  - It contains all registered baby names from 1880 to 2014, ordered by year.
  - Obtained from Kaggle: https://www.kaggle.com/kaggle/us-baby-names/version/2
- ```pinyin.txt``` contains all possible Chinese pinyin combinations, without intonation.
  - It is created from Chinese character & pinyin dataset ```pinyin_dictionary.txt```, which is obtained from https://github.com/mozillazg/pinyin-data
  
# Start Searching
Run the script ```search_name.py``` will give you a table of English names that is valid in Chinese pinyin, along with some other information:
| name    | n_syllable | cnt    |
|---------|------------|--------|
| Mia     | 2          | 144315 |
| Luke    | 2          | 137094 |
| Anna    | 2          | 118826 |
| Natalie | 3          | 134998 |
- ```n_syllable``` tells you how many Chinese characters can be interpreted from this name. Usually Chinese given names only have 2 syllables. English names may have 3 or 4.
- ```cnt``` is the number this name has been used in the given period. In this case there are 144k babies named Mia during year 2000-2014.

The search result is saved in ```pinyin_names.csv```.

To customize the name dataset you want to use, run ```names_cleanup.py``` separately and change the year you want to include.
