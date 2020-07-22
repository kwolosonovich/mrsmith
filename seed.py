from models import db
from models import User, Like

def seed_database():
    db.drop_all()
    db.create_all()

    test_user = User(
        username="Ava",
        email="ava@gmail.com", 
        password="password",
        authenticated=True,
    )
    
    db.session.add(test_user)
    db.session.commit()