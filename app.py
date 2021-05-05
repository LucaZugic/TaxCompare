from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates

app = Flask(__name__)

convert = CurrencyRates().convert


@app.route('/', methods=['GET'])
def index():
    success = 'alert-lower'
    return render_template('index.html', success=success)


@app.route('/submit', methods=['POST'])
def compute():

    with_NI = "& Nation Insurance"
    
    if request.method == 'POST':

        income_1 = request.form['income_1']
        currency_1 = request.form['currency_1'] 
        region_1 = request.form['region_1']
        income_2 = request.form['income_2']
        currency_2 = request.form['currency_2']
        region_2 = request.form['region_2']

        if income_1 != '' and income_2 != '':
            income_1 = float(income_1)
            income_2 = float(income_2)
        elif income_1 != '':
            income_1 = float(income_1)
            if region_1 == 'Scot0':
                if currency_1 != 'GBP':
                    burden = convert('GBP', currency_1, compute_tax_scotland(convert(currency_1, 'GBP', income_1)))
                else:
                    burden = compute_tax_scotland(income_1)
            elif region_1 == 'Scot1':
                pass
            elif region_1 == 'Eng0':
                pass
            elif region_1 == 'Eng1':
                pass

            net_income = income_1 - burden
            return render_template('index.html', annual_net_income_1=net_income, monthly_net_income_1=round(net_income/12,2), cur1=currency_1,
            annual_tax_1=burden, monthly_tax_1=round(burden/12,2))
        elif income_2 != '':
            income_2 = float(income_2)
        else:
            alert_message = "Please enter at least one income."
            return render_template('index.html', missing_value_alert_message=alert_message)

        return render_template('index.html', annual_net_income_1=income_1, annual_net_income_2=income_2)
    
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



