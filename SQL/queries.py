from sqlalchemy import *

from Config_BDD import campagnes, parameters

engine = create_engine("sqlite+pysqlite:///mydb", echo=True)

#delete(campagnes).where()

killCampaign = update(campagnes).where(campagnes.c.id == 1).values(state = "killed") # should be contrained and not be updated

#addParam = insert(parameters).values(campaing_id = , name = , param = )

with engine.connect() as conn:
    #conn.execute(killCampaign)
    #conn.execute(addParam)
    conn.commit()
    '''
    result = conn.execute(someSelectQuery)
    conn.execute(someQuery)
    conn.commit()
    '''