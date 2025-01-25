from config import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    # Eliminar el constructor __init__()
    # El constructor predeterminado de SQLAlchemy asignará los valores directamente
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }
