import json
import streamlit as st
import re

# text
st.title('Geiriau | Words')
st.subheader("What they talk about in the Welsh parliament")
    
# @st.cache_data(max_entries = 1)
with open('year_FL.json') as json_data:
    d = json.load(json_data)

# collect user input and cast to lowercase
user_input = st.text_input("Look up a word", 'donation').lower()
 
search_dict = {}
for y in d:
    result = next((v[1] for i, v in enumerate(d[y]) if v[0] == user_input), None)
    search_dict[y] = result

# make line chart
st.line_chart(search_dict)

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
