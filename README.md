# FastAPI - Auth - Mongodb - Docker

<h3><strong>Avaliable endpoints:</strong></h3>
<ul>
<li> <strong>/authreq/{pageid}</strong> (Requiries token auth)</li>
<li> <strong>/token</strong></li>
<li> <strong>/noauthreq (Doesn't require token)</strong></li>
</ul>

## Usage
1) Set the corresponding enviroment variables in the .env file:
```bash
secret_key="54dab0156a2269h0fb13893ff1f1134d59696622749366721g6n80e193g21672"
algorithm="HS256" 
URI="mongodb://root:root123@192.168.100.5:27017/?tls=false"
```

2) For now, it is assumed that the DB was set correctly

3) Add your endpoints and adapt the code to your needs (app directory).

4) (OPT for local testing) Install py dependencies and create an enviroment
```bash
[postgresql]
python -m venv env
source env/bin/activate
pip install -r requirements.txt
fastapi dev ./app/main.py
```

5) Once everything has been set up simply use `docker compose up` to have your container up and running.
Or check this resource for more options: https://github.com/yova-l/fastAPI-docker-template

## Resources that helped developed this API:
* https://www.youtube.com/watch?v=5GxQ1rLTwaU Auth
* https://www.youtube.com/watch?v=Hs9Fh1fr5s8 Extra

Consumer app example included.