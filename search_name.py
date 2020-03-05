import pandas as pd
from names_cleanup import filter_name_dataset
import os.path

def check_suffix(s, lexica, depth=0):
    '''Searches in s for matching strings in lexica.'''

    depth += 1   # recursion depth, number of syllables.
    #print('checking', s, 'depth', depth)
    if s in lexica: return True, depth

    flag = False
    for i in range(1,len(s)):
        #print('- checking',i, s[0:i])
        if s[0:i] in lexica: 
            flag_r, depth_r = check_suffix(s[i:], lexica, depth)
            if flag_r:
                flag = True
                depth = depth_r
        else: pass
        if flag: break
    return flag, depth


def pick_values(df, val_col, cnt_col='cnt', gt_than=10):
    ''' return the values in given df that has more than gt_than counts.'''
    return df[df[cnt_col] > gt_than][val_col].to_list()


if __name__ == "__main__":
    # Parameters that might be useful
    name_popularity = 100000   # count of a name. Unpopular name won't be considered.
    pinyin_popularity = 20    # a pinyin's popularity, to filter out rarely used pinyin.
    pinyin_exclusion = ['e']  # some pinyin that you don't want to use.

    # import names list
    names_fn = '.\\input_files\\names_count.csv'

    if not os.path.exists(names_fn):
        # Consider run names_cleanup.py manually to suit your needs.
        filter_name_dataset()

    names_df = pd.read_csv(names_fn)
    names = pick_values(names_df, 'name', gt_than=name_popularity)

    # import pinyin lexica
    lexica_df = pd.read_csv('.\input_files\pinyin.txt', names=['pinyin','cnt'])
    lexica = pick_values(lexica_df, 'pinyin', gt_than=pinyin_popularity)
    
    # some pinyin you don't want in the name
    for item in pinyin_exclusion:
        lexica.remove(item)

    # start the search!
    pinyin_names = {
        'name':[],
        'n_syllable':[],
        'cnt':[]
    }
    for name in names:
        valid, n_syllable = check_suffix(name.lower(), lexica)
        if valid:
            pinyin_names['name'].append(name)
            pinyin_names['n_syllable'].append(n_syllable)
            pinyin_names['cnt'].append(names_df[names_df.name==name]['cnt'].values[0])
    
    # Display and save.
    print('Found {} valid pinyin names out of {}.'.format(
        len(pinyin_names['name']), len(names)))
    print ('Result saved in pinyin_names.csv.')

    pinyin_names = pd.DataFrame(pinyin_names)
    pinyin_names = pinyin_names.sort_values(by='n_syllable')
    print(pd.DataFrame(pinyin_names))
    pinyin_names.to_csv('pinyin_names.csv', index=False)