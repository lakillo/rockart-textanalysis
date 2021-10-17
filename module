
# FUNCTIONS

# - - - - - - - - - -

def stripNonAlphaNum(text):
    # Removes all non-alphanumeric characters from given text
    import re
    return re.sub(r'\W+', '', text)

# - - - - - - - - - -

def spaceNonAlphaNum(text):
    # Replaces all non-alphanumeric characters from given text with whitespace
    import re
    return re.sub(r'\W+', ' ', text)

# - - - - - - - - - - 

def locateArticles(URL):
    # Returns the locations of all of the valid articles from the given URL
    from bs4 import BeautifulSoup
    import requests
    import csv
    import re

    # PARSE WEBPAGE
    # Format agent as a browser to allow permission to access page content
    agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # Extract the raw HTML page content 
    page = requests.get(URL, headers=agent)
    # Parse the page content
    soup = BeautifulSoup(page.text, 'lxml')

    # EXTRACT SITE NAME AND URL
    # Find the tag which denotes the start location of the article section
    location = soup.find_all('script')[-1]
    articles_tag = location.next_sibling

    # From the start location, find only URLs which contain 'article' in the link name
    for i in articles_tag.next_siblings:
        articles = soup.find_all('a', attrs={'href': re.compile("^article")})

    return articles

# - - - - - - - - - -

def findStart(options):
    # For use with the extractData function
    # Finds the correct start location for scraping from of a list of options
    from bs4 import BeautifulSoup, Tag

    for i in options:
        if isinstance(i, Tag):
            if i.name == 'br':
                pass
            elif i.name == 'b':
                return True
    else:
        return False

# - - - - - - - - - -

def stripTags(string):
    # Strips all text from a string which is enclosed by the characters < and >
    # Also removes < and >
    inside = 0
    text = ''

    for char in string:
        if char == '<':
            inside = 1
        elif (inside == 1 and char == '>'):
            inside = 0
        elif inside == 1:
            continue
        else:
            text += char

    return text

# - - - - - - - - - -

def extractDes(start_loc):
    # Extract all relevant text from the description section
    # Requires the correct start location to be provided
    from bs4 import BeautifulSoup, NavigableString
    import re

    des = ''
    for i in start_loc.next_siblings:
        if i.name == 'br':
            des = des + ' '
        elif i.name == 'b':
            break
        else:
            text = str(i)
            stripped = stripTags(text)
            no_breaks = (re.sub(r'\s+', ' ', stripped))
            des = des + no_breaks
    des_1 = des.strip()
    if des_1[-1] != '.':
        des_1 = des_1 + '.'
    des_2 = des_1.replace('  ', ' ')

    return des_2

# - - - - - - - - - -

def extractCap(tag):
    # Extract all relevant text from image captions
    # Requires the find_all of the tag containing the captions to be provided
    from bs4 import BeautifulSoup
    import re

    cap = []
    for i in tag:
        if i.text == None:
            pass
        else:
            cap.append(i.text.strip())
    cap_1 = [re.sub(r'\s+', ' ', a) for a in cap]
    cap_2 = [str(d) + '.' for d in cap_1]
    cap_3 = [e.replace('..', '.') for e in cap_2]
    cap_full = ('\n\n'.join([str(c) for c in cap_3])) + '\n\n'
        
    return cap_full

# - - - - - - - - - - 

def extractCom(tag):
    # Extract all relevant text from the comments section
    # Requires the find_all of the tag containing the comments to be provided
    from bs4 import BeautifulSoup, NavigableString, Tag
    import re
    com = ''
    counter = 0
    for i in tag:
        if i.text.__contains__('(Score:'):
            pass
        elif counter % 3 == 0:
            pass
        else:
            raw = i.text.strip()
            if raw == '':
                pass
            else:
                no_breaks = (re.sub(r'\s+', ' ', raw))
                if no_breaks[-1] != '.':
                    no_breaks = no_breaks + '.'
                com = com + no_breaks + '\n\n'
        counter = counter + 1

    return com

