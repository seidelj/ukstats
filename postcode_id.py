import os, urllib2
from bs4 import BeautifulSoup
from models import PostalCode, Session

session = Session()

prefix="http://neighbourhood.statistics.gov.uk/NDE2/Disco/SearchSByAByPostcode?LevelTypeId="
#141&Postcode=CM129SL

def main():
	for instance in session.query(PostalCode).all():
		get_ids(instance)
	session.commit()

def get_ids(instance):
	pcode = str(instance.code).replace(" ","")
	llsoa_url = "{}141&Postcode={}".format(prefix, pcode)
	mlsoa_url = "{}140&Postcode={}".format(prefix, pcode)
	
	response = urllib2.urlopen(llsoa_url)
	data = response.read()
	soup = BeautifulSoup(data)
	
	llsoa_id =  soup.find_all("areaid")[1].get_text()

	response = urllib2.urlopen(mlsoa_url)
	data = response.read()
	soup = BeautifulSoup(data)
	
	mlsoa_id = soup.find_all("areaid")[1].get_text()
	
	instance.mlsoa = mlsoa_id
	instance.llsoa = llsoa_id
	
if __name__ == "__main__":
	main()
