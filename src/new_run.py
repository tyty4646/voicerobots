from flask import Flask
from flask import render_template, request, redirect, jsonify, make_response
from motors import Motors

app = Flask(__name__)
m = Motors(20, 21, 16, 12, 1, 7)

@app.route('/control')
def control():
    return render_template('index.html')

def handle_data(x, y):
    # normalize x and y from [-100, 100] to the interval [-1, 1]
    x = float(x) / 100.0
    y = float(y) / 100.0

    m.set_duty_cycle(x, y)

@app.route('/control/data', methods=["POST"])
def control_data():
    req = request.get_json()
    handle_data(req['x'], req['y'])
    return "Thx brah"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

