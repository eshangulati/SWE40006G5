from flask import Flask, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # Add this line to expose metrics

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
                <h1>Home</h1>
                <p>Welcome to my website</p>
                <p>Click on the links above to perform some operations: add or multiply two numbers, or generate a random number between 1-1000</p>
            </main>
        </body>
        </html>
    """

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num1 = num1 if num1 else 0

        num2 = request.form.get('num2')
        num2 = num2 if num2 else 0

        sum = int(num1) + int(num2)

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
                    <input type="number" name="num1" placeholder="First number" value="{num1 if request.method == 'POST' else ''}"> <br>
                    <input type="number" name="num2" placeholder="Second number" value="{num2 if request.method == 'POST' else ''}"> <br>
                    <input type="submit" name="submit" value="Add">
                </form>
                {'<p>The sum of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(sum) + '</p>' if request.method == 'POST' else ''}
            </main>
        </body>
        </html>
    """

@app.route('/mul', methods=['GET', 'POST'])
def mul():
    if request.method == 'POST':
        num1 = request.form.get('num1')
        num1 = num1 if num1 else 0

        num2 = request.form.get('num2')
        num2 = num2 if num2 else 0

        product = int(num1) * int(num2)

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
                    <input type="number" name="num1" placeholder="First number" value="{num1 if request.method == 'POST' else ''}"> <br>
                    <input type="number" name="num2" placeholder="Second number" value="{num2 if request.method == 'POST' else ''}"> <br>
                    <input type="submit" name="submit" value="Multiply">
                </form>
                {'<p>The product of ' + str(num1) + ' and ' + str(num2) + ' is ' + str(product) + '</p>' if request.method == 'POST' else ''}
            </main>
        </body>
        </html>
    """

@app.route('/random')
def random():
    import random
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