# - - - - - - - - - -

def extractData(URL):
    # Return a CSV file containing the site name, URL, region, country, and all textual data from the given article URL
    # Return False for any articles which have an incorrect topic, and are thus irrelevant
    from bs4 import BeautifulSoup
    import requests
    import os
    import re

    # PARSE WEBPAGE
    # Format agent as a browser to allow permission to access page content
    agent = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    # Extract the raw HTML page content 
    page = requests.get(URL, headers=agent)
    # Parse the page content
    soup = BeautifulSoup(page.text, 'lxml')

    # Extract site name, url, region and country and store in variables
    name_tag = soup.find('meta',  property='og:title')
    url_tag = soup.find('meta',  property='og:url')
    region_tag = soup.find('meta',  property='og:region')
    country_tag = soup.find('meta',  property='og:country-name')

    name = (name_tag['content'] if name_tag else 'No meta title given')
    url = (url_tag['content'] if url_tag else 'No meta url given')
    region = (region_tag['content'] if region_tag else 'No meta region given')
    country = (country_tag['content'] if country_tag else 'No meta country given')

    # Confirm that the article topic is correct, otherwise return False and the article will be skipped
    topic = soup.find('a', class_='topic')
    if topic == None:
        return False
    if topic.text == 'Events':
        return False

    # EXTRACT DESCRIPTION
    # The description is not contained within a unique tag and has to be found by its previous sibling (either a toolbar or an image)
    # Find the correct sibling to start scraping from
    toolbar = soup.find('a', href=(re.compile('whatpub')))
    description_image = soup.find('a', class_='image')
    start_options = [toolbar.next_sibling, description_image.next_sibling]

    # Extract the text using the correct start location
    start_loc = findStart(start_options)
    if start_loc == True:
        description = extractDes(description_image)
    else:
        description = extractDes(toolbar)

    # EXTRACT IMAGE CAPTIONS
    # Find the specfic tags which contain the captions
    caption_tag = soup.find_all('font', size='1')[0:-2]
    # Extract the text from the captions
    caption_text = extractCap(caption_tag)

    # EXTRACT COMMENTS
    # Find the specfic tags which contain the comments
    comment_tag = soup.find_all('font', size='2')[6:-2]
    # Extract the text from the comments
    comment_text = extractCom(comment_tag)

    # Store all text in one variable
    all_text = (description + '\n' + caption_text + '\n' + comment_text)

    return name, url, region, country, description, caption_text, comment_text, all_text

# - - - - - - - - - -

def removeStopwords(word_list, stopwords):
    # Remove any stopwords from a given list of words
    return [w for w in word_list if w not in stopwords]

# - - - - - - - - - -

def wordListToFreqDict(word_list):
    # Return a dictionary of word-frequency pairs from a list of words
    wordfreq = [word_list.count(p) for p in word_list]
    return dict(zip(word_list,wordfreq))

# - - - - - - - - - -

def sortFreqDict(freq_dict):
    # Sort a dictionary of word-frequency pairs in order of descending frequency
    aux = [(freq_dict[key], key) for key in freq_dict]
    aux.sort()
    aux.reverse()
    return aux

# - - - - - - - - - -

def Top20(df_cat, csv_writer, text_type):
    # Creates a CSV file containing the top 20 most frequent words, their ranking, keyword, frequency and length
    # Requires a string of text, the correct CSV writer name, and the text type to be provided
    import csv

    # Remove newlines
    text = df_cat.replace('\n', ' ')
    # Create a list to access individual words in the texts
    word_list = text.split()
    #word_list = stripNonAlphaNum(all_text)
    word_list = [stripNonAlphaNum(item) for item in word_list]

    # Remove stopwords from word_list
    sw = open('stopwordlist_plus.txt', 'r')
    stopwords = sw.read()
    # Remove all case formatting from word_list and and remove stopwords
    casefold_list = [item.casefold() for item in word_list]
    casefold_list = removeStopwords(casefold_list, stopwords)
    # Determine frequencies of occurrences for each word
    dictionary = wordListToFreqDict(casefold_list)
    sorted_dict = sortFreqDict(dictionary)

    # Write top 20 results to CSV file
    counter = 0
    for x in range(0,20,1):
        item = sorted_dict[counter]
        ranking = counter + 1
        keyword = item[1]
        frequency = item[0]
        length = len(keyword)
        csv_writer.writerow([ranking, keyword, str(frequency), str(length), text_type])
        counter = counter + 1

