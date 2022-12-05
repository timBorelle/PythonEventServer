# Serveur Python

## Déployer la stack

``` bash
docker-compose up -d
```

## Vérifier les conteneurs Docker
``` unix
docker ps
```

## Inéragir avec le serveur

### Depuis votre poste
``` unix
curl localhost/list_events
```

### Via le client (en ligne de commande)

Entrer dans le conteneur du client
``` unix
docker exec -it $(docker ps | grep cli-client | head -c 12) /bin/sh
```

### 1. Ajouter un événement
``` unix
curl -X POST web/add_event?start=12345678\&stop=177777777\&tags=cool,hello,world
```

```
{
  "event": "{'start': '12345678', 'stop': '177777777', 'tags': ['cool', 'hello', 'world'], '_id': ObjectId('638e154143e1db94e5aec5e2')}",
  "message": "Your event has been added",
  "success": true
}
```


### 2. Lister les événements
``` unix
curl web/list_events
```

```
{
  "data": [
    "{'_id': ObjectId('638e154143e1db94e5aec5e2'), 'start': '12345678', 'stop': '177777777', 'tags': ['cool', 'hello', 'world']}", 
    "{'_id': ObjectId('638e159043e1db94e5aec5e3'), 'start': '12345678', 'stop': None, 'tags': ['hello', 'world']}"
  ],
  "success": true
}
```

### 3. Supprimer tous les événements
``` unix
curl web/remove_events
```

```
{
  "message": "2 documents deleted.",
  "success": true
}
```

### Visualiser les événements depuis l'interface Mongo Express
[http://localhost:7081/db/local/events](http://localhost:7081/db/local/events)
