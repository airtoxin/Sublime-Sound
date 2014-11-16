import sublime, sublime_plugin
from subprocess import call
from os import listdir
from os.path import join, normpath, dirname, abspath, exists, splitext
import sys
from random import choice

try:
    import winsound
except Exception:
    pass

__file__ = normpath(abspath(__file__))
__path__ = dirname(__file__)
libs_path = join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from decorators import thread

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        super(EventSound, self).__init__(*args, **kwargs)
        self.play = getattr(self, sublime.platform() + '_play')
        events = ["on_new", "on_clone", "on_load", "on_load", "on_pre_save", "on_modify"]
        self.events = [event + "_async" if sublime.version() == "3" else event for event in events]
        self.set_event_triggers()

    def set_event_triggers(self):
        # Create instance methods: self.on_new(self, view) or self.on_new_async(self, view) ...
        for event in self.events:
            def func(view):
                self.throttle(lambda: self.play(event), 100)
            setattr(self, event, func)

    @thread
    def osx_play(self, event_name):
        self.on_play_flag = False
        dir_path = join(sublime.packages_path(), "Sound", "sounds", event_name)
        if exists(dir_path):
            sound_files = [f for f in listdir(dir_path) if f.endswith(".wav") ]
            if not len(sound_files) == 0:
                volume = self.get_volume()
                call(["afplay", "-v", str(volume / 100), join(dir_path, choice(sound_files))])

    @thread
    def win_play(self, event_name):
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

    def throttle(self, func, time):
        # Creates a function that, when executed, will only call the func function at most once per every time milliseconds.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(func, time)

    def get_volume(self):
        volume = sublime.load_settings("Sound.sublime-settings").get("volume")
        if volume == None or volume < 0:
            volume = 0
        elif volume > 100:
            volume = 100
        return volume
