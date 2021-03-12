from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from database import metadata, db_session


class Brand(object):
    query = db_session.query_property()

    def __init__(self,
                 id=None,
                 name=None,
                 transparency=None,
                 worker_emp=None,
                 env_mgmt=None,
                 url=None):
        self.id = id
        self.name = name
        self.transparency = transparency
        self.worker_emp = worker_emp
        self.env_mgmt = env_mgmt
        self.url = url


brand = Table('brand', metadata, Column('id', Integer, primary_key=True),
              Column('name', String), Column('transparency', Integer),
              Column('worker_emp', Integer), Column('env_mgmt', Integer),
              Column('url', String))

mapper(Brand, brand)