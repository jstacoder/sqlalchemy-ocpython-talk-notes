import sqlalchemy as sa
import datetime
'''
        * projects
            - id
            - name
            - tasks
            - due_date
            - date_added
            - date_modified
        * tasks
            - id
            - name             
            - project (id)
            - due_date
            - date_added
            - date_modified
            - priority_level (id)
        * priority_levels
            - id
            - name
'''     
meta = sa.MetaData()

id_column = lambda: sa.Column('id',sa.Integer,primary_key=True)
name_column = lambda: sa.Column('name',sa.String(255),unique=True,nullable=False)
date_added_column = lambda: sa.Column('date_added',sa.DateTime,default=sa.func.now())
date_modified_column = lambda: sa.Column('date_modified',sa.DateTime,default=sa.func.now(),onupdate=sa.func.now())
due_date_column = lambda: sa.Column('due_date',sa.DateTime,nullable=True)

projects = sa.Table('projects',meta,
     id_column(),
     name_column(),
     due_date_column(),
     date_added_column(),
     date_modified_column(),
)

project = {
    'name':'test project',
    'due_date':datetime.datetime.now()
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
    },
    {
        'name':'Task2',
        'priority_level_id':2,
        'project_id':1,
    },
    {
        'name':'Task3',
        'priority_level_id':3,
        'project_id':1,
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

engine = sa.create_engine('sqlite:///memory.db',echo=True)
meta.bind = engine
meta.create_all()

engine.execute(lvl_ins,levels)
engine.execute(project_ins,project)
engine.execute(task_ins,_tasks)

