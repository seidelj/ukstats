from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref

engine = create_engine('postgresql://postgres:joseph@localhost/ukstats')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class PostalCode(Base):
	__tablename__ = 'postalcode'
	id = Column(Integer, Sequence("postalcode_id_seq"), primary_key=True)
	code = Column(String)
	llsoa = Column(String)
	mlsoa = Column(String)
	reference_area = Column(String)

class CensusData(Base):
	__tablename__ = 'censusdata'
	id = Column(Integer, Sequence("census_id_seq"), primary_key=True)
	owned_hh = Column(String)
	male = Column(String)
	christian = Column(String)
	density = Column(String)
	gt_3bedrooms = Column(String)
	mainlanguage_english = Column(String)
	lone_parent = Column(String)
	gt_2people_per_hh = Column(String)
	full_time_worker = Column(String)
	gte_lvl4_education = Column(String)
	verygood_health = Column(String)
	good_health = Column(String)
	white = Column(String)
	uk_citizen = Column(String)
	avg_age = Column(String)
	avg_hh_income = Column(String)
	postalcode_id = Column(Integer, ForeignKey('postalcode.id'))	

	postalcode = relationship('PostalCode', backref=backref('censusdata', order_by=id))
	
class SubjectiveMeasure(Base):
	__tablename__ = 'subjectivemeasure'
	id = Column(Integer, Sequence("subjectivemeasure_id_seq"), primary_key=True)
	satisfaction = Column(String)
	worthwhile = Column(String)
	happy_yesterday = Column(String)
	postalcode_id = Column(Integer, ForeignKey('postalcode.id'))

	postalcode = relationship('PostalCode', backref=backref('subjectivemeasure', order_by=id))

class CensusFields(Base):
	__tablename__ = 'censusfields'
	id = Column(Integer, Sequence("censusfields_id_seq"), primary_key=True)
	fieldname = Column(String)
	totalpos = Column(String)
	fieldpos = Column(String)
	prefix = Column(String)
	postfix = Column(String)
	operation = Column(String)	
	layer = Column(String)

Base.metadata.create_all(engine)
