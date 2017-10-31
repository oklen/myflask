from flask_restful import Api
from flask import Blueprint, Flask
from views import MessageResource, MessageListResource, \
     CategoryResource, CategoryListResourse
import config
bp_app = Blueprint('api', __name__)
api = Api(bp_app)
api.add_resource(MessageResource, '/message/<int:id>')
api.add_resource(MessageListResource, '/messages/')
api.add_resource(CategoryResource, '/category/<int:id>')
api.add_resource(CategoryListResourse, '/categorys/')


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from models import db
    db.init_app(app)

    app.register_blueprint(bp_app, url_prefix='/api')
    return app, db


app, db = create_app('config')

if __name__ == '__main__':

    app.run()
