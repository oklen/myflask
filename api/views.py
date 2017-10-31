from flask import Blueprint, request, jsonify, make_response
from models import Message, Category, MessageSchema, CategorySchema, db
from sqlalchemy.exc import SQLAlchemyError
from flask_restful import Api, Resource
import status

api_bp = Blueprint('api', __name__)
category_schema = CategorySchema()
message_schema = MessageSchema()
api = Api(api_bp)


class MessageResource(Resource):
    def get(self, id):
        message = Message.query.get_or_404(id)
        result = message_schema.dump(message).first
        return result

    def patch(self, id,):
        message = Message.query.get_or_404(id)
        message_dict = request.get_json(force=True)
        if 'message' in message_dict:
            message.message = message_dict['message']
        dump_message, dump_error = message_schema.dump(message)
        if dump_error:
            return dump_error, status.HTTP_400_BAD_REQUEST
        validated_errors = message_schema.vaildate(dump_message)
        if validated_errors:
            return validated_errors, status.HTTP_400_BAD_REQUEST
        try:
            message.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({'error': str(e)})
            return resp, status.HTTP_401_UNAUTHORIZED

        def delete(self, id):
            message = Message.query.get_or_404(id)
            try:
                Message.delete(message)
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": e})
                return resp, status.HTTP_401_UNAUTHORIZED


class MessageListResource(Resource):
    def get(self):
        message = Message.query.all()
        result = message_schema.dump(message, many=True).data
        return result

    def post(self):
        message_dict = request.get_json()
        if not message_dict:
            response = {'message': 'No input data'}
            return response, status.HTTP_400_BAD_REQUEST
        if not is_unique(Message, message=message_dict['message']):
            return {'Error': 'Message already existing'},
        status.HTTP_400_BAD_REQUEST
        error = message_schema.validate(message_dict)
        if error:
            return error, 401
        try:
            category_name = message_dict['category']['name']
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                category = Category(name=category_name)
                db.session.add(category)
            message = Message(
                message=message_dict['message'],
                duration=message_dict['duration'],
                category=category
            )
            Message.add(message)
            query = message.query.get(message.id)
            result = message_schema.dump(query)
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            error = {'error': str(e)}
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR


class CategoryResource(Resource):
    def get(self, id):
        query = Category.query.get(id)
        result = category_schema.dump(query)
        return result, status.HTTP_200_OK

    def patch(self, id):
        category = Category.query.get_or_404(id)
        category_dict = request.get_json()
        if category_dict is None:
            response = jsonify({'error': 'Empty Post'})
            return response, status.HTTP_400_BAD_REQUEST
        error = category_schema.validate(category_dict)
        if error:
            return error, status.HTTP_400_BAD_REQUEST
        try:
            if 'name' in category_dict:
                category.name = category_dict['name']
            category.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            query = jsonify({'error': str(e)})
            return query, status.HTTP_401_UNAUTHORIZED

        def delete(self, id):
            category = Category.query.get_or_404(id)
            try:
                category.delete(category)
                resp = make_response()
                return resp, status.HTTP_204_NO_CONTENT
            except SQLAlchemyError as e:
                db.session.rollback()
                error = jsonify({'error': str(e)})
                return error, status.HTTP_401_UNAUTHORIZED


class CategoryListResourse(Resource):
    def get(self):
        query = Category.query.all()
        result = category_schema.dump(query, many=True)
        return result, status.HTTP_200_OK

    def post(self):
        category_dict = request.get_json()
        if not category_dict:
            resp = {'error': 'Empty Post'}
            return resp, status.HTTP_400_BAD_REQUEST
        if not is_unique(Category, id=Category['id']):
            return {"error": 'Repeat!'}, status.HTTP_400_BAD_REQUEST
        error = category_schema.validate(category_dict)
        if error:
            return error, status.HTTP_400_BAD_REQUEST
        try:
            category = Category(category_dict['name'])
            Category.add(category)
            query = Category.query.get(category.id)
            message = category_schema.dump(query)
            return message, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            error = jsonify({'error': e})
            return error, status.HTTP_400_BAD_REQUEST


def is_unique(cls, id=None, message=None):
    if id is not None:
        query = cls.query.filter_by(id=id).first()
    elif message is not None:
        query = cls.query.filter_by(message=message).first()
        if query is None:
            return False
        elif query.id == 0:
            return True
        else:
            return True
