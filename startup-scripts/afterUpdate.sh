# 
# put commands to run after git update here - don't modify checkUpdate.sh or
# else you need an extra reboot
echo "Git changed - copying code across"
sudo chown pi.pi -R /home/pi/g54mrt-useful-code
sudo cp /home/pi/g54mrt-useful-code/startup-scripts/rc.local /etc/rc.local
cd /home/ubi
sudo -u ubi bash ./getlatest.sh
