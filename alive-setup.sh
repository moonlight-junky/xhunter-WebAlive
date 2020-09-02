#!/bin/bash
apt update
apt install python3.7 -y
apt install python3-pip -y
apt install python3.7-dev -y
apt install python-pip -y
python3.7 -m pip install --upgrade pip
python -m pip install --upgrade pip
apt install vim -y
apt install tmux -y
apt install git -y
apt install zip -y
apt install unzip -y
apt install libnss3-tools -y
apt install wget -y
apt install curl -y
apt-get clean && apt update && apt upgrade -y \
    && python3.7 -m pip install celery[redis] requests simplejson redis

apt-get install -yq --no-install-recommends \
    libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 \
    libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 \
    libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 libnss3

python3.7 -m pip install -r ~/xhunter-WebAlive/requirements.txt
chmod 777 ~/xhunter-WebAlive/xalive/w.sh
