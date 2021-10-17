# rockart-textanalysis
A text analysis program to explore online written content about prehistoric rock art.

Link to presentation: ​https://youtu.be/2zKbLZZodYA 

# Introduction
The aim of this program is to contribute to the understanding of how and why members of a certain online community value prehistoric rock art in Scotland. This program focuses on a specific online community which has an interest in rock art: users of the website ‘The Megalithic Portal’ (TMP). This website has a current total of 277 articles on individual rock art sites in Scotland which are written and contributed to by users. My program extracts the description, image caption and comment data from each of these articles. It then finds the top 20 words used across each text type, visualises these words in a scatter plot, and also performs sentiment analysis, creating polarity and subjectivity fingerprints for each text type and extracting the sentences with the most extreme values. The resulting set of data shows what kind of language and sentiment people are using to talk about rock art in Scotland on this website.

# Program overview
This program is divided into five parts: directory creation, web scraping and parsing, text processing, sentiment analysis and visualisation.

# Directory creation
The user is prompted for inputs to create a new directory for storage of the program outputs. 

The program outputs are: 
- a CSV file containing raw data
- a CSV file containing the top 20 word data
- four TXT files storing the sentences with the most extreme values
- four visualisations each for the polarity and subjectivity fingerprints
- two keys for the fingerprint visualisations
- a scatter plot visualisation of the top 20 word data. 

# Web scraping and parsing
Relevant data is extracted from the website article page's three sections of user-generated content: description, caption and comment.

# Text processing
Extracted text is cleaned and stored in the output CSV file. The top 20 words are found for description, caption and comment. Stopwords are used to bound the analysis.

# Sentiment analysis
A fingerprint visualisation containing the polarity and subjectivity values of each sentence is created. A key to explain the visualisation is also created. Two lists containing either the lowest or highest values sentences are created, with the output of TXT files for the most negative, most positive, most objective and most subjective statements.

# Visualisation
A visualisation program creates a scatter plot showing the frequency counts of the top 20 keywords per text type. The different text types are distinguished through colour coding, and the length of the keywords is also visualised through the size of the dot. This visualisation shows all of the different aspects of the data that was collected in the CSV file: the keyword, its ranking, frequency, length, and text type. All of the data relating to one point can be viewed by hovering over each plotted point on the graph when the graph is viewed in-browser.
