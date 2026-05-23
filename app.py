from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Allowed math functions
allowed_functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt,
    'log': math.log,
    'exp': math.exp
}


# Safe function evaluator
def evaluate_function(expression, x):

    allowed_names = {
        'x': x,
        'pi': math.pi,
        'e': math.e,
        **allowed_functions
    }

    return eval(
        expression,
        {"__builtins__": {}},
        allowed_names
    )


# Home Route
@app.route('/')
def home():

    return render_template('index.html')


# Calculation Route
@app.route('/calculate', methods=['POST'])
def calculate():

    try:

        # Get user inputs
        function = request.form['function']
        x = float(request.form['x'])
        h = float(request.form['h'])
        method = request.form['method']

        # Prevent division by zero
        if h == 0:

            return render_template(
                'result.html',
                error='Step size h cannot be zero.'
            )

        # FORWARD DIFFERENCE
        if method == 'forward':

            fxh = evaluate_function(function, x + h)
            fx = evaluate_function(function, x)

            derivative = round((fxh - fx) / h, 6)

            formula = "f'(x) = [f(x+h) - f(x)] / h"

            steps = [
                f"f(x+h) = {round(fxh, 6)}",
                f"f(x) = {round(fx, 6)}",
                f"Derivative = ({round(fxh, 6)} - {round(fx, 6)}) / {h}",
                f"Derivative = {derivative}"
            ]

        # BACKWARD DIFFERENCE
        elif method == 'backward':

            fx = evaluate_function(function, x)
            fxh = evaluate_function(function, x - h)

            derivative = round((fx - fxh) / h, 6)

            formula = "f'(x) = [f(x) - f(x-h)] / h"

            steps = [
                f"f(x) = {round(fx, 6)}",
                f"f(x-h) = {round(fxh, 6)}",
                f"Derivative = ({round(fx, 6)} - {round(fxh, 6)}) / {h}",
                f"Derivative = {derivative}"
            ]

        # CENTRAL DIFFERENCE
        elif method == 'central':

            fx1 = evaluate_function(function, x + h)
            fx2 = evaluate_function(function, x - h)

            derivative = round((fx1 - fx2) / (2 * h), 6)

            formula = "f'(x) = [f(x+h) - f(x-h)] / 2h"

            steps = [
                f"f(x+h) = {round(fx1, 6)}",
                f"f(x-h) = {round(fx2, 6)}",
                f"Derivative = ({round(fx1, 6)} - {round(fx2, 6)}) / (2 × {h})",
                f"Derivative = {derivative}"
            ]

        else:

            return render_template(
                'result.html',
                error='Invalid method selected.'
            )

        # Send result to HTML
        return render_template(
            'result.html',
            function=function,
            x=x,
            h=h,
            method=method.capitalize(),
            derivative=derivative,
            formula=formula,
            steps=steps
        )

    except Exception as e:

        return render_template(
            'result.html',
            error=f'Error: {str(e)}'
        )


# Run Flask App
if __name__ == '__main__':

    app.run(debug=True)