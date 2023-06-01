# rpi_server_modules
util for server running in rpi 
```commandline
python server_zmq.py config.yaml
```
for set custom gpio pins to i2c edit /boot/config.txt
```commandline
dtoverlay=i2c-gpio,i2c_gpio_sda=5,i2c_gpio_scl=6
```
