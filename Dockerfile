FROM hypriot/rpi-python:2.7

# Create app directory
RUN mkdir -p /apps/dht22Service

# Install npm modules
RUN pip install pymongo==3.2.2
RUN apt-get update && \
apt-get install -y git && \
apt-get install -y build-essential

WORKDIR /tmp/
# forked pigpio because they don't have any releases in their repo and don't want their updates to break functionality
RUN git clone https://github.com/cpitzak/pigpio.git
WORKDIR /tmp/pigpio/
RUN git checkout tags/v55
RUN make -j4
RUN make install

WORKDIR /apps/dht22Service

COPY . /apps/dht22Service

CMD [ "python", "job.py" ]