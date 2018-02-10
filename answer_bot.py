#answering bot for trivia
import urllib2
import operator
import json
import wikipedia

def get_question():
	return questions, answers

def get_page(link):
    try:
        
        if link.find('mailto')!=-1:
            return ''
        req = urllib2.Request(link, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError,urllib2.HTTPError,ValueError) as e:
                return ''

#return points from google
def google_results(sim_ques,option):

#return points from wiki
def wikipedia_results(sim_ques,option):

#return points for each question
def get_points():




