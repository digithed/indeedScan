from bs4 import BeautifulSoup
import requests
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import json
import timeit


#user input data

job = input("Input job: ")
city = input("Input city (i.e. new york, NY): ")
page_num = input("Input number of pages to scan (usually 10 jobs per page): ")

#Start timer for calculating runtime

start = timeit.default_timer()

#variables for cleaning data

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))

#loop for creating links for each page based on number of desired pages entered

pages = []
for i in range(0,int(page_num)*10,10):
	link = f"&start={i}"
	pages.append(link)

#main program

def program(pages):
	final_list = []
	cleaned_list = []
	for p in pages:
		link = f"https://www.indeed.com/jobs?q={job}&l={city}{p}"
		page = requests.get(link)
		document = page.text
		soup = BeautifulSoup(document, 'html.parser')
		description = soup.find_all("div", {'class': 'summary'})

		for i in description:
			text = i.text.strip()
			final_list.append(text)

		for f in final_list:
			tokens = tokenizer.tokenize(f)
			clean = [w for w in tokens if not w in stop_words]
			lowercase = [w.lower() for w in clean]
			filtered_words = [x for x in lowercase if x not in job and x not in city]
			cleaned_list += filtered_words

	fdist1 = FreqDist(cleaned_list)
	stop = timeit.default_timer()
	print('Time: ', stop - start)
	return fdist1.plot(20, title=f"Top 20 keywords for {job} jobs on indeed.com\nCity: {city}\nnumber of postings={len(pages)*10}")


program(pages)
