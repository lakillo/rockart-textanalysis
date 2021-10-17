
# A PROGRAM TO ANALYSE THE LANGUAGE USED 
# TO TALK ABOUT PREHISTORIC ROCK ART IN SCOTLAND 
# ONLINE AT THE MEGALITHIC PORTAL

# - - - - - - - - - -

from PIL import Image, ImageFont, ImageDraw
from textblob import TextBlob
from finalModule import *
import pandas as pd
import caffeine
import time
import sys
import csv
import re
import os

# - - - - - - - - - -

# CREATE NEW DIRECTORY TO STORE ALL SEARCH RESULTS

print('')
# Loop which allows the user to create a new directory or use an existing one
while True:
	print('Create new search directory.')
	# Ask the user to specify the name for the new directory
	search_name = input('Enter name for this search: ')
	# If it doesn't already exist, create the new directory and break loop
	if not os.path.exists(search_name):
		os.makedirs(search_name)
		print('Directory created.')
		break
	else:
		# If the directory already exists, ask the user to confirm use (break loop) or decline (restart loop)
		if input('Directory already exists, use this directory? [y/n] \n * Warning: this may overwrite existing files: ') == 'y':
			print('Using existing directory.')
			break
print('')

# Create non-alphanumeric version of the search name for use in filenames
clean_name = stripNonAlphaNum(search_name)

# - - - - - - - - - -

# EXTRACT RAW DATA FROM EACH ARTICLE LISTED ON A SEARCH INDEX PAGE AND WRITE TO CSV

# Prepare a CSV file to store raw data from each article
filename_raw = search_name + '/' + clean_name + '_raw_data'
f_raw = csv.writer(open(filename_raw + '.csv','w'))
f_raw.writerow(['Site name', 'URL', 'Region', 'Country', 'Description text', 'Caption text', 'Comment text', 'All text'])

# Loop which allows the user to extract data from multiple search index pages
while True:
	# Ask user to input the search index page URL
	if input('Get article data from search index page? [y/n]: ') == 'y':
		index_page_url = input('Enter search index page URL: ')
		print('Getting article data...')
		# Find individual article URLs in search index page
		articles = locateArticles(index_page_url)
		for i in articles:
			elem = i.next_element
			if elem.name == ('b'):
				# Extract individual article URL
				url = i.get('href')
				url = 'https://www.megalithic.co.uk/' + url
				time.sleep(3)
				# Extract raw data from article
				data_tuple = extractData(url)
				# Only continue with articles which have the correct topic class
				if data_tuple != False:
					#Write all raw data to CSV file
					f_raw.writerow(data_tuple)
					# Throttle requests to the server with a delay of 3 seconds
					time.sleep(3)
		print('Article data stored.')
		print('')
	else:
		break

# - - - - - - - - - -

# Loop which allows the user to proceed analysis of the raw data, or close the program
while True:
	if input('Proceed with data analysis? [y/n]: ') == 'y':
		print('Data analysis in progress...')
		break
	else:
		print('Data analysis cancelled.')
		sys.exit()

# - - - - - - - - - -

# FIND THE TOP 20 MOST FREQUENT WORDS USED IN ALL TEXT, 
# THE DESCRIPTION, THE IMAGE CAPTIONS, AND THE COMMENTS

# Prepare a CSV file to store the top 20 words, their frequency and length, and their text type (eg: description, comment)
filename_t20 = search_name + '/' + clean_name + '_top_20_words'
f_t20 = csv.writer(open(filename_t20 + '.csv','w'))
f_t20.writerow(['Ranking', 'Keyword', 'Frequency', 'Length', 'Text type'])

# Read all data from each text type stored in the raw data CSV
raw_csv = (filename_raw + '.csv')
df = pd.read_csv(raw_csv, usecols=['Description text', 'Caption text', 'Comment text', 'All text'])

# Combine all rows of 'All text' column into one string
all_col = df['All text']
all_cat = (all_col.str.cat(sep=' '))
# Combine all rows of 'Description text' column into one string
des_col = df['Description text']
des_cat = (des_col.str.cat(sep=' '))
# Combine all rows of 'Caption text' column into one string
cap_col = df['Caption text']
cap_cat = (cap_col.str.cat(sep=' '))
# Combine all rows of 'Comment text' column into one string
com_col = df['Comment text']
com_cat = (com_col.str.cat(sep=' '))

# Extract the top 20 words for each different text type and write all results to one CSV file
Top20(all_cat, f_t20, 'all text')
Top20(des_cat, f_t20, 'description')
Top20(cap_cat, f_t20, 'caption')
Top20(com_cat, f_t20, 'comment')
# Confirm that the data has been extracted
print('Top 20 words extracted.')

# - - - - - - - - - -

# FIND THE POLARITY FINGERPRINT OF THE TEXTUAL DATA

# Create a key image to show how the colour scale relates to polarity values 
polarityKey(search_name)

# Create a polarity fingerprint visualisation for each text type
polarityPrint(all_cat, search_name, '_all_text')
polarityPrint(des_cat, search_name, '_des')
polarityPrint(cap_cat, search_name, '_cap')
polarityPrint(com_cat, search_name, '_com')
# Confirm that the visualisation has been created
print('Polarity fingerprint created.')

# - - - - - - - - - -

# FIND THE SUBJECTIVITY FINGERPRINT OF THE TEXTUAL DATA

# Create a key image to show how the colour scale relates to subjectivity values 
subjectivityKey(search_name)

# Create a subjectivity fingerprint visualisation for each text type
subjectivityPrint(all_cat, search_name, '_all_text')
subjectivityPrint(des_cat, search_name, '_des')
subjectivityPrint(cap_cat, search_name, '_cap')
subjectivityPrint(com_cat, search_name, '_com')
# Confirm that the visualisation has been created
print('Subjectivity fingerprint created.')
print('')

# - - - - - - - - - -

# FIND THE SENTENCES WITH THE HIGHEST AND LOWEST VALUES 
# FOR POLARITY AND SUBJECTIVITY

# Prepare TXT files to store the results
filename_neg = search_name + '/' + clean_name + '_most_neg'
f_neg = open(filename_neg + '.txt','w')
filename_pos = search_name + '/' + clean_name + '_most_pos'
f_pos = open(filename_pos + '.txt','w')
filename_obj = search_name + '/' + clean_name + '_most_obj'
f_obj = open(filename_obj + '.txt','w')
filename_sub = search_name + '/' + clean_name + '_most_sub'
f_sub = open(filename_sub + '.txt','w')

# Find the sentences with the highest and lowest polarity values
p_result = polarityLoHi(str(all_cat))
# Find the sentences with the highest and lowest subjectivity values
s_result = subjectivityLoHi(str(all_cat))

# Write the results to the TXT files
[f_neg.write((str(elem)) + '\n\n') for elem in p_result[0]]
[f_pos.write((str(elem)) + '\n\n') for elem in p_result[1]]
[f_obj.write((str(elem)) + '\n\n') for elem in s_result[0]]
[f_sub.write((str(elem)) + '\n\n') for elem in s_result[1]]

# Close the TXT files
f_neg.close()
f_pos.close()
f_obj.close()
f_sub.close()

print('Highest and lowest sentiment value sentences extracted.')
print('')

# - - - - - - - - - -

# CREATE A VISUALISATION OF THE TOP 20 WORDS DATA

# Prompt the user to run the separate visualisation program (doesn't run properly otherwise)
print('* Run visualisation program to complete analysis.')
print('')

# - - - - - - - - - -

