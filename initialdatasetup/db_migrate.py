import sys
sys.path.append('../')

from backend.domains.database import Base, engine
Base.metadata.create_all(bind=engine)