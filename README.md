# senedd_words

This app allows you to compare the frequency of a word in the Welsh parliament (the Senedd) from one year to the next, since the election of May 2016. 

It shows how often a word was used in the parliament as a proportion of all the words uttered that year. So looking up 'Brexit' shows it was used much more often in 2019, as a proportion of everything said that year, than in other years.

![picture](brexit_search.png)

The word Brexit was used 1,145 times in the Senedd in 2019, and was just under 0.1% of all the 1,378,551 words heard there in 2019. This percentage figure is what's used to compare a word between one year and the next.

The app uses the [files](https://www.theyworkforyou.com/pwdata/scrapedxml/senedd/en/) assembled by [They Work For You](https://www.theyworkforyou.com/) from the Senedd's [open data](https://senedd.wales/help/open-data/) and runs on [streamlit](https://streamlit.io/).

It was made by [@aodhanlutetiae](https://x.com/aodhanlutetiae) and takes the [the Westminster version](https://parli-n-grams.puntofisso.net/) of [@puntofisso](https://puntofisso.net/) as inspiration.

## The data

The words considered are those uttered in *plenary* sessions, i.e. when all Senedd members meet in the main chamber (usually twice a week). It does not include committee meetings. When all the proceedings are collected for a full year there are over a million words. These are then cleaned to remove punctuation, capital letters and metadata.

This is updated weekly and can be downloaded as a json file [here](https://seneddbucket.s3.amazonaws.com/year_WL.json).

## Ideas

- When do we talk about people: Boris, Gething, Bates?
- What about particular companies: Amazon, Airbnb, Tata?
- What about groups: teachers, nurses, farmers, carers?
- What about technology: Tiktok, Snapchat, Instagram? 
- Or concepts: trolling, distancing?
- What about topics: speed, donation, lockdown, adhd?
- What never gets mentioned?

## Welsh

This parliament is different to Westminster because two languages are used. This means that some of the words are spoken in Welsh and appear in the transcript with an English translation. The question of potentially differing trends in English-language discussions versus discussions in Welsh is ignored.
