import logging
from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics
import random

app = Flask(__name__)

# Setup Prometheus Metrics
metrics = PrometheusMetrics(app, path='/metrics')

# Static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

# Setup logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

@app.before_request
def log_request_info():
    logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', request.get_data())

@app.route('/')
def hello_world():
    logging.info('Home route accessed')
    return """
    <!DOCTYPE html>
    <html data-theme="light">
    <head>
        <title>Home</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li>Home</li>
                    <li><a href="/add">Add</a></li>
                    <li><a href="/mul">Multiply</a></li>
                    <li><a href="/random">Random</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>Home</h1>
            <p>Welcome to my website</p>
            <p>Click on the links above to perform some operations: add or multiply two numbers, or generate a random number between 1-1000</p>
        </main>
    </body>
    </html>
    """

@app.route('/add', methods=['GET', 'POST'])
def add():
    num1 = request.form.get('num1') if request.method == 'POST' else ''
    num2 = request.form.get('num2') if request.method == 'POST' else ''
    sum = int(num1) + int(num2) if num1 and num2 else 0
    logging.info(f'Addition: {num1} + {num2} = {sum}')
    return f"""
    <!DOCTYPE html>
    <html data-theme="light">
    <head>
        <title>Add Two Numbers</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li>Add</li>
                    <li><a href="/mul">Multiply</a></li>
                    <li><a href="/random">Random</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>Add Two Numbers</h1>
            <form method="post" action="add">
                <input type="number" name="num1" placeholder="First number" value="{num1}">
                <br>
                <input type="number" name="num2" placeholder="Second number" value="{num2}">
                <br>
                <input type="submit" name="submit" value="Add">
            </form>
            {'<p>The sum of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(sum) + '</p>' if request.method == 'POST' else ''}
        </main>
    </body>
    </html>
    """

@app.route('/mul', methods=['GET', 'POST'])
def mul():
    num1 = request.form.get('num1') if request.method == 'POST' else ''
    num2 = request.form.get('num2') if request.method == 'POST' else ''
    product = int(num1) * int(num2) if num1 and num2 else 0
    logging.info(f'Multiplication: {num1} * {num2} = {product}')
    return f"""
    <!DOCTYPE html>
    <html data-theme="light">
    <head>
        <title>Multiply Two Numbers</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/add">Add</a></li>
                    <li>Multiply</li>
                    <li><a href="/random">Random</a></li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>Multiply Two Numbers</h1>
            <form method="post" action="mul">
                <input type="number" name="num1" placeholder="First number" value="{num1}">
                <br>
                <input type="number" name="num2" placeholder="Second number" value="{num2}">
                <br>
                <input type="submit" name="submit" value="Multiply">
            </form>
            {'<p>The product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(product) + '</p>' if request.method == 'POST' else ''}
        </main>
    </body>
    </html>
    """

@app.route('/random')
@metrics.do_not_track()
@metrics.counter('random_number_counter', 'Number of random numbers generated')
def random_number():
    num = random.randint(1, 1000)
    logging.info(f'Generated random number: {num}')
    return f"""
    <!DOCTYPE html>
    <html data-theme="light">
    <head>
        <title>Random Number</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.classless.min.css">
    </head>
    <body>
        <header>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/add">Add</a></li>
                    <li><a href="/mul">Multiply</a></li>
                    <li>Random</li>
                </ul>
            </nav>
        </header>
        <main>
            <h1>Random Number</h1>
            <p>Your random number is {num}</p>
            <a href="/random">Generate new random number</a>
        </main>
    </body>
    </html>
    """

@app.route('/test')
@metrics.counter('test_counter', 'Test counter')
def test():
    logging.info('Test endpoint accessed')
    return 'Test successful'

if __name__ == '__main__':
    # Log all available routes
    print("\nAvailable routes in the Flask app:")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Route: {rule.rule}")
        logging.info(f"Endpoint: {rule.endpoint}, Route: {rule.rule}")

    app.run(host='0.0.0.0', port=80, debug=True)
