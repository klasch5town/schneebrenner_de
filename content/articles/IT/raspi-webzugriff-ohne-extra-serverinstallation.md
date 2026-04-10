Title: Raspi-Webzugriff ohne extra Serverinstallation
Date: 2015-04-04 12:44
Modified: 2024-05-20 11:55
Author: klasch
Tags: Computer, Linux, python, Raspberry-Pi
Slug: raspi-webzugriff-ohne-extra-serverinstallation
Status: published

Wenn man einen Raspberry-Pi remote betreibt, dann bleibt für die Interaktion nicht viel mehr übrig, als die Remote-Shell, ein Web-Frontend oder das Umleiten des X-Servers auf die Host-Maschine. In diesem Beitrag will ich mich auf die zweite Variante konzentrieren und aufzeigen, wie das sehr schnell ohne Installation eines eigenen Webservers, wie den Apache oder Nginx, geht.  
Das Setup, welches ich gewählt habe, ist [CherryPy](https://cherrypy.dev "CherryPy - A Minimalist Python Web Framework"), weil mit diesem Framework ein Web-Server mitkommt und außerdem mit der Raspberry-Pi Haus- und Hof-Programmiersprache Python gefüttert wird.  
Bei meinen Programmierausflügen mit Python versuche ich immer auf die 3er Version von Python zu setzen, weswegen ich hier auch die Anleitung dafür auslege.  
Als erstes muss man sich den Python Package Manager PIP installieren, um damit dann CherryPy zu installieren - das alles habe ich bereits in meinem Artikel [PIP für Python 3.x unter Linux installieren](http://schneebrenner.de/?p=144 "PIP für Python 3.x unter Linux installieren") beschrieben.  
Als nächsten Schritt legt man am besten ein cherryPy-Verzeichnis an und speichert darin die cherryPy-Scripte. Hier darf natürlich das obligatorische Hello-World nicht fehlen. Auf der [CherryPy-Doku-Seite](https://docs.cherrypy.dev/en/latest/ "CherryPy - A Minimalist Python Web Framework") ist dieses auch gleich an erster Stelle platziert. Ist man mit der graphischen Oberfläche direkt auf dem RasPi unterwegs so funktioniert das auf Anhieb, aber in meinem Fall soll der Zugriff ja remote innerhalb des Hausnetzwerkes erfolgen. Dazu muss das Script noch etwas angepasst werden und zusätzlich noch eine Konfigurationsdatei angelegt werden. Man könnte zwar die Konfiguration auch noch mit in das Python-Script packen, aber wir wollen bei unseren Experimenten ja nicht jedes Mal die selbe Konfiguration mit in das Script packen - das Angeben einer externen Konfigurationsdatei ist hier wohl deutlich komfortabler.  
So habe ich das helloWorld-Beispiel folgendermaßen abgewandelt  

    #!/usr/bin/python3

    import cherrypy

    class HelloWorld(object):  
    def index(self):  
    return "Hello World\!"  
    index.exposed = True

    if __name__ == '__main__':  
    cherrypy.quickstart(HelloWorld(), config="cherryPy.conf")  
    [/python]

und die dazugehörige Konfigurationsdatei cherryPy.conf wie folgt aufgebaut:

    [code]  
    [global]  
    server.socket_host = "192.168.10.17"  
    server.socket_port = 8080  
    server.thread_pool = 10  
    [/code]

Startet man nun das Script mit `python3 cpHelloWorld.py`, so sieht man wie der Server aufgesetzt wird.

    pi@raspberrypi ~/cherryPy $ python3 cpHelloWorld.py 
    [04/Apr/2015:09:52:37] ENGINE Listening for SIGHUP.
    [04/Apr/2015:09:52:37] ENGINE Listening for SIGTERM.
    [04/Apr/2015:09:52:37] ENGINE Listening for SIGUSR1.
    [04/Apr/2015:09:52:37] ENGINE Bus STARTING
    [04/Apr/2015:09:52:37] ENGINE Started monitor thread 'Autoreloader'.
    [04/Apr/2015:09:52:37] ENGINE Started monitor thread '_TimeoutMonitor'.
    [04/Apr/2015:09:52:37] ENGINE Serving on http://192.168.10.17:8080
    [04/Apr/2015:09:52:37] ENGINE Bus STARTED

Die Hello-World Seite kann nun von jeder beliebigen Maschine im Netz unter der angegebenen IP-Adresse aufgerufen werden:  
![cherryPyHelloWorld]({static}/images/cherryPyHelloWorld.png)  
Und das tolle an diesem Setup ist, dass das Script nach einer Änderung nicht jedes Mal neu gestartet werden muss, sondern das Framework eine Modifikation der Datei automatisch erkennt und diese neu ausliefert.  
Einfach mal ausprobieren und im Script aus "Hello World" ein "Hello Raspi-World" machen und die Datei abspeichern. Die Konsolenausgabe zeigt an, dass die Änderung erkannt wurde:

    [04/Apr/2015:12:21:55] ENGINE Restarting because /home/pi/cherryPy/cpHelloWorld.py changed.
    [04/Apr/2015:12:21:55] ENGINE Stopped thread 'Autoreloader'.
    [04/Apr/2015:12:21:55] ENGINE Bus STOPPING
    [04/Apr/2015:12:21:55] ENGINE HTTP Server cherrypy._cpwsgi_server.CPWSGIServer(('192.168.10.17',8080)) shut down
    [04/Apr/2015:12:21:55] ENGINE Stopped thread '_TimeoutMonitor'.
    [04/Apr/2015:12:21:55] ENGINE Bus STOPPED
    [04/Apr/2015:12:21:55] ENGINE Bus EXITING
    [04/Apr/2015:12:21:55] ENGINE Bus EXITED
    [04/Apr/2015:12:21:55] ENGINE Waiting for child threads to terminate...
    [04/Apr/2015:12:21:55] ENGINE Re-spawning cpHelloWorld.py
    [04/Apr/2015:12:21:58] ENGINE Listening for SIGHUP.
    [04/Apr/2015:12:21:58] ENGINE Listening for SIGTERM.
    [04/Apr/2015:12:21:58] ENGINE Listening for SIGUSR1.
    [04/Apr/2015:12:21:58] ENGINE Bus STARTING
    [04/Apr/2015:12:21:58] ENGINE Started monitor thread 'Autoreloader'.
    [04/Apr/2015:12:21:58] ENGINE Started monitor thread '_TimeoutMonitor'.
    [04/Apr/2015:12:21:59] ENGINE Serving on http://192.168.150.175:8080
    [04/Apr/2015:12:21:59] ENGINE Bus STARTED

Nun gilt es nur noch im Browser einen Reload zu veranlassen und siehe da, schon erscheint die Änderung im Browser.  
![cherryPy\_helloRaspiWorld]({static}/images/cherryPy_helloRaspiWorld.png)  
Nun lässt sich das Script beliebig erweitern. Dazu rate ich die [Tutorials der cherryPy-Dokumentation](http://docs.cherrypy.org/en/latest/tutorials.html "cherryPy - Tutorials") genauer zu studieren - evtl. gibt es ja auch noch einen weiteren Beitrag zu diesem Thema. Mal schauen, was die Zeit bringt.  
Noch viel Spaß beim Ausprobieren!

    HINWEIS:
    Ich habe zwar beim Update (Übertragen von Wordpress nach Pelican) die Links überprüft,
    aber nicht, ob das Beispiel noch funktioniert!