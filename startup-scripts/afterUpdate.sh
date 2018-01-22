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
fi
cd /home/g54mrt
sudo cp /home/pi/g54mrt-useful-code/grovepi-base/getlatest.sh .
sudo chown g54mrt.g54mrt /home/g54mrt/getlatest.sh
sudo -u g54mrt bash ./getlatest.sh
