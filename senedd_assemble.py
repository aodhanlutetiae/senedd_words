import os
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import json
import warnings
warnings.simplefilter(action = 'ignore', category = Warning)
from collections import Counter
import sys




# 1. CHECK IF THERE ARE NEW XML FILES AVAILABLE ONLINE

def collect_list(lang = 'en'):

    """makes a list of available proceedings files online and will allow us to print the number of new xml files.
    Can take string argument for 'en' or 'cy' depending on which directory you want to check but sets 'en' as default """

    # print statement
    print("Collecting list of available XML files from They Work For You")
    
    # collect web page
    my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:84.0) Gecko/20100101 Firefox/84.0"}
    eng_url = f'https://www.theyworkforyou.com/pwdata/scrapedxml/senedd/{lang}/'
    req = requests.get(eng_url, headers = my_headers)
    soup = bs(req.content, features="lxml")

    # assemble list of links from the soup
    xml_list = []
    for x in soup.find_all('td'):
        for y in x.find_all('a'):
            filename = y.text
            xml_list.append(filename)

    # remove a trailing piece of text that gets collected too
    xml_list = xml_list[1:]

    return xml_list

# run function to get current online XML file urls as a list; assign results to variable
xml_list_en = collect_list()

# make a list of the XML files already held locally
current_dir_files_list = list(os.listdir("senedd_data"))

# if there's no difference in length, just print a message that there are no new files, and exit here
if len(xml_list_en) == len(current_dir_files_list):
    print('No new files to collect. Stopping program.')
    # update log before exiting
    f = open("harvesting_log.txt", "a")
    time_now = time.strftime("%a %b %d %Y %H:%M", time.localtime(time.time()))
    nb = len(current_dir_files_list)
    f.write(f"file run at {time_now}, {nb} (real) xml files held \n")
    f.close()
    sys.exit(0)
    
# otherwise make a list of what needs to be collected and report
else:
    diff_list = list(set(xml_list_en) - set(current_dir_files_list))
    diff_len = len(diff_list)

    print(f"New files! {diff_len} new xml file(s) of proceedings")
    
    
    

# 2. COLLECT ANY NEWLY AVAILABLE FILES

def collect_xmls(url_list):

    """Given a list of XML urls for the Senedd proceedings by date, this code collects all the files and stores them locally"""

    base_url = 'https://www.theyworkforyou.com/pwdata/scrapedxml/senedd/en/'

    for x in range(len(url_list)):

        # download the file
        file = url_list[x]
        this_url = base_url + file
        req = requests.get(this_url)

        # write (save) the file, which always has a different name to the other files
        with open(f'senedd_data/{file}', 'wb') as file:
            file.write(req.content)
        
        # pause
        time.sleep(1)
        
    response = "Finished collecting new XML files"
    return response

# use the function to collect the new XMLs
collect_xmls(diff_list)
    
# create a final list of all the XML file names now held locally
current_dir_files_list = list(os.listdir("senedd_data"))

# remove any empty files from list: check for size in bytes. Drop anything < 100 bytes
# note: this is what generates the 'nb files held' statement at end, so count and log will be correct but the drive will still hold the tiny file
for x in current_dir_files_list:
    size = os.path.getsize((f'senedd_data/{x}'))
    if size < 100:
        current_dir_files_list.remove(x)
    
print(f'{len(current_dir_files_list)} XML files now held locally')




# 3. ASSEMBLE ALL XML FILES INTO A SINGLE DF

# Create dfs for all the local XML files and assemble these dfs into a single dictionary
print('Assembling mega_df')
df_dict = {}
soucis = []
for x in current_dir_files_list:
    
    try:
        year_ext = x[6:10]
        # make a df from an xml file and add col with year
        df = pd.read_xml(f'senedd_data/{x}', xpath = './/p')
        df['year'] = year_ext
        # add df to dictionary
        df_dict[x] = df
        
    except:
        soucis.append(x)

# flag up any problems in extracting from XML files
pb_len = len(soucis)
print (f"{pb_len} ignored problem file(s):", soucis)

# build a single df from the dictionaries just assembled
mega_df = pd.concat(df_dict, ignore_index = True)

# ---------------- OPTIONAL ------------ un-comment this to save the csv locally 
# mega_df.to_csv('mega.csv', index = False)

