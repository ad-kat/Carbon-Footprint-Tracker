from flask import Flask, render_template
from database import load_basicinfo_from_db

app = Flask(__name__, template_folder="templates")

RECOMMENDATIONS = [
    {
        'id': 1,
        'desc': "save more on electricity"
    },
    {
        'id': 2,
        'desc': "show about a stroll in the park?"
    },
    {
        'id': 3,
        'desc': "schedule not too busy? try walking to work."
    },
    {
        'id': 4,
        'desc': "Friend reunion parties? CARPOOL!!!"
    },
    {
        'id': 5,
        'desc': "sunny day? Lights off in the morning"
    },
]






@app.route("/")
def hello_world():
  return render_template('dashboard.html', recs=RECOMMENDATIONS)


@app.route('/basicinfo', methods=['GET'])
def basic_info():
  info = load_basicinfo_from_db()
  return render_template('basicinfo.html', basics=info)


@app.route('/offset', methods=['GET'])
def offset():
  return render_template('offset.html')


@app.route('/points', methods=['GET'])
def points():
  return render_template('points.html')


@app.route('/shop', methods=['GET'])
def shop():
  return render_template('shop.html')


@app.route('/today', methods=['GET'])
def today():
  return render_template('today.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
