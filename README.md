# Bell Controller
## A bell controller, designed for church

This software has been built on Debian Jessie, on a Raspberry PI 2, using python 2.7.

### Packages needed
* python (main debian repository)
* python-rpi.gpio (main raspbian repository)

To be checked for other dependencies.

### Instructions
#### General informations
* this daemon is tested in `/usr/local/bell-controller` directory.
* Sounds to be played have to be placed in sound/ directory. Files inside need to have no spaces or other non ASCII character into the file name.
* The file can be played also from external sources using the fifo created by the daemon. 
* Pinout description can be found in the official web site https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/ or in a more clean way in https://github.com/Dot-and-Net/IoTHelpers/wiki/Raspberry-Pi-2-and-3-Pinout

More information about the expected behavior are in [info.md](info.md)

#### Autostart as a service 
1. put the repository on `/usr/local/bell-controller`
2. copy the `bell-controller.service` file into `/etc/systemd/system/bell-controller.service`
3. run `systemctl enable bell-controller.service`

#### Play file from an external source 
The fifo is hardcoded into `/var/run/bell.fifo`

In order to play one file, simply put into the pipe the filename you want to play.

The file name will be looked into `sound/` directory and played if exists.




#### Customization of the daemon
Current pins are hardcoded

| function        | pin number | Pin definition |
|-----------------|------------|----------------|
| Play "FESTA"    | 11         | GPIO 17        |
| Play "FUNERALE" | 13         | GPIO 27        |
| Play "ORA_PIA"  | 15         | GPIO 22        |
| Stop all play   | 33         | GPIO 13        |
| shutdown        | 35         | GPIO 19        |

Currently filename are hardcoded and bonded to one GPIO.
````
  * GPIO 17: "1-FESTA.wav",
  * GPIO 27: "2-FUNERALE.wav",
  * GPIO 22: "3-ORA_PIA.wav",```
````

#### Other current hardware link

| Item             | function | pin number | Pin definition |
|------------------|----------|------------|----------------|
| Coupling circuit | power    | 4          | 5V             |
| Coupling circuit | GND      | 6          | GND            |
| Relais           | power    | 2          | 5V             |
| Relais           | GND      | 9          | GND            |
| Relais           | switch   | 37         | GPIO 26        |
| LED Raspberry    | power    | 17         | 3,3V           |
| LED Raspberry    | GND      | 20         | GND            |


## TODO
### Web interface
A web interface is needed to change the cron

### Privilege sepaeration
The root user is not really needed to run this software. Especially if the web server has to be implemented to change the cron.

### Definition of GPIO and functions in a json/xml/... file
The code should be clean from the hardcoded pin
