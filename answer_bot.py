#answering bot for trivia HQ and Cash Show
import urllib.request as urllib2
import operator
import wikipedia
import os
from google import google
from bs4 import BeautifulSoup

#Sample questions from previous games
sample_questions = {
	'Who are readers asked to find in the "Where\'s Waldo" books?': 
		['Michael Bulbe',
		'Amelia Earhart',
		'Waldo'],
	'Which of these is a US State?':
		['Chihuahua',
		'Saskatchewan' ,
		'Louisiana'],
	'Which of these is a common material used in 3D printers?':
		['Durocarbon filament',
		'Polyabsorbic styrene',
		'Polyactic acid'],
	'Which of these songs does not feature whistling?':
		['Graveyard Whistling',
		'Young Folks',
		'Pumped Up Kicks'],
	'Which NFL great started his pro career with 10 straight losses?':
		['Brett Favre',
		'Dan Marino',
		'Troy Aikman'],
	'Why cant we go to the sun?':
		['hot',
		'cold',
		'far'],
	'Which of these movies is about baseball? ':
		['Kingpin',
		'CaddyShack',
		'Mr Baseball'],
	'Who wrote the poem “O Captain! My Captain!”?':
		['William Shakespeare',
		'Walt Whitman',
		'Sarah Palin'],
	'Wallace & Gromit are movie characters in which style of animation?':
		['Cel animation',
		'Claymation',
		'3D CGI'],
	'Which city has two of the four longest suspension bridges in the US?':
		['San Francisco',
		'New York City',
		'Tacoma'],
	'Which of these describes a board used in logistics and transportation?':
		['Pallet',
		'Palette',
		'Palate'],
	'Who wrote the most #1 hit singles after Paul McCartney and Lennon?':
		['Michael Jackson',
		'Max Martin',
		'Taylor Swift'],
	'Which one of these Japanese alcoholic drinks is made from rice, yams and wear or brown sugar?':
		['Umeshu',
		'Shochu',
		'Chubai'],
	'In a 1961 speech, JFK announced his moon ambitions, but also acknowledged which other strategy?':
		['Navy SEAL training',
		'Dismantling the CIA',
		'Cambodia opium trade']
}

# List of words to clean from the question during google search
remove_words=[
	'who', 'what', 'where', 'when', 'of', 'and', 'that', 'have', 'for','the','why','the',
    'on', 'with', 'as', 'this', 'by', 'from', 'they', 'a', 'an', 'and', 'my','are',
    'in', 'to', '?', ',', 'these', 'is', 'does', 'which', 'his','her','not','we','go'
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

#get page
def get_page(link):
    try:
        if link.find('mailto')!=-1:
            return ''
        req = urllib2.Request(link, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' })
        html = urllib2.urlopen(req).read()
        return html
    except (urllib2.URLError,urllib2.HTTPError,ValueError) as e:
                return ''
'''
#return points from wiki //options is a list, sim_ques is string
def wikipedia_results(sim_ques,options):
	points=[]
	wiki_results=wikipedia.search(sim_ques)
	page=wikipedia.page(wiki_results[0])
	content=page.content
	for o in options:
		points=[content.count(o)]+points
	if 'not' in sim_ques.lower():
		for p in points:
			p=-p
	return points

#return points from google
def google_results(sim_ques,options):
	num_pages=3
	points=[]
	content=""
	search_results=google.search(sim_ques,num_pages)
	for s in search_results:
		content+=s.description
	for o in options:
		points=[content.count(o)]+points
	if 'not' in sim_ques.lower():
		for p in points:
			p=-p
	return points
'''
def split_string(source):
    splitlist= ",!-.;/?@ #"
    output=[]
    atsplit = True 
    for char in source:
        if char in splitlist:
            atsplit=True
        else:
            if atsplit:
                output.append(char)
                atsplit= False
            else:
                output[-1] = output[-1] +char
    return output

def google_wiki(sim_ques,options):
	num_pages=1
	points=list()
	content=""
	for o in options:
		o+=' wiki'
		o=o.lower()
		search_results=google.search(o,num_pages)
		link=search_results[0].link
		content=get_page(link)
		soup = BeautifulSoup(content)
		temp=0
		page=soup.get_text().lower()
		#print(page)
		words=split_string(sim_ques)
		for word in words:
			temp=temp+page.count((" "+word+" "))
			#print(word+str(page.count(word)))
		#print(page.count("the"))
		points.append(temp)
	return points


#return points for each question
def get_points():
	simq=""
	x=0
	for key in sample_questions:
		x=x+1
		points=[]
		simq=simplify_ques(key)
		options=sample_questions[key]
		simq=simq[:-1]
		simq=simq.lower()
		#points+=wikipedia_results(simq,options)
		#points+=google_results(simq,options)
		points=google_wiki(simq,options)
		print(str(x)+". "+key+"\n")
		for point,option in zip(points,options):
			print(option+" { points: "+str(point)+" }\n")

get_points()




