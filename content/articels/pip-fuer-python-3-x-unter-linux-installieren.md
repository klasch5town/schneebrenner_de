Title: PIP für Python 3.x unter Linux installieren
Date: 2015-02-22 13:23
Author: klasch
Category: IT
Tags: Computer, Linux, Programmieren, python, Raspberry-Pi
Slug: pip-fuer-python-3-x-unter-linux-installieren
Status: published

Jetzt bin ich schon zum dritten Mal über die Notwendigkeit gestolpert, den [python package-manager pip](https://en.wikipedia.org/wiki/Pip_%28package_manager%29 "python package manager PIP") für Python 3.x zu installieren und habe jedes Mal danach im Internet suchen müssen - nein, nicht googeln, sondern suchen mit [DuckDuckGo](https://duckduckgo.com/ "Suchmachine DuckDuckGo").  
Nachdem meine Linux-Maschinen alle auf [Debian](http://de.wikipedia.org/wiki/Debian "Linux Distribution Debian") basieren, reicht mir die Installation via Debian Package Manager =\> [Advanced Package Tool (APT)](https://en.wikipedia.org/wiki/Advanced_Packaging_Tool "Advanced Package Tool").  
Es genügt dafür folgende Eingabe auf der Kommandozeile:  

    sudo apt-get install python3-pip 

Danach kann man dann Module für Python 3.x installieren indem man folgende Befehlssyntax verwendet:  

    sudo pip-3.2 install cherrypy

Bei meiner Installation (auf dem Raspberry-Pi mit [Raspbian](http://www.raspbian.org/ "Raspberry-Pi OS Raspbian")) waren noch folgende Alternativen möglich:  

    pip      pip-2.6  pip-2.7  pip-3.2

Zumindest weiß ich jetzt beim nächsten mal, wo ich ohne Suchen nachschauen kann und hoffe, dass dieser kurze Artikel vielleicht dem Einen und/oder der Anderen dort draußen in den Weiten des Internet auch hilfreich ist.
