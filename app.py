from os import stat
import os
import random
import bcrypt
import string
import logging
from flask import Config, Flask,render_template,request,url_for,session,redirect,jsonify
from flask.config import ConfigAttribute
from flask_mail import Mail,Message
from flask_session import Session
from werkzeug.utils import secure_filename
from config import Config
# Database import
from Database.database import Database
from Database.admin import Admin
from Database.aution import Auctioin
from Database.addischeretauser import AddisCheretaUser
from Database.verfication import Verfication
from Database.seller import Seller
from Database.buyer import Buyer
from Database.finalauctionmessage import FinalAuctionMessage
from Database.item import Item
from Database.rating import Rating
from datetime import datetime,timedelta

app=Flask(__name__)
# What is secret key in app ?
app.secret_key = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = Config().email # Use Our actual Gmail address
app.config['MAIL_PASSWORD'] = Config().mailpassword      # Use Our generated App Password from gmail Api
app.config['MAIL_USE_TLS'] = True # What is TLS and Why is set to true
app.config['MAIL_USE_SSL'] = False # What is SSL and Why is set to false
app.config["SESSION_TYPE"] = "filesystem" # This refering to the flask_session folder where it contains the session files
app.config['UPLOAD_FOLDER']="./static/upload" # location of the any of the images that are uploaded

Session(app)
mail=Mail(app)
db=Database()
aution=Auctioin()
verf=Verfication()
salt=bcrypt.gensalt()
buyer=Buyer()
admin=Admin()
finalauctionmessage=FinalAuctionMessage()
rating=Rating()
seller=Seller()
item=Item()
addischeretauser=AddisCheretaUser()

@app.route('/forgotpassword',methods=['GET','POST'])
def forgotpassword():
    if request.method == "POST":
        email=request.form["email"]
        # not finsihed yet
        result=addischeretauser.GetAddisCheretaUserData(email)[4]
        if result is []:
            return redirect(url_for('regsister'))
        else:
            session['email']=email
            session['forgot']='true'
            code=verf.UpdateVerficationTable(email)
            if code[0]=="code":
                msg=Message(
                subject="Welcome To addischereta!",
                sender=Config().email,
                recipients=[email]
                )
                msg.body=f"""
                    please Enter code {code[1]} to change password don't share this code with anyone. 
                """
                mail.send(msg)
                return redirect(url_for('verfication'))

    return render_template('forgotpassword.html')


@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method == "POST":
        new_password=request.form['new_password']
        confirm_password=request.form['confirm_password']
        if new_password !=confirm_password:
            return render_template('createnewpassword.html')
        addischeretauser.ResetPassWordForUser(session['email'],new_password)
        return render_template('login.html')
    return render_template('createnewpassword.html')


@app.route('/login',methods=['GET','Post'])
def login():
    if request.method == "POST":
        email=request.form['email']
        password=request.form['password']
        userdata=addischeretauser.GetAddisCheretaUserData(email)
        if userdata==[]:
            return render_template('login')
        elif bcrypt.checkpw(password.encode('utf'),userdata[8])==True:
            # to user page
            session["logged"]=True
            session["UID"]=userdata[0]
            return redirect(url_for('userdashboard'))
        elif bcrypt.checkpw(password.encode('utf'),userdata[8])==False:
            return render_template('login.html')
    return render_template('login.html')
    
@app.route('/verfication',methods=['GET','POST'])
def verfication():
    
    if session['forgot']=='true' and request.method == "POST":
        code=request.form["code"]
        result=verf.GetEmailForVerfication(session['email'])
        now=datetime.now()
        if datetime.strptime(result[2].split(".")[0],"%Y-%m-%d %H:%M:%S") > now and code == str(result[0]):
            session['status']="active"
            return redirect(url_for("reset"))
        else:
            return render_template("verfication.html",message=False)
    elif session['forgot']=='false' and request.method=="POST":
        code=request.form["code"]
        result=verf.GetEmailForVerfication(session['email'])
        now=datetime.now()
        if datetime.strptime(result[2].split(".")[0],"%Y-%m-%d %H:%M:%S") > now and code == str(result[0]):
            session['status']="active"
            return redirect(url_for("login"))
        else:
            return render_template("verfication.html",message=False)
    return render_template("verfication.html")

