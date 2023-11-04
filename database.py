from sqlalchemy import create_engine, text
from datetime import datetime

db_string = "mysql+pymysql://dm0q0fvgm2t9jb5ewrh5:pscale_pw_XrPoK4stnCYAtbxGAl2vLBMIvTYoyU4ZmYiFyW6XBTc@aws.connect.psdb.cloud/carbon-footprint?charset=utf8mb4"
engine = create_engine(db_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_basicinfo_from_db():
  with engine.connect() as conn:
    query = "select users.user_id,username,fullname,email_id,carbon_emission,measurement_date,total_members,house_size,waste_production from users, carbon_footprint, household_data where users.user_id=1 and carbon_footprint.user_id=1 and household_data.user_id=1"
    result = conn.execute(text(query))

    info = []
    for row in result.all():
      info.append(list(row))
    finfo = []
    for row in info:
      newrow = []
      for item in row:
        newrow.append(str(item))
      finfo.append(newrow)
    return finfo


def load_users_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from users"))

    users = []
    for row in result.all():
      users.append(list(row))
    return users


def load_activities_from_db():
  with engine.connect() as conn:
    result = conn.execute(
        text("select * from daily_activities where user_id=1"))

    data = []
    for row in result.all():
      data.append(list(row))

    fdata = []
    for row in data:
      newrow = []
      for item in row:
        newrow.append(str(item))
      fdata.append(newrow)
    return fdata


def load_offsets_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from offsets where user_id=1"))

    data = []
    for row in result.all():
      data.append(list(row))

    fdata = []
    for row in data:
      newrow = []
      for item in row:
        newrow.append(str(item))
      fdata.append(newrow)
    return fdata


def upload_offsets(data):
  with engine.connect() as conn:
    user_id = 1
    date = datetime.now().strftime('%Y-%m-%d')

    query = f"INSERT INTO offsets (user_id, walk, carpool, cycle, tree, pubtrans, recycle, cleanup, date) VALUES ({user_id}, '{data['walk']}', '{data['carpool']}', '{data['cycle']}', '{data['tree']}', '{data['pubtrans']}', '{data['recycle']}', '{data['cleanup']}', '{date}')"
    conn.execute(text(query))


def upload_today(data):
  with engine.connect() as conn:
    user_id = 1
    date = datetime.now().strftime('%Y-%m-%d')

    query = f"INSERT INTO daily_activities (user_id, wastepoints, drivekms, meal, laundry, utensils, date) VALUES ({user_id}, {data['waste']}, {data['kms']}, '{data['meal']}', '{data['laundry']}', '{data['utensils']}', '{date}')"
    conn.execute(text(query))
