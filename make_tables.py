from sqlalchemy import MetaData,Table,Column,String,Integer,DateTime,func,Text,ForeignKey,null,create_engine,Sequence,insert,select
import datetime


meta = MetaData()

TABLE_FMT = lambda l=8: '{:<%d}| ' % l

def make_table(name,cols):
    table = Table(name,meta)
    for c in cols:
        table.append_column(c)
    return table

def create_with_engine(e):
    meta.bind = e
    meta.drop_all()
    meta.create_all(checkfirst=True)

id_col = lambda seq_name: Column('id',Integer,Sequence('{}_id_seq'.format(seq_name)),primary_key=True)
name_col = lambda nullable=True,unique=False: Column('name',String(255),unique=unique,nullable=nullable)
date_col = lambda name,default_null=False: Column(name,DateTime,default=func.now() if not default_null else null())

users_table = make_table(
                    'users',
                    [
                        id_col('user'),
                        name_col(),
                        date_col('date_added')
                    ]
)

emails_table = make_table(
                    'emails',
                    [
                        id_col('email'),
                        Column(
                            'address',
                            String(255),
                            nullable=False
                        ),
                        Column(
                            'user_id',
                            Integer,
                            ForeignKey('users.id')
                        )
                    ]
)

engine = create_engine('sqlite:///:memory:')
engine2 = create_engine('mysql+pymysql://talk:talk@localhost:3306/talk')
engine3 = create_engine('postgresql+psycopg2://talk3:talk@localhost:5432/talk3')


create_with_engine(engine)
create_with_engine(engine2)
create_with_engine(engine3)
# INSERING DATA

names = [
    'kyle',
    'joe',
    'jake',
    'jill',
    'jessica',
    'juan',
]

addresses = [
    'a@b.com',
    'b@c.com',
    'c@d.com',
    'd@e.com',
    'e@g.com',
    '4@2.com', 
]

users = map(
  lambda name: dict(name=name),names
)

emails = map(
  lambda address: dict(address=address,user_id=addresses.index(address)+1),addresses
)


ins = insert(users_table).values(users)

engine.execute(ins)
engine2.execute(ins)
engine3.execute(ins)

ins = insert(emails_table).values(emails)

engine.execute(ins)
engine2.execute(ins)
engine3.execute(ins)

# select data

display_select  = lambda driver,result: '{}\n\n\t{}'.format(driver.title(),'\n\t'.join(map(str,result.fetchall())))

def get_fmt(val):
    fmt = ''
    for itm in val:
        fmt +=  TABLE_FMT(len(str(itm))>=8 and len(str(itm)) or 8)
    return fmt

fmt = lambda val: '| '+get_fmt(val).format(*(map(lambda x: type(x) == datetime.datetime and x.ctime() or x,val)))

fmt_result = lambda res: '\n\n{}\n{}\n'.format(fmt(res.keys()),'-'*len(str(res.keys()))) + '\n'.join(map(str,map(fmt,res.fetchall())))

sel = users_table.select()
res1 = engine.execute(sel)
res2 = engine2.execute(sel)
res3 = engine3.execute(sel)

#for i in res1.fetchall():
    #for itm in i:
        #print type(itm)

print 'sqlite'
print fmt_result(res1)
print 'mysql'
print fmt_result(res2)
print 'postgresql'
print fmt_result(res3)


sel = select([users_table.c.id,users_table.c.date_added,users_table.c.name,emails_table.c.address]).select_from(users_table.join(emails_table))
res1 = engine.execute(sel)
res2 = engine2.execute(sel)
res3 = engine3.execute(sel)

print fmt_result(res1)
print fmt_result(res2)
print fmt_result(res3)

sel = select([users_table.c.id,users_table.c.name,emails_table.c.id,emails_table.c.address]).select_from(users_table.join(emails_table))

res1 = engine.execute(sel)
res2 = engine2.execute(sel)
res3 = engine3.execute(sel)

print fmt_result(res1)
print fmt_result(res2)
print fmt_result(res3)
