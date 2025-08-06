ECHO docker ps -f ancestor=auto_post_api
docker image rm auto_post_api -f
docker build -t auto_post_api .
docker container run -d -p 30502:9004/tcp -p 30502:9004/udp auto_post_api
cmd /k