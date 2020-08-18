#!/bin/bash

# Start the Xbox 360 controller driver.
# Run that script, and connect the controller, A is mapped to P and B to C

sudo rmmod xpad
sudo xboxdrv --ui-buttonmap A=key:KEY_P
