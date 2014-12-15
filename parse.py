import os, re, argparse, os, sys
from bs4 import BeautifulSoup
from sqlalchemy import update
from models import Session, PostalCode, CensusData, CensusFields
from sqlutils import get_or_create
session = Session()
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def main():
	for postalcode in session.query(PostalCode).all():
		parse_pages(postalcode)
		if not postalcode.reference_area:
			postalcode.reference_area = get_ref_area(postalcode)
	session.commit()

def parse_pages(postalcode):
	for instance in session.query(CensusFields).all():
		fieldDir = os.path.join(PROJECT_ROOT, instance.fieldname)
		filename = os.path.join(fieldDir, "{}.html".format(postalcode.id))
		print filename
		with open(filename) as f:
			fieldValue = parse_page(f, instance)
			print fieldValue
			if fieldValue:
				censusdata, created = get_or_create(session, CensusData, postalcode_id=postalcode.id)
				session.query(CensusData).filter(CensusData.id==censusdata.id).update({str(instance.fieldname): fieldValue})
			else:
				sys.exit("Could not parse a value from {}".format(filename))

def parse_page(f, info):
	soup = BeautifulSoup(f, "lxml")
	table = soup.find(class_="dataTable")
	rows = table.find_all('tr')
	data = parse_table(rows)
	if info.operation == "division":
		output = divide(data, info)
	elif info.operation == "none":
		field = clean_field(info.fieldpos)
		output = data[int(field[0])][int(field[1])-2].replace(",","")
	elif info.operation == "freq_dist_avg":
		output = get_freq_dist_avg(data, info)
	else:
		output = None

	return output

def get_ref_area(page):
	directory = os.path.join(PROJECT_ROOT, 'male')
	filename = os.path.join(directory,"{}.html".format(page.id))
	with open(filename) as f:
		soup = BeautifulSoup(f, "lxml")
		header = soup.find('h1').get_text()
		ref_area = header.split(": ")
		ref_area = ref_area[1].split(" (")
		ref_area = ref_area[0]
		return ref_area

def clean_field(i):
	field = str(i).replace("(",'').replace(")","").replace(",",'').replace(" ","")
	return field	

def divide(d, i):
	field = clean_field(i.fieldpos)
	total = clean_field(i.totalpos)
	numerator = d[int(field[0])][int(field[1])-2]
	denominator = d[int(total[0])][int(total[1])-2]
	numerator = int(numerator.replace(",",""))
	denominator = int(denominator.replace(",",""))
	avg = float(numerator) / denominator
	return avg

def get_freq_dist_avg(d, i ):
	total = clean_field(i.totalpos)
	denominator = d[int(total[0])][int(total[1])-2]
	denominator = int(denominator.replace(",",""))

	counter = 0	
	numerator = 0
	for row in d[2:]:
		numerator += (counter * float(row[0]))
		counter += 1
	avg = float(numerator / denominator)
	return avg

def parse_table(rows):
	data = []
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.get_text() for ele in cols]
		data.append([ele for ele in cols])
	return data

if __name__ == "__main__":
	main()


