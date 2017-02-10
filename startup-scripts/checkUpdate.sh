#!/bin/bash
cd /home/pi/g54mrt-useful-code

# wait until github is connectable
until (/usr/bin/wget -O - https://www.github.com > /dev/null)
do
  echo "waiting for github"
  sleep 1
done

#pull any changes from git
if git pull | grep -q "up-to-date"; then
echo "no changes"
else
echo "changed git - copying code across"
sudo chown pi.pi -R /home/pi/g54mrt-useful-code
sudo cp /home/pi/g54mrt-useful-code/startup-scripts/rc.local /etc/rc.local
sudo cp -r /home/pi/g54mrt-useful-code/grovepi-base/* /home/ubi/
sudo chown ubi.ubi /home/ubi/*
fi
sudo systemctl disable serial-getty@ttyAMA0.service
sudo /usr/bin/python /home/pi/g54mrt-useful-code/startup-scripts/checkFirmware.py
