from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Research (db.Model, SerializerMixin):
    __tablename__ = 'researchs'

    serialize_rules = ('-research_authors','authors')

    
    id = db.Column( db.Integer, primary_key=True )
    year = db.Column (db.Integer, nullable=False)
    topic = db.Column (db.String, nullable=False)
    page_count = db.Column (db.Integer, nullable=False)

    research_authors = db.relationship ('ResearchAuthor', backref='research',
                                         cascade = 'all, delete-orphan')
    authors = association_proxy('research_authors', 'author')

    @validates('year')
    def validate_year(self, key, year):
        if len(str(year)) != 4:
            raise ValueError("Year must be 4 characters")
        return year


class ResearchAuthor (db.Model, SerializerMixin):
    __tablename__ = 'research_authors'

    serialize_rules = ('-research_authors.authors', '-research_authors.research')

    research_id = db.Column( db.Integer, db.ForeignKey( 'researchs.id' ) )
    author_id = db.Column( db.Integer, db.ForeignKey( 'authors.id' ) )
    id = db.Column( db.Integer, primary_key=True )
   


class Author (db.Model, SerializerMixin):
    __tablename__ = 'authors'

    serialize_rules = ('-research_authors',)

    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String)
    id = db.Column( db.Integer, primary_key=True )
    research_authors = db.relationship( 'ResearchAuthor', backref='author' )
    researchs = association_proxy('research_authors', 'author')

    @validates("field_of_study")
    def validate_field_of_study (self, key, field_of_study):
        if field_of_study not in ['AI', 'Robotics', 'Machine Learning', 'Vision', 'Cybersecurity']:
            raise ValueError("field_of_study invalid")
        return field_of_study 

     
  