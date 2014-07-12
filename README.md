Sublime-Sound
=============

Sublime-Text plugin to play event sounds.
Fun :smile:

||osx|linux|windows|
|:----:|:----:|:----:|:----:|
|Sublime Text 2|:o:|:x:|:x:|
|Sublime Text 3|:o:|:x:|:x:|

##Installation

__Package Control: Install Package__ > Select __Sound__

##Events

+ __on_new__: called when new file buffer is created.
+ __on_load__: called when the file is finished loading.
+ __on_save__: called when file view has been saved.
+ __on_close__: called when a file view is closed.
+ __on_clone__: called when a file view is cloned from an existing one.

##Custom Sounds

You can customize sounds by replace file.
The file exists __PackageDirectory > Sound > sounds__. 

Only supports mp3 file.
