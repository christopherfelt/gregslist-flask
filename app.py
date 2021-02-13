from flask import Flask, flash, render_template, request, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = "random string"

# bootstrap
# database
# user auth

db = SQLAlchemy(app)
class Car(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    img_url = db.Column(db.String)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    price = db.Column(db.Float)

    def __init__(self, title, img_url, make, model, price):
        self.title = title
        self.img_url = img_url
        self.make = make
        self.model = model
        self.price = price

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_email = db.Column(db.String(100), unique=True, nullable=False)



# car_items = [
#     {"name":"car1", "price": 123.12},
#     {"name": "car2", "price": 345.75}
# ]

@app.route("/", methods=["GET"])
def landing_page():
    return render_template('index.html')

@app.route("/cars", methods=["GET"])
def cars():
    
    car_items = Car.query.all()

    fields = [
        {"name":"title", "label": "Title", "type":"text"},
        {"name":"img_url", "label": "Image URL", "type": "text"},
        {"name":"make", "label": "Make", "type": "text"},
        {"name":"model", "label":"Model", "type": "text"},
        {"name":"price", "label": "Price", "type": "float"}]


    return render_template('list.html', item_type="Cars", item_type_title="Cars",
                             item_nums=len(car_items), items=car_items, info_html="car_info.html", 
                             fields=fields)

@app.route("/form-handler", methods=['POST'])
def handle_data():
    if request.method == "POST":
        new_car = Car(request.form['title'],
                        request.form['img_url'], request.form['make'],
                        request.form['model'], request.form['price'])
        db.session.add(new_car)
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('cars'))
        # return jsonify(request.form)



if __name__ == "__main__":
    db.create_all()
    app.run(debug = True)