#!/usr/bin/env python3

import signal

import gi
import dbus
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')

from gi.repository import Gtk
from gi.repository.Gdk import ScrollDirection
from gi.repository import AppIndicator3
from gi.repository import Notify

APPINDICATOR_ID = "kupiakos-brightness-changer"


class BrightnessApp:
    def __init__(self):
        icon_theme = Gtk.IconTheme.get_default()
        self.indicator = AppIndicator3.Indicator.new(
            APPINDICATOR_ID,
            icon_theme.lookup_icon('weather-clear', 16, 0).get_filename(),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES)
        bus = dbus.SessionBus()
        settings = bus.get_object(
            'org.gnome.SettingsDaemon', '/org/gnome/SettingsDaemon/Power')
        self.screen = dbus.Interface(
            settings, 'org.gnome.SettingsDaemon.Power.Screen')
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.build_menu())
        self.indicator.connect('scroll-event', self.scroll)
        Notify.init(APPINDICATOR_ID)

    def build_menu(self):
        menu = Gtk.Menu()

        item_quit = Gtk.MenuItem("Quit")
        item_quit.connect('activate', quit)
        menu.append(item_quit)

        menu.show_all()

        return menu

    def scroll(self, obj, amt, direction):
        if direction == ScrollDirection.UP:
            self.screen.StepUp()
        elif direction == ScrollDirection.DOWN:
            self.screen.StepDown()

    def quit(self, source):
        Notify.uninit()
        Gtk.main_quit()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = BrightnessApp()
    Gtk.main()
