# answering bot for trivia HQ and Cash Show
import json
import urllib.request as urllib2
from bs4 import BeautifulSoup
from google import google
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import pyscreenshot as grab

# Sample questions from previous games
sample_questions = {}

# List of words to clean from the question during google search
remove_words = []

# load sample questions
def load_json():
	global remove_words, sample_questions
	remove_words = json.loads(open("Data/settings.json").read())["remove_words"]
	sample_questions = json.loads(open("Data/questions.json").read())

# take screenshot of Show
def screen_grab(loc):
	return None

# construct the argument parse and parse the arguments // pytesseract
def parse_OCR():
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
	args = vars(ap.parse_args())

# get questions and options
def read_screen():
	ap = argparse.ArgumentParser(description='HQ_Bot')
	ap.add_argument("-i", "--image", required=True,help="path to input image to be OCR'd")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
	args = vars(ap.parse_args())

	# load the example image and convert it to grayscale
	image = cv2.imread(args["image"])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# check to see if we should apply thresholding to preprocess the
	# image
	if args["preprocess"] == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	# make a check to see if median blurring should be done to remove
	# noise
	elif args["preprocess"] == "blur":
		gray = cv2.medianBlur(gray, 3)

	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)
	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	print(text)
 
	# show the output images
	cv2.imshow("Image", image)
	cv2.imshow("Output", gray)
	cv2.waitKey(0)

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

		#Too slow to check another page
		'''
		#search a non wiki page.. searching becoming too slow
		link = search_results[0].link
		content = get_page(link)
		soup= BeautifulSoup(content)
		page= page + soup.get_text().lower()
		'''
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
	#load_json()
	#get_points()
	read_screen()