# music-lib


Docker to prepare a mysql instance:
```
docker run --name mysql-local -e MYSQL_ROOT_PASSWORD=<set password here> -d -p 3306:3306 mysql:latest
```