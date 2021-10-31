from flask import Flask, redirect, sessions, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "erdgibgvjdfgvgrfder9e76d87g68fc9xgvdyx7b"

@app.route("/")
def red():
    return redirect(url_for("home"))

@app.route("/home", methods=["POST", "GET"])
def home():
    if "name" in session:
        return redirect(url_for("start"))
    if request.method == "POST":
        user = request.form["username"]
        session["name"] = user
        return redirect(url_for("start"))
    else:      
        return render_template("index.html") 


@app.route("/fail")
def fail():
    return render_template("fail.html")


@app.route("/start", methods=["POST", "GET"])
def start():
    if request.method == "POST":
        if request.form.get("logout_button") == "logout":
            return redirect(url_for("logout"))
        elif request.form.get("submit_button") == "submit":
            session["flav0"] = request.form.get("flav1")
            session["flav1"] = request.form.get("flav2")
            session["flav2"] = request.form.get("flav3")
            return redirect(url_for("flavour"))

    if "name" in session:
        return render_template("start.html")

    else:
        return redirect(url_for("home"))

@app.route("/logout")
def logout():
    print(session["name"])
    print(session["flav0"],session["flav1"],session["flav2"])
    session.pop("name", None)
    session.pop("flav", None)
    return redirect(url_for("home"))

@app.route("/flavour", methods=["POST", "GET"])
def flavour():
    if request.method == "POST":
        if request.form.get("logout_button") == "logout":
            return redirect(url_for("logout"))
    else:
        return render_template("flavour.html") 


if __name__ == "__main__":
    app.run(debug=True)
