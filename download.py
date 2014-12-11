import os, urllib2, time
from models import Session, CensusData, CensusFields, PostalCode

session = Session()

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

def main():
	get_or_create_dirs()
	for instance in session.query(CensusFields).all():
		download_pages(instance)

def get_or_create_dirs():
	for instance in session.query(CensusFields).all():
		if not os.path.exists(os.path.join(PROJECT_DIR, instance.fieldname)):
			os.makedirs(os.path.join(PROJECT_DIR, instance.fieldname))

def download_pages(fieldinfo):
	for instance in session.query(PostalCode).all():
		new_file = os.path.join(os.path.join(PROJECT_DIR, fieldinfo.fieldname), "{}.html".format(instance.id))
		if not os.path.exists(new_file):
			html = download_page(fieldinfo, instance)
			if html:
				save_file(html, new_file)
		else:
			print "Already downloaded {}".format(new_file)

def download_page(fieldinfo, instance):
	url_code = str(instance.code).replace(" ", "+").replace(" ","")
	url = "{}{}{}".format(fieldinfo.prefix, url_code, fieldinfo.postfix)
	html = None
	try:
		response = urllib2.urlopen(url)
		if response.code == 200:
			print "Downloading {}".format(url)
			html = response.read()
		else:
			print "Invalid URL: {}".format(url)
	except urllib2.HTTPError:
		print "Failed to open {}".format(url)
	
	return html

def save_file(html, filename):
	try:
		with open(filename, 'w') as f:
			f.write(html)
	except IOError:
		print "Couldn't write to file {}".format(new_file)


if __name__ == "__main__":
	main()
