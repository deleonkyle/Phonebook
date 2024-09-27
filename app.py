from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phonebook.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    company = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)


@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        company = request.form['company']
        notes = request.form['notes']
        
        new_contact = Contact(name=name, phone=phone, email=email, address=address, company=company, notes=notes)

        try:
            db.session.add(new_contact)
            db.session.commit()
            flash('Contact added successfully!', 'success')
            return redirect('/')
        except:
            flash('Error! There was an issue adding the contact.', 'error')
            return redirect('/add')
    return render_template('add_contact.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    if request.method == 'POST':
        contact.name = request.form['name']
        contact.phone = request.form['phone']
        contact.email = request.form['email']
        contact.address = request.form['address']
        contact.company = request.form['company']
        contact.notes = request.form['notes']

        try:
            db.session.commit()
            flash('Contact updated successfully!', 'success')
            return redirect('/')
        except:
            flash('Error! There was an issue updating the contact.', 'error')
            return redirect(f'/edit/{id}')
    return render_template('edit_contact.html', contact=contact)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successfully!', 'success')
        return redirect('/')
    except:
        flash('Error! There was an issue deleting the contact.', 'error')
        return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
