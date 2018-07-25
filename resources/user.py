from flask_restful import Resource,reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required=True,
        help='Username field cannot be blank'
    ),
    parser.add_argument('password',
        type = str,
        required=True,
        help='Password field cannot be blank'
    )

    def post(self):
        data = UserRegister.parser.parse_args()
        #check if username already exist
        if UserModel.find_by_username(data['username']):
            return {"message": "that user already exist"},400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created successfully."},201
