import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import csv
from collections import defaultdict

wiki_template = "https://temtem.gamepedia.com/%s"
species_page = "Temtem_Species"

def lookup(page):
	raw = urllib2.urlopen(wiki_template % page)
	return BeautifulSoup(raw, 'html.parser')

headers = ["num", "name", "type1", "type2", "hp", "sta", "spe", "atk", "def", "satk", "sdef", "total"]
def parse_table():
	soup = lookup(species_page)
	table_body = soup.find('table', attrs={'class': 'temtem-list'}).find('tbody')
	tems = []
	for row in table_body.findAll("tr"):
		x = defaultdict(str)
		ind = 0
		for col in row.findAll("td"):
			x[headers[ind]] = col.text.strip()
			if 'colspan' in col.attrs:
				ind += int(col['colspan'])
			else:
				ind += 1
		try:
			n = int(x['spe'])
			n = int(x['hp'])
			n = int(x['sta'])
			n = int(x['atk'])
			n = int(x['def'])
			n = int(x['satk'])
			n = int(x['sdef'])
		except:
			continue
		tems.append(x)
	return tems

def main():
	x = parse_table()
	with open('../csv/species.csv', 'wb') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(headers)
		for a in x:
			row = map(lambda t:a[t], headers)
			writer.writerow(row)


if __name__ == '__main__':
	main()
