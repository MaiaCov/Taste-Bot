from flask import Flask, redirect, sessions, url_for, render_template, request, session, flash
import sys 
import os
sys.path.append(os.path.abspath("./function"))
from function import *


app = Flask(__name__) 
app.secret_key = "erdgibgvjdfgvgrfder9e76d87g68fc9xgvdyx7b"  #secret key, dont touch

@app.route("/") #This is the main page
def red():  #red==redirect
    return redirect(url_for("home")) #Going to redirect the page to /home

@app.route("/home", methods=["POST", "GET"]) #The methods is needed here because the /home works with POST requests
def home():
    if "name" in session:  #checks if the user is already in the session
        return redirect(url_for("choice"))  #if so is going to auto-redirect to the start page 
    if request.method == "POST":  #Checks if the user POST something in the page (clicked in a button)
        if check_email(request.form.get("email")):
            session["email"] = request.form["email"]
            session["name"] = request.form["username"]  #Store the user Name in a session (temporaly until the user leaves the browser or click in the logout button)
            return redirect(url_for("choice"))  #When the name is stored in the session, its redirect to the start page 
        else:
            flash("Your email is not valid.", "+info")
            return redirect(url_for("home"))
    else:      
        return render_template("index.html")  #render the html file


@app.route("/choice", methods=["POST", "GET"])  #The start page is going to work with POST request so is needed to add the POST method
def choice():
    if "choice" in session:
        return redirect(url_for("start"))
    elif request.method == "POST":  #Checks if the user clicked in a button(if the user sends a post request)
        session["choice"] = request.form.get("submit_button")
        return redirect(url_for("start"))
    else:
        return render_template("choice.html")


@app.route("/start", methods=["POST", "GET"])  #The start page is going to work with POST request so is needed to add the POST method
def start():
    if request.method == "POST":  #Checks if the user clicked in a button(if the user sends a post request)
        if request.form.get("logout_button") == "logout":  #Checks if the user clicked in the logout button(In the html with the name "logout_button")
            return redirect(url_for("logout"))  #redirect the user to the logout page
        elif request.form.get("submit_button") == "submit":  #Checks ift the user clicked in the submit button(In the html with the name "submit_button")
            if request.form.get("flav1").split() and request.form.get("flav2").split() and request.form.get("flav3").split():
                session["flav0"] = request.form.get("flav1")  #store the user flavor1 in the session
                session["flav1"] = request.form.get("flav2")  #store the user flavor2 in the session
                session["flav2"] = request.form.get("flav3")  #store the user flavor3 in the session
                return redirect(url_for("flavour"))  #redirect the user to the /flavour page
            else:
                flash("Write in all parameters.", "+info")
                return redirect(url_for("home"))

    if "name" in session:  #If the user is in the session, is going to render the html file and let the user there
        return render_template("start.html")  #render the html file

    else:  #If the user is not in the session is going to be redirect to the home page
        return redirect(url_for("home"))  #redirecting to the home page



@app.route("/flavour", methods=["POST", "GET"])  #The flavour page needs the "POST" method because was the button to logout
def flavour():
    if "flav0" not in session:
        return redirect(url_for("home"))
    if request.method == "POST":  #checks if the user is sending a POST request (clicked in a button)
        if request.form.get("logout_button") == "logout":  #checks if the user clicked in the logout button
            return redirect(url_for("logout"))  #redirect the user to the logout page
    else:
        return render_template("flavour.html")   #render the html file


@app.route("/logout")  #logout page, this page doesnt have html file because the user never is going to see this page, is auto-redirect to the home page
def logout():
    print(session)
    session.clear()
    flash("You have been logged out.", "+info")
    return redirect(url_for("home"))  #redirects the user to the home page so they can create another session



@app.route("/fail") #Fail page, didnt code yet, when the user goes to a diferent url, it should be redirect to this page
def fail():
    return render_template("fail.html")  #render the html file



if __name__ == "__main__":  #The webserver starts this way
    app.run(debug=True)  #webserver starts running with the debug True
