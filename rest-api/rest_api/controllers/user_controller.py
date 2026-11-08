import re
import uuid

from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from rest_api.models.user import User
from rest_api.services.database.database_client import db
from rest_api.services.database.user_sql import UserSQL

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_email(email):
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(EMAIL_REGEX, email))


class UserController(object):
    @staticmethod
    def create_user():
        request_data = request.get_json(silent=True)
        if not isinstance(request_data, dict):
            return jsonify({"error": "name and email are required"}), 400
        if "name" not in request_data:
            return jsonify({"error": "name is required"}), 400
        if "email" not in request_data:
            return jsonify({"error": "email is required"}), 400
        if not validate_email(request_data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        user_ = User(
            id=uuid.uuid4().hex,
            name=request_data["name"],
            email=request_data["email"],
        )
        db.session.add(user_.to_user_sql())
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "the email is already in use"}), 400

        stored = db.session.query(UserSQL).filter(UserSQL.id == user_.id).one()
        body = User.from_user_sql(stored).to_dict()
        body["message"] = "User created successfully."
        return jsonify(body), 200

    @staticmethod
    def get_user(user_id: str):
        user_sql = db.session.query(UserSQL).filter(UserSQL.id == user_id).one_or_none()
        if not user_sql:
            return jsonify({"error": "User not found"}), 404
        return jsonify(User.from_user_sql(user_sql).to_dict()), 200

    @staticmethod
    def fetch_all_users():
        users = db.session.query(UserSQL).all()
        if not users:
            return jsonify({"error": "User not found"}), 404
        return jsonify([User.from_user_sql(user).to_dict() for user in users]), 200

    @staticmethod
    def patch_user(user_id: str):
        user_sql = db.session.query(UserSQL).filter(UserSQL.id == user_id).one_or_none()
        if not user_sql:
            return jsonify({"error": "User not found"}), 404

        request_data = request.get_json(silent=True)
        if not request_data or ("name" not in request_data and "email" not in request_data):
            return jsonify({"error": "No valid fields to update. You need name or email to update"}), 400
        if "name" in request_data:
            user_sql.name = request_data["name"]
        if "email" in request_data:
            if not validate_email(request_data["email"]):
                return jsonify({"error": "Invalid email format"}), 400
            user_sql.email = request_data["email"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "the email is already in use"}), 400

        body = User.from_user_sql(user_sql).to_dict()
        body["message"] = "User updated successfully."
        return jsonify(body), 200

    @staticmethod
    def put_user(user_id: str):
        user_sql = db.session.query(UserSQL).filter(UserSQL.id == user_id).one_or_none()
        if not user_sql:
            return jsonify({"error": "User not found"}), 404

        request_data = request.get_json(silent=True)
        if not request_data:
            return jsonify({"error": "No valid fields to update. You need name and email."}), 400
        if "name" not in request_data:
            return jsonify({"error": "You need name to update."}), 400
        if "email" not in request_data:
            return jsonify({"error": "You need email to update."}), 400
        if not validate_email(request_data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        user_sql.name = request_data["name"]
        user_sql.email = request_data["email"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "the email is already in use"}), 400

        body = User.from_user_sql(user_sql).to_dict()
        body["message"] = "User updated successfully."
        return jsonify(body), 200

    @staticmethod
    def delete_user(user_id: str):
        user_sql = db.session.query(UserSQL).filter(UserSQL.id == user_id).one_or_none()
        if not user_sql:
            return jsonify({"error": "User not found"}), 404
        db.session.delete(user_sql)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), 200


user_controller = UserController()
