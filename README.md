Sublime-Sound
=============

Sublime-Text plugin to play event sounds.
Fun :smile:

__Supported Platforms__

||osx|linux|windows|
|:----:|:----:|:----:|:----:|
|Sublime Text 2|:o:|:x:|:x:|
|Sublime Text 3|:o:|:x:|:x:|

##Installation

You can install from [Package Control](https://sublime.wbond.net/).

__Package Control: Install Package__ > Select __Sound__

##Event Sounds

+ __on_new__: played when new file buffer is created.
+ __on_load__: played when the file is finished loading.
+ __on_save__: played when file view has been saved.
+ __on_close__: played when a file view is closed.
+ __on_clone__: played when a file view is cloned from an existing one.
+ __on_modify__: played when a file view is changed.

##Custom Sounds

You can customize sounds by replace file. (Only supports mp3 file)

###Single sound file

+ on_new
+ on_load
+ on_save
+ on_close
+ on_clone

These events sound file exists on __PackageDirectory > Sound > sounds__ directory.

###Multi sounds file

+ on_modify

These events sound file exists on __PackageDirectory > random_sounds > event_name__ directory.
