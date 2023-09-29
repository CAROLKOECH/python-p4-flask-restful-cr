from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

# Resource to get all newsletters and create a new one
class NewslettersResource(Resource):
    def get(self):
        newsletters = Newsletter.query.all()
        return [n.to_dict() for n in newsletters], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        args = parser.parse_args()

        new_record = Newsletter(title=args['title'], body=args['body'])
        db.session.add(new_record)
        db.session.commit()

        return new_record.to_dict(), 201

api.add_resource(NewslettersResource, '/newsletters')

# Resource to get a single newsletter by ID
class NewsletterResource(Resource):
    def get(self, id):
        newsletter = Newsletter.query.get(id)
        if newsletter:
            return newsletter.to_dict(), 200
        else:
            return {"message": "Newsletter not found"}, 404

api.add_resource(NewsletterResource, '/newsletters/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
