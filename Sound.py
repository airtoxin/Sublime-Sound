import sublime, sublime_plugin
from subprocess import call
from os.path import join, normpath, dirname, abspath
import sys
from random import randrange

__file__ = normpath(abspath(__file__))
__path__ = dirname(__file__)
libs_path = join(__path__, 'libs')
if libs_path not in sys.path:
    sys.path.insert(0, libs_path)

from decorators import thread

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        super(EventSound, self).__init__(*args, **kwargs)

        if sublime.platform() == "osx":
            self.play = self.osx_play
        elif sublime.platform() == "linux":
            pass  # TODO
        elif sublime.platform() == "windows":
            pass  # TODO

    @thread
    def osx_play(self, event_name, random=False):
        self.on_play_flag = False
        if not random:
            file_path = join(sublime.packages_path(), "Sound", "sounds", event_name) + ".mp3"
        else:
            num_files = sublime.load_settings("Sound.sublime-settings").get("random_sounds")[event_name]["num_files"]
            file_path = join(sublime.packages_path(), "Sound", "random_sounds", event_name, str(randrange(1, num_files))) + ".mp3"
        call(["afplay", file_path])

    def on_new_async(self, view):
        # Called when a new buffer is created. Runs in a separate thread, and does not block the application.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False  # TODO: use decorator
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_new"), 100)

    def on_clone_async(self, view):
        # Called when a view is cloned from an existing one. Runs in a separate thread, and does not block the application.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_clone"), 100)

    def on_load_async(self, view):
        # Called when the file is finished loading. Runs in a separate thread, and does not block the application.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_load"), 100)

    def on_close(self, view):
        # Called when a view is closed (note, there may still be other views into the same buffer).
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_close"), 100)

    def on_pre_save_async(self, view):
        # Called after a view has been saved. Runs in a separate thread, and does not block the application.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_save"), 100)

    def on_modified_async(self, view):
        # Called after changes have been made to a view. Runs in a separate thread, and does not block the application.
        if not hasattr(self, "on_play_flag"): self.on_play_flag = False
        if self.on_play_flag: return
        self.on_play_flag = True
        sublime.set_timeout(lambda: self.play("on_modify", random=True), 100)
