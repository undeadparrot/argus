=====
argus
=====

Eventy system for semantic knowledge management, document review, etc.

This is not meant to be implemented as one application, or even using a cohesive stack. Argus is meant to be a collection of services and applications writing to a common event log, giving me the opportunity to implement parts of it with libraries and technologies that I am curious about.

The choice of writing events is to allow me to change how the system works and just reprocess the log, without losing information.
Previous hobby attempts have been plagued by changing something and having to migrate or throw away the old data.
The event log is more resilient, and it allows me to start capturing data even before there is an application to use it. I can send notes to the 'notes' topic via cURL right now, and not worry about a proper Notes app until I feel like it.

> If you are looking for a personal wiki with some semantic elements, I would recommend `Trilium <https://github.com/zadam/trilium>`_ instead.

------------
Architecture
------------

The core of Argus should be the event log. All other applications built on it would rebuild
their state from the event log, and write changes to it ala event sourcing. 


--------------------------
Things I would like to try
--------------------------


RDF
---

I would like to build a semantic graph of knowledge from the event log.

Web Sockets
-----------

To update pages after events are processed (considering that event-sourcing makes this eventually consistent). 

-------
Plugins
-------


Browser History
---------------

This tracks page navigations as a graph (this URL led to these other URLs).


Clipboard
---------

Monitors the clipboard for changes and logs any stored strings.

Active Window
-------------

Monitors which window is open on the desktop, and logs any changes

File Changes
------------

Monitors for changes to files within configured folders, such as Documents.

Snipping Tool
-------------

Save content from the browser.


Events

