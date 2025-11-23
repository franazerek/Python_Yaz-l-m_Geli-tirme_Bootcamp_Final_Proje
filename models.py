from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Gorev(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(100), nullable=False)
    aciklama = db.Column(db.String(255))
    tamamlandi = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Gorev {self.id} - {self.baslik}>"