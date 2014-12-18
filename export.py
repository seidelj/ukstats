import csv, os
from models import Session, CensusData, SubjectiveMeasure, PostalCode

session = Session()
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

def main():
	fieldsDict = get_field_names()
	with open(os.path.join(PROJECT_DIR, 'rusty.csv'), 'w') as f:
		write_csv(fieldsDict, f)
	print "All done"

def write_csv(modelinfo, f):
	writer = csv.writer(f, csv.excel)
	header = modelinfo['PostalCode'] + modelinfo['CensusData'] + modelinfo['SubjectiveMeasure']
	writer.writerow(header)
	fieldList = modelinfo['CensusData'] + modelinfo['SubjectiveMeasure']
	for postalcode in session.query(PostalCode).all():
		objList = []
		#Write the postalcode list before anything else
		for field in modelinfo['PostalCode']:
			objList.append(getattr(postalcode, field))
		for field in fieldList:
			objList += write_objlist(modelinfo, field, postalcode)
		writer.writerow(objList)

def write_objlist(m, f, postalcode):
	objList = []
	for key, value in m.items():
		if key != 'PostalCode':
			q = session.query(globals()[key]).filter_by(postalcode_id=postalcode.id).first()
			try:
				objList.append(getattr(q, f))
			except AttributeError:
				continue
	
	return objList

def get_field_names():
	postalFields = []
	for c in PostalCode.__table__.columns:
		censusFields = []
		postalFields.append(c.name)

	censusFields = []
	for c in CensusData.__table__.columns:
		if c.name != "id" and c.name != "postalcode_id":
			censusFields.append(c.name)
	
	subjectiveFields = []
	for c in SubjectiveMeasure.__table__.columns:
		if c.name != "id" and c.name != "postalcode_id":
			subjectiveFields.append(c.name)
	fieldDict = {
		'PostalCode': postalFields,
		'CensusData': censusFields,
		'SubjectiveMeasure': subjectiveFields,
	}
	return fieldDict

if __name__ == "__main__":
	main()
