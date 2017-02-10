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
# run things that need to be run after this git update
/bin/bash /home/pi/g54mrt-useful-code/startup-scripts/afterUpdate.sh
fi

sudo chown pi.pi -R /home/pi/g54mrt-useful-code
sudo systemctl disable serial-getty@ttyAMA0.service
sudo /usr/bin/python /home/pi/g54mrt-useful-code/startup-scripts/checkFirmware.py
