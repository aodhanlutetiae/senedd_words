import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests

st.title('Geiriau | Words')
st.subheader("What they talk about in the Welsh parliament")

@st.cache_data
def load_data(url):
    req = requests.get(url)
    return req.json()

aws_l = 'https://seneddbucket.s3.amazonaws.com/year_WL.json'
with st.spinner(text="Hang on, we're loading up nine years of politicians talking..."):
    d = load_data(aws_l)

user_input = st.text_input("Look up a word", 'donation').lower()

search_dict = {}
for y in d:
    total_words = len(d[y])
    term_count = len([x for x in d[y] if x == user_input])
    perc = (term_count / total_words) * 100
    search_dict[y] = perc

df = pd.Series(search_dict).to_frame().reset_index()
df.columns = ['year', 'value']
df2 = df.reset_index().set_index('year')['value']

st.line_chart(df2)

st.markdown('[About](https://github.com/aodhanlutetiae/senedd_words/blob/main/README.md)')
