from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    currencies = ['GBP £', 'EUR €', 'CHF -', 'USD $']
    regions = ['England w/ NI', 'England w/o NI', 'Scotland w/ NI', 'Scotland w/o NI', 'Germany', 'Switzerland', 'Texas', 'New York']
    return render_template('index.html', currencies=currencies, regions=regions)


@app.route('/compute', methods=['POST'])
def compute():
    income = request.form['income']
    region = request.form['region']
    return 


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


def computer_ni_scotland():
    pass


if __name__ == "__main__":
    app.run(debug=True)



