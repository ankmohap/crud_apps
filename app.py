from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///terminals.db'
app.config['SECRET_KEY'] = 'Baari@2023'  
db = SQLAlchemy(app)

# Define the Terminal model
class Terminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    terminal = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20))
    satellite = db.Column(db.String(50))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    address = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    regional_manager = db.Column(db.String(50))
    terminal_manager = db.Column(db.String(50))

# Create or update the database
with app.app_context():
    db.create_all()


# Terminal form for creating and editing terminals
class TerminalForm(FlaskForm):
    terminal = StringField('Terminal', validators=[DataRequired()])
    status = StringField('Status')
    satellite = StringField('Satellite')
    state = StringField('State')
    city = StringField('City')
    address = StringField('Address')
    zip_code = StringField('Zip Code')
    regional_manager = StringField('Regional Manager')
    terminal_manager = StringField('Terminal Manager')
    submit = SubmitField('Submit')

@app.route('/')
def index():
    terminals = Terminal.query.all()
    return render_template('index.html', terminals=terminals)

@app.route('/create', methods=['GET', 'POST'])
def create_terminal():
    form = TerminalForm()
    if form.validate_on_submit():
        terminal = Terminal(
            terminal=form.terminal.data,
            status=form.status.data,
            satellite=form.satellite.data,
            state=form.state.data,
            city=form.city.data,
            address=form.address.data,
            zip_code=form.zip_code.data,
            regional_manager=form.regional_manager.data,
            terminal_manager=form.terminal_manager.data
        )
        db.session.add(terminal)
        db.session.commit()
        flash('Terminal created successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_terminal(id):
    terminal = Terminal.query.get(id)
    form = TerminalForm(obj=terminal)
    if form.validate_on_submit():
        form.populate_obj(terminal)
        db.session.commit()
        flash('Terminal updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, terminal=terminal)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_terminal(id):
    terminal = Terminal.query.get(id)
    db.session.delete(terminal)
    db.session.commit()
    flash('Terminal deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True,port=8080)

