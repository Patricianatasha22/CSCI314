from asyncio.windows_events import NULL
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Users, Author, ConferenceChair, Reviewer, SystemAdmin

# Real Time Database
import pyrebase

config = {
    "apiKey": "AIzaSyBFYgCF5NjAuugKkgssw1V1XnlVr9dY5Kw",
    "authDomain": "research-management-syst.firebaseapp.com",
    "databaseURL": "https://research-management-syst-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "projectId": "research-management-syst",
    "storageBucket": "research-management-syst.appspot.com",
    "messagingSenderId": "152013328445",
   "appId": "1:152013328445:web:d47c0136f99861c8509a54",
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

# log in page
def index(request):
    name = database.child('author').child('username').get().val()

    return render(request, 'index.html', {"name": name})

def checkLogin(request):

    if(request.POST):

        selectedRole = request.POST['roleList']

        username = request.POST['username']
        password = request.POST['password']

        if(selectedRole == "Author"):
            # author = Author.getAuthor(username, password)
            db_password = database.child('author').child('password').get().val()
            db_username = database.child('author').child('username').get().val()
            print(db_username)
            if(db_password == password and db_username == username):

                request.session['AuthorLogged'] = database.child('author').child('id').get().val();

                #Redirects to author index
                messages.success(request, "Successfully Logged-in")
                return redirect('authorViewPaper')

            else:
                messages.error(request, "Invalid username or password.")
                return redirect('index')
            
        elif(selectedRole == "Reviewer"):
            db_password = database.child('reviewer').child('password').get().val()
            db_username = database.child('reviewer').child('username').get().val()

            # reviewer = Reviewer.getReviewer(username, password)

            if(db_password == password and db_username == username):

                request.session['ReviewerLogged'] = database.child('reviewer').child('id').get().val();

                messages.success(request, "Successfully Logged-in")
                return redirect('biddedPaper') #TOBEUPDATED

            else:
                messages.error(request, "Invalid username or password.")
                return redirect('index')

        elif(selectedRole == "Conference Chair"):
            # Conf = ConferenceChair.getConferenceChair(username, password)
            db_password = database.child('conferenceChair').child('password').get().val()
            db_username = database.child('conferenceChair').child('username').get().val()

            if(db_password == password and db_username == username):

                request.session['ConfLogged'] = database.child('conferenceChair').child('id').get().val();

                messages.success(request, "Successfully Logged-in")
                return redirect('CCallocationPaper') #TOBEUPDATED

            else:
                messages.error(request, "Invalid username or password.")
                return redirect('index')
        elif(selectedRole == "System Admin"):
            # SysAdmin = SystemAdmin.getSystemAdmin(username, password)
            db_password = database.child('systemAdmin').child('password').get().val()
            db_username = database.child('systemAdmin').child('username').get().val()
            if(db_password == password and db_username == username):

                request.session['SysAdminLogged'] = database.child('systemAdmin').child('id').get().val();

                return redirect('systemAdminPage') #TOBEUPDATED

            else:
                messages.error(request, "Invalid username or password.")
                return redirect('index')

    return redirect('index')