# python -m config.db_migrate

import sys
sys.path.append('../')
from .database import init_db
init_db()