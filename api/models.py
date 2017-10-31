from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, pre_load, validate
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
import status
import re
import sqlalchemy as sql


db = SQLAlchemy()
ma = Marshmallow()


class CURD():
    def add(rescourse):
        db.session.add(rescourse)
        db.session.commit()

    def update():
        db.session.commit()

    def delete():
        db.session.delete()


class Message(db.Model, CURD):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), index=True, nullable=False)
    duration = db.Column(db.Numeric, nullable=False)
    created_time = db.Column(db.DATETIME,
                             default=db.func.current_timestamp())
    printed_times = db.Column(db.Integer,
                              nullable=False,
                              default=0)
    printed_once = db.Column(db.Boolean,
                             default=False)
    category_id = db.Column(sql.ForeignKey('category.id',
                                          on_delete='CASCADE'), nullable=False)
    category = db.relationship('Category', backref=db.backref('message',
                                                  lazy='dynamic',
                                                  order_by='Message.message'))

    def __init__(self, message, duration, category):
        self.message = message
        self.duration = duration
        self.category = category


class Category(db.Model, CURD):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class CategorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(3))
    url = ma.URLFor('api.categoryresource', id='<id>', _external=True)
    message = fields.Nested('MessageSchema', many=True, exclude=('category',))


class MessageSchema(ma.Schema):
    id = fields.Integer(dump_only=True, primary_key=True)
    message = fields.String(required=True, validate=validate.Length(1))
    duration = fields.Integer()
    printed_Once = fields.Boolean()
    printed_times = fields.Integer()
    created_date = fields.DateTime()
    category = fields.Nested(CategorySchema,
                             only=['id', 'url', 'name'],
                             required=True)
    url = ma.URLFor('api.messageresource', id='<id>', _external=True)

    @pre_load(pass_many=False)
    def process_category(self, data):
        category = data.get('category')
        if category:
            if isinstance(category, dict):
                category_name = category.get('name')
            else:
                category_name = category
            category_dict = dict(name=category_name)
        else:
            category_dict = {}
            data['category'] = category_dict
        return data


class User(db.Model, CURD):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    hashed_password = db.Column(db.String(80),
                                validate=validate.Length(3), nullable=True)

    def verfiy_password(self, password):
        return password_context.verfiy_password(password, self.hashed_password)

    def create_password(self, password):
        if len(password) < 8:
            return {'error': 'Too short'}
        if not re.search(r'[a-z]', password):
            return {'error':
                    'You password shoule at least includeone character'}
        self.hashed_password = password_context.encrypt(password)
        query = User.query.filter_by(name=self.name).first()
        result = UserSchema.dump(query)
        return result, status.HTTP_201_CREATED

    def __init__(self, name):
        self.name = name


class UserSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(80)
    created_date = fields.datetime()