# - - - - - - - - - -

def hasNumbers(string):
    # Returns True if any character in a given string is a digit
    # Otherwise returns False
    if any(char.isdigit() for char in string):
        return True
    else:
        return False

# - - - - - - - - - -

def polarityLoHi(text):
    # Returns two lists containing the sentences with the highest and lowest polarity values from a given text
    from textblob import TextBlob
    import re
    
    # Define the sentence objects in the text
    sentences = TextBlob(text).sentences
    # Prepare the empty lists
    polarity_lo = []
    polarity_hi = []

    # Iterate through the sentence objects
    # Append the sentences with the relevant values to the relevant list
    for sentence in sentences:
        if sentence == '.':
            pass
        else:
            pol = TextBlob(str(sentence)).sentiment[0]
            if pol < -0.75:
                polarity_lo.append(str(sentence))
            elif 0.75 < pol <= 1:
                polarity_hi.append(str(sentence))

    # Remove any breaks in the text to format the output neatly
    polarity_lo = [re.sub(r'\s+', ' ', elem) for elem in polarity_lo]
    polarity_hi = [re.sub(r'\s+', ' ', elem) for elem in polarity_hi]

    # Return the two lists
    return polarity_lo, polarity_hi

# - - - - - - - - - -

def subjectivityLoHi(text):
    # Returns two lists containing the sentences with the highest and lowest subjectivity values from a given text
    from textblob import TextBlob
    import re
    
    # Define the sentence objects in the text
    sentences = TextBlob(text).sentences
    # Prepare the empty lists
    subjectivity_lo = []
    subjectivity_hi = []

    # Iterate through the sentence objects
    # Append the sentences with the relevant values to the relevant list
    for sentence in sentences:
        if sentence == '.':
            pass
        else:
            subj = TextBlob(str(sentence)).sentiment[1]
            if subj == 0:
                subjectivity_lo.append(str(sentence))
            elif subj == 1:
                subjectivity_hi.append(str(sentence))

    # Remove any breaks in the text to format the output neatly
    subjectivity_lo = [re.sub(r'\s+', ' ', elem) for elem in subjectivity_lo]
    subjectivity_hi = [re.sub(r'\s+', ' ', elem) for elem in subjectivity_hi]

    # Return the two lists
    return subjectivity_lo, subjectivity_hi

# - - - - - - - - - -

def polarityColour(text):
    from textblob import TextBlob 

    # Define the colours to be used to show the different values
    colours = [(215,48,39),(244,109,67),(253,174,97),(254,224,144),(255,255,191),(224,243,248),(171,217,233),(116,173,209),(69,117,180)]
    # Define the colour to be returned per specific sentiment value
    polarity = TextBlob(text).sentiment[0]
    if polarity < -0.75:
        return colours[0]
    elif polarity < -0.5:
        return colours[1]
    elif polarity < -0.25:
        return colours[2]
    elif polarity < 0:
        return colours[3]
    elif polarity == 0:
        return colours[4]
    elif polarity < 0.25:
        return colours[5]
    elif polarity < 0.5:
        return colours[6]
    elif polarity < 0.75:
        return colours[7]
    elif polarity <= 1:
        return colours[8]

# - - - - - - - - - -

def subjectivityColour(text):
    from textblob import TextBlob 

    # Define the colours to be used to show the different values
    colours = [(53,151,143),(90,180,172),(199,234,229),(245,245,245),(253,224,239),(233,163,201),(197,27,125)]
    # Define the colour to be returned per specific sentiment value
    subjectivity = TextBlob(text).sentiment[1]
    if subjectivity == 0:
        return colours[0]
    elif subjectivity < 0.25:
        return colours[1]
    elif subjectivity < 0.5:
        return colours[2]
    elif subjectivity == 0.5:
        return colours[3]
    elif subjectivity < 0.75:
        return colours[4]
    elif subjectivity < 1:
        return colours[5]
    elif subjectivity == 1:
        return colours[6]

