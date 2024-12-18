from flask import Flask, request
from prometheus_client import Counter, generate_latest, multiprocess, CollectorRegistry
import random

app = Flask(__name__)

REQUESTS = Counter('app_requests_total', 'Total number of requests to the app')
RANDOM_NUMBER_COUNTER = Counter('random_number_counter_total', 'Number of random numbers generated')

@app.before_request
def increment_request_count():
    REQUESTS.inc()

@app.route('/')
def hello_world():
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
            <h1>Totally Accurate Home</h1>
            <p>Welcome to my website</p>
            <p>Click on the links above to perform some operations: add or multiply two numbers, or generate a random number between 1-1000</p>
            <p>Project by Eshan Gulati, Khang Vo, Al Hamid Arath</p>
        </main>
    </body>
    </html>
    """

@app.route('/add', methods=['GET', 'POST'])
def add():
    num1 = request.form.get('num1') if request.method == 'POST' else ''
    num2 = request.form.get('num2') if request.method == 'POST' else ''
    sum = int(num1) + int(num2) if num1 and num2 else 0
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
def random_number():
    RANDOM_NUMBER_COUNTER.inc()
    num = random.randint(1, 1000)
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
@app.route('/metrics')
def metrics():
    # Expose Prometheus metrics at /metrics endpoint
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry)



if __name__ == '__main__':
    # Log all available routes
    print("\nAvailable routes in the Flask app:")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Route: {rule.rule}")
    app.run(host='0.0.0.0', port=80, debug=True,use_reloader=False)
