import os
os.environ.setdefault(
    'DATABASE_URI','sqlite:///memory.db'
)
from example_engine import engine,sa
column = sa.sql.expression.column
table = sa.sql.expression.table
select = sa.sql.expression.select
func = sa.sql.expression.func

projects  = table('projects',column('id'),column('name'),column('due_date'))
tasks = table('tasks',column('id'),column('name'),column('project_id'))


print select([tasks.c.name]).select_from(projects.join(tasks,tasks.c.project_id==projects.c.id))

print str(sa.sql.expression.select([projects]))
print str(select([tasks]))
