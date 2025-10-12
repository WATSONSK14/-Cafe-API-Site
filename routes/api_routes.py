from dataclasses import field

from flask import request, jsonify, Blueprint
from sqlalchemy.sql.functions import user
from werkzeug.security import generate_password_hash
from model import db, User, Cafe, create_and_store_api_key_for_user, decrypt_key


api_bp = Blueprint('api', __name__)


@api_bp.route('/users',methods=['POST'])
def add_user():
    data = request.get_json()
    required_fields = ["username","email","password"]

    if not data:
        return jsonify({"error":"No data provided"}),400
    for field in required_fields:
        if field not in data:
            return jsonify({"error":"Missing required field"}),400
    try:
        password = data['password']
        username = data['username']
        email = data['email']
        check_user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
        check_email = db.session.execute(db.select(User).filter_by(email=email)).scalar()
        if check_user:
            return jsonify({"error":"Username already exists"}),400
        if check_email:
            return jsonify({"error":"Email already exists"}),400

        password_hash = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=password_hash,
        )
        db.session.add(new_user)
        db.session.commit()
        create_and_store_api_key_for_user(new_user)
        try:
            api_key = decrypt_key(new_user.api_key_enc)
        except Exception as e:
            return jsonify({"error": "API key decryption failed"}), 500

        return jsonify({"success": True, "user": f"Username : {username} Password: {password}  API-KEY: {api_key}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/users/<string:username>/info',methods=['GET'])
def user_info(username):
    api_key = request.headers.get('X-API-KEY')
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar()

    if not user:
        return jsonify({"error":"User not found"}), 404
    if not api_key:
        return jsonify({"error":"API key not found"}), 401
    try:
        decrypt_api_key = decrypt_key(user.api_key_enc)
    except Exception as e:
        return jsonify({"error": "API key decryption failed"}), 500

    if api_key != decrypt_api_key:
        return jsonify({"error": "API key does not match"}), 403
    return jsonify({"User": {"username": user.username,"email": user.email}, "Cafes":[cafe.to_dict() for cafe in user.cafes]}), 200



@api_bp.route('/cafes', methods=['GET'])
def all_cafes_api():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@api_bp.route('/cafes/<string:username>', methods=['POST'])
def add_cafe_api(username):
    api_key = request.headers.get('X-API-KEY')
    if not api_key:
        return jsonify({"error": "API key not provided"}), 401

    data = request.get_json()
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar()
    if not user:
        return jsonify({"error":"User does not exist"}), 404

    try:
        decrypted_key = decrypt_key(user.api_key_enc)
    except Exception:
        return jsonify({"error": "API key decryption failed"}), 500

    if api_key != decrypted_key:
        return jsonify({"error": "API key does not match"}), 403

    map_url_check = db.session.execute(db.select(Cafe).filter_by(map_url=data['map_url'])).scalar()

    required_fields = ["can_take_calls", "coffee_price", "country", "has_sockets", "has_toilet", "has_wifi", "img_url", "location", "map_url", "name"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error":f"Required field {field} not provided"}), 400

    if map_url_check:
        return jsonify({"error":  "Cafe already exists"}), 400

    new_cafe = Cafe(
        name=data["name"],
        map_url=data["map_url"],
        img_url=data["img_url"],
        location=data["location"],
        country=data["country"],
        has_toilet=data["has_toilet"],
        has_wifi=data["has_wifi"],
        has_sockets=data["has_sockets"],
        can_take_calls=data["can_take_calls"],
        coffee_price=data["coffee_price"],
        user_id=user.id,
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({"success":"Cafe Added Successfully","cafe": new_cafe.to_dict()}), 201


@api_bp.route('/cafes/<int:cafe_id>', methods=['PATCH','PUT'])
def update_cafe_api(cafe_id):
    data = request.get_json()
    api_key = request.headers.get('X-API-KEY')
    fields = ["can_take_calls", "coffee_price", "country", "has_sockets", "has_toilet",
              "has_wifi", "img_url", "location", "map_url", "name"]

    if not data:
        return jsonify({"error": "No data provided"}), 400

    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe not found"}), 404

    user = db.session.execute(db.select(User).filter_by(id=cafe.user_id)).scalar()
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        decrypted_key = decrypt_key(user.api_key_enc)
    except Exception:
        return jsonify({"error": "API key decryption failed"}), 500
    if api_key != decrypted_key:
        return jsonify({"error": "API key is incorrect"}), 403


    if "map_url" in data:
        check_map_url = db.session.execute(db.select(Cafe).filter_by(map_url=data["map_url"])).scalar()
        if check_map_url and check_map_url.id != cafe.id:
            return jsonify({"error": "Map url already exists"}), 400

    try:
        if request.method == 'PUT':
            missing = [field for field in fields if field not in data]
            if missing:
                return jsonify({"error": f"Missing required fields: {missing}"}), 400
            for field in fields:
                setattr(cafe, field, data[field])
        else:
            for field in fields:
                if field in data:
                    setattr(cafe, field, data[field])

        db.session.commit()
        return jsonify({"success": "Cafe updated successfully", "cafe": cafe.to_dict()}), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500

@api_bp.route('/cafes/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.headers.get('X-API-KEY')

    cafe = db.session.get(Cafe, cafe_id)
    if not cafe:
        return jsonify({"error": "Cafe not found"}), 404

    user = db.session.get(User, cafe.user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        decrypted_key = decrypt_key(user.api_key_enc)
    except Exception:
        return jsonify({"error": "API key decryption failed"}), 500

    if not api_key:
        return jsonify({"error": "API key not provided"}), 401

    if api_key != decrypted_key:
        return jsonify({"error": "API key is incorrect"}), 403

    db.session.delete(cafe)
    db.session.commit()
    return jsonify({"success": "Cafe deleted successfully"}), 200
