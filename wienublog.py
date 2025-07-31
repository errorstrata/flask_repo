from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
api = Api(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_ECHO'] = True
db=SQLAlchemy(app)

class BlogModel (db.Model):
	  id = db.Column(db.Integer , primary_key = True)
	  div_name = db.Column(db.String(50), nullable = False)
	  image_path = db.Column(db.String(200), nullable = False )
	  description = db.Column(db.String(200), nullable = False)
	  ul_name = db.Column(db.String(50), nullable = False)
	  like = db.Column(db.Integer, nullable = True)
	  bore = db.Column(db.Integer, nullable = True)
	  surprise = db.Column(db.Integer, nullable = True)
	  dislike = db.Column(db.Integer, nullable = True)

with app.app_context():
	   db.create_all()

class Blog(Resource):
    def post(self):
        data = request.get_json()
        div_name = data.get('launch') 
        image_path = data.get('launching')
        description = data.get('header')
        ul_name = data.get('reactions')
        like = data.get('like')
        bore = data.get('bore')
        surprise = data.get('surprise')
        dislike = data.get('dislike')

        newblog = BlogModel(
            div_name=div_name,
            image_path=image_path,
            description=description,
            ul_name=ul_name,
            like=like,
            bore=bore,
            surprise=surprise,
            dislike=dislike
        )
        db.session.add(newblog)
        db.session.commit()
        return {'message': 'data has been uploaded'}, 200

    def get(self):
        blogs = BlogModel.query.all()
        create_blog = [{'id':blog.id, 'div_name':blog.div_name, 'image_path':blog.image_path, 'description':blog.description, 'ul_name':blog.ul_name, 'like':blog.like, 'bore':blog.bore, 'surprise':blog.surprise, 'dislike':blog.dislike}for blog in blogs]
        return jsonify(create_blog)  # this was just misaligned by a few spaces
        
    def put(self,id):
        data = request.get_json()
        blog = db.session.get(BlogModel,id)
        
        if not  blog:
            return {'message':'blog does not exist'}, 404
        
        blog.div_name = data.get('div_name',blog.div_name)
        blog.image_path = data.get('image_path',blog.image_path)
        blog.description = data.get('description',blog.description)
        blog.ul_name = data.get('ul_name',blog.ul_name)
        blog.like = data.get('like',blog.like)
        blog.bore = data.get('bore',blog.bore)
        blog.surprise = data.get('surprise',blog.surprise)
        blog.dislike = data.get('dislike',blog.dislike)

        db.session.commit()
        return {'message':'updated successfully'}
        
    def delete(self, id):
       blog = db.session.get(BlogModel,id)
       if blog:
           db.session.delete(blog)
           db.session.commit()
           return {'message': f'Blog {id} deleted successfully'}, 200
       else:
           return {'message': f'Blog {id} not found'}, 404
        
api.add_resource(Blog, '/blog' , '/blog/<int:id>')
