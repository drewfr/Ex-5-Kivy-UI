import os
import pygame

# os.environ['DISPLAY'] = ":0.0"
# os.environ['KIVY_WINDOW'] = 'egl_rpi'

from kivy.app import App
from kivy.properties import StringProperty
import pickle
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.clock import Clock

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.kivy.selfupdatinglabel import SelfUpdatingLabel
from pidev.Joystick import Joystick
from pidev.stepper import stepper

from datetime import datetime

pygame.init()
joy = Joystick(number=0, ssh_deploy=True)

time = datetime

MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
SECOND_WINDOW_NAME = 'second'
THIRD_WINDOW_NAME = 'third'
ADMIN_SCREEN_NAME = 'admin'


class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    counter = StringProperty("0")
    num = 0
    count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.change_pos_label, 0.2)

    def change_pos_label(self, dt):
        self.lb2.text = "x: " + str(joy.get_axis('x')) + "    y: " + str(joy.get_axis('y'))

    def animate_it(self, widget, *args):
        animate = Animation(
            background_color=(0, 0, 1, 1))

        for x in range(20):
            animate += Animation(
                size_hint=(.3, .3))

            animate += Animation(size_hint=(.2, .2))

        animate.start(widget)

    def move_to_second(self):
        SCREEN_MANAGER.current = "second"

    def move_to_third(self):
        SCREEN_MANAGER.current = "third"

    def turn_on(self):
        self.ids.btn2.text = "on"

    def turn_off(self):
        self.ids.btn2.text = "off"

    def add_one(self):
        self.num += 1
        self.counter = str(self.num)

    def change_label(self):
        self.count += 1
        if self.count % 2:
            self.lb1.text = "Motor on"
        else:
            self.lb1.text = "Motor off"


class SecondWindow(Screen):
    counter = StringProperty("0")
    num = 0
    count = 0

    def go_home(self):
        SCREEN_MANAGER.current = 'main'

    def turn_on(self):
        self.ids.btn2.text = "on"

    def turn_off(self):
        self.ids.btn2.text = "off"

    def add_one(self):
        self.num += 1
        self.counter = str(self.num)

    def change_label(self):
        self.count += 1
        if self.count % 2:
            self.lb1.text = "Motor on"
        else:
            self.lb1.text = "Motor off"

    def sliderfunction(self, *args):
        # print(*args)
        self.ids.labelvalue.text = str(int(args[1]))


class ThirdWindow(Screen):

    def go_home(self):
        SCREEN_MANAGER.current = "main"

    def click(self):
        self.ids.my_image.source = 'images2.jpeg'

    def off_click(self):
        self.ids.my_image.source = 'images.jpeg'
        self.go_home()

    def animate_it(self, widget, *args):
        animate = Animation(
            background_color=(0, 0, 1, 1))

        for x in range(20):
            animate += Animation(opacity=1,
                                 size_hint=(.3, .3))

            animate += Animation(size_hint=(.2, .2))

        animate.start(widget)

    def anima(self, widget, *args):
        anim = Animation(x=50) + Animation(size=(80, 80), duration=2.)
        anim.start(widget)

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        print("Callback from MainScreen.pressed()")

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        quit()


"""
Widget additions
"""
Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(SecondWindow(name=SECOND_WINDOW_NAME))
SCREEN_MANAGER.add_widget(ThirdWindow(name=THIRD_WINDOW_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

"""
MixPanel
"""


def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()
