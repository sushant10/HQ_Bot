#answering bot for trivia HQ and Cash Show
import urllib.request as urllib2
import operator
import json
import wikipedia
import os
from google import google


#Sample questions from previous games
sample_questions = {
	'Who are readers asked to find in the "Where\'s Waldo" books?': 
		['Michael Bulbe',
		'Amelia Earhart',
		'Waldo']
	'Which of these is a US State?':
		['Chihuahua'
		'Saskatchewan' 
		'Louisiana']
	'Which of these is a common material used in 3D printers?':
		['Durocarbon filament',
		'Polyabsorbic styrene',
		'Polyactic acid']
	'Which of these songs does not feature whistling?':
		['Graveyard Whistling',
		'Young Folks',
		'Pumped Up Kicks']
	'Which NFL great started his pro career with 10 straight losses?':
		['Brett Favre',
		'Dan Marino',
		'Troy Aikman']
}

# List of words to clean from the question during google search
remove_words=[
	'who', 'what', 'where', 'when', 'of', 'and', 'that', 'have', 'for',
    'on', 'with', 'as', 'this', 'by', 'from', 'they', 'a', 'an', 'and', 'my',
    'in', 'to', '?', ',', 'these', 'is', 'does'
]

#get questions and options
def get_question():
	return questions, answers

#simplify question and remove which,what....etc //question is string
def simplify_ques(question):
	qwords = question.split()
	cleanwords  = [word for word in qwords if word.lower() not in remove_words]
	clean_question = ' '.join(cleanwords)
	return clean_question

#get page(probably not needed)
def get_page(link):
    try:
        if link.find('mailto')!=-1:
            return ''
        req = urllib2.Request(link, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError,urllib2.HTTPError,ValueError) as e:
                return ''

#return points from wiki //options is a list, sim_ques is string
def wikipedia_results(sim_ques,options):
	points=[]
	wiki_results=wikipedia.search(sim_ques)
	page=wikipedia.page(wiki_results[0])
	content=page.content()
	for o in options:
		points=content.count(o)+points
	if 'not' in sim_ques.lower():
		for p in points:
			p=-p
	return points

#return points from google
def google_results(sim_ques,options):
	num_pages=1
	points=[]
	content=""
	search_results=google.search(sim_ques,num_pages)
	for s in search_results:
		content+=s.description
	for o in options:
		points=content.count(o)+points
	if 'not' in sim_ques.lower():
		for p in points:
			p=-p
	return points

#return points for each question
def get_points():




