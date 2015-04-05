import sublime, sublime_plugin
import urllib, tarfile, os, json
from subprocess import call
from os import listdir
from os.path import join, exists
from random import choice

try:
    import winsound
except Exception:
    pass

from .libs.decorators import thread

STATUS_KEY = "SUBLIMESOUND"
SETTING_NAME = "Sound.sublime-settings"
BASE_SOUNDSET_URL = "https://github.com/airtoxin/Sublime-SoundSets/blob/master/{0}.tar.gz?raw=true"
PACKLIST_URL = "https://raw.githubusercontent.com/airtoxin/Sublime-SoundSets/master/packlist.json"
SOUNDS_DIR_PATH = join(sublime.packages_path(), "Sound", "sounds")

def show_status(message):
    sublime.active_window().active_view().set_status(
        STATUS_KEY,
        message
    )
    sublime.set_timeout(
        lambda: sublime.active_window().active_view().erase_status(STATUS_KEY),
        5000
    )

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        super(EventSound, self).__init__(*args, **kwargs)
        self.play = getattr(self, sublime.platform() + "_play")

    @thread
    def osx_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(
            sublime.packages_path(),
            "Sound",
            "sounds",
            sublime.load_settings(SETTING_NAME).get("soundset"),
            event_name
        )
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                volume = self.get_volume()
                call(["afplay", "-v", str(volume / 100), join(dir_path, choice(sound_files))])

    @thread
    def windows_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(sublime.packages_path(), "Sound", "sounds", event_name)
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                winsound.PlaySound(join(dir_path, choice(sound_files)), winsound.SND_FILENAME | winsound.SND_ASYNC)

    @thread
    def linux_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(sublime.packages_path(), "Sound", "sounds", event_name)
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                call(["aplay", join(dir_path, choice(sound_files))])

    def on_new_async(self, view):
        # Called when a new buffer is created. Runs in a separate thread, and does not block the application.
        self.throttle(
            lambda: self.play("on_new"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def on_clone_async(self, view):
        # Called when a view is cloned from an existing one. Runs in a separate thread, and does not block the application.
        self.throttle(
            lambda: self.play("on_clone"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def on_load_async(self, view):
        # Called when the file is finished loading. Runs in a separate thread, and does not block the application.
        self.throttle(
            lambda: self.play("on_load"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def on_close(self, view):
        # Called when a view is closed (note, there may still be other views into the same buffer).
        self.throttle(
            lambda: self.play("on_close"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def on_pre_save_async(self, view):
        # Called after a view has been saved. Runs in a separate thread, and does not block the application.
        self.throttle(
            lambda: self.play("on_save"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def on_modified_async(self, view):
        # Called after changes have been made to a view. Runs in a separate thread, and does not block the application.
        self.throttle(
            lambda: self.play("on_modify"),
            sublime.load_settings(SETTING_NAME).get("min_span")
        )

    def throttle(self, func, time):
        # Creates a function that, when executed, will only call the func function at most once per every time milliseconds.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(func, time)

    def get_volume(self):
        volume = sublime.load_settings(SETTING_NAME).get("volume")
        return min(100, max(0, volume))

class InstallSoundsetCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        def on_done(name):
            extract_name = join(sublime.packages_path(), "Sound", "sounds")
            tarfile_name = join(extract_name, name + ".tar.gz")
            status_key = "SOUND"
            try:
                urllib.request.urlretrieve(
                   BASE_SOUNDSET_URL.format(name),
                   tarfile_name
                )
                tarfile.open(tarfile_name, "r").extractall(extract_name)
                os.remove(tarfile_name)
            except:
                sublime.active_window().active_view().set_status(
                    status_key,
                    "Soundset Install Failed: " + name
                )
                sublime.set_timeout(
                    lambda: sublime.active_window().active_view().erase_status(status_key),
                    3000
                )
        def on_change(change):
            pass
        def on_cancel():
            pass

        sublime.active_window().show_input_panel(
            "Input soundset_name",
            "",
            on_done,
            on_change,
            on_cancel
        )


class ChangeSoundsetCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        soundsets = [s for s in os.listdir(join(sublime.packages_path(), "Sound", "sounds")) if not s.startswith(".")]
        def on_done(i):
            if i == -1: return
            self.change_setting(soundsets[i])

        sublime.active_window().show_quick_panel(
            soundsets,
            on_done
        )

    def change_setting(self, soundset_name):
        sublime.load_settings(SETTING_NAME).set("soundset", soundset_name)
        sublime.save_settings(SETTING_NAME)


class ToggleSoundCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        current_volume = sublime.load_settings(SETTING_NAME).get("volume")
        sublime.load_settings(SETTING_NAME).set("volume", -current_volume)
        sublime.save_settings(SETTING_NAME)
