from fastapi import FastAPI, HTTPException

app = FastAPI()

# Liste les routes disponibles dans l'API
@app.get('/')
async def routes():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Liste les clusters disponibles dans Cigri
@app.get('/clusters')
async def clusters():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère les informations d'un cluster en particulier
@app.get('/clusters/{clusterId}')
async def cluster(clusterId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Liste toutes les campagnes en cours
@app.get('/campaigns')
async def campaigns():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère les informations d'une campagne en particulier
@app.get('/campaigns/{campaignId}')
async def campaign(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère le JDL d'une campagne en particulier
@app.get('/campaigns/{campaignId}/jdl')
async def campaignJdl(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Liste l'ensemble des jobs d'une campagne spécifique
@app.get('/campaigns/{campaignId}/jobs')
async def campaignJobs(campaignId: int, limit: int, offset: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère le détail d'un job spécifique d'une campagne en particulier
@app.get('/campaigns/{campaignId}/jobs/{job_id}')
async def campaignJob(campaignId: int, jobId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère les jobs terminés de la campagne spécifiée
@app.get('/campaigns/{campaignId}/jobs/finished')
async def campaignFinishedJobs(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Soumettre une nouvelle campagne
@app.post('/campaigns')
async def submitCampaign():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Mettre à jour une campagne (status, nom)
@app.put('/campaigns/{campaignId}')
async def updateCampaign(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Supprime une campagne
@app.delete('/campaigns/{campaignId}')
async def deleteCampaign(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Liste les événements d'une campagne donnée
@app.get('/campaigns/{campaignId}/events')
async def campaignEvents(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Corrige (ferme) les événements d'une campagne donnée
@app.delete('/campaigns/{campaignId}/events')
async def deleteCampaignEvents(campaignId: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Liste les abonnements aux notifications de l'utilisateur actuel
@app.get('/notifications')
async def notifications():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# S'abonner au service de notification mail
@app.post('/notifications/mail')
async def subscribeMail():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# S'abonner au service de notification Jabber
@app.post('/notifications/jabber')
async def subscribeJabber():
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Se désabonner d'un système de notification
@app.delete('/notifications/{system}')
async def unsubscribe(system: str):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère un événement spécifique
@app.get('/events/{id}')
async def event(id: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Corrige (ferme) l'événement spécifié
@app.delete('/events/{id}')
async def deleteEvent(id: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Corrige (ferme) l'événement spécifié et resoumet le job
@app.delete('/events/{id}')
async def eventAndResubmitJob(id: int, resumbit = None):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")

# Récupère l'usage actuel de la grille entre deux dates (unix timestamps)
@app.get('/gridusage')
async def gridUsage(fromDate: int, toDate: int):
    raise HTTPException(status_code=404, detail="Not Yet Implemented")
