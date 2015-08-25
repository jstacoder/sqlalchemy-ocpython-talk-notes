from sqlalchemy import Table,Column,select,insert,String,Integer,Date,ForeignKey,MetaData,func,Boolean,null,Text
import datetime

meta = MetaData('sqlite:///:memory:')

id_col = lambda: Column('id',Integer,primary_key=True)
date_col = lambda name: Column(name,Date,server_default=func.now())
null_date = lambda name: Column(name,Date)

projects = Table('projects',meta,
    id_col(),
    date_col('date_added'),
    Column('name',String(255),unique=True,nullable=False),
    Column('archived',Boolean,default=False),
)

tasks = Table('tasks',meta,
    id_col(),
    date_col('date_added'),
    Column('name',String(255),unique=True,nullable=False),
    Column('description',Text),
    null_date('due_date'),
    Column('project_id',Integer,ForeignKey('projects.id')),
    Column('is_complete',Boolean,default=False),
)

meta.create_all()
# add_proj,get_proj,add_task,get_task,list_projects

def add_proj(name):
    projects.insert().values(name=name).execute()

def get_proj(name,get_id=False):
    proj = projects.select().where(projects.c.name==name).execute().fetchone()
    proj_tasks = tasks.select().where(tasks.c.project_id==proj.id).execute().fetchall()
    return get_id and proj.id or (proj.name,proj_tasks)

def add_task(project_name,task):
    tasks.insert().values(project_id=get_proj(project_name,True),**task).execute()

def complete_task(task_id):
    tasks.update(tasks,{tasks.c.is_complete:True}).where(tasks.c.id==task_id).execute()

add_proj('testing')

task = {'name':'taskA','description':'my first task','due_date':datetime.datetime(2017,8,13)}
task2 = {'name':'taskG','description':'my next task'}
task3 = {'name':'taskY','description':'another task','due_date':datetime.datetime(2017,8,15)}
add_task('testing',task)
add_task('testing',task2)
add_task('testing',task3)


def print_project(name):
    _proj = get_proj(name)

    print 'Project: {}'.format(_proj[0])
    FMT = '|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|{:^15}|'
    head = FMT.format('id','date','name','description','due_date','proj_id','complete')
    print head
    print '-'*len(head)
    print '\n'.join(map(str,map(lambda x: FMT.format(*map(str,x)),_proj[1])))
    print '\n\n'

print_project('testing')

complete_task(2)

print_project('testing')

