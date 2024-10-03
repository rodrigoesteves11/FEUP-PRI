from lxml import html
import requests

# Define the URL of the website to scrape
url = 'https://species.wikimedia.org/w/index.php?title=Special:AllPages&from=A+History+of+British+Ferns'

# Send an HTTP request to the website and retrieve the HTML content
response = requests.get(url)


# Parse the HTML content using lxml
tree = html.fromstring(response.content)

# Extract specific elements from the HTML tree using XPath
# For example, let's extract the titles of all the links on the page
link_titles = tree.xpath('//a/@title')

# Print the extracted link titles
for title in link_titles:
    print(title)
