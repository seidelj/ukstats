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

class CensusData(Base):
	__tablename__ = 'censusdata'
	id = Column(Integer, Sequence("census_id_seq"), primary_key=True)
	owned_hh = Column(Integer)
	male = Column(Integer)
	christian = Column(Integer)
	density = Column(Integer)
	gt_3bedrooms = Column(Integer)
	mainlanguage_english = Column(Integer)
	lone_parent = Column(Integer)
	gt_2people_per_hh = Column(Integer)
	full_time_worker = Column(Integer)
	gte_lvl4_education = Column(Integer)
	verygood_health = Column(Integer)
	good_health = Column(Integer)
	white = Column(Integer)
	uk_citizen = Column(Integer)
	avg_age = Column(Integer)
	avg_hh_income = Column(Integer)
	postalcode_id = Column(Integer, ForeignKey('postalcode.id'))	

	postalcode = relationship('PostalCode', backref=backref('censusdata', order_by=id))
	
class SubjectiveMeasure(Base):
	__tablename__ = 'subjectivemeasure'
	id = Column(Integer, Sequence("subjectivemeasure_id_seq"), primary_key=True)
	satisfaction = Column(Integer)
	worthwhile = Column(Integer)
	happy_yesterday = Column(Integer)
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

Base.metadata.create_all(engine)
