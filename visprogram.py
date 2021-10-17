from finalModule import stripNonAlphaNum
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# - - - - - - - - - -

# CREATE A VISUALISATION OF THE TOP 20 WORDS DATA

print('')
# Ask user to re-enter the search name so the program can read from the right directory
search_name = input('Re-enter search name to read from directory: ')
# Define the filename info the program needs to find the raw data
clean_name = stripNonAlphaNum(search_name)
#filename_t20 = search_name + '/' + clean_name + '_top_20_words'
filename_t20 = search_name + '/' + clean_name + '_top_20_words_minus_cochno'

# Create a pandas dataframe from the top 20 words CSV file 
df = pd.read_csv(filename_t20 + '.csv')
# Create a scatter plot using plotly express and the pandas dataframe
#fig = px.scatter(df, x='Ranking', y='Frequency', size='Length', color='Text type', hover_data=['Keyword'], text='Keyword', labels={'x':'Keyword ranking', 'y':'Keyword frequency'}, title='Top 20 most frequent words used to describe prehistoric rock art in Scotland on The Megalithic Portal')
fig = px.scatter(df, x='Ranking', y='Frequency', size='Length', color='Text type', hover_data=['Keyword'], text='Keyword', labels={'x':'Keyword ranking', 'y':'Keyword frequency'}, title='Top 20 most frequent words used to describe prehistoric rock art in Scotland on The Megalithic Portal (minus data for The Cochno Stone)')
# Confirm that the visualisation has been created
print('Top 20 words visualisation created.')
print('')
# Open visualisation in browser
fig.show()
