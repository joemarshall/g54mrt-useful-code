#!/bin/bash
cd /home/pi/g54mrt-useful-code

sudo mkdir /home/g54mrt/.ssh
sudo cp /home/pi/g54mrt-useful-code/startup-scripts/authorized_keys /home/g54mrt/.ssh/
sudo chown g54mrt.g54mrt /home/g54mrt/.ssh 

# wait until github is connectable
until (/usr/bin/wget -O - https://www.github.com > /dev/null)
do
  echo "waiting for github"
  sleep 1
done

set -o pipefail
#pull any changes from git
if git pull | grep -q "up-to-date"; then
echo "no changes"
else
    if [ $? -ne 0 ]
    then
        # error doing git pull - re-copy repository
        cd /tmp
        rm -rf g54mrt-useful-code
        git clone https://github.com/joemarshall/g54mrt-useful-code.git
        if [ $? -eq 0 ]
        then
          cd ~
          rm -rf g54mrt-useful-code
          mv /tmp/g54mrt-useful-code ./g54mrt-useful-code
        fi
    fi
# run things that need to be run after this git update
/bin/bash /home/pi/g54mrt-useful-code/startup-scripts/afterUpdate.sh
fi

sudo chown pi.pi -R /home/pi/g54mrt-useful-code
sudo systemctl disable serial-getty@ttyAMA0.service
sudo /usr/bin/python /home/pi/checkFirmware.py
