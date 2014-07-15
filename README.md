Sublime-Sound
=============

Sublime-Text plugin to play event sounds.
Fun :smile:

__Supported Platforms__

||osx|linux|windows|
|:----:|:----:|:----:|:----:|
|Sublime Text 2|:o:|:x:|:o:|
|Sublime Text 3|:o:|:x:|:o:|

##Installation

You can install from [Package Control](https://sublime.wbond.net/).

__Package Control: Install Package__ > Select __Sound__

##Event Lists

+ __on_new__: played when new file buffer is created.
+ __on_load__: played when the file is finished loading.
+ __on_save__: played when file view has been saved.
+ __on_close__: played when a file view is closed.
+ __on_clone__: played when a file view is cloned from an existing one.
+ __on_modify__: played when a file view is changed.

##Custom Sounds

You can customize playing sounds by replace file. (only supports mp3 file now)

Replace mp3 on __Preference > Package Settings > Sound > Open sounds > event_name__ directory.

###Random playing sounds

By default, 8 defferent sounds played in each key types(on modify event). In this way, you can also be assigned to the event multiple sounds.

1. Put your sound files on event name directory
2. Rename these files sequentially
3. Edit num_files property in _settings - User_
