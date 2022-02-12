# Program to explain how to use File chooser in kivy

# import kivy module
import kivy

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require('1.9.0')

# BoxLayout arranges widgets in either in
# a vertical fashion that is one on top of
# another or in a horizontal fashion
# that is one after another.
from kivy.uix.boxlayout import BoxLayout


# create the layout class
class Filechooser(BoxLayout):
    def select(self, *args):
        try:
            self.label.text = args[1][0]
        except:
            pass


# Create the App class
class Editor(App):
    def build(self):
        return Filechooser()


# run the App
if __name__ == '__main__':
    Editor().run()