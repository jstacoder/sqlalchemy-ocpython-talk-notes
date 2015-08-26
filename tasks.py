from sqlalchemy import Table,Column,select,insert,String,Integer,Date,ForeignKey,MetaData,func,Boolean,null,Text,delete
from task_cmd_api import run_argv
from task_cmd_ui import _print_project
import datetime
import os

meta = MetaData('sqlite:///tasks.db')

id_col = lambda: Column('id',Integer,primary_key=True)
date_col = lambda name: Column(name,Date,server_default=func.now())
null_date = lambda name: Column(name,Date)

projects = Table('projects',meta,
    id_col(),
    date_col('date_added'),
    Column('name',String(255),unique=True,nullable=False),
    Column('archived',Boolean,default=False),
)

proj_select = select([projects.c.name])

tasks = Table('tasks',meta,
    id_col(),
    date_col('date_added'),
    Column('name',String(255),unique=True,nullable=False),
    Column('description',Text),
    null_date('due_date'),
    Column('project_id',Integer,ForeignKey('projects.id')),
    Column('is_complete',Boolean,default=False),
)

task_select = select([tasks.c.id,tasks.c.name,tasks.c.description,tasks.c.due_date,tasks.c.is_complete])

def add_proj(name,*args,**kwargs):
    projects.insert().values(name=name).execute()

def add_task(project_name,task,*args,**kwargs):
    task = type(task) == dict and task or dict(name=task,description=args[0],due_date=datetime.datetime(*map(int,args[1].split(','))))
    tasks.insert().values(project_id=get_proj_tasks(project_name,True),**task).execute()

def remove_project(name,*args,**kwargs):
    delete(projects).where(projects.c.name==name).execute()

def complete_task(task_id=None,*args,**kwargs):
    if task_id is None:
        for p in proj_select.execute().fetchall():
            complete = filter(lambda x: x.is_complete,get_proj_tasks(p.name))
            if complete:
                _print_project(p.name,complete)
    else:
        tasks.update(tasks,{tasks.c.is_complete:True}).where(tasks.c.id==task_id).execute()

def get_proj_tasks(name,get_id=False,*args,**kwargs):
    proj = projects.select().where(projects.c.name==name).execute().fetchone()
    proj_tasks = task_select.where(tasks.c.project_id==proj.id).execute().fetchall()
    return get_id and proj.id or proj_tasks

def list_projects():
    projs = []
    for proj in projects.select().execute():
        projs.append(dict(id=proj.id,name=proj.name,tasks=map(lambda x: (x.name,x.id,x.due_date,x.is_complete,x.description),tasks.select().where(tasks.c.project_id==proj.id).execute())))
    return projs

def display_projects(proj_name=None,*args,**kwargs):
    if proj_name is None:
        for proj in proj_select.execute():
            print_project(proj.name)
    else:
        print_project(proj_name)

action_funcs =  [
        display_projects,
        add_proj,
        add_task,
        complete_task,
        remove_project,
]

def print_project(name):
    _print_project(name,get_proj_tasks(name))


def main():
    if os.environ.get('SQL_SEED'):
       seed_data(meta,add_proj,add_task)
    run_argv(action_funcs)

if __name__ == "__main__":
    main()

