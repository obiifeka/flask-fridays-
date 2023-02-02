from flask import Flask,redirect,url_for,render_template,request,flash
from  flask_wtf import  FlaskForm
from wtforms import (StringField, SubmitField)
from wtforms.validators import DataRequired

app=Flask(__name__)
app.config['SECRET_KEY'] = "Z3cjjSdefewwefkw9cdferv"

# Create A Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

@app.route('/',methods=['GET','POST'])
def index(): 
    flash ("Welcome To Our Website!")
    first_name = "Obi"
    stuff = "this is  a <strong>Bold.</strong> text"
    seke = "hope you are  understanding the concept"
    favorite_pizza = ["pepperoni", "cheese", "mushroom", 41]
    return render_template("index.html",first_name=first_name,
   stuff=stuff,seke=seke, favorite_pizza=favorite_pizza)

# Create Custom Error Pages.
@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found():
    return render_template("500.html"),500



@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form =  NamerForm()
    #Validate Form
    if form.validate_on_submit():
        flash('Form Submitted Successfully')
        name = form.name.data
        form.name.data =  " "
    return render_template("name.html",name=name,form=form)
        
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)