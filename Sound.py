import sublime, sublime_plugin
from subprocess import check_output, call
import threading

class EventSound(sublime_plugin.EventListener):
    def __init__(self, *args, **kargs):
        super(EventSound, self).__init__(*args, **kargs)

        if sublime.platform() == "osx":
            self.play = self.osx_play
        elif sublime.platform() == "linux":
            pass  # TODO
        elif sublime.platform() == "windows":
            pass  # TODO

    def osx_play(self, filename):
        thread = threading.Thread(target=self._osx_play, args=(filename,))
        thread.start()

    def _osx_play(self, filename):
        call(["afplay", sublime.packages_path() + "/Sublime-Sound/sounds/" + filename + ".mp3"])

    def on_new_async(self, view):
        # Called when a new buffer is created. Runs in a separate thread, and does not block the application.
        self.play("on_new")

    def on_clone_async(self, view):
        # Called when a view is cloned from an existing one. Runs in a separate thread, and does not block the application.
        self.play("on_clone")

    def on_load_async(self, view):
        # Called when the file is finished loading. Runs in a separate thread, and does not block the application.
        self.play("on_load")

    def on_close(self, view):
        # Called when a view is closed (note, there may still be other views into the same buffer).
        self.play("on_close")

    def on_pre_save_async(self, view):
        # Called after a view has been saved. Runs in a separate thread, and does not block the application.
        self.play("on_save")
