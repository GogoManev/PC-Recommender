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
    return render_template("index.html", text=text1)


@views.route("/preferences")
def preferences():
    error = request.args.get('error')
    return render_template("pref.html", error=error)


@views.route("/recommender", methods=['POST', 'GET'])
def recommender():
    error = None
    PC = None
    if request.method == 'GET':
        return redirect(url_for('views.preferences', error='Please enter your preferences first!'))
    if request.method == 'POST':
        if request.form['Budget'] < str(0):
            error = 'Please enter a valid number for your budget!'

        if int(request.form['Budget']) < 50:
            return "<h1>You are too poor to afford a PC 🤣🤣🤣</h1>\
            <a href='/'>Vurni se</a>"

        if request.form['Portability'] == 'No':
            PC = pickAComputer('configs.txt')
        elif request.form['Portability'] == 'Yes':
            pass
        else:
            error = 'Please try again later!'

        if error:
            return redirect(url_for('views.preferences', error=error))

        return render_template('recommender.html', form_data=request.form, PC=PC)


def pickAComputer(file):
    config = open(file, 'r')
    lines = config.readlines()
    index = None
    PC = None

    for line in lines:
        if 50 <= int(request.form['Budget']) < 300:
            index = 0
        elif 300 <= int(request.form['Budget']) < 700:
            index = 1
        elif 700 <= int(request.form['Budget']):
            index = 2

        if index is not None:
            GPU, CPU, RAM = lines[index].strip().split(', ')
            PC = {'GPU': GPU, 'CPU': CPU, 'RAM': RAM}

    return PC
