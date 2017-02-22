# 
# put commands to run after git update here - don't modify checkUpdate.sh or
# else you need an extra reboot
echo "Git changed - copying code across"
sudo chown pi.pi -R /home/pi/g54mrt-useful-code
sudo cp /home/pi/g54mrt-useful-code/startup-scripts/rc.local /etc/rc.local
sudo cp -r /home/pi/g54mrt-useful-code/grovepi-base/* /home/ubi/
sudo chown ubi.ubi /home/ubi/*
sudo sed s/enable_uart=0/enable_uart=1/ </boot/config.txt