@app.route('/regsister',methods=['GET','POST'])
def regsister():
    if 'forgot' in session:
        return redirect(url_for('login'))
    if request.method == "POST":
        firstname=request.form["Firstname"]
        middlename=request.form["Middlename"]
        lastname=request.form["Lastname"]
        email=request.form["Email"]
        phonenumber=request.form["Phonenumber"]
        userlocation=request.form["Location"]
        photo=request.files["Photo"]
        password=request.form["Password"]
        re_password=request.form["re_password"]
        if password!=re_password:
            # to bechanged into reg
            return redirect(url_for('regsister'))
        if email is None:
            return render_template('regsister.html',message="Problem With Email")
        emailresult=addischeretauser.ExistsInAddisCheretaUser(email) 
        if emailresult==True:
            return render_template('regsister.html',message="Email Exists")
        if photo.filename=="":
            photo=''
        elif photo and db.AllowedFile(photo.filename):
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(photo.filename)))
            photo=photo.filename
        password=bcrypt.hashpw(password.encode('utf-8'), salt)        
        result=addischeretauser.InsertAddisCheretaUser(firstname,middlename,lastname,email,phonenumber,userlocation,photo,password)
        if result!="True":
            return render_template("regsister.html")
        code=''.join(random.choices(string.digits, k=6))
        status="deactive"
        session['status']=status
        session['email']=email
        futureTime=datetime.now()+timedelta(minutes=10)
        result=verf.InsertVerficationTable(code,email,futureTime,status)
        if result!="True":
            return render_template("regsister.html")
        msg=Message(
                subject="Welcome To addischereta!",
                sender=Config().email,
                recipients=[email]
         )
        msg.body=f"""
                Hi {firstname} {lastname},

                Congratulations on signing up! 🎉 We're thrilled to have you join our community. Get ready to explore all the exciting features and benefits we have in store for you.

                If you have any questions or need assistance getting started, feel free to reach out. We're here to help!
                
                please enter {code} to verify and activate the account

                Welcome again, and enjoy your journey with us!

                Best,
                team addischereta
            """
        mail.send(msg)
        session['forgot']='false'
        return redirect(url_for('verfication'))
    return render_template('regsister.html')

@app.route('/resend')
def resend():
    email=session['email']
    session['forgot']='true'
    code=verf.UpdateVerficationTable(email)
    if code[0]=="code":
        msg=Message(
            subject="Welcome To addischereta!",
            sender=Config().email,
            recipients=[email]
        )
        msg.body=f"""
                    please Enter code {code[1]} to change password don't share this code with anyone. 
                """
    mail.send(msg)
    return redirect(url_for('verfication'))


@app.route("/userdashboard/delete/<IID>/<Price>")
def deleteBid(IID,Price):
    if "logged" in session and session["logged"]==True:
        ok=buyer.DeleteWithBuyerIdAndPrice(Price,session["UID"],IID)
        return redirect(url_for("userdashboard"))
    return redirect("http://127.0.0.1:5000/")

@app.route("/userdashboard")
def userdashboard():
    if "logged" in session:
        bid=buyer.GetUserBidWithUserId(str(session["UID"]))
        useritems=[]
        for i in item.UserItemDashboardWithUID(str(session["UID"])):
            if buyer.HighestBid(i[5])==None:
                useritems.append(list(i)+[0])
            else:
                useritems.append(list(i)+[buyer.HighestBidWinnerWithId(i[5])[0],buyer.HighestBidWinnerWithId(i[5])[1]])
        return render_template("userdashbord.html",userbid=bid,userItem=useritems)
    else:
        return redirect(url_for("/"))
    
@app.route("/updateName/<IID>",methods=["GET","POST"])
def UpdateName(IID):
    if request.method=="POST":
        itemname=request.form["itemname"]
        ok=item.UpdateName(itemname,IID,str(session["UID"]))
        if ok==True:
            return redirect(url_for("userdashboard")) 
    return redirect(url_for("userdashboard"))

@app.route("/updateStartingPrice/<IID>",methods=["GET","POST"])
def updateStartingPrice(IID):
    if request.method=="POST":
        startingprice=request.form["startingprice"]
        ok=item.UpdateStartingPrice(startingprice,IID,str(session["UID"]))
        if ok==True:
            return redirect(url_for("userdashboard")) 
    return redirect(url_for("userdashboard"))