# - - - - - - - - - -

def polarityKey(search_name):
    # Create a key PNG of the colours used to represent values in polarityColour
    from PIL import Image, ImageFont, ImageDraw
    from textblob import TextBlob

    # Prepare image to store colour coded sentiment analysis data
    image = Image.new('RGB', (250, 100), 'black')
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), 'Polarity key')
    # Define the colour values to be used
    colours = [(215,48,39),(244,109,67),(253,174,97),(254,224,144),(255,255,191),(224,243,248),(171,217,233),(116,173,209),(69,117,180)]

    # Draw a rectangle for each colour value and label with the polarity scale
    x = 20
    y = 40
    a = 40
    b = 60
    for colour in colours:
        draw.rectangle([x, y, a, b], fill=colour, outline=None)
        x = x + 20
        a = a + 20
    draw.text((20, 65), 'negative      ->      positive')

    # Save the key as a PNG image
    clean_name = stripNonAlphaNum(search_name)
    image.save(search_name + '/' + clean_name + '_polarity_key.png')

# - - - - - - - - - -

def subjectivityKey(search_name):
    # Create a key PNG of the colours used to represent values in polarityColour
    from PIL import Image, ImageFont, ImageDraw
    from textblob import TextBlob

    # Prepare image to store colour coded sentiment analysis data
    image = Image.new('RGB', (250, 100), 'black')
    draw = ImageDraw.Draw(image)
    draw.text((20, 20), 'Subjectivity key')
    # Define the colour values to be used
    colours = [(53,151,143),(90,180,172),(199,234,229),(245,245,245),(253,224,239),(233,163,201),(197,27,125)]

    # Draw a rectangle for each colour value and label with the subjectivity scale
    x = 20
    y = 40
    a = 40
    b = 60
    for colour in colours:
        draw.rectangle([x, y, a, b], fill=colour, outline=None)
        x = x + 20
        a = a + 20
    draw.text((20, 65), 'objective -> subjective')

    # Save the key as a PNG image
    clean_name = stripNonAlphaNum(search_name)
    image.save(search_name + '/' + clean_name + '_subjectivity_key.png')

# - - - - - - - - - -

def polarityPrint(df_cat, search_name, text_type):
    # Create a visualisation of the polarity values per sentence in a given text
    from PIL import Image, ImageFont, ImageDraw
    from textblob import TextBlob

    # Define the colour values to be used
    colours = [(215,48,39),(244,109,67),(253,174,97),(254,224,144),(255,255,191),(224,243,248),(171,217,233),(116,173,209),(69,117,180)]
    # Create a list of sentence objects from the text
    sentences = TextBlob(df_cat).sentences
    # Prepare image to store the analysis data
    image = Image.new('RGB', (1000, 1700), 'black')
    draw = ImageDraw.Draw(image)

    # Create an image showing each sentence colour coded by polarity value, plus the resulting totals of each value
    x = 40
    y = 40
    a = 60
    b = 60
    limit = 900
    count_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Draw a coloured rectangle for each sentence, colour coded by polarity value
    for sentence in sentences:
        polarity_colour = polarityColour(str(sentence))
        # Count the frequencies of each value assignment
        if polarity_colour == colours[0]:
            count_list[0] = count_list[0] + 1
        elif polarity_colour == colours[1]:
            count_list[1] = count_list[1] + 1
        elif polarity_colour == colours[2]:
            count_list[2] = count_list[2] + 1
        elif polarity_colour == colours[3]:
            count_list[3] = count_list[3] + 1
        elif polarity_colour == colours[4]:
            count_list[4] = count_list[4] + 1
        elif polarity_colour == colours[5]:
            count_list[5] = count_list[5] + 1
        elif polarity_colour == colours[6]:
            count_list[6] = count_list[6] + 1
        elif polarity_colour == colours[7]:
            count_list[7] = count_list[7] + 1
        elif polarity_colour == colours[8]:
            count_list[8] = count_list[8] + 1
        draw.rectangle([x, y, a, b], fill=polarity_colour, outline=None)
        x = x + 20
        a = a + 20
        if x == limit:
            x = 40
            y = y + 20
            a = 60
            b = b + 20
    # Draw a rectangle for each polarity value at the bottom of the image, plus its frequency total
    p = 0
    x = 40
    y = 1600
    a = 60
    b = 1620
    font = ImageFont.truetype('tunga.ttf', 30)
    for count in count_list:
        draw.rectangle([x, y, a, b], fill=colours[p], outline=None)
        draw.text((a + 10, b - 30), str(count_list[p]), font=font)
        x = x + 100
        a = a + 100
        p = p + 1

    # Save everything as a PNG image
    clean_name = stripNonAlphaNum(search_name)
    image.save(search_name + '/' + clean_name + text_type + '_polarity_fingerprint.png')
    #image.save(search_name + '/' + clean_name + text_type + '_polarity_fingerprint_minus_cochno.png')

