from flask import Blueprint, render_template

views = Blueprint(__name__, "views")

text1 = "WOW"


@views.route("/")
def home():
    return render_template("index.html", text=text1, test=test())


@views.route("/test")
def test():
    return render_template("test.html")
