from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Laddar bokningar från JSON
def load_bookings():
    if os.path.exists("bookings.json"):
        with open("bookings.json", "r") as f:
            return json.load(f)
    return []

# Sparar bokningar till JSON
def save_bookings(bookings):
    with open("bookings.json", "w") as f:
        json.dump(bookings, f, indent=4)

# Startsidan
@app.route("/")
def index():
    bookings = load_bookings()
    return render_template("index.html", bookings=bookings)

# Lägga till en bokning
@app.route("/add", methods=["POST"])
def add_booking():
    name = request.form["name"]
    date_time = request.form["date_time"]

    if not name or not date_time:
        flash("Alla fält måste fyllas i!")
        return redirect(url_for("index"))

    bookings = load_bookings()
    bookings.append({"name": name, "date_time": date_time})
    save_bookings(bookings)
    flash("Bokningen har lagts till!")
    return redirect(url_for("index"))

# Tar bort en bokning
@app.route("/delete/<int:index>")
def delete_booking(index):
    bookings = load_bookings()
    if 0 <= index < len(bookings):
        del bookings[index]
        save_bookings(bookings)
        flash("Bokningen har tagits bort!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
