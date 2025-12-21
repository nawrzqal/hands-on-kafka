@echo off
setlocal
pushd %~dp0

docker-compose up --build -d
docker-compose logs -f kafka consumer-1 consumer-2 consumer-3

popd
endlocal
