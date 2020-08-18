#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import time

import picamera
import pygame
from pygame.locals import *

# Directory to save pictures
SAVE_PATH_ROOT = os.path.expanduser("~/photobooth/")


class DisplayUI:
    """ Manage the UI """

    def __init__(self):
        """ Init l'affichage de l'UI """
        # Init Pygame
        pygame.init()

        # Set background
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.surface = pygame.Surface(self.screen.get_size())
        self.background = self.surface.convert()

        # Displayed message
        self.little_message = ""
        self.number = ""
        self.image_displayed = ""

    def set_little_message(self, msg):
        """ Define the message to display in top of the screen """
        self.little_message = msg
        return self

    def set_number(self, number):
        """ Define the number to display in the middle of the screen """
        self.number = number
        return self

    def set_image_displayed(self, photo_path):
        """ Define the path of the picture to display """
        self.image_displayed = photo_path
        return self

    def _get_text_pos_center(self, text):
        """ Return the text  """
        textpos = text.get_rect()
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().centery
        return textpos

    def update(self):
        """ Met a jour l'affichage """
        self.background.fill(pygame.Color("black"))  # Black background

        small_font = pygame.font.Font(None, 30)

        if not self.image_displayed == "":
            picture = pygame.image.load(self.image_displayed)
            picture = pygame.transform.scale(picture, (1440, 1050))
            self.background.blit(picture, (120, 0))

        if not self.number == "":
            font = pygame.font.Font(None, 500)
            text = font.render(self.number, 1, (0, 0, 255))
            self.background.blit(text, self._get_text_pos_center(text))

        if not self.little_message == "":
            self.background.blit(
                small_font.render(
                    self.little_message,
                    1,
                    (255, 255, 255)
                ),
                (0, 0)
            )

        self.screen.blit(self.background, (0, 0))

        # Draw a rect in the screen to delimit an area
        # which will be printed (change it if you change the screen or the printer)
        pygame.draw.rect(self.screen, pygame.Color("white"), (-5, 120, 1690, 840), 1)
        pygame.display.flip()


class Camera:
    """ Manage the camera (Raspberry Camera) """

    def __init__(self, display, save_path):
        """ Turn on the camera, and display a message  """
        self.display = display
        self.display.set_little_message("Chargement...").update()
        self.save_path = save_path

        self.camera = picamera.PiCamera()
        self.camera.preview_alpha = 120
        self.camera.resolution = (2592, 1944)
        self.camera.start_preview()

    def close(self):
        """ Turn off the camera """
        self.camera.stop_preview()

    def hide_preview(self):
        """ Hide the preview to display another picture in the screen """
        self.camera.preview_alpha = 0

    def show_preview(self):
        """ Display the preview """
        self.camera.preview_alpha = 120

    def capture(self):
        """ Capture a photo after a countdown of 5 seconds """
        self.display.set_message("")
        for countdown in ["5", "4", "3", "2", "1"]:
            self.display.set_number(countdown).update()
            time.sleep(1)

        filename = 'photo_'
        filename += datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename += '.jpg'

        # capture the image
        self.camera.capture(os.path.join(self.save_path, filename))
        self.display.set_number("").set_message("").update()

        return os.path.join(self.save_path, filename)


if __name__ == "__main__":
    display = DisplayUI()
    camera = Camera(display, SAVE_PATH_ROOT)

    display.set_little_message("").update()

    # True if the user asked to exit
    should_exit = False

    # Path of the last photo captured
    image = ""
    image_displayed = False

    while not should_exit:

        # Gestion du message affiche et de l'ecran affiche (photo ou prise de vue)
        if image == "":
            display.set_little_message("A pour prendre une photo").set_image_displayed("").update()
            image_displayed = False
            camera.show_preview()
        else:
            if not image_displayed:
                display.set_little_message("Appuyer sur A pour prendre une nouvelle photo").set_image_displayed(
                    image).update()
                camera.hide_preview()
                image_displayed = True

        try:
            for event in pygame.event.get():
                # Exit
                if event.type == pygame.QUIT:
                    should_exit = True
                # Keyboard pressed
                if event.type == pygame.KEYDOWN:
                    # Exit or not print
                    if event.key == pygame.K_ESCAPE:
                        if image != "":
                            image = ""
                        else:
                            should_exit = True
                    elif event.key == pygame.K_p:
                        # Print
                        if image != "":
                            image = ""
                        # Capture
                        else:
                            image = camera.capture()
        except KeyboardInterrupt:
            should_exit = True

    camera.close()
