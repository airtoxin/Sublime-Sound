import sublime, sublime_plugin
from subprocess import call
from os import listdir
from os.path import join, normpath, dirname, abspath, exists, splitext
import sys
from random import choice

try:
    import winsound
except ImportError:
    pass

__file__ = normpath(abspath(__file__))
__path__ = dirname(__file__)
libs_path = join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from decorators import thread

sounds_path = join(sublime.packages_path(), "Sound", "sounds")

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        super(EventSound, self).__init__(*args, **kwargs)

        if sublime.platform() == "osx":
            self.play = self.osx_play
        elif sublime.platform() == "linux":
            pass  # TODO
        elif sublime.platform() == "windows":
            self.play = self.win_play

    @thread
    def osx_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(sounds_path, event_name)
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                call(["afplay", join(dir_path, choice(sound_files))])

    @thread
    def win_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(sounds_path, event_name)
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                winsound.PlaySound(join(dir_path, choice(sound_files)), winsound.SND_FILENAME | winsound.SND_ASYNC)

    def on_new_async(self, view):
        # Called when a new buffer is created. Runs in a separate thread, and does not block the application.
        self.throttle(lambda: self.play("on_new"), 100)

    def on_clone_async(self, view):
        # Called when a view is cloned from an existing one. Runs in a separate thread, and does not block the application.
        self.throttle(lambda: self.play("on_clone"), 100)

    def on_load_async(self, view):
        # Called when the file is finished loading. Runs in a separate thread, and does not block the application.
        self.throttle(lambda: self.play("on_load"), 100)

    def on_close(self, view):
        # Called when a view is closed (note, there may still be other views into the same buffer).
        self.throttle(lambda: self.play("on_close"), 100)

    def on_pre_save_async(self, view):
        # Called after a view has been saved. Runs in a separate thread, and does not block the application.
        self.throttle(lambda: self.play("on_save"), 100)

    def on_modified_async(self, view):
        # Called after changes have been made to a view. Runs in a separate thread, and does not block the application.
        self.throttle(lambda: self.play("on_modify"), 100)

    def throttle(self, func, time):
        # Creates a function that, when executed, will only call the func function at most once per every time milliseconds.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(func, time)


class OpenSoundsDirectoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if sublime.platform() == "osx":
            call(["open", sounds_path])
        elif sublime.platform() == "linux":
            pass  # TODO
        elif sublime.platform() == "windows":
            call(["explorer", sounds_path])
