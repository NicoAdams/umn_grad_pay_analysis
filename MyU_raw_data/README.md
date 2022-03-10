# Data Source
Pay data gathered from MyU following a [guide posted on AskMN](https://askmn.libanswers.com/umtc_faq/faq/341039) taking "observations" in Janurary, June, and October over the last several years.
This data was then anonymized and merged into the [data.csv](data.csv) file in this repo.
The merging was done by [merge.py](merge.py).

# Obtain Raw Data
As the guide linked above says, non-University researchers must contact a UMN librarian in order to gather this data.

If you are a member of UMN, then you are able to access the data following the above guide. 
In order to get the same data that was used to generate the anonymized data here,
you will want to use the "Search" functionality in the "Job Code - Job Title" drop down box.
You then add (press the double right arrow) the following three searches to the list of job codes to include.
1. `Contains` "Professor" to get the faculty jobs (approximately)
2. `Starts` "95" to get the graduate students jobs (approximately)
3. `Starts` "9301" to get the presidents job

After this selection of the "Job Code - Job Title" is made, then you just go through the various dates in the past downloading the data.
**Note**: Make sure to scroll to the bottom of the page to click "Export". The first "Export" you see is only for the summaries displayed at the top.

