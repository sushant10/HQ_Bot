# answering bot for trivia HQ and Cash Show
import json
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import google

# Sample questions from previous games
sample_questions = {}

# List of words to clean from the question during google search
remove_words = []

#load sample questions
def load_json():
	global remove_words, sample_questions
	remove_words = json.loads(open("settings.json").read())["remove_words"]
	sample_questions = json.loads(open("questions.json").read())


# get questions and options
def get_question():
	return questions, answers


# simplify question and remove which,what....etc //question is string
def simplify_ques(question):
	qwords = question.split()
	cleanwords = [word for word in qwords if word.lower() not in remove_words]
	temp = ' '.join(cleanwords)
	clean_question=""
	#remove ?
	for ch in temp:
		if ch!="?":
			clean_question=clean_question+ch
	return clean_question


# get page
def get_page(link):
	try:
		if link.find('mailto') != -1:
			return ''
		req = urllib2.Request(link, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'})
		html = urllib2.urlopen(req).read()
		return html
	except (urllib2.URLError, urllib2.HTTPError, ValueError) as e:
		return ''

def split_string(source):
	splitlist = ",!-.;/?@ #"
	output = []
	atsplit = True
	for char in source:
		if char in splitlist:
			atsplit = True
		else:
			if atsplit:
				output.append(char)
				atsplit = False
			else:
				output[-1] = output[-1] + char
	return output


def google_wiki(sim_ques, options):
	num_pages = 1
	points = list()
	content = ""
	for o in options:
		o = o.lower()
		search_results = google.search(o, num_pages)
		o += ' wiki'
		search_wiki = google.search(o, num_pages)

		link = search_wiki[0].link
		content = get_page(link)
		soup = BeautifulSoup(content)
		page = soup.get_text().lower()

'''
		#search a non wiki page.. searching becoming too slow
		link = search_results[0].link
		content = get_page(link)
		soup= BeautifulSoup(content)
		page= page + soup.get_text().lower()
'''

		# print(page)
		temp=0
		words = split_string(sim_ques)
		for word in words:
			temp = temp + page.count((" " + word + " "))
		# print(word+str(page.count(word)))
		# print(page.count("the"))
		points.append(temp)
	return points


# return points for each question
def get_points():
	simq = ""
	x = 0
	for key in sample_questions:
		x = x + 1
		points = []
		simq = simplify_ques(key)
		options = sample_questions[key]
		simq = simq.lower()
		# points+=wikipedia_results(simq,options)
		# points+=google_results(simq,options)
		points = google_wiki(simq, options)
		print(str(x) + ". " + key + "\n")
		for point, option in zip(points, options):
			print(option + " { points: " + str(point) + " }\n")


if __name__ == "__main__":
	load_json()
	get_points()
