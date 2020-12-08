from sqlalchemy import create_engine  
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
import json
import uuid

base = declarative_base()

class State(base):  
    __tablename__ = 'mapstates'
    uuid = Column(String, primary_key=True, unique=True)
    data = Column(JSONB)

class MapState:
  
  def __init__(self, databaseURL):
    db = create_engine(databaseURL)
    global base
    base.metadata.create_all(db)
    Session = sessionmaker(db)
    self._session = Session()


  def pushState(self, input, commit = False):
    id = uuid.uuid4().hex[:8]
    while self._session.query(State).filter_by(uuid=id).first() is not None:
      id = uuid.uuid4().hex[:8]
    newState = State(uuid=id, data=input)
    self._session.add(newState)
    if commit:
      self._session.commit()
    return id

  def pullState(self, id):
    state = self._session.query(State).filter_by(uuid=id).first()
    if state:
      return state.data
    else:
      return None