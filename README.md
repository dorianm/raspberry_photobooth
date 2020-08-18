# Photobooth Raspberry PI

Source code of my project to build a photobooth from a Raspberry Pi v3 and the Camera Module v2. It has been develop for a photo animation at a weeding. Feel free to use it !

### Equipment used

- Raspberry PI v3
- Raspberry Camera Module v2
- Xbox 360 Controller
- An awesome handmade wood box

### How it works

The [script](photobooth.py) is minimal, it display the Camera module preview in the screen and wait the user to press a key. The P key capture a photo and display it. The user can press P again to continue (and take another photo). 

To be more user-friendly, I add a Xbox 360 Controller and map the P key to the A button. (see the [Bash script](start_controller.sh)) 
