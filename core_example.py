import os

from bs4 import Tag
from csv import writer
import sqlalchemy as sa
import datetime
from example_engine import engine
    
meta = sa.MetaData()

id_column = lambda: sa.Column('id',sa.Integer,primary_key=True)
name_column = lambda: sa.Column('name',sa.String(255),unique=True,nullable=False)
date_added_column = lambda: sa.Column('date_added',sa.DateTime,default=sa.func.now())
date_modified_column = lambda: sa.Column('date_modified',sa.DateTime,default=sa.func.now(),onupdate=sa.func.now())
due_date_column = lambda: sa.Column('due_date',sa.Date,nullable=True,default=sa.null())

projects = sa.Table('projects',meta,
     id_column(),
     name_column(),
     due_date_column(),
     date_added_column(),
     date_modified_column(),
)

project = {
    'name':'test project',
}

project_ins = projects.insert().values(**project)

tasks = sa.Table('tasks',meta,
        id_column(),
        name_column(),
        due_date_column(),
        date_added_column(),
        date_modified_column(),
        sa.Column('project_id',sa.Integer,sa.ForeignKey('projects.id')),
        sa.Column('priority_level_id',sa.Integer,sa.ForeignKey('priority_levels.id')),        
)

_tasks = [
    {
        'name':'Task1',
        'priority_level_id':1,
        'project_id':1,
        'due_date':datetime.datetime(2015,8,13)
    },
    {
        'name':'Task2',
        'priority_level_id':2,
        'project_id':1,
        'due_date':datetime.datetime(2013,8,15)
    },
    {
        'name':'Task3',
        'priority_level_id':3,
        'project_id':1,
        'due_date':datetime.datetime(2003,8,20)
    }
]

task_ins = tasks.insert()

priority_levels = sa.Table('priority_levels',meta,
        id_column(),
        name_column(),
        sa.Column('order',sa.Integer,nullable=False),
)

levels = [
            {
                'name':'highest',
                'order':1,
            },
            {
                'name':'high',
                'order':2,
            },
            {
                'name':'medium',
                'order':3,
            },
            {
                'name':'low',
                'order':4,
            },
            {
                'name':'lowest',
                'order':5,
            },
]
lvl_ins = priority_levels.insert()

projects_tasks = sa.Table('projects_tasks',meta,
        sa.Column('project_id',sa.Integer,sa.ForeignKey('projects.id')),
        sa.Column('task_id',sa.Integer,sa.ForeignKey('tasks.id')),
        sa.PrimaryKeyConstraint('project_id','task_id')
)

ptins = projects_tasks.insert()

sel = sa.select([tasks.c.project_id,tasks.c.id])

meta.bind = engine
meta.create_all()

engine.execute(lvl_ins,levels)
engine.execute(project_ins,project)
engine.execute(task_ins,_tasks)


data = map(lambda x: dict(task_id=x[1],project_id=x[0]),engine.execute(sel).fetchall())

engine.execute(ptins,data)

sql = '''select projects.name as project, tasks.due_date as due_on, tasks.name as task_name 
            from tasks 
        join projects_tasks
            on tasks.id = projects_tasks.task_id 
        join projects 
            on projects.id = projects_tasks.project_id
        '''

#stmt = tasks.select([projects.c.name,tasks.c.due_date,tasks.c.name]).join(projects_tasks,tasks.c.id==projects_tasks.c.task_id).join(projects,projects.c.id==projects_tasks.c.project_id)

cols = [projects.c.name,tasks.c.due_date,tasks.c.name]
sel = select(cols)

stmt = sel.select_from(
    tasks.join(projects_tasks).join(projects)
)

#w = writer(open('tst.csv','w'))
print sql
results = engine.execute(sql)
print results.fetchall()

print stmt
results = engine.execute(stmt)
print results.fetchall()

#w.writerow(results.keys())
#w.writerows(results.fetchall())