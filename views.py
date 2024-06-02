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
    pc = None
    links = None
    image = None

    if request.method == 'GET':
        return redirect(url_for('views.preferences', error='Please enter your preferences first!'))
    if request.method == 'POST':
        if request.form['Budget'] < str(0):
            error = 'Please enter a valid number for your budget!'

        if 0 < int(request.form['Budget']) < 50:
            return "<h1>You are too poor to afford a PC 🤣🤣🤣</h1> \
            <a href='https://www.jobs.bg/'> Fix that </a> \
            <br> \
            <a href='/'>Vurni se</a>"

        if (request.form['Portability'] == 'No' and request.form['Prebuilt'] == 'No' or
                request.form['Prebuilt'] == "Don't Care"):
            pc, links, image = pickAComputer('configs.txt')
        elif (request.form['Portability'] == 'No' and request.form['Prebuilt'] == 'Yes' or
              request.form['Prebuilt'] == "Don't Care"):
            pc, links, image = pickAComputer('prebuilts.txt')
        elif request.form['Portability'] == 'Yes':
            pc, links, image = pickAComputer('laptops.txt')
        else:
            error = 'Please try again later!'

        if error:
            return redirect(url_for('views.preferences', error=error))

        return render_template('recommender.html', form_data=request.form, PC=pc, links=links, image=image)


def pickAComputer(file):
    config = open(file, 'r')
    lines = config.readlines()
    index = None
    pc = None
    links = None
    image = None

    for line in lines:
        if 380 <= int(request.form['Budget']) < 580:
            index = 0
        elif 580 <= int(request.form['Budget']) < 900:
            index = 1
        elif 900 <= int(request.form['Budget']) < 1300:
            index = 2
        elif 1300 <= int(request.form['Budget']) < 1700:
            if request.form['Usage'] == 'Gaming':
                index = 3
            else:
                index = 4
        elif 1700 <= int(request.form['Budget']) < 2100:
            if request.form['OS'] == "Windows" or request.form['Usage'] == 'Gaming':
                index = 5
            elif request.form['OS'] == "macOS" or request.form['Usage'] != "Gaming":
                index = 6

        if request.form['OS'] == "macOS":
            index = 6

        if index is not None:
            if request.form['Portability'] == 'No':
                if request.form['Prebuilt'] == 'Yes':
                    Brand, Model, Price, CPU, RAM, GPU, VRAM, Motherboard, Storage, PSU, Case, Cooler, OS, Link, Image = \
                    lines[
                        index].strip().split(', ')
                    pc = {'Brand': Brand, "Model": Model, "Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM,
                          "GPU VRAM": VRAM, "Motherboard": Motherboard, "Storage": Storage, "Power Supply Unit": PSU,
                          "Computer Case": Case, "Operating System": OS}
                    links = {'Computer Link': Link}
                    image = Image
                elif request.form['Prebuilt'] == 'No':
                    (Price, CPU, RAM, GPU, VRAM, Motherboard, Storage, PSU, Case, Cooler, CPUl, Cl, Ml, RAMl, GPUl,
                     Sl, PSUl, Casel, Image) = lines[index].strip().split(', ')
                    pc = {"Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM, "GPU VRAM": VRAM,
                          "Motherboard": Motherboard, "Storage": Storage, "Power Supply Unit": PSU,
                          "Computer Case": Case}
                    links = {"CPU Link": CPUl, "Cooler Link": Cl, "Motherboard Link": Ml, "RAM Link": RAMl,
                             "GPU Link": GPUl, "Storage Link": Sl, "PSU Link": PSUl, "Case Link": Casel}
                    image = Image
                # if request.form['Prebuilt'] == "Don't Care":
                # kato napravq vsichki konfiguracii
            else:
                (Brand, Model, Price, CPU, RAM, GPU, VRAM, Storage, DisplaySize, DisplayRes, DisplayBri,
                 Battery, Camera, Bluetooth, wifi, Weight, PA, OS, Color, Link, Image) = lines[index].strip().split(
                    ', ')
                pc = {'Brand': Brand, "Model": Model, "Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM,
                      "GPU VRAM": VRAM, "Storage": Storage, "Display": DisplaySize, "Resolution": DisplayRes,
                      "Display Brightness": DisplayBri, "Battery": Battery, "Camera": Camera, "Bluetooth": Bluetooth,
                      "Wi-FI": wifi, "Laptop Weight": Weight, "Power Adapter": PA,
                      "Operating System": OS, "Laptop Color": Color}
                links = {'Laptop Link': Link}
                image = Image

    return pc, links, image
