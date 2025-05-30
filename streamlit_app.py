import json
import streamlit as st
import re

# text
st.title('Geiriau | Words')
st.subheader("What they talk about in the Welsh parliament")

# load data
with open('year_FL.json') as json_data:
    d = json.load(json_data)

# collect user input and cast to lowercase. And log
user_input = st.text_input("Look up a word and see how frequently it's been used in the Senedd over time", 'donation').lower()
 
# make a dictionary of the results for the word looked up each year
search_dict = {}
for y in d:
    result = next((v[1] for v in d[y] if v[0] == user_input), float(0))
    search_dict[y] = result

# make line chart
st.line_chart(search_dict)

# extract the most recent update from the log file and print for the 'Last updated' line
with open('harvesting_log.txt') as f:
    update_list = list(f.readlines())
    last_line = update_list[-1:][0]
    ll = re.split(' at |, ', last_line)[1]
    update = 'Last update: ' + ll
st.markdown(update)

# print link to the README on the github repo
st.link_button('About', 'https://github.com/aodhanlutetiae/senedd_words/blob/main/README.md',  use_container_width=False)

