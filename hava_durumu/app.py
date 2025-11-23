import requests
from flask import Flask, render_template, request
import json
import os
import datetime

def jsona_kaydet(weather):
    try:
        simdi = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        veri = {
            "tarih": simdi,
            "sehir": weather["city"],
            "sicaklik": weather["temp"],
            "nem": weather["humidity"],
            "durum": weather["desc"]
        }

        kayitlar = []
        if os.path.exists("hava_durumu.json"):
            with open("hava_durumu.json", "r", encoding="utf-8") as dosya:
                kayitlar = json.load(dosya)

        kayitlar.append(veri)

        with open("hava_durumu.json", "w", encoding="utf-8") as dosya:
            json.dump(kayitlar, dosya, ensure_ascii=False, indent=2)

        print("JSON'a kaydedildi:", veri)

    except Exception as e:
        print("JSON kayıt hatası:", e)


app = Flask(__name__)

API_KEY = "ae7c36382f3a3a91d26dc7d85340fd87"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")

        params = {
            "q": city,
            "APPID": API_KEY,
            "units": "metric",
            "lang": "tr"
        }

        try:
            response = requests.get(BASE_URL, params=params, timeout=5)

            print("API URL:", response.url)
            print("Status:", response.status_code)
            print("Raw:", response.text)

            if response.status_code == 200:
                data = response.json()

                weather_data = {
                    "city": data["name"],
                    "temp": data["main"]["temp"],
                    "desc": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"]
                }

                jsona_kaydet(weather_data)

            elif response.status_code == 404:
                error_message = "Şehir bulunamadı."
            else:
                error_message = f"API hatası oluştu. Kod: {response.status_code}"

        except requests.exceptions.RequestException:
            error_message = "Bağlantı hatası. İnternetinizi kontrol edin."

    return render_template("index.html", weather=weather_data, error=error_message)



@app.route("/kayitlar")
def kayitlar():
    kayitlar = []
    error_message = None

    try:
        if os.path.exists("hava_durumu.json"):
            with open("hava_durumu.json", "r", encoding="utf-8") as dosya:
                kayitlar = json.load(dosya)

            if not kayitlar:
                error_message = "Henüz kayıt yok."
        else:
            error_message = "Henüz kayıt yok."
    except Exception as e:
        error_message = f"Kayıtlar okunurken hata oluştu: {e}"

    return render_template("kayitlar.html", kayitlar=kayitlar, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)




