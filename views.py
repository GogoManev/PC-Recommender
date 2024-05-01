from flask import Blueprint, redirect, render_template, request, url_for

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
    error = request.args.get('error')
    return render_template("pref.html", error=error)


@views.route("/recommender", methods=['POST', 'GET'])
def recommender():
    error = None
    if request.method == 'GET':
        return redirect(url_for('views.preferences', error='Please enter your preferences first!'))
    if request.method == 'POST':
        if request.form['Budget'] < str(0):
            error = 'Please enter a valid number for your budget!'
        if error:
            return redirect(url_for('views.preferences', error=error))

        if int(request.form['Budget']) < 50:
            return "<h1>You are too poor to afford a PC 🤣🤣🤣</h1>\
            <a href='/'>Vurni se</a>"

        return render_template('recommender.html', form_data=request.form)
