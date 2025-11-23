import os
from flask import Flask, render_template, request, redirect, url_for
from models import db, Gorev

app = Flask(__name__)

# --- Veritabanı ayarları ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "todo.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Uygulama başlarken tabloyu oluştur
with app.app_context():
    db.create_all()


# Ana sayfa: görevleri listele (R)
@app.route("/")
def index():
    gorev_listesi = Gorev.query.order_by(Gorev.id).all()
    return render_template("index.html", gorev_listesi=gorev_listesi)


# Görev ekleme (C)
@app.route("/add", methods=["POST"])
def add():
    baslik = request.form.get("baslik")
    aciklama = request.form.get("aciklama")

    if baslik:  # Boş başlık ekleme
        yeni = Gorev(baslik=baslik, aciklama=aciklama, tamamlandi=False)
        db.session.add(yeni)
        db.session.commit()

    return redirect(url_for("index"))


# Görev durumunu değiştir (U)
@app.route("/update/<int:gorev_id>")
def update(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    gorev.tamamlandi = not gorev.tamamlandi
    db.session.commit()
    return redirect(url_for("index"))


# Görev sil (D)
@app.route("/delete/<int:gorev_id>")
def delete(gorev_id):
    gorev = Gorev.query.get_or_404(gorev_id)
    db.session.delete(gorev)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)