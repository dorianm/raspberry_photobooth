# Photobooth Raspberry PI

Source code of my project to build a photobooth from a Raspberry Pi v3 and the Camera Module v2. It has been develop for a photo animation at a weeding. Feel free to use it !

### Equipment used

- Raspberry PI v3
- Respberry Camera Module v2
- Canon Selphy CP910
- Xbox 360 Controller
- An awesome wood box made by hand

### How it works

The [script](photobooth.py) is minimal, it display the Camera module preview in the screen and wait the user to press a key. The P key capture a photo and display it. The user can press P again to print the photo or press C to continue. 

To be more user-friendly, I add a Xbox 360 Controller and map the P key to the A button and the C key to the B button. (see the [Bash script](start_controller.sh)) 

### Note about the printer

The Canon Selphy CP910 has some issues with Cups in USB. The printer can print one picture and then freeze. So after few searches, I found this threads which propose a solution [raspberrypi.org](https://www.raspberrypi.org/forums/viewtopic.php?p=747363#p747363)
