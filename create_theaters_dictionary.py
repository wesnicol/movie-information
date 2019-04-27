


from get_theaters import *

theaters_movies = {}

theater_list = get_theaters()

for theaters in theater_list:

    # the next thing you need to do is instead of manually assigning movies
	# assign a list of movies that is returned by another script (much like get_theaters)
	
	theaters_movies[theaters] = ['movie1',
								 'movie2',
								 'movie3',
								 'movie4',
								]
								
								
							


print (theaters_movies)