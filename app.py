import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup
from itertools import tee

url = "https://co.pacific.wa.us/sheriff/corrections/"
r = requests.get(url)
soup = BeautifulSoup(r.text)
table = soup.table
tbody = table.tbody
all_rows = tbody.contents
final_csv_data = []

important_rows = []

# all_rows = [x for x in all_rows if x != '\n']

for row in all_rows:
    if row != '\n':
        important_rows.append(row)

print(important_rows)
#
# for row in important_rows:
#     print('***')
#     print(row)
#     print('***')

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
