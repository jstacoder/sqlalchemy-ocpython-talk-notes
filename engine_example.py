import os
# examples of creating and using engines
from sqlalchemy import create_engine, select, func, Table, Column, String, Integer, MetaData
engines = {}
# create an engine to connect to a specific database, it is usually the only backend specific part, the connection
# connect to a specific sql backend via a connection_url
# sqlite database - absolute path - dbfile: /home/me/example.db
engines['sqlite_absolute'] = create_engine('sqlite:///{}'.format(os.path.join(os.getcwd(),'example.db')),echo=True)

# sqlite database - relative path - dbfile: $(pwd)/example.db
engines['sqlite_relative'] = create_engine('sqlite:///example.db')

# sqlite database - in memory database, no dbfile created
engines['sqlite'] = create_engine('sqlite:///:memory:')

# mysql, uri format mysql<+ext>://USERNAME:PASSWORD@HOSTNAME:PORT/DBNAME
engines['mysql'] = create_engine('mysql://example:example@localhost:3306/example',echo=True)

# mysql using pymysql adapter, pip install pymysql-sa
engines['pymysql'] = create_engine('mysql+pymysql://example:example@localhost:3306/example')

# postgresql, pip install psycopg2 
# uri format postgresql<+ext>://USERNAME:PASSWORD@HOSTNAME:PORT/DBNAME
engines['pgsql'] = create_engine('postgresql://example:example@localhost:5432/example',echo=True)

# or explicitly use psycopg2
engines['psycopg2'] = create_engine('postgresql+psycopg2://example:example@localhost:5432/example')


# using engines
# execute raw sql
sql = 'select CURRENT_TIMESTAMP'
print '\n'.join(map(str,map(lambda x: engines[x].execute(sql).fetchall(),engines)))

# execute expression statements
sql = select([func.now()])
print '\n'.join(map(str,map(lambda x: engines[x].execute(sql).fetchall(),engines)))

# execute statements made from tables directly
meta = MetaData()
users = Table('users',meta,
        Column('id',Integer,primary_key=True),
        Column('name',String(255),nullable=False),
)
for e in engines:
    meta.bind = engines[e]
    meta.drop_all()
    meta.create_all()
ins = users.insert()
names = ['hank','carl','joel']
map(lambda x: engines[x].execute(ins,map(lambda x: dict(name=x),names)),engines)
sel = users.select()
print '\n'.join(map(str,map(lambda x: engines[x].execute(sel).fetchall() ,engines)))
