from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import load_basicinfo_from_db, load_activities_from_db, upload_offsets, load_offsets_from_db, upload_today
import sqlalchemy
from datetime import datetime

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
  data = load_activities_from_db()
  news = load_offsets_from_db()
  return render_template('points.html', activities=data, offsets=news)


@app.route('/today', methods=['GET'])
def today():
  return render_template('today.html')


@app.route("/upload_offsets", methods=['post'])
def apply_offsets():

  walk = request.form.get('walk')
  carpool = request.form.get('carpool')
  cycle = request.form.get('cycle')
  tree = request.form.get('tree')
  pubtrans = request.form.get('pubtrans')
  recycle = request.form.get('recycle')
  cleanup = request.form.get('cleanup')
  date = datetime.now().strftime('%Y-%m-%d')
  data = {
      'walk': walk,
      'carpool': carpool,
      'cycle': cycle,
      'tree': tree,
      'pubtrans': pubtrans,
      'recycle': recycle,
      'cleanup': cleanup,
      'date': date
  }
  upload_offsets(data)
  return render_template('success_offset.html', success=data)


@app.route("/upload_today", methods=['post'])
def apply_today():

  tempwaste = request.form.get('wasteBins')
  tempkms = request.form.get('carKms')
  waste = "0"
  kms = "0"
  if tempkms == "":
    kms = "0"
  else:
    kms = tempkms
  if tempwaste == "":
    waste = "0"
  else:
    waste = tempwaste
  meal = request.form.get('meal')
  laundry = request.form.get('laundry')
  utensils = request.form.get('utensils')

  date = datetime.now().strftime('%Y-%m-%d')
  data = {
      'waste': waste,
      'kms': kms,
      'meal': meal,
      'laundry': laundry,
      'utensils': utensils,
      'date': date
  }
  upload_today(data)

  return render_template('success_today.html', success=data)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
