from bs4 import BeautifulSoup
import requests

def getSolution(ques, sol):
	r = session.get(sol).content
	soup = BeautifulSoup(r, 'html.parser')
	code = soup.find('pre', class_ = "linenums").get_text()
	return code

def findCorrectSolution(ques):
	r = session.get(r"https://cses.fi/problemset/view/"+ques+"/").content
	soup = BeautifulSoup(r,'html.parser')
	if int(soup.find('p').string.split()[-1]) == 0: # No of submissions
		return None

	for link in soup.find_all('a', attrs = {'class':'details-link'}):
		sol = link['href']
		res = soup.find('a', href = sol, class_ ='').span['class'][2] #get status of a solution
		if res == 'full':
			return 'https://cses.fi'+sol
	return None

def createSession(username, password):
	loginData = {
		'nick': username,
		'pass': password
	}
	with requests.Session() as s:
		url = 'https://cses.fi/login'
		soup = BeautifulSoup(s.get(url).content, 'html.parser')
		loginData['csrf_token'] = soup.find('input', attrs = {'name':'csrf_token'})['value']
		r = s.post(url, data = loginData)
		return s
		
def getQuestions():
	ques = dict()
	r = session.get(r'https://cses.fi/problemset/').content
	soup = BeautifulSoup(r, 'html.parser')
	for t in soup.find_all('li', class_ = 'task'):
		quesID = t.a['href'].split('/')[-1]
		ques[quesID] =  t.a.string
	return ques

if __name__ == "__main__":
	r = requests.get("https://cses.fi/problemset/").content
	soup = BeautifulSoup(r,'html.parser')
	username = ''
	password = ''
	session = createSession(username, password)
	questions = getQuestions()
	for _ in questions:
		sol = findCorrectSolution(_);
		if not sol:
			continue
		code = getSolution(_, sol)
		ext = '.cpp'
		path = 'cses/' + _ + ' - ' + questions[_] + ext
		file = open(path, 'w')
		file.writelines(code.split('\n'))
		file.close()
