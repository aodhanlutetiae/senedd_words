# senedd_words

This app allows you to compare the frequency of a word in the Welsh parliament (the Senedd) from one year to the next, since the election of May 2016. 

It shows how often a word was used in the parliament as a proportion of all the words uttered that year. So looking up 'Brexit' shows it was used much more often in 2019, as a proportion of everything said that year, than in other years.

<img src="brexit_search.png" width="600">

The word Brexit was used 2,990 times in the Senedd in 2019, which was just under 0.1% of the roughly three million words heard there in 2019. This percentage figure is what's used to compare a word between one year and the next.

If you want to find the particular Senedd discussions where a word appears, you can search [here](https://www.theyworkforyou.com/senedd/).

The app runs on Streamlit. It uses the [files](https://www.theyworkforyou.com/pwdata/scrapedxml/senedd/en/) assembled by [They Work For You](https://www.theyworkforyou.com/) from the Senedd's [open data](https://senedd.wales/help/open-data/). It was made by [@aodhanlutetiae](https://x.com/aodhanlutetiae) and takes the [Westminster version](https://parli-n-grams.puntofisso.net/) built by [@puntofisso](https://puntofisso.net/) as inspiration.

## The data

The words considered are those uttered in *plenary* sessions, i.e. when all Senedd members meet in the main chamber (usually twice a week: Tuesday and Wednesday). It does not include committee meetings. Once all the proceedings have been collected, the words are cleaned to remove punctuation, capital letters etc. and metadata.

## Ideas

- When do we talk about people: Sunak, Gething, Putin?
- What about companies: Amazon, Airbnb, Tata?
- What about groups: teachers, nurses, farmers, carers?
- What about technology: Tiktok, Snapchat, Instagram, Whatsapp? 
- Or concepts: trolls, distancing?
- What about topics: speed, donation, lockdown, adhd, foodbanks, European?
- What never gets mentioned?

## Welsh

This parliament is different to Westminster because two languages are used. This means that some of the words are spoken in Welsh and appear in the transcript with an English translation. The question of potentially differing trends in English-language versus Welsh discussions is ignored.
