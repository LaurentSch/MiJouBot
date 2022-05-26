FROM ubuntu:18.04
ENTRYPOINT []
RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip
RUN pip3 install rasa==3.0.8-full
ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh