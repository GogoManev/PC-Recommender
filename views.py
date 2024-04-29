from flask import Blueprint, render_template, request

views = Blueprint(__name__, "views")

text1 = "WOW"
form_data = {
    'key1(field1_name)': 'value1(field1_value)',
    'key2(field2_name)': 'value2(field2_value)',
    'key3(field3_name)': 'value3(field3_value)',
    'key4(field4_name)': 'value4(field4_value)',
}


@views.route("/")
def home():
    return render_template("index.html", text=text1, test=test())


@views.route("/test")
def test():
    return render_template('test.html')


@views.route("/preferences")
def preferences():
    return render_template("pref.html")


@views.route("/recommender", methods=['POST', 'GET'])
def recommender():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('recommender.html', form_data=form_data)
