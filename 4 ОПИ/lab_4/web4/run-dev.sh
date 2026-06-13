#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

docker compose up -d

if [[ ! -d frontend/node_modules ]]; then
	( cd frontend && npm install )
fi

( cd frontend && npm run build )

mkdir -p src/main/resources/static
rm -rf src/main/resources/static/*
cp -R frontend/dist/. src/main/resources/static/

./mvnw -DskipTests spring-boot:run

#WINDOWS_IP=$(ip route show | grep -i default | awk '{ print $3}')
#docker run --rm \
#    -v "$PWD:/var/loadtest" \
#    --add-host host.docker.internal:$WINDOWS_IP \
#    -it yandex/yandex-tank