@app.route("/updatedatestored/<IID>",methods=["GET","POST"])
def updatedatestored(IID):
    if request.method=="POST":
        datestored=request.form["datestored"]
        ok=item.UpdateDateStored(datestored,IID,str(session["UID"]))
        if ok==True:
            return redirect(url_for("userdashboard")) 
    return redirect(url_for("userdashboard"))


@app.route("/rateIID/<IID>",methods=["GET","POST"])
def rateIID(IID):
    if "logged" in session and session["logged"]==True:
        if request.method=="POST":
            ratedvalue=request.form["star"]
            sellerUID=item.GetItemWithIID(IID)[1]
            ok=rating.InsertingRating(session["UID"],sellerUID,ratedvalue)
            if ok==True:
                return redirect(f"http://127.0.0.1:5000/items/{IID}")
            else:
                return redirect(f"http://127.0.0.1:5000/items/{IID}")
    return redirect("http://127.0.0.0.1:5000")

@app.route("/rateUID/<UID>",methods=["GET","POST"])
def rateUID(UID):
    if "logged" in session and session["logged"]==True:
        if request.method=="POST":
            star=request.form["star"]
            ok=rating.InsertingRating(session["UID"],UID,star)
            if ok==True:
                return redirect(url_for("userdashboard"))
            elif ok==False:
                result=addischeretauser.GetPhonenumberEmailWithUID(UID)
                return render_template("userprofile.html",Phonenumber=result[0],Email=result[1],UID=UID)
        result=addischeretauser.GetPhonenumberEmailWithUID(UID)
        photo=addischeretauser.GetPhotoWithUID(UID)
        ratedvalue=rating.BayesianRatingOfUser(UID)
        if type(ratedvalue)!=float:
            rateUID="Not Rated Yet"
        if result==[] or photo==False:
            return render_template("userprofile.html",Phonenumber="+2510000000",Email="John@Doe.com",UID=UID,Photo="None")
        photo=f"upload/{photo}"
        return render_template("userprofile.html",Phonenumber=result[0],Email=result[1],UID=UID,Photo=photo,Rating=ratedvalue)
    return redirect("http://127.0.0.0.1:5000")



@app.route("/search",methods=["GET","POST"])
def search():
    if "logged" in session and session["logged"]==True:
        if request.method=="POST":
            result=[]
            price=request.form["price"]
            if price.isdigit()!=True:
                return render_template("search.html",table=[])
            categories=request.form["categories"]
            name=request.form["name"]
            result=item.Search(name,price,categories)
            if result is []:
                return render_template("search.html",table=result)
            return render_template("search.html",table=result)
        result=item.GetAllItemLimit()
        return render_template("search.html",table=result)
    else:
        return redirect(url_for('login'))

@app.route("/items/<IID>",methods=["GET","POST"])
def items(IID):
    if "logged" not in session:
        return redirect("http://127.0.0.1:5000/")
    result=item.GetItemWithIID(IID)
    sellerratevalue=rating.BayesianRatingOfUser(item.GetItemWithIID(IID)[1])
    if type(sellerratevalue)!=float:
        sellerratevalue=0
    itemname=result[2]
    desciption=result[3]
    photo="upload/"+result[6]
    price=result[8]
    category=result[7]
    status=result[4]
    maxPrice=buyer.HighestBid(IID)
    if maxPrice==None:
        maxPrice=0
    maxBuyerUid=buyer.HighestBidWinnerWithId(IID)[1]
    buyerWinner=False
    phonenumber=""
    email=""
    if session['UID']==maxBuyerUid:
        itemownerInformation=addischeretauser.GetPhonenumberEmailWithUID(item.GetItemWithIID(IID)[1])
        phonenumber=itemownerInformation[1]
        email=itemownerInformation[0]
        buyerWinner=True
    return render_template("item.html",IIDS=IID,photos=photo,desciptions=desciption,itemnames=itemname,startingprice=price,categories=category,state=status,MaxPrice=maxPrice,Email=email,Phonenumber=phonenumber,buyerwinner=buyerWinner,Rate=sellerratevalue)
    
@app.route("/addauction",methods=["GET","POST"])
def addauction():
    if "logged" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        itemname=request.form["itemName"]
        startingprice=request.form["startingprice"]
        description=request.form["description"]
        category=request.form["category"]
        endDate=request.form["endDate"]
        uid=session["UID"]
        photo=request.files["Photo"]
        if photo.filename=="":
            photo=''
        elif photo and db.AllowedFile(photo.filename):
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(photo.filename)))
            photo=photo.filename
        ok=item.InsertItemTable(uid,itemname,description,photo,category,startingprice,endDate)
        if ok==False:
            return render_template("addauction.html")
        else:
            return redirect(url_for('userdashboard'))
    return render_template("addauction.html")

