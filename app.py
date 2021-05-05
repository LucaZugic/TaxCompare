from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates

app = Flask(__name__)

convert = CurrencyRates().convert


@app.route('/', methods=['GET'])
def index():
    success = 'alert-lower'
    return render_template('index.html', success=success)


@app.route('/compute', methods=['POST'])
def form1():

    with_NI = "& Nation Insurance"
    
    if request.method == 'POST':

        income_1 = float(request.form['income_1'])
        currency_1 = request.form['currency_1'] 
        region_1 = request.form['region_1']

        return render_template('index.html', anual_net_income_1 = income_1)
    
    else:
        return render_template('index.html')


@app.route('/form2', methods=['POST'])
def form2():
    print(income_1)
    with_NI = "& Nation Insurance"
    
    if request.method == 'POST':

        income_1 = float(request.form['income_2'])
        currency_1 = request.form['currency_2'] 
        region_1 = request.form['region_2']

        return render_template('index.html')
    
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


def compute_tax_scotland(income):
    if income <= 12570:
        return 0
    elif income <= 14667:
        return (income - 12570) * .19
    elif income <= 25296:
        return (income - 14667) * .2 + (14667 - 12570) * .19
    elif income <= 43663:
        return (income - 25296) * .21 + (25296 - 14667) * .2 + (14667 - 12570) * .19
    elif income <= 150000:
        return (income - 43663) * .41 + (43663 - 25296) * .21 + (25296 - 14667) * .2 + (14667 - 12570) * .19


def compute_ni_scotland():
    pass


if __name__ == "__main__":
    app.run(debug=True)



