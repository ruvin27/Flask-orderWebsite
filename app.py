from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    material = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        order_name = request.form['name']
        order_material = request.form['material']
        order_quantity = request.form['quantity']
        new_order = Order(name = order_name, material = order_material, quantity = order_quantity)

        try:
            db.session.add(new_order)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        orders = Order.query.order_by(Order.date_created).all()
        return render_template('index.html', orders=orders)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Order.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    order = Order.query.get_or_404(id)

    if request.method == 'POST':
        order.name = request.form['name']
        order.material = request.form['material']
        order.quantity = request.form['quantity']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', order=order)

@app.route('/view/<int:id>', methods=['GET'])
def view(id):
    order = Order.query.get_or_404(id)
    return render_template('view.html', order=order)



if __name__ == "__main__":
    app.run(debug=True)
