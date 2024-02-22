from sqlalchemy import *

from Config_BDD import campagnes, parameters

engine = create_engine("sqlite+pysqlite:///mydb", echo=True)

#delete(campagnes).where()

def killCampaign (id = 1):
    killCampaign = update(campagnes).where(campagnes.c.id == id).values(state = "test2") # should be contrained and not be updated
    with engine.connect() as connect:
        connect.execute(killCampaign)
        connect.commit()

#addParam = insert(parameters).values(campaing_id = , name = , param = )
''''
with engine.connect() as conn:
    #conn.execute(killCampaign)
    #conn.execute(addParam)
    conn.commit()
    
    result = conn.execute(someSelectQuery)
    conn.execute(someQuery)
    conn.commit()
    '''

if __name__ == "__main__":
    killCampaign()


    ###
    #   transformer les queries en fonction gros porc
    ###