from datetime import datetime, timedelta
from .. import db

class Pet(db.Model):
    __tablename__ = 'pet'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(250), nullable = False)
    breed = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250), nullable = False)
    birth = db.Column(db.DateTime, nullable = True)
    adoption = db.Column(db.DateTime, nullable = True)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    last_modified_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    user = db.relationship('User',
        backref = db.backref('pets'), lazy = True)

    # def __repr__(self):
    #     return f"<Pet : {self.id}, {self.name}, {self.breed}, {self.gender}, {self.birth}, {self.adoption}>"

    @staticmethod
    def generate_fake(count):
        # Generate a number of fake pets for testing.
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        from faker import Faker
        from .test_samples import dog_name_samples, breed_samples
        
        fake = Faker()

        seed()
        for i in range(count):
            # get random datetime
            timestamp = fake.date_time_between(start_date='-10y')
            date = timestamp.date()
            time = timestamp.time()
            temp_datetime = datetime.combine(date, time)
            p = Pet(
                name=choice(dog_name_samples),
                breed=choice(breed_samples),
                gender=choice(['male', 'female']),
                # get random datetime
                birth=temp_datetime,
                # be adopt after 8 weeks
                adoption=temp_datetime + timedelta(weeks = 8),
                
                # match one foreign_key by one user
                # user id start from 1
                user_id = i+1
            )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()