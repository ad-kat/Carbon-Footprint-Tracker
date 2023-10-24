from flask import Flask, render_template

app = Flask(__name__)

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


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
