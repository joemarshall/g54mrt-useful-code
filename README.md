This repository contains useful python code for G54UBI

Folders:

grovepi-base                The base classes for talking to the grovepi, 
                            useful if you have your own pi. The lab raspberry pi
                            kits get their code from here.
 
sensors1                    Code and sample data referred to in sensors 1 lecture
sensors2                    Code and sample data referred to in sensors 2 lecture
sensors4                    Code and sample data referred to in sensors 4 lecture

code-requests               Code which we wrote when people wanted to do particular things
-   customserver.py             If you run this on your PI, it will host a web server which 
                                is similar to the fixed sensor boxes, so you can read data from a PC via HTTP.
                                
-   plotdata.py                 wxPython code which is used in lectures to show live sensor graphs

-   statemachine.py             An example of a basic state machine based logic for dealing with sensor data                            

othersensors                Code for talking to sensors which we don't actually have, 
                            where we helped people with accessing their own sensors.

install-your-own-pi.txt     Instructions for installing the grovepi stuff from scratch 
                            on your own raspberry pi. We can flash you a card with the lab
                            image if you don't want to do this.

                            