#answering bot for trivia HQ and Cash Show
import urllib2
import operator
import json
import wikipedia


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




