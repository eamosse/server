# Installer le serveur 

- Récupérer les sources 
```
git clone https://github.com/eamosse/server.git
```

- Installer Node JS (https://nodejs.org/en/) 

- Installer Mongo DB (https://www.mongodb.com/) 

- Installer Python 3 (https://www.continuum.io/downloads) 

- Executer les requetes suivantes dans une console 
```
> cd sparqlwrapper
> python config.py install
> cd ..
> pip install -e pythonhelpers
> pip install pymongo
> node install express
> node install body-parser
> node install method-override
> node install mongodb
```
- Lancer le script permettant de récupérer les données de DBPedia (il faut que MongoDb soit lancé)
```
pythdon dbpedia_query.py
```
- Lancer le serveur (il sera disponible sur le port 5000)
```
node index.js 
```
