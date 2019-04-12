from lxml import html, etree
import datetime
import requests
import re
import os
import sys
import unicodecsv as csv
import argparse
import json
# from exceptions import ValueError

def parse(location, showdate):
	print("Fetching Locations..")
	searchedLocation = location
	searchedDate = showdate
	movie_listings = []

	# Cookies for searching theater location
	cookie = {
		'akamai_generated_location': '{"zip":"""","city":"CLIFTON","state":"NJ","county":"PASSAIC","areacode":"""","lat":"40.8800","long":"-74.1446","countrycode":""""}'
	}
	# Headers to get location details from their auto complete query
	location_headers = {
		'referer': 'https://www.fandango.com/',
		'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
		'x-requested-with': 'XMLHttpRequest'
	}
	# Location autocomplete API endpoint
	location_url = 'https://www.fandango.com/napi/home/autocompleteDesktopSearch/' + searchedLocation
	data = {
		'zipCode': '',
		'city': '',
		'state': '',
		'date': str(searchedDate),
		'page': 1,
		'favTheaterOnly': False,
		'limit': 30,
		'offset': 0,
		'isdesktop': True
	}
	# Retrieving available locations
	location_response = requests.get(location_url, cookies=cookie, headers=location_headers).json()
	locations = location_response.get('resultsByType',{}).get('locations',{}).get('items',{})

	if locations:
		# Selecting first location from available locations
		searched_location = locations[0]
		searched_location_url = searched_location.get('link')
		location_name = searched_location.get('name')
		state = searched_location.get('state')
		# Getting city from location name, city is necessary to get theater lists if you are passing location as input
		city = location_name.split(',')[0].strip() if ',' in location_name else None

		if city and state:
			data['city'] = city
			data['state'] = state
		else:
			# city,state is not necessary if you are passing zipcode as input
			data['zipCode'] = location_name

		# Headers for getting theater listing for the searched location
		theater_headers = {
			'accept': '*/*',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9,ml;q=0.8',
			'referer': searched_location_url,
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
			'x-requested-with': 'XMLHttpRequest'
		}
		movie_url = 'https://www.fandango.com/napi/theaterswithshowtimes'

		# Fetching Movie details for search location
		print("Fetching movie details")
		try:
			movie_response = requests.get(movie_url, params=data, headers=location_headers).json()
		except:
			print("Failed to get movie details")

		all_theaters = movie_response.get('theaters')
		if all_theaters:
			# Iterating through each each theater
			for theater in all_theaters:
				theater_name = theater.get('name')
				address = theater.get('address1')
				city = theater.get('city')
				state = theater.get('state')
				zipcode = theater.get('zip')
				theater_address = address + ' ' + city + ' ' + state + ' ' + zipcode
				all_movies = theater.get('movies')
				# Iterating through each movie in a thaater
				if all_movies:
					for movie in all_movies:
						# cleaning data
						movie_name = movie.get('title').strip()
						duration = str(movie.get('runtime'))
						genre = ','.join(' '.join(movie.get('genres')).split()).strip()
						movie_rating = movie.get('rating')
						star_rating = str(movie['stars']['totalRating']
										  ['stars']['points']).strip()

						movie_data = {
							"Theatre_Name": theater_name,
							"Theatre_Address": theater_address,
							"Movie_Name": movie_name,
							"Show_Date": searchedDate,
							"Movie_Rating": movie_rating,
							"Star_Rating": star_rating,
							"Duration": duration,
							"Genre": genre,
							"Location_or_Zipcode": searchedLocation
						}
						movie_listings.append(movie_data)
				else:
					print("No movies in %s"%(theater_name))

			return movie_listings

		else:
			print("No theaters found")
	else:
		print("No location found")

if __name__ == "__main__":

	''' eg-:python fandango.py 20001 2017-12-31 '''

	argparser = argparse.ArgumentParser()
	argparser.add_argument('location', help='theater location (zipcode or city+state)', type=str)
	argparser.add_argument('showdate', help='movie show time', type=str)
	args = argparser.parse_args()
	location = args.location
	showdate = args.showdate
	validdate = False

	try:
		datetime.datetime.strptime(showdate, '%Y-%m-%d')
		validdate =True

	except ValueError:
		print("Invalid showdate, showdate should be YYYY-MM-DD format")

	if validdate:
		searchdate = datetime.datetime.strptime(showdate, '%Y-%m-%d').date()
		today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
		datenow = datetime.datetime.strptime(today,'%Y-%m-%d').date()

		if searchdate >= datenow:
			scraped_data = parse(location, showdate)

			if scraped_data:
				print("Writing data to output file")
				with open('%s-%s-movie-results.csv' % (location, showdate), 'wb')as csvfile:
					fieldnames = ['Theatre_Name', 'Theatre_Address', 'Movie_Name',
								  'Show_Date', 'Location_or_Zipcode', 'Duration', 'Genre', 'Movie_Rating', 'Star_Rating']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
					writer.writeheader()
					for data in scraped_data:
						writer.writerow(data)
			else:
				print("Your search for %s, in %s does not match any movies" % (location, showdate))
		else:
			print("Entered date is already passed")