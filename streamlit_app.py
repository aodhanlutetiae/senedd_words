import pandas as pd
import streamlit as st
import requests
import re

# text
st.title('Geiriau | Words')
st.subheader("What they talk about in the Welsh parliament")

# define function that loads the data
@st.cache_data(max_entries = 1)
def load_data(url):
    req = requests.get(url)
    return req.json()

# use the function with AWS as address: 214 MB. Run waiting message
aws_l = 'https://seneddbucket.s3.amazonaws.com/year_WL.json'
aws_l_test = 'https://seneddbuckettest.s3.amazonaws.com/test_data_100k_10MB.json'

with st.spinner(text="Hang on, we're loading up nine years of politicians talking..."):
    d = load_data(aws_l_test)

# collect user input and cast to lowercase
user_input = st.text_input("Look up a word", 'donation').lower()

# work through each year(key) in the dictionary to get len of wordlist(value) 
# and to count occurences of word queried by user. Then add results to new dict
search_dict = {}
for y in d:
    total_words = len(d[y])
    term_count = len([x for x in d[y] if x == user_input])
    perc = (term_count / total_words) * 100
    search_dict[y] = perc

# make a df from the dictionary just assembled
df = pd.DataFrame.from_dict(search_dict, orient='index', columns=['value'])

# make line chart
st.line_chart(df)

# extract the most recent update from the log file and print for the 'Last updated' line
with open('repo_log.txt') as f:
    for line in f:
        pass
    last_line = line
    ll = re.split(' at |, ', last_line)[1]
    update = 'Last update: ' + ll
st.markdown(update)

# print link to the README on the github repo
st.markdown('[About](https://github.com/aodhanlutetiae/senedd_words/blob/main/README.md)')
