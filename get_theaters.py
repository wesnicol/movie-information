# import libraries
import requests
from bs4 import BeautifulSoup
import sys
import datetime

#URL of the webpage being scraped (printer friendly version in this case)


# the url is built by accepting the date in format mm-dd-yyyy
# and the location as a 5 digit zip code

def get_theaters():


	def build_url_austin(date):
		return ('https://www.fandango.com/theaterlistings-prn.aspx?location=austin%2C%20tx&pn=1&sdate=' + date + '&tid=AAUQP,AATHS,AAYBF,AANCC,AANOT,AAWJB,AAPOB,AAPFV,AAYEI,AAQCN')
		
		


	now = datetime.datetime.now()
	date = now.strftime("%m-%d-%Y")
	# date = sys.argv[1] # date is the first argument with the called script


	print('getting urls...')

	# query the website and return the html
	response_austin = requests.get(build_url_austin(date))


	print('done getting urls')
	print('')


	html_austin = response_austin.content

	# parse the html using beautiful soup and store in variable `soup`
	soup_austin = BeautifulSoup(html_austin, )

	theaters_austin = soup_austin.find_all('h4')
	
	theater_list = []
	for tag in theaters_austin:
		
		theater_name = (tag.text.strip())
		theater_list.append(theater_name)
		
		
	return theater_list

'''
	i = 0
	while(i < len(theaters_austin)):
		print(theaters_austin[i].text)
		i = i+1
	print('')
'''







'''****************************** SAN MARCOS *************************************************'''

'''
def build_url_sm(date):
	return ('https://www.fandango.com/theaterlistings-prn.aspx?location=san%20marcos%2C%20tx&pn=1&sdate=' + date + '&tid=AAYBE,AAOCK,AAXKM,AAWOG,AAKBQ,AAXNY')
	
	
print('getting urls...')

response_sm = requests.get(build_url_sm(date))

print('done getting urls')
print('')


html_sm = response_sm.content

soup_sm = BeautifulSoup(html_sm)

theaters_sm = soup_sm.find_all('h4')

i = 0
while(i < len(theaters_sm)):
	print(theaters_sm[i].text)
	i = i+1
print('')

'''


'''*********************************** SAN ANTONIO **************************************************'''
'''
def build_url_sa(date):
	return ('https://www.fandango.com/theaterlistings-prn.aspx?location=san%20antonio%2C%20tx&pn=1&sdate=' + date + '&tid=AAYBE,AAOCK,AAXKM,AAWOG,AAKBQ,AAXNY')
	
	
print('getting urls...')

response_sa = requests.get(build_url_sa(date))

print('done getting urls')
print('')


html_sa = response_sa.content

soup_sa = BeautifulSoup(html_sa)

theaters_sa = soup_sa.find_all('h4')


i = 0
while(i < len(theaters_sa)):
	print(theaters_sa[i].text)
	i = i+1
print('')


'''









