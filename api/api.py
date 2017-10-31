from models import MessageModel
from flask_restful import abort, Resource, marshal_with, reqparse, fields
from datetime import datetime
import status


class MessageManager():
    last_id = 0

    def __init__(self):
        self.message = {}

    def insert_message(self, message):
        self.last_id += 1
        message.id = self.__class__.last_id
        self.message[message.id] = message

    def get_message(self, id):
        return self.message.get(id)

    def delete_message(self, id):
        del self.message[id]


message_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'duration': fields.Integer,
    'created_date': fields.DateTime,
    'printed_times': fields.Integer,
    'printed_once': fields.Boolean,
}

message_manager = MessageManager()


class Message(Resource):
    def abort_if_message_doesn_exist(self, id):
        if id not in message_manager.message:
            abort(
                status.HTTP_404_NOT_FOUND,
                message="Message {0} doesn't exist".format(id)
            )

    @marshal_with(message_fields)
    def get(self, id):
        self.abort_if_message_doesn_exist(id)
        return message_manager[id]

    def delete(self, id):
        self.abort_if_message_doesn_exist(id)
        del message_manager[id]

    @marshal_with(message_fields)
    def patch(self, id):
        self.abort_if_message_doesn_exist(id)
        parse = reqparse.RequestParser()
        message = message_manager.get_message(id)
        parse.add_argument('message', type=str)
        parse.add_argument('duration', type=int)
        parse.add_argument('printed_times', type=int)
        parse.add_argument('printed_once', type=bool)
        request = parse.parse_args()
        if 'message' in request:
            message.message = request['message']
        if 'duration' in request:
            message.duration = request['duration']
        if 'printed_times' in request:
            message.printed_times = request['printed_times']
        if 'printed_once' in request:
            message.printed_once = request['printed_once']
        return message


class MessageList(Resource):
    @marshal_with(message_fields)
    def get(self):
        return [m for m in message_manager.message.values()]

    @marshal_with(message_fields)
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('message', type=str, required=True,
                           help='Message cannot be blank')
        parse.add_argument('duration', type=int, required=True,
                           help='Message cannot be blank')
        parse.add_argument('message_category', type=int, required=True,
                           help='Message cannot be blank')
        args = parse.parse_args()
        message = MessageModel(
            message=args['message'],
            duration=args['duration'],
            message_category=args['message_category'],
            created_date=datetime.utcnow())
        message_manager.insert_message(message)
        return message, status.HTTP_201_CREATED
