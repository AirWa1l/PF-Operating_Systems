
user="totti"
password="pote"
database="proves"

docker run --name $database -p 5432:5432 -e POSTGRES_USER=$user -e POSTGRES_PASSWORD=$password -e POSTGRES_DB=os_db -d postgres && docker exec -it $database bin/bash

