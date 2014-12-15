import csv, os
from models import Session, CensusFields, PostalCode
from sqlutils import get_or_create

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

session = Session()

def main():
	filename = os.path.join(PROJECT_DIR, 'censusfields.csv')
	import_censusfield(filename)
	
#	import_postalcodes(filename)	

def import_postalcodes(filename):
	with open(filename, 'rb') as f:
		mycsv = csv.reader(f)
		next(mycsv, None)
		for row in mycsv:
			postalcode, created = get_or_create(session, PostalCode, code=row[0])	
		session.commit()

def import_censusfield(filename):
	with open(filename, 'rb') as f:
		mycsv = csv.reader(f)
		next(mycsv, None) # Skip headers
		for row in mycsv:
			censusfield = CensusFields(fieldname=row[0], totalpos=row[1], fieldpos=row[2], prefix=row[3], postfix=row[4], operation=row[5], layer=row[6])
			session.add(censusfield)
		session.commit()

if __name__ == "__main__":
	main()
	
