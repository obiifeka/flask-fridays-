from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route('/<name>')
def user(name):
    return render_template("user.html", name=name)

@app.route('/',methods=['GET','POST'])
def index(): 
    first_name = "Obi"
    stuff = "this is  a <strong>Bold.</strong> text"
    seke = "hope you are  understanding the concept"
    favorite_pizza = ["pepperoni", "cheese", "mushroom", 41]
    return render_template("index.html",first_name=first_name,
   stuff=stuff,seke=seke, favorite_pizza=favorite_pizza)

# Create Custom Error Pages
@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"),404

@app.errorhandler(500)
def page_not_found():
    return render_template("500.html"),500

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)