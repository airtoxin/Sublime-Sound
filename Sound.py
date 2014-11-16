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
        self.filepaths = {}

    @thread
    def _play(self, dirname, func):
        self.on_play_flag = False
        dir_path = join(sublime.packages_path(), "Sound", "sounds", dirname)
        sound_files = self.filepaths.setdefault(dir_path, self._get_sound_files(dir_path))
        if not len(sound_files) == 0:
            func(dir_path, sound_files)

    def osx_play(self, dirname):
        def func(dir_path, sound_files):
            volume = self.get_volume()
            call(["afplay", "-v", str(volume / 100), join(dir_path, choice(sound_files))])
        self._play(dirname, func)

    def win_play(self, dirname):
        def func(dir_path, sound_files):
            winsound.PlaySound(join(dir_path, choice(sound_files)), winsound.SND_FILENAME | winsound.SND_ASYNC)
        self._play(dirname, func)

    def linux_play(self, dirname):
        def func(dir_path, sound_files):
            call(["aplay", join(dir_path, choice(sound_files))])
        self._play(dirname, func)

    def _get_sound_files(self, dir_path):
        if exists(dir_path):
            return [f for f in listdir(dir_path) if f.endswith(".wav") ]
        else:
            return []

    def on_new(self, view):
        self.throttle(lambda: self.play("on_new"), 100)

    def on_clone(self, view):
        self.throttle(lambda: self.play("on_clone"), 100)

    def on_load(self, view):
        self.throttle(lambda: self.play("on_load"), 100)

    def on_close(self, view):
        self.throttle(lambda: self.play("on_close"), 100)

    def on_pre_save(self, view):
        self.throttle(lambda: self.play("on_save"), 100)

    def on_modified(self, view):
        self.throttle(lambda: self.play("on_modify"), 100)

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
