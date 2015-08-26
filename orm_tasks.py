import datetime
import os
from sqlalchemy.ext.declarative import declarative_base,declared_attr
from sqlalchemy import Column,String,Integer,Date,orm,create_engine,func,Boolean,ForeignKey
from task_cmd_api import run_argv
from task_cmd_ui import _print_project
from seed import seed_data

base = declarative_base()
#engine = create_engine('sqlite:///x.db')
engine = create_engine('sqlite:///tasks.db')
base.metadata.bind = engine

Session = orm.scoped_session(orm.sessionmaker(bind=engine))
session = Session()

class Project(base):
    __tablename__ = 'projects'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False,unique=True)
    date_added = Column(Date,default=func.now())
    tasks = orm.relation('Task',lazy='dynamic')

class Task(base):
    __tablename__ = 'tasks'

    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False,unique=True)
    date_added = Column(Date,default=func.now())
    description = Column(String(500))
    due_date = Column(Date)
    is_complete = Column(Boolean,default=False)
    project_id = Column(Integer,ForeignKey('projects.id'))
    project = orm.relation('Project',uselist=False)

def _get_proj(name):
    return session.query(Project).filter(Project.name==name).first()

def get_proj_tasks(name):
    return map(lambda x: (x.id,x.name,x.description,x.due_date,x.is_complete),_get_proj(name).tasks.all())

def display_projects():
    for p in session.query(Project).all():
        _print_project(p.name,get_proj_tasks(p.name))

def add_proj(name,*args,**kwargs):
    p = Project()
    p.name = name
    session.add(p)
    session.commit()

def add_task(proj_name,task,*args,**kwargs):
    dte = len(args) >= 2 and datetime.datetime(*map(int,args[1].split(','))) or None
    p = _get_proj(proj_name)
    task = type(task) == dict and task or dict(name=task,description=args[0],due_date=dte)
    p.tasks.append(Task(**task))
    session.add(p)
    session.commit()

def complete_task(task_id):
    task = session.query(Task).get(task_id)
    task.is_complete = True
    session.add(task)
    session.commit()

def remove_project(proj_name):
    p = session.query(Project).filter(Project.name==proj_name).first()
    session.delete(p)
    session.commit()


base.metadata.create_all()

action_funcs =  [
        display_projects,
        add_proj,
        add_task,
        complete_task,
        remove_project,
]

def main():
    if os.environ.get('SQL_SEED'):
        seed_data(base.metadata,add_proj,add_task)
    run_argv(action_funcs)

if __name__ == "__main__":
    main()
