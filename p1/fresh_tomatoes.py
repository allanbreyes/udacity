import webbrowser
import os
import re
import csv

def read_template(template):
    """ returns html string from `templates/_<template>.html` """
    return ''.join([row for row in open('templates/_{}.html'.format(template),
                                        'r').readlines()])

# styles and scripting for the page
main_page_head = read_template('head')

# the main page layout and title bar
main_page_content = read_template('content')

# a single movie entry html template
movie_tile_content = read_template('movie')

def create_movie_tiles_content(movies):
    """ generates movie tile html content for a list of Movie objects """
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_image_url,
            trailer_youtube_id=trailer_youtube_id,
            year=movie.year
        )
    return content

def open_movies_page(movies, filename='fresh_tomatoes.html'):
    """ creates output movie html and opens it in browser """
    # Create or overwrite the output file
    output_file = open(filename, 'w')

    # Replace the placeholder for the movie tiles with the actual dynamically generated content
    rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2) # open in a new tab, if possible

class Movie(object):
    """ represents a movie """
    def __init__(self, title, image_url, youtube_url, year):
        self.title = title
        self.poster_image_url = image_url
        self.trailer_youtube_url = youtube_url
        self.year = year

    def __str__(self):
        return self.title

def get_movies(filename):
    """ pulls movie data from csv and returns a list a Movie objects """
    movies = []
    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for movie in reader:
            movies.append(Movie(title=movie['name'],
                                image_url=movie['image_url'],
                                youtube_url=movie['youtube_url'],
                                year=movie['year']))
    return movies

def main():
    """ main subroutine """
    movies = get_movies('data/fresh_tomatoes.csv')
    open_movies_page(movies, 'fresh_tomatoes.html')

if __name__ == '__main__':
    main()
