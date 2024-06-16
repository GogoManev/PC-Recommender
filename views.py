from flask import Blueprint, redirect, render_template, request, url_for
from abc import ABC, abstractmethod

views = Blueprint(__name__, "views")

form_data = {
    'key1(field1_name)': 'value1(field1_value)',
    'key2(field2_name)': 'value2(field2_value)',
    'key3(field3_name)': 'value3(field3_value)',
    'key4(field4_name)': 'value4(field4_value)',
}


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/about")
def about():
    return render_template("about.html")


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
    index = None
    system = None
    budget = int(request.form['Budget'])
    usage = request.form["Usage"]
    portability = request.form['Portability']
    os = request.form["OS"]
    prebuilt = request.form['Prebuilt']

    if request.method == 'GET':
        return redirect(url_for('views.preferences', error='Please enter your preferences first!'))
    if request.method == 'POST':
        if budget < 0:
            error = 'Please enter a valid number for your budget!'

        if 0 <= budget < 380:
            return "<h1>You are too poor to afford a PC 🤣🤣🤣</h1> \
            <a href='https://www.jobs.bg/'> Fix that </a> \
            <br> \
            <a href='/'>Vurni se</a>"

        if portability == 'No' and prebuilt != 'Yes':
            system = Computer(pc, links, image)
            index = system.picker(budget, usage, os)
            pc, links, image = system.file('configs.txt', index)
        elif portability == 'No' and prebuilt != 'No':
            system = Prebuilt(pc, links, image)
            index = system.picker(budget, usage, os)
            pc, links, image = system.file('prebuilts.txt', index)
        elif portability == 'Yes':
            system = Laptop(pc, links, image)
            index = system.picker(budget, usage, os)
            pc, links, image = system.file('laptops.txt', index)
        else:
            error = 'Please try again later!'

        if error:
            return redirect(url_for('views.preferences', error=error))
        else:  
            return render_template('recommender.html', form_data=request.form, PC=pc, links=links, image=image)


class System():
    def __init__(self, pc, links, image):
        self._pc = pc
        self._links = links
        self._image = image

    def picker(self, budget, usage, os):
        index = None

        if 380 <= budget < 620:
            index = 0
        elif 620 <= budget < 920:
            index = 1
        elif 920 <= budget < 1290:
            index = 2
        elif 1290 <= budget < 1900:
            if usage == 'Gaming':
                index = 3
            else:
                index = 4

        elif 1900 <= budget:
            if os == "Windows" or usage == 'Gaming':
                index = 5
            elif os == "macOS" or usage != "Gaming":
                index = 6

        if os == "macOS":
            index = 6

        return index

    @abstractmethod
    def file(self, file, index):
        pass


class Prebuilt(System):
    def file(self, file, index):
        config = open(file, 'r')
        lines = config.readlines()

        Brand, Model, Price, CPU, RAM, GPU, VRAM, Motherboard, Storage, PSU, Case, Cooler, OS, Link, Image = lines[
            index].strip().split(', ')
        self._pc = {'Brand': Brand, "Model": Model, "Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM,
                    "GPU VRAM": VRAM, "Motherboard": Motherboard, "Storage": Storage, "Power Supply Unit": PSU,
                    "Computer Case": Case, "Cooler": Cooler, "Operating System": OS}
        self._links = {'Computer Link': Link}
        self._image = Image

        return self._pc, self._links, self._image


class Computer(System):
    def file(self, file, index):
        config = open(file, 'r')
        lines = config.readlines()

        (Price, CPU, RAM, GPU, VRAM, Motherboard, Storage, PSU, Case, Cooler, CPUl, Cl, Ml, RAMl, GPUl,
         Sl, PSUl, Casel, Image) = lines[index].strip().split(', ')
        self._pc = {"Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM, "GPU VRAM": VRAM,
                    "Motherboard": Motherboard, "Storage": Storage, "Power Supply Unit": PSU,
                    "Computer Case": Case, "Cooler": Cooler}
        self._links = {"CPU Link": CPUl, "Cooler Link": Cl, "Motherboard Link": Ml, "RAM Link": RAMl,
                       "GPU Link": GPUl, "Storage Link": Sl, "PSU Link": PSUl, "Case Link": Casel}
        self._image = Image

        return self._pc, self._links, self._image


class Laptop(System):
    def file(self, file, index):
        config = open(file, 'r')
        lines = config.readlines()

        (Brand, Model, Price, CPU, RAM, GPU, VRAM, Storage, DisplaySize, DisplayRes, DisplayBri,
         Battery, Camera, Bluetooth, wifi, Weight, PA, OS, Color, Link, Image) = lines[index].strip().split(', ')
        self._pc = {'Brand': Brand, "Model": Model, "Price": Price, 'CPU': CPU, 'GPU': GPU, 'RAM': RAM,
                    "GPU VRAM": VRAM, "Storage": Storage, "Display": DisplaySize, "Resolution": DisplayRes,
                    "Display Brightness": DisplayBri, "Battery": Battery, "Camera": Camera, "Bluetooth": Bluetooth,
                    "Wi-FI": wifi, "Laptop Weight": Weight, "Power Adapter": PA, "Operating System": OS,
                    "Laptop Color": Color}
        self._links = {'Laptop Link': Link}
        self._image = Image

        return self._pc, self._links, self._image
