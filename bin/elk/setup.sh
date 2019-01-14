# Start Elastic
docker run -d \
  -p 9200:9200 \
  -p 9300:9300 \
  --name elk_es \
  -e LOGSPOUT=ignore \
  elasticsearch:1.5.2

# Start Kibana
docker run -d \
  -p 5601:5601 \
  --link elk_es:elasticsearch \
  --name kibana \
  -e LOGSPOUT=ignore \
  kibana:4.1.2

# Create Data Container to store config file
docker create -v /config --name logstash_config busybox; docker cp logstash.conf logstash_config:/config/

# Start LogStash with access to data container with volumes from
docker run -d \
  -p 5000:5000 \
  -p 5000:5000/udp \
   --volumes-from logstash_config \
  --link elk_es:elasticsearch \
  --name logstash \
  -e LOGSPOUT=ignore \
  logstash:2.1.1  -f /config/logstash.conf

# Start LogSpout
ip=$(cat /etc/hosts | grep docker | awk '{ print $1 }')
docker run -d \
  -v /var/run/docker.sock:/tmp/docker.sock \
  --name logspout \
  -e LOGSPOUT=ignore \
  -e DEBUG=true \
  --publish=$ip:8000:80 \
  gliderlabs/logspout:master syslog://$ip:5000

docker run -d \
  -v /var/run/docker.sock:/tmp/docker.sock \
  --name logspout4 \
  -e LOGSPOUT=ignore \
  -e DEBUG=true \
  --publish=$ip:8000:80 \
  gliderlabs/logspout:master syslog://$ip:5000


# Check Elastic & Kibana

curl 'http://docker:9200/_cat/health?v'

curl 'https://localhost:5601'


# TEST! generate logs
docker run -d ubuntu bash -c 'for i in {0..60}; do echo "Logging Message $i"; sleep 1; done'

curl docker:8000/logs
docker logs logstash