@app.route("/bid/<IID>",methods=["GET","POST"])
def biditem(IID):
    if "logged" in session and session["logged"]==True:
        if request.method=="POST":
            bidPrice=request.form["bid"]
            bidTime=datetime.now()
            UID=session["UID"]
            ok=buyer.InsertBuyerTable(UID,IID,bidTime,bidPrice)
            if ok==True:
                return redirect(f"http://127.0.0.1:5000/items/{IID}")
            return redirect(f"http://127.0.0.1:5000/items/{IID}")
    return redirect("http://127.0.0.1:5000/")  

@app.route("/adminlogin",methods=["GET","POST"])
def adminlogin():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        result=admin.GetAdminWithUsername(username)
        if result==[]:
            return render_template("adminlogin.html")
        elif bcrypt.checkpw(password.encode('utf'),result[0][1])==True:
            session["admin"]=username
            return redirect(url_for('adminDashborad'))
        elif bcrypt.checkpw(password.encode('utf'),result[0][1])==False:
            return render_template("adminlogin.html") 
    return render_template("adminlogin.html")

@app.route("/adminDashborad")
def adminDashborad():
    if "admin" in session:
        auctiondatalist=item.ListOfAuction()
        auctiondatalistNumber=len(auctiondatalist)
        addisuser=[]
        for i in addischeretauser.GetAllUserDataUidFirstNameEtc():
            if type(rating.BayesianRatingOfUser(i[0]))==float:
                addisuser.append(list(i)+[rating.BayesianRatingOfUser(i[0])])
            else:
                addisuser.append(list(i)+[0])
        return render_template("adminDashborad.html",auctiondata=auctiondatalist,auctiondataNumber=auctiondatalistNumber,addisuserdata=addisuser)
    return render_template("adminlogin.html")

@app.route("/adminDashborademail",methods=["GET","POST"])
def adminDashboradEmail():
    if "admin" not in session:
        return render_template("adminlogin.html")
    if request.method=="POST":
        try:
            emailOption=request.form["emailOption"]
            if emailOption=="allUsers":
                subject=request.form["subject"]
                body=request.form["body"]
                msg=Message(
                subject=subject,
                sender=Config().email,
                recipients=addischeretauser.GetAllCheretaUserEmail()
                )
                msg.body=body
                mail.send(msg)
                return redirect("adminDashborad")
            elif emailOption=="emailAddress":
                recipientEmail=request.form["recipientEmail"]
                subject=request.form["subject"]
                body=request.form["body"]
                msg=Message(
                subject=subject,
                sender=Config().email,
                recipients=[recipientEmail]
                )
                msg.body=body
                mail.send(msg)
                return redirect(url_for("adminDashborad"))
        except Exception as e:
            return redirect(url_for("adminDashborad"))

    return render_template("adminDashborad.html")

@app.route("/all-users-users-table")
def allUsersTable():
    if "admin" not in session:
        return render_template("adminlogin.html")
    return jsonify(addischeretauser.GetCheretaUserDataJson())

@app.route("/adminlogout")
def adminlogout():
    session.pop('admin',None)
    return redirect(url_for('adminlogin'))

@app.route("/item/time/<IID>")
def IIDtime(IID):
    if "logged" in session and session["logged"]==True:
        ok=item.GetItemWithIID(IID)
        if ok==[]:
            return jsonify([])
        return jsonify(ok)
    return redirect("http://127.0.0.1:5000/")

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/logout")
def logout():
    session.pop('status',None)
    session.pop('email',None)
    session.pop('forgot',None)
    session.pop('UID',None)
    session.pop('logged',None)
    return render_template('home.html')

if __name__=="__main__":
    # # to be turned on deployemnt for logging
    # logging.basicConfig(
    #     filename='error.log',  # Log to 'error.log'
    #     level=logging.ERROR,   # Only log errors and critical issues
    #     format='%(asctime)s - %(levelname)s - %(message)s'  # Log format
    # )

    # # Redirect Flask's logger to the root logger
    # handler = logging.FileHandler('error.log')
    # handler.setLevel(logging.DEBUG)
    # app.logger.addHandler(handler)
    app.run(debug=True)
