import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import csv
from collections import defaultdict

wiki_template = "https://temtem.gamepedia.com/%s"
species_page = "Techniques"

def lookup(page):
	raw = urllib2.urlopen(wiki_template % page)
	return BeautifulSoup(raw, 'html.parser')

headers = ['name', 'type', 'synergy_type', 'class', 'damage', 'stamina', 'hold', 'priority']
def parse_table():
	soup = lookup(species_page)
	table_body = soup.find('table').find('tbody')
	moves = []
	for row in table_body.findAll("tr")[1:]:
		x = defaultdict(str)
		ind = 0
		for col in row.findAll("td"):
			header = headers[ind]
			if header == 'type':
				types = map(lambda t: t['href'][1:].split('_')[0].lower(), col.findAll('a'))
				x['type'] = types[0]
				if len(types) > 1:
					x['synergy_type'] = types[1]
				ind += 1
			elif header == 'class':
				x[header] = col.find('a')['title'].strip().lower()
			elif header == 'priority':
				x[header] = col.find('a')['title'].strip().lower().split('_')[0]
			else:
				x[header] = col.text.strip()
			ind += 1
		if x['stamina'] == '-':
			continue
		moves.append(x)
	return moves

def main():
	x = parse_table()
	with open('../csv/moves.csv', 'wb') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(headers)
		for a in x:
			row = map(lambda t:a[t], headers)
			writer.writerow(row)


if __name__ == '__main__':
	main()
