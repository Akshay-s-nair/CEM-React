from flask import Flask, render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
import random
app = Flask(__name__)
lis=[['NAME','NOS','PRODUCT','PRICE']]
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.db'
app.config['SECRET_KEY']='qwertyuiop'


db=SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30),nullable=False, unique=True)
    password=db.Column(db.String(30),nullable=False)
    
    created_at=db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return '<Name %r>'% self.name
    
class products(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(128))
    price=db.Column(db.Float)
    # quantity=db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>'% self.name


with app.app_context():
    db.create_all()

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/home')
def about(): 
    return render_template('index.html')

def authenticate_user(name, password):
    list = Users.query.filter_by(name=name).first()
    if list and list.password == password:
        return 1, list.id
    else:
        return 0, None

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password= request.form.get('password')
        if name=='':
            flash("please enter the Name")
            return redirect(url_for('login'))
        elif password=='':
            flash("please enter the Password")
            return render_template('login.html')
        
        result,lisid= authenticate_user(name, password)
        if result==1:
            return render_template('index.html',val=name.capitalize(), lis=lis)
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if(request.method == 'POST'):
        name = request.form.get('name')
        name.capitalize()
        mail = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('re-password')
        if confirm != password:
            flash("passwords doesn't match")
            redirect(url_for('register'))
        idd=random.randint(1,1000000)
        entry = Users(id=idd,name=name, email=mail, password=password, created_at=datetime.now())
        db.session.add(entry)
        db.session.commit()
    return render_template('login.html')

# @app.route('/login', methods = ['GET', 'POST'])
# def cart():
#     return 'welcome to cart'

@app.route('/login/addcart/<int:value>/<string:name>/<string:personname>', methods = ['GET', 'POST'])
def addcart(value,name,personname):
    lis.append([personname,name,value])
    print(lis)
    return render_template('added.html',val=personname)

@app.route('/login/cart', methods = ['GET', 'POST'])
def cart():
    y=0
    if len(lis)>1:
        for i in lis[1:]:
            y+=i[2]
    
    l=len(lis)
    return render_template('cart.html', val=lis,total=y,len=l)

# @app.route('/login/<string:personname1>/addcart/<int:value>/<string:name>/<string:personname>', methods = ['GET', 'POST'])
# def addcart2(personname1,value,name,personname):
#     lis.append([name,value])
#     print(lis)
#     return render_template('added.html',val=personname)

@app.route('/invoice', methods = ['GET', 'POST'])
def invoice():
    global lis
    y=0
    for i in lis[1:]:
        y+=i[2]
    print(y)
    l=len(lis)
    return render_template('invoice.html',vala=lis,total=y,len=l)

@app.route('/delete/<int:pos>', methods = ['GET', 'POST'])
def delete(pos):
    global lis
    y=0
    lis.pop(pos)
    l=len(lis)
    for i in lis[1:]:
        y+=i[2]
    print('deleted',y)
    return render_template('cart.html', val=lis,total=y,len=l)


if __name__=='__main__':
    app.run(debug=True)