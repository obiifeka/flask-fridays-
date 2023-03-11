from flask import (Flask,redirect,
                   url_for,render_template,
                   request,flash)
from flask_login import ( UserMixin,
                         login_user ,
                         LoginManager,
                         login_required, 
                         login_remembered,
                         logout_user, 
                         login_url)
from  flask_wtf import  FlaskForm
from wtforms import (StringField, SubmitField,
                     PasswordField,BooleanField,
                     TextAreaField,
                     ValidationError)
from flask_wtf.file import FileField, FileRequired
from datetime import  date, datetime
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.config['SECRET_KEY'] = "Z3cjjSdefewwefkw9cdferv"
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///bloger.db'
#app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql+pymysql://root:password123@localhost/our_users'
db = SQLAlchemy(app)
#migrate = Migrate(app,db )

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))




class Users(db.Model,UserMixin):
    
    id             = db.Column(db.Integer,primary_key=True)
    firstname      = db.Column(db.String(200),nullable=False)
    lastname      = db.Column(db.String(200),nullable=False)
    username       = db.Column(db.String(20) ,nullable=False,unique=True)
    email          = db.Column(db.String(200),nullable=False,unique=True)
    favorite_color = db.Column(db.String(200))
    date_added     = db.Column(db.DateTime,default=datetime.utcnow)
    password_hash  = db.Column(db.String(120))
     
     
     
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self,password):
        self.check_password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return '<Name %r>' % self.name 
   
    


# Create A Form Class
class NamerForm(FlaskForm):
    name   = StringField("What's Your Name", validators=[DataRequired()])
    photo  = FileField( 'Photo ', )
    submit = SubmitField("Submit")
    
class PasswordForm(FlaskForm):
    email                 = StringField("What's Your Email", validators=[DataRequired()])
    password_hash   = PasswordField("What's Your Password", validators=[DataRequired()])
    photo                 = FileField( 'Photo ', )
    submit                = SubmitField("Submit")
   
   
# class UpdateForm(FlaskForm):
#     name   = StringField("What's Your Name", validators=[DataRequired()])
#     email  = StringField( 'Photo ', )
#     submit = SubmitField("Submit")

class PhotoForm(FlaskForm):
    photo = FileField(validators=[FileRequired()])
    
class Userform(FlaskForm):
   
        firstname           = StringField(" First Name", validators=[DataRequired()])
        lastname            = StringField(" Last Name", validators=[DataRequired()])
        username            = StringField(" Username", validators=[DataRequired()])
        email               = StringField(" Email", validators=[DataRequired()])
        favorite_color      = StringField(" Favorite Color")
        password_hash       = PasswordField('Enter Password',validators=[DataRequired(),EqualTo('check_password_hash2', message='Passwords must match!')])
        password_hash2      = PasswordField('Confirm Password',validators=[DataRequired()])
        submit = SubmitField("Submit")


  

class LoginForm(FlaskForm):
        username  = StringField(" Username",validators=[DataRequired()])
        password  = PasswordField(" Password",validators=[DataRequired()])
        submit    = SubmitField("Submit ")
        




 

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    form =  Userform()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name           = request.form['name']
        name_to_update.email          = request.form['email']
        name_to_update.password_hash  = request.form['password_hash']
        name_to_update.favorite_color = request.form['favorite_color']
        
        try:
            db.session.commit()
            flash('Details Updated Successfully')
            return render_template("update.html",
                                   form=form, 
                                   name_to_update=name_to_update,id=id)
        except:
            flash('Error looks  like there was a problem')
            return render_template("update.html",
                                     form=form, 
                                     name_to_update=name_to_update)
    else:
        return render_template("update.html"
                               ,form=form, 
                               name_to_update=name_to_update,id = id)
        
@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    
    form =  Userform()
     

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User Deleted Successfully')
        
        our_users = Users.query.order_by(Users.date_added)
        return render_template("add_user.html",
            form=form, 
            name=name,
            our_users=our_users)
    
    except:
            flash(" WHoops there was a problem deleting  user,try again")
            return render_template("add_user.html",
            form=form, 
            name=name,
            our_users=our_users)
 

@app.route('/user/<name>')
def user(name):
    form = PhotoForm
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




@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    form =  NamerForm()
    #Validate Form
    if form.validate_on_submit():
        flash('Form Submitted Successfully')
        name = form.name.data
        photo = form.photo.data
        form.name.data =  " "
        form.photo.data =  " "
        
    return render_template("name.html",name=name,form=form)

@app.route('/test_pw', methods=['GET','POST'])
def test_pw():
    email       = None
    password    = None
    pw_to_check = None
    passed      = None
    form =  PasswordForm()
    #Validate Form
    if form.validate_on_submit():
        #flash('Form Submitted Successfully')
        email     = form.email.data
        password  = form.password_hash.data
        photo     = form.photo.data
        #clear the form
        form.email.data          =  " "
        form.password_hash.data  =  " "
        form.photo.data          =  " "
    user_to_check = Users.query.filter_by(email=email).first()
    #passed = check_password_hash(pw_to_check.password_hash ,password)
        
    return render_template("test_pw.html",email=email,password=password,form=form,user_to_check=user_to_check,passed=passed)

    
@app.route('/date')
def get_current_date():
        favorite_pizza = {
            "John":"Pepperoni",
            "Mary": "Cheese",
            "Tim": "Mushroom"
        }
        return favorite_pizza
        #return{"Date": date.today()}


@app.route('/add_user',methods=['GET','POST'])
def add_user():
    name = None
    form =  Userform()
    
    if form.validate_on_submit():
        print ('added')  
        user = Users.query.filter_by(email=form.email.data).first()
        if  user is None:
            
            hashed_pw  = generate_password_hash(form.password_hash.data, "sha256")
            user =Users(  
            firstname      = form.firstname.data,
            lastname       = form.lastname.data,
            username       = form.username.data,
            email          = form.email.data,
            favorite_color = form.favorite_color.data,
            password_hash  = form.hashed_pw)  
           
                     
            db.session.add(user) 
           
            db.session.commit()
            
            
        name = form.name.data
        form.firstname.data      =  " "
        form.lastname.data       =  " "
        form.username.data       =  " "
        form.email.data          =  " "
        form.favorite_color.data =  " "
        form.password_hash       =  " "
        flash('Added Successfully')  
    our_users = Users.query.order_by(Users.date_added)    
    return render_template("add_user.html",
        form=form, 
        name=name,our_users=our_users)

   




@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if  user:
            if check_password_hash(user.password_hash,form.password.data):
                login_user(user)
                print('ok')
                flash("Login Successfully!!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong  Password - Try Again")
        else:
            flash ("That User Doesn't Exist Try Again")
    return render_template('login.html',form=form)

@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = LoginForm()
    return render_template('dashoboard.html')
    

@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash ("You Have Been Logged  Out!  Thanks For Stopping By....")
    return redirect(url_for('login'))

        
        
    
    
        
if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=8000,debug=True)