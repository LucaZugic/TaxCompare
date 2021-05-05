from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates

app = Flask(__name__)

convert = CurrencyRates().convert


@app.route('/', methods=['GET'])
def index():
    success = 'alert-lower'
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def compute():

    
    
    if request.method == 'POST':

        incomes = [request.form['income_1'], request.form['income_2']]
        currency = (request.form['currency_1'], request.form['currency_2'])
        region = (request.form['region_1'], request.form['region_2'])
        burden = [0, 0]
        percentage_burden = [0, 0]
        net_income = [0, 0]
        alert_types = ('alert-higher', 'alert-lower', 'alert-equal')
        alert = ['', '']
        ni_extension = ['', '']

        has_income = [False, False]

        for i, income in enumerate(incomes):
            if income != '':
                has_income[i] = True
                income = float(income)

                if region[i] == 'Scot0':
                    if currency != 'GBP':
                        burden[i] = convert('GBP', currency[i], compute_tax_scotland(convert(currency[i], 'GBP', income)))
                    else:
                        burden[i] = compute_tax_scotland(income)
                elif region[i] == 'Scot1':
                    ni_extension[i] = "& Nation Insurance"
                    if currency != 'GBP':
                        burden[i] = convert('GBP', currency[i], (compute_tax_scotland(convert(currency[i], 'GBP', income)) + compute_ni(convert(currency[i], 'GBP', income))))
                    else:
                        burden[i] = compute_tax_scotland(income)
                elif region[i] == 'Eng0':
                    if currency != 'GBP':
                        burden[i] = convert('GBP', currency[i], compute_tax_england(convert(currency[i], 'GBP', income)))
                    else:
                        burden[i] = compute_tax_england(income)
                elif region[i] == 'Eng1':
                    ni_extension[i] = "& Nation Insurance"
                    if currency != 'GBP':
                        burden[i] = convert('GBP', currency[i], (compute_tax_england(convert(currency[i], 'GBP', income)) + compute_ni(convert(currency[i], 'GBP', income))))
                    else:
                        burden[i] = compute_tax_england(income) + compute_ni(income)
            
                net_income[i] = round(income - burden[i], 2)
                percentage_burden [i] = round((burden[i] / income) * 100, 2)

        if has_income[0] and has_income[1]:

            net_income_difference = net_income[1] - net_income[0]

            if net_income_difference < 0:
                income_alert[0] = alert_types[0]
                income_alert[1] = alert_types[1]
            elif net_income_difference > 0:
                income_alert[0] = alert_types[1]
                income_alert[1] = alert_types[0]
            else:
                income_alert[0] = alert_types[2]
                income_alert[1] = alert_types[2]

            tax_percentage_difference = percentage_burden[1] - percentage_burden[0]
            
            if tax_percentage_difference < 0:
                perc_alert[0] = alert_types[0]
                perc_alert[1] = alert_types[1]
            elif tax_percentage_difference > 0:
                perc_alert[0] = alert_types[1]
                perc_alert[1] = alert_types[0]
            else:
                perc_alert[0] = alert_types[2]
                perc_alert[1] = alert_types[2]

            tax_difference = burden[1] - burden[0]

            if tax_difference < 0:
                tax_alert[0] = alert_types[0]
                tax_alert[1] = alert_types[1]
            elif tax_difference > 0:
                tax_alert[0] = alert_types[1]
                tax_alert[1] = alert_types[0]
            else:
                tax_alert[0] = alert_types[2]
                tax_alert[1] = alert_types[2]

            if currency[0] != currency[1]:
                pass
            else:
                return render_template('index.html',
                    # Income 1:
                    annual_net_income_1=net_income[0],
                    monthly_net_income_1=round(net_income[0] / 12, 2),
                    cur1=currency[0],
                    ni_extension_1=ni_extension[0],
                    tax_alert_1=tax_alert[0],
                    percentage_alert_1=perc_alert[0],
                    percentage_tax_1=str(percentage_burden[0]) + " %",
                    annual_tax_1=round(burden[0], 2),
                    monthly_tax_1=round(burden[0] / 12, 2),
                    # Differences:
                    annual_net_difference=abs(net_income[1] - net_income[0]),
                    monthly_net_difference=round(abs(net_income[1] - net_income[0]) / 12, 2),
                    percentages_difference=str(abs(percentage_burden[1] - percentage_burden[0])) + " %",
                    annual_tax_difference=abs(burden[1] - burden[0]),
                    monthly_tax_difference=round(abs(burden[1] - burden[0]) / 12, 2),
                    difference_currency=currency[0],
                    # Income 2:
                    annual_net_income_2=net_income[1],
                    monthly_net_income_2=round(net_income[1] / 12, 2),
                    cur2=currency[1],
                    ni_extension_2=ni_extension[1],
                    tax_alert_2=tax_alert[1],
                    percentage_alert_2=perc_alert[1],
                    percentage_tax_2=str(percentage_burden[1]) + " %",
                    annual_tax_2=round(burden[1], 2),
                    monthly_tax_2=round(burden[1] / 12, 2))
        elif has_income[0]:
            return render_template('index.html', annual_net_income_1=net_income[0], monthly_net_income_1=round(net_income[0] / 12, 2), cur1=currency[0],
            ni_extension_1=ni_extension[0], percentage_tax_1=str(percentage_burden[0]) + " %", annual_tax_1=round(burden[0], 2), monthly_tax_1=round(burden[0] / 12, 2))
        elif has_income[1]:
            return render_template('index.html', annual_net_income_2=net_income[1], monthly_net_income_2=round(net_income[1] / 12, 2), cur2=currency[1],
            ni_extension_2=ni_extension[1], percentage_tax_2=str(percentage_burden[1]) + " %", annual_tax_2=round(burden[1], 2), monthly_tax_2=round(burden[1] / 12, 2))
        else:
            alert_message = "Please enter at least one income."
            return render_template('index.html', missing_value_alert_message=alert_message)
        
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
    elif income <= 100000:
        return (income - 43663) * .41 + (43663 - 25296) * .21 + (25296 - 14667) * .2 + (14667 - 12570) * .19
    elif income <= 125140:
        return (income - 43663) * .41 + (43663 - 25296) * .21 + (25296 - 14667) * .2 + (14667 - (12570 - (income-100000)/2)) * .19
    elif income <= 150000:
        return (income - 43663) * .41 + (43663 - 25296) * .21 + (25296 - 14667) * .2 + 14667 * .19
    else:
        return (income - 150000) * .46 +(150000 - 43663) * .41 + (43663 - 25296) * .21 + (25296 - 14667) * .2 + 14667 * .19


def compute_tax_england(income):
    if income <= 12570:
        return 0
    elif income <= 50270:
        return (income - 12570) * .2
    elif income <= 100000:
        return (income - 50270) * .4 + (50270 - 12570) * .2
    elif income <= 125140:
        return (income - 50270) * .4 + (50270 - (12570 - (income-100000)/2)) * .2
    elif income <= 150000:
        return (income - 50270) * .4 + (43663 - 25296) * .21 + 25296 * .2
    else:
        return (income - 150000) * .45 + (150000 - 50270) * .4 + (50270 - 25296) * .2


def compute_ni(income):
    monthly_income = income / 12
    if monthly_income <= 797:
        return 0
    elif monthly_income <= 4189:
        return (monthly_income - 797) * .12 * 12
    else:
        return ((4189 - 797) * .12 + (monthly_income - 4189) * .02) * 12


if __name__ == "__main__":
    app.run(debug=True)

