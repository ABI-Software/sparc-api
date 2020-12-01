import psycopg2
from psycopg2.extras import Json, DictCursor
import uuid

class MapState:
  '''
  This example demonstrates how to read and export a simple mesh
  '''
  
  def __init__(self):
    '''Initialise PyZinc Objects'''
    self._conn = psycopg2.connect(
      database="mapstate")
    #self.pushData()
    # create a cursor


  def pushState(self, state):
    cur = self._conn.cursor()
    id = uuid.uuid4().hex[:8]
    cur.execute('INSERT into mapstate (uuid, dict) values (%s, %s)', [id, Json(state)])
    cur.close()
    return id

  def pullState(self, uuid):
    cur = self._conn.cursor()
    cur.execute('SELECT dict FROM mapstate where uuid = %s', [uuid])
    row = cur.fetchone()
    cur.close()
    return row
