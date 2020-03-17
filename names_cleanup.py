# This script convert the original names dataset to a set of unique values,
# and count the number of each name.
# The process may take time, so it's done in a separated script.

import pandas as pd

def filter_name_dataset(
        year_thres=2000,
        skiprows=1300000,
        fn_in='.\\input_files\\NationalNames.csv',
        fn_out='.\\input_files\\names_count.csv'
        ):
    '''
    Convert 

    Parameters:
    -----------
    year_thres: the earliest year you want to keep. In the dataset, earliest 
    year on record is 1880.

    skiprows: pandas.read_csv function paramter, use this to save loading time.
    Will not work on other dataset.
    - year >= 2000: 1300000,
    - year >= 1990: 1000000,
    - year >= 1980:  800000,
    - year >= 1970:  600000,
    - year >= 1950:  400000,
    - year >= 1930:  200000

    fn_in: input file path, the original names dataset. From Kaggle:
    https://www.kaggle.com/kaggle/us-baby-names/version/2

    fn_out: the filtered and counted names file path.

    Returns:
    --------
    No returns. This function outputs a .csv file.
    '''

    # Use skiprows to save some time
    col_names = ['id','name','year','gender','cnt']
    names = pd.read_csv(fn_in, skiprows=skiprows, names=col_names)

    # filter by year
    names = names.loc[names.year>=year_thres]
    # names.to_csv('NamesYearThres.csv', index=False)

    # count male and female names separately
    names_cnt = names.drop(columns=['id','year'])
    female_names = names_cnt[names_cnt['gender'] == 'F']
    female_names = female_names.groupby(female_names['name']).sum()
    female_names.columns = ['female_cnt']
    male_names = names_cnt[names_cnt['gender'] == 'M']
    male_names = male_names.groupby(male_names['name']).sum()
    male_names.columns = ['male_cnt']

    # merge female names and male names
    names_cnt = pd.merge(male_names, female_names, on='name', how='outer')
    names_cnt = names_cnt.fillna(value=0).astype('int')

    # names_cnt = names_cnt.sort_values(by='cnt', ascending=False)
    print(names_cnt.describe())
    names_cnt.to_csv(fn_out)


if __name__ == "__main__":
    fn_in='.\\input_files\\NationalNames.csv'
    fn_out='.\\input_files\\names_count.csv'
    filter_name_dataset(year_thres=2000, skiprows=1300000,
        fn_in=fn_in, fn_out=fn_out)
