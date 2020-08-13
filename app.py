import requests
import csv
from bs4 import BeautifulSoup

# We define the website we want to scrape here
url = "https://co.pacific.wa.us/sheriff/corrections/"

# We define r as a python variable, and say "use requests, use the get function within requests, and get the url"
# For additional documentation, always start with the library's documentation page
# In this case, requests' documentation page is here: https://requests.readthedocs.io/en/master/user/quickstart/
r = requests.get(url)

# We create a new variable called soup, and say "use the BeautifulSoup function and give it r.text"
# Again, you can read BeautifulSoup's documentation here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
soup = BeautifulSoup(r.text)

# Remember to use the web inspector in Chrome, Firefox, Safari, Microsoft Edge of whatever browser you use...
# ...to find out what the structure of the page is. In this case, we know all the data we want is in a HTML table
table = soup.table
tbody = table.tbody
all_rows = tbody.contents

# We are creating two empty lists, one called "final_csv_data" and the other "important_rows"
# We know they're lists because they are square brackets [] and there is nothing in it
# You can read more on lists in python here: https://www.geeksforgeeks.org/python-list/
final_csv_data = []
important_rows = []

# This is a loop! And loops are the bread and butter of programming, at the end of the day
# Essentially, what we are doing next can be described as "For every item in this list, do something"
# The first line says "We are going to call every item within all_rows a 'row'"
# The second line says "As we are going through every row, if the row is not a \n, do something"
# And the third line descibes what that "something" is, in this case, we append it to the list we made earlier
for row in all_rows:
    if row != '\n':
        important_rows.append(row)

# Here, we are printing (displaying) to our terminal everything that's inside our list called important_rows
print(important_rows)

paired_data = zip(important_rows[0::2], important_rows[1::2])

for inmate, inmate_info in paired_data:
    print('---')
    # inmate_dict = {}
    # inmate_dict['charges'] = []
    # print(inmate)
    # print(inmate.find_all('td', 'inmate'))
    # print(type(inmate.find_all('td', 'inmate')))
    # print(inmate.find_all('td', 'inmate')[0].get_text())
    name = inmate.find_all('td', 'inmate')[0].get_text()
    # print(name)
    # inmate_dict['name'] = name
    # print('\n')
    # print('***')
    # print(inmate_info)
    inmate_rows = inmate_info.find_all('tr')[1:]
    print(inmate_rows)
    for bond in inmate_rows:
        print('***')
        items = bond.find_all('td')
        date = items[0].get_text()
        charge = items[-1].get_text()
        bail = items[-3].get_text()
        print('Name: ' +name)
        print('Date: '+str(date))
        print('Charge: '+str(charge))
        print('Bail: '+str(bail))
        dict = {}
        dict['Description'] = charge
        dict['Name'] = name
        dict['Date'] = date
        dict['Bail'] = bail
        print(dict)
        print('***')
        print('\n')
        final_csv_data.append(dict)
    # print(inmate_info.find_all('tr')[1:])
    # print('***')

    print('---')
    print('\n')

header = final_csv_data[0].keys()
with open('scraped_list.csv', 'w', newline='') as csv_file:
    dict_writer = csv.DictWriter(csv_file, header)
    dict_writer.writeheader()
    dict_writer.writerows(final_csv_data)