# - - - - - - - - - -

def subjectivityPrint(df_cat, search_name, text_type):
    # Create a visualisation of the subjectivity values per sentence in a given text
    from PIL import Image, ImageFont, ImageDraw
    from textblob import TextBlob

    # Define the colour values to be used
    colours = [(53,151,143),(90,180,172),(199,234,229),(245,245,245),(253,224,239),(233,163,201),(197,27,125)]
    # Create a list of sentence objects from the text
    sentences = TextBlob(df_cat).sentences
    # Prepare image to store the analysis data
    image = Image.new('RGB', (1000, 1700), 'black')
    draw = ImageDraw.Draw(image)

    # Create an image showing each sentence colour coded by polarity value, plus the resulting totals of each value
    x = 40
    y = 40
    a = 60
    b = 60
    limit = 900
    count_list = [0, 0, 0, 0, 0, 0, 0]
    # Draw a coloured rectangle for each sentence, colour coded by polarity value
    for sentence in sentences:
        subjectivity_colour = subjectivityColour(str(sentence))
        # Count the frequencies of each value assignment
        if subjectivity_colour == colours[0]:
            count_list[0] = count_list[0] + 1
        elif subjectivity_colour == colours[1]:
            count_list[1] = count_list[1] + 1
        elif subjectivity_colour == colours[2]:
            count_list[2] = count_list[2] + 1
        elif subjectivity_colour == colours[3]:
            count_list[3] = count_list[3] + 1
        elif subjectivity_colour == colours[4]:
            count_list[4] = count_list[4] + 1
        elif subjectivity_colour == colours[5]:
            count_list[5] = count_list[5] + 1
        elif subjectivity_colour == colours[6]:
            count_list[6] = count_list[6] + 1
        draw.rectangle([x, y, a, b], fill=subjectivity_colour, outline=None)
        x = x + 20
        a = a + 20
        if x == limit:
            x = 40
            y = y + 20
            a = 60
            b = b + 20
    # Draw a rectangle for each polarity value at the bottom of the image, plus its frequency total
    p = 0
    x = 40
    y = 1600
    a = 60
    b = 1620
    font = ImageFont.truetype('tunga.ttf', 30)
    for count in count_list:
        draw.rectangle([x, y, a, b], fill=colours[p], outline=None)
        draw.text((a + 10, b - 30), str(count_list[p]), font=font)
        x = x + 100
        a = a + 100
        p = p + 1
        
    # Save everything as a PNG image
    clean_name = stripNonAlphaNum(search_name)
    image.save(search_name + '/' + clean_name + text_type + '_subjectivity_fingerprint.png')
    #image.save(search_name + '/' + clean_name + text_type + '_subjectivity_fingerprint_minus_cochno.png')

# - - - - - - - - - -

