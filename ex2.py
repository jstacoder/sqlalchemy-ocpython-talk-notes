from sqlalchemy import create_engine,MetaData,Table,Column,String,Integer,select,insert

engine = create_engine('sqlite:///:memory:',echo=True)

def run_sql(sql):
    return engine.execute(sql)

def main():
    meta = MetaData()
    users = Table('users',meta,
            Column('id',Integer,primary_key=True),
            Column('name',String(255),nullable=False),
            Column('age',Integer,default=0)
    )
    sel = select([users.c.name,users.c.age])
    ins = insert(users)

    meta.bind = engine 

    meta.create_all()

    run_sql(ins,dict(name='kyle',age=44))
    run_sql(ins,dict(name='joe',age=14))
    run_sql(ins,dict(name='john'))

    print run_sql(sel).fetchall()


if __name__ == "__main__":
    main()

