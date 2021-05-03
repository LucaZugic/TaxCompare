from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    currencies = ['GBP £']
    regions = ['England w/ NI', 'England w/o NI', 'Scotland w/ NI', 'Scotland w/o NI']
    return render_template('index.html', currencies=currencies, regions=regions)


@app.route('/compute', methods=['POST', 'GET'])
def compute():
    
    income_1 = request.form.get('inc1', None)
    income_2 = request.form.get('income_2', None)
    currency_1 = request.form.get('currency_1', None)
    currency_2 = request.form.get('currency_2', None)
    region_1 = request.form.get('region_1', None)
    region_2 = request.form.get('region_2', None)
   
    if income_1 != '' and income_2 != '':
        if region_1 == 'England w/ NI':
            tax_1 = compute_tax_england(income_1)
            ni_1 = compute_ni_england(income_1)
        elif region_1 == 'England w/o NI':
            tax_1 = compute_tax_england(income_1)
            return render_template('index.html', tax_1=tax_1)
        elif region_1 == 'Scotland w/ NI':
            tax_1 = compute_tax_scotland(income_1)
            ni_1 = compute_ni_scotland(income_1)
        elif region_1 == 'Scotland w/o NI':
            tax_1 = compute_tax_scotland(income_1)
        if region_2 == 'England w/ NI':
            tax_2 = compute_tax_england(income_2)
            ni_2 = compute_ni_england(income_1)
        elif region_2 == 'England w/o NI':
            tax_2 = compute_tax_england(income_2)
        elif region_2 == 'Scotland w/ NI':
            tax_2 = compute_tax_scotland(income_2)
            ni_2 = compute_ni_scotland(income_2)
        elif region_2 == 'Scotland w/o NI':
            tax_2 = compute_tax_scotland(income_2)


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