# clean the mega df
# remove NAN from the p (paragraph) col
mega_df = mega_df[mega_df.p.isnull()!= True]
# remove opening metadata line on each session that gives time and Llywydd
mega_df = mega_df[mega_df.p.str.startswith("The Assembly met at") == False]
# remove all dodgy apostrophes
mega_df = mega_df.replace("`|’|‘", "'", regex=True)

# conclude with mega_df dimensions
print(f'mega_df now assembled: {mega_df.shape}')




# 4. ASSEMBLE A DICTIONARY OF {YEAR:[{'word': 0.02, 'word': 0.003, etc. }}, YEAR: ...]}

def year_to_list(yr, df):
    
    """get clean lowercase word list, then a freq dict - from a year"""
    
    # filter dataframe for year supplied in argument
    fil = df[df.year == yr]
    
    # get a series from the column containing the text (p), and make into a list
    df_series = fil.p
    df_list = list(df_series)

    # limit list elements to strings and lowercase them
    df_string_only_list = [x for x in df_list if type(x) == str]
    string_of_words = ' '.join(df_string_only_list)
    word_list = string_of_words.split()
    lower_word_list = [x.lower() for x in word_list]

    # clean up metalanguage left in the list
    b = [x for x in lower_word_list if x[-1:] != "]" and x[:1] != '[']
    c = [x for x in b if x.startswith("oaq") == False]
    d = [x for x in c if x.startswith("ndm") == False]

    # # remove things standing alone that are not words (long dash, short dash etc.)
    things = ['—', '-', '&', '£', '/', '+']
    done2 = [x for x in d if x not in things]

    # trim words with single quote marks at tail        
    d3 = []
    for x in done2:
        if x[-1:] == "'":
            ok = x[:-1]
            d3.append(ok)
        else:
            d3.append(x)
            
    # trim words with single quote marks at top        
    d4 = []
    for x in d3:
        if x[:1] == "'":
            ok = x[1:]
            d4.append(ok)
        else:
            d4.append(x)
            
    # remove trailing punctuation (second dash removes long dash) and trailing quote marks (again)
    problems = ['.', ':', ';', '!', '?', ',', '-', '—', '"', "'"]     
    clean = [x[:-1] for x in d4 if x[-1:] in problems]              
    remaining = [x for x in d4 if x[-1:] not in problems]
    done = clean + remaining

    # remove trailing punctuation AGAIN
    clean2 = [x[:-1] for x in done if x[-1:] in problems]              
    remaining2 = [x for x in done if x[-1:] not in problems]
    done2 = clean2 + remaining2

    # remove possessive s
    cleaned_s = [x[:-2] for x in done2 if x[-2:] == "'s"]
    remaining_s = [x for x in done2 if x[-2:] != "'s"]
    done_s = cleaned_s + remaining_s

    # remove numbers 
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    non = [x for x in done_s if x not in numbers]
    
    # remove standalone letters (except A, I and X (= twitter)) and empty words of len(0)
    letters = ['', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    non_nl = [x for x in non if x not in letters]

    # remove opening single and double quote marks
    guai = ["'", '"']
    ng = [x[1:] for x in non_nl if x[:1] in guai]              
    nong = [x for x in non_nl if x[:1] not in guai]
    fatto = ng + nong
    # remove closing single and double quote marks
    ng2 = [x[:-1] for x in fatto if x[-1:] in guai]              
    nong2 = [x for x in fatto if x[-1:] not in guai]
    fatto2 = ng2 + nong2
    
    # get a freq list for all the terms in this year-dict
    c = Counter(fatto2)
    year_freq = [(i, c[i] / len(fatto2) * 100.0) for i in c] 
    
    return year_freq
    
# make a year list from the df, in order
years_int = list(mega_df.year.unique())
years_int.sort()

# use the function to create a freq list (VALUE) for each year (KEY), then append to years_fl_dict
print('Assembling dictionary of frequencies')
years_fl_dict = {}
for x in years_int:
    freq_list = year_to_list(x, mega_df)
    years_fl_dict[x] = freq_list
    
# export dictionary as a json file
with open('year_FL.json', 'w') as f:
    json.dump(years_fl_dict, f)
    
# update log
f = open("harvesting_log.txt", "a")
time_now = time.strftime("%a %b %d %Y %H:%M", time.localtime(time.time()))
nb = len(current_dir_files_list)
f.write(f"file run at {time_now}, {nb} (real) xml files held \n")
f.close()
    