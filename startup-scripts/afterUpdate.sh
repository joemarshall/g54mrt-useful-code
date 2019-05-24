# 
# put commands to run after git update here - don't modify checkUpdate.sh or
# else you need an extra reboot
echo "Git changed - copying code across"
sudo chown pi.pi -R /home/pi/g54mrt-useful-code
if [ -s "/home/pi/g54mrt-useful-code/startup-scripts/checkUpdate.sh" ] 
then
    sudo cp /home/pi/g54mrt-useful-code/startup-scripts/checkUpdate.sh /home/pi/checkUpdate.sh
    sudo cp /home/pi/g54mrt-useful-code/startup-scripts/rc.local /etc/rc.local
    sudo cp /home/pi/g54mrt-useful-code/startup-scripts/showIP.py /home/pi/showIP.py
    sudo cp /home/pi/g54mrt-useful-code/grovepi-base/grovelcd.py /home/pi/grovelcd.py
    sudo cp /home/pi/g54mrt-useful-code/grovepi-base/grovepi.py /home/pi/grovepi.py
    sudo cp /home/pi/g54mrt-useful-code/grovepi-base/smbus2 /home/pi/smbus2
fi
cd /home/g54mrt
sudo cp /home/pi/g54mrt-useful-code/grovepi-base/getlatest.sh .
sudo chown g54mrt.g54mrt /home/g54mrt/getlatest.sh
sudo -u g54mrt bash ./getlatest.sh

sudo mkdir /home/g54mrt/.ssh
sudo cp /home/pi/g54mrt-useful-code/startup-scripts/authorized_keys /home/g54mrt/.ssh/
sudo chown g54mrt.g54mrt /home/g54mrt/.ssh
sudo chown g54mrt.g54mrt /home/g54mrt/.ssh/authorized_keys
sudo chmod 644 /home/g54mrt/.ssh/authorized_keys

