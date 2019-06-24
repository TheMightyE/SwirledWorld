# SwirledWorld

Web app uses Twitter API to search for the entered keywords. Outputs a poem that is arbitrarily generated using the most popular posts of the searched query.

# Dependencies for the Python program

_Twython_<br>
`python -m pip install twython`

_Pandas_<br>
`sudo apt install python-pandas`

_NLTK_<br>
`python -m pip install nltk`

_NLTK stopwords_<br>
`python -m nltk.downloader stopwords`

In the your python code, you must tell your program where the nltk stopwords are located on your server. This is how:<br>
`import nltk`<br>
`nltk.data.path.append("PATH_TO_NLTK_DATA")`<br>

For me the path to nltk data is at `/home/pi/nltk_data`
