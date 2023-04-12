#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError
from models import db, Research, Author, ResearchAuthor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api =Api(app) 
class Researchs (Resource):
    def get (self):
        researchs_list = [r.to_dict() for r in Research.query.all()]
        return make_response(researchs_list, 200)
    
api.add_resource(Researchs, '/researchs')


class ResearchsById (Resource):
    def get (self, id):
        r = Research.query.filter_by(id=id).first()
        if r==None:
            return make_response( {'error': "Research paper not found"}, 404)
        return make_response( r.to_dict(), 200)   
    
def delete (self, id):
    r = Research.query.filter_by(id=id).first()
    if r == None:
        return make_response( { "error": "Research paper not found"}, 404)
    # instead of cascade. This is a for loop deleting instances not needed in model.py
    #for ra in r_instance.research_authors:
    #   db.session.de;ete(r)
    #   db.session.commit()
    db.session.delete( r )
    db.session.commit()
    return make_response( {}, 204)

api.add_resource(ResearchsById, "/researchs/<int:id>")


class Authors (Resource):
    def get (self):
        authors_list = [a.to_dict() for a in Author.query.all()]
        return make_response(authors_list, 200)
    
api.add_resource(Authors, '/authors')

class ResearchsAuthor (Resource):
    def post (self):
        data = request.get_json()
        new_author = ResearchAuthor(author_id= data['author_id'], research_id = data['research_id'])

        db.session.add(new_author)
        db.session.commit()
        return make_response( {new_author.to_dict()}, 200)
        
api.add_resource(ResearchsAuthor, '/researchsAuthor')

if __name__ == '__main__':
    app.run(port=5555, debug=True)


# @app.route('/')
# def index():
#     return '<h1>Code challenge</h1>'

# @app.route('/research')
# def restaurants():

#     pass



