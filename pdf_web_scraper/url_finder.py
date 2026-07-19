import requests
from bs4 import BeautifulSoup

# Fetch and parse the page
#r = requests.get = 'https://www.cde.ca.gov'
response = requests.get('https://www.cde.ca.gov/SchoolDirectory/details?cdscode=01100170136101')
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)
# Find the main content container
content_div = soup.find('href', class_='td')
print(content_div)