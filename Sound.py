import sublime, sublime_plugin
from subprocess import check_output, call
import threading, random

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kwargs):
        super(EventSound, self).__init__(*args, **kwargs)

        if sublime.platform() == "osx":
            self.play = self.osx_play
            self.random_play = self.osx_random_play
        elif sublime.platform() == "linux":
            pass  # TODO
        elif sublime.platform() == "windows":
            pass  # TODO

    def osx_play(self, filename):
        threading.Thread(target=lambda: self._osx_play(filename)).start()

    def osx_random_play(self, dirname):
        threading.Thread(target=lambda: self._osx_random_play(dirname)).start()

    def _osx_play(self, filename):
        self.on_play_flag = False
        call(["afplay", "{0}/Sublime-Sound/sounds/{1}.mp3".format(sublime.packages_path(), filename)])

    def _osx_random_play(self, dirname):
        self.on_play_flag = False
        num_files = sublime.load_settings("Sound.sublime-settings").get("random_sounds")["on_modify"]["num_files"]
        call(["afplay", "{0}/Sublime-Sound/random_sounds/{1}/{2}.mp3".format(sublime.packages_path(), dirname, random.randrange(1, num_files))])

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
        sublime.set_timeout(lambda: self.random_play("on_modify"), 100)
