from sqlalchemy import create_engine, text

db_string = "mysql+pymysql://3ukz4qcmgyrybc678dx4:pscale_pw_swFdDVjKgtZ12HDGikyk3qNJO8tTEJkknjSyx1i1MnO@aws.connect.psdb.cloud/carbon-footprint?charset=utf8mb4"
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
