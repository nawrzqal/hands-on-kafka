@echo off
setlocal
pushd %~dp0

start "Producer API" cmd /k "python producer.py"
start "Consumer API 1" cmd /k "set CONSUMER_PORT=5002 && python consumer.py"
start "Consumer API 2" cmd /k "set CONSUMER_PORT=5003 && python consumer.py"
start "Consumer API 3" cmd /k "set CONSUMER_PORT=5004 && python consumer.py"

start "Producer UI" cmd /k "streamlit run producer_ui.py"

popd
endlocal
