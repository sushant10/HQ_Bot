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
import pyscreenshot as Imagegrab

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Sample questions from previous games
sample_questions = {}

# List of words to clean from the question during google search
remove_words = []

# load sample questions
def load_json():
	global remove_words, sample_questions
	remove_words = json.loads(open("Data/settings.json").read())["remove_words"]
	sample_questions = json.loads(open("Data/questions.json").read())

# take screenshot of question 
def screen_grab(to_save):
	# 31,228 485,620 co-ords of screenshot// left side of screen
	im = Imagegrab.grab(bbox=(31,228,485,620))
	im.save(to_save)

# get OCR text //questions and options
def read_screen():
	screenshot_file="Screens/to_ocr.png"
	screen_grab(screenshot_file)
	ap = argparse.ArgumentParser(description='HQ_Bot')
	ap.add_argument("-i", "--image", required=False,default=screenshot_file,help="path to input image to be OCR'd")
	ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
	args = vars(ap.parse_args())

	# load the image 
	image = cv2.imread(args["image"])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	if args["preprocess"] == "thresh":
		gray = cv2.threshold(gray, 0, 255,
			cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	elif args["preprocess"] == "blur":
		gray = cv2.medianBlur(gray, 3)

	# store grayscale image as a temp file to apply OCR
	filename = "Screens/{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)
	# load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)
	os.remove(screenshot_file)
	#print(text)
	# show the output images
	'''cv2.imshow("Image", image)
	cv2.imshow("Output", gray)
	os.remove(screenshot_file)
	if cv2.waitKey(0):
		cv2.destroyAllWindows()
	'''
	return text

# get questions and options from OCR text
def parse_question():
	text = read_screen()
	lines = text.splitlines()
	question = ""
	options = list()
	flag=False

	for line in lines :
		if not flag :
			question=question+" "+line
		
		if '?' in line :
			flag=True
			continue
		
		if flag :
			if line != '' :
				options.append(line)
			
	return question, options


# simplify question and remove which,what....etc //question is string
def simplify_ques(question):
	qwords = question.split()
	cleanwords = [word for word in qwords if word.lower() not in remove_words]
	temp = ' '.join(cleanwords)
	clean_question=""
	#remove ?
	for ch in temp: 
		if ch!="?" or ch!="\"" or ch!="\'":
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
	words = split_string(sim_ques)
	for o in options:
		o = o.lower()
		#search_results = google.search(o, num_pages)
		o += ' wiki'
		search_wiki = google.search(o, num_pages)

		link = search_wiki[0].link
		content = get_page(link)
		soup = BeautifulSoup(content,"lxml")
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
		for word in words:
			temp = temp + page.count(word)
		# print(word+str(page.count(word)))
		# print(page.count("the"))
		points.append(temp)
	return points


# return points for sample_questions
def get_points_sample():
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

def get_points_live():
	question,options=parse_question()
	simq = ""
	points = []
	simq = simplify_ques(question)
	simq = simq.lower()
	# points+=wikipedia_results(simq,options)
	# points+=google_results(simq,options)
	points = google_wiki(simq, options)
	print(question + "\n")
	for point, option in zip(points, options):
		print(option + " { points: " + str(point) + " }\n")

if __name__ == "__main__":
	load_json()
	#get_points_sample()
	while(1):
		keypressed = input('Press s to screenshot or q to quit:\n')
		if keypressed == 's':
			get_points_live()
		elif keypressed == 'q':
			break
		else:
			print("Unknown input")
	

