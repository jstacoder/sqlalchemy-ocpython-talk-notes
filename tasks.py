from sqlalchemy import Table,Column,select,insert,String,Integer,Date,ForeignKey,MetaData,func,Boolean,null,Text,delete
from fabric.colors import blue,green,cyan,magenta,red
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

def get_proj_tasks(name,get_id=False,*args,**kwargs):
    proj = projects.select().where(projects.c.name==name).execute().fetchone()
    proj_tasks = task_select.where(tasks.c.project_id==proj.id).execute().fetchall()
    return get_id and proj.id or proj_tasks

def add_task(project_name,task,*args,**kwargs):
    task = type(task) == dict and task or dict(name=task,description=args[0],due_date=datetime.datetime(*map(int,args[1].split(','))))
    tasks.insert().values(project_id=get_proj_tasks(project_name,True),**task).execute()

def complete_task(task_id=None,*args,**kwargs):
    if task_id is None:
        for p in proj_select.execute().fetchall():
            complete = filter(lambda x: x.is_complete,get_proj_tasks(p.name))
            if complete:
                _print_project(p.name,complete)
    else:
        tasks.update(tasks,{tasks.c.is_complete:True}).where(tasks.c.id==task_id).execute()

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
    

def remove_project(name,*args,**kwargs):
    delete(projects).where(projects.c.name==name).execute()

ACTIONS = {
    'list':display_projects,
    'create':add_proj,
    'add':add_task,
    'complete':complete_task,
    'remove':remove_project,
}

def run_argv():
    import sys
    if any(filter(lambda x: x in sys.argv,['-h','--help'])):
        display_usage()

    if len(sys.argv) <= 1 or sys.argv[1] not in ACTIONS:
        display_error()

    ACTIONS[sys.argv[1]](*sys.argv[2:])

def seed_data():
    meta.drop_all()
    meta.create_all()
    add_proj('testing')
    
    add_proj('my_next_test')

    task = {'name':'taskA','description':'my first task','due_date':datetime.datetime(2017,8,13)}
    task2 = {'name':'taskG','description':'my next task'}
    task3 = {'name':'taskY','description':'another task','due_date':datetime.datetime(2017,8,15)}

    add_task('testing',task)
    add_task('testing',task2)
    add_task('testing',task3)

    task = {'name':'CtaskA','description':'my B task','due_date':datetime.datetime(2017,8,13)}
    task2 = {'name':'BtaskG','description':'my Xtask'}
    add_task('my_next_test',task)
    add_task('my_next_test',task2)

def print_project(name):
    _print_project(name,get_proj_tasks(name))

def _print_project(name,data):
    _proj = data

    print 'Project: {}'.format(name)
    FMT = '|{:^15}|{:^15}|{:^25}|{:^15}|{:^15}|'
    head = FMT.format('id','name','description','due_date','complete')
    print head
    print '-'*len(head)
    print '\n'.join(map(str,map(lambda x: FMT.format(*map(str,x)),_proj)))
    print '\n\n'


def display_error():
    print red("ERROR!!")
    print red('An ACTION must be supplied, see usage below.\n\n')
    display_usage()

def display_usage():
    import sys
    print green('''{0}\n\tA command line task manager\n\n\nUSAGE:\n{0} [ACTION [arg [arg ...]]]

    Actions:
      {0} list [PROJECT_NAME]\t\t\t\t\t\t\tList PROJECT_NAME or all projects

      {0} create PROJECT_NAME\t\t\t\t\t\t\tCreate new collection of tasks under PROJECT_NAME

      {0} add PROJECT_NAME <[TASK_NAME]> <[DESCRIPTION]> <[DUE [Y,M,D]]>\t\tAdd new task TASK_NAME to PROJECT_NAME

      {0} complete [TASK_ID]\t\t\t\t\t\t\tComplete Task_id or list all completed tasks

      {0} remove PROJECT_NAME\t\t\t\t\t\t\tRemove PROJECT_NAME

    '''.format(sys.argv[0]),True)
    sys.exit(0)

def main():
    if os.environ.get('SQL_SEED'):
       seed_data()
    run_argv()

if __name__ == "__main__":
    main()

