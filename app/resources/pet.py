from flask import request
from flask_restful import Resource
from app.models.pet import Pet, PetSchema
from app import db
from app.utils.decorators import confirm_account
import datetime
from sqlalchemy.exc import IntegrityError

# make instances of schemas
pet_schema = PetSchema()
# pets_schema = PetSchema(many=True)

class PetRegisterApi(Resource):
    @confirm_account
    def post(self):
        # check that pet's name already exists
        pet = Pet.query.filter_by(user_id=request.json['user_id'], name=request.json['name']).first()
        if pet:
            return {
                "msg" : f"name \'{pet.name}\' already exists"
            }, 409
        new_pet = Pet(
            name = request.json['name'],
            breed = request.json['breed'],
            gender = request.json['gender'],
            birth = request.json['birth'],
            adoption = request.json['adoption'],
            #user_id is not nullable
            user_id = request.json['user_id']
        )
        db.session.add(new_pet)
        db.session.commit()
        return pet_schema.dump(new_pet), 200


class PetApi(Resource):
    @confirm_account
    def get(self, pet_id):
        selected_pet = Pet.query.filter_by(id = pet_id).first()
        return pet_schema.dump(selected_pet), 200

    @confirm_account
    def put(self, pet_id):
        # check that pet's name already exists
        # check with updated user_id
        duplicated_pet = Pet.query.filter_by(user_id=request.json['user_id'], name=request.json['name']).first()
        if duplicated_pet:
            return {
                "msg" : f"name \'{duplicated_pet.name}\' already exists"
            }, 409
        try:
            updated_pet = Pet.query.filter_by(id = pet_id).first()
            updated_pet.name = request.json['name']
            updated_pet.breed = request.json['breed']
            updated_pet.gender = request.json['gender']
            updated_pet.birth = request.json['birth']
            updated_pet.adoption = request.json['adoption']
            updated_pet.last_modified_date = datetime.datetime.now()
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status" : "Fail",
                "msg" : "Integrity error on updating pet profile"
            }, 409
        return pet_schema.dump(updated_pet), 200

    @confirm_account
    def delete(self, pet_id):
        deleted_pet = Pet.query.filter_by(id = pet_id).first()
        try:
            db.session.delete(deleted_pet)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return {
                "msg" : "IntegrityError of deleting pet profile, maybe because of foreign keys."
            }, 409
        return {
            "msg" : "Successfully deleted pet profile."
        }, 200
