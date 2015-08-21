import os
import sqlalchemy as sa
from sqlalchemy import create_engine


engine = create_engine(os.environ.get('DATABASE_URI') or 'sqlite:///:memory:',echo=False)
