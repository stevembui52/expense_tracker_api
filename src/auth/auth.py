from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..database.database import User, db
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1/auth")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        username = request.json.get("username")
        email = request.json.get("email")
        password = request.json.get("password")

        if not username or username == '':
            return jsonify({'message':'please provide username'}), 400
        if not email or email == '':
            return jsonify({'message':'please provide email'}), 400
        if len(username)<4:
            return jsonify({'message':'Username should have atleast 4 characters'}), 400
        if len(password)<4:
            return jsonify({'message':'password too short'}), 400
        if not validators.email:
            return jsonify({'message':'please provide a valid email'}), 400
        if not username.isalnum() or " " in username:
            return jsonify({"Error":"Username should be alphanumeric with no spaces"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'message':'Username taken!!!!'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'message':'Email taken!!!!'}), 400

        
        # hashing the password
        hashed_pwd = generate_password_hash(password=password)

        user = User(username=username, email=email, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        return jsonify({"message":"user created successifully"},
                    {"User":{"username":user.username,"email":user.email, "Registered":user.created_at}}), 201


@auth_bp.post('/login')
def login():
    email = request.json["email"]
    password = request.json["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password=password):
        access = create_access_token(identity=str(user.user_id))
        refresh = create_refresh_token(identity=str(user.user_id))

        return jsonify({"message":"user logged in successifully",
                    "username":user.email,
                    "access":access,
                    "refresh":refresh}), 200
    return jsonify({"message":"invalid credentials"}), 401


@auth_bp.get('/users')
@jwt_required()
def show_users():
        data = []

        users = User.query.all()
        if users:
            for user in users:
                data.append({"username": user.username, "email":user.email,
                            "created":user.created_at, "updated":user.updated_at})
            return jsonify({"data":data}), 200
        return jsonify({"message":"show the world your users"})