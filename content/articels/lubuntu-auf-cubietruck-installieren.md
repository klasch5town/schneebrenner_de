Title: Lubuntu auf Cubietruck installieren
Date: 2014-10-12 19:15
Author: klasch
Category: IT
Tags: cubietruck, linux, ubuntu
Slug: lubuntu-auf-cubietruck-installieren
Status: published

Ich habe schon seit längerem mir ein [Cubietruck-Board](http://linux-sunxi.org/Cubietruck "Cubietruck-Board") zugelegt.

Nun habe ich mir endlich die Zeit genommen, das im Flash liegende Android durch ein Lubuntu zu ersetzen. Dabei hat mir folgende Anleitung geholfen:  
<http://dyhr.com/2013/11/22/how-to-install-lubuntu-server-on-cubietruck-from-mac-os-x/>  
bzw.  
[http://docs.cubieboard.org/tutorials/ct1/installation/cb3\_lubuntu-12.10-desktop\_nand\_installation\_v1.00](http://docs.cubieboard.org/tutorials/ct1/installation/cb3_lubuntu-12.10-desktop_nand_installation_v1.00 "http://docs.cubieboard.org/tutorials/ct1/installation/cb3_lubuntu-12.10-desktop_nand_installation_v1.00")

Nach der Installation hatte ich noch das Problem, dass mein Keyboard-Layout auf US eingestellt war. Abhilfe schafft der Aufruf von:

```
dpkg-reconfigure console-setup
```

Kaum hatte ich alles soweit am Laufen, wollte ich dem System ein update/upgrade gönnen und gab den Befehl dazu:

```
sudo apt-get install update
```

Leider war die Aktion nicht mit dem Erfolg gekrönt. Statt einem satten Update teilte mir der Rechner mit, dass einige Update URLs nicht erreichbar wären:

```
Hit http://ppa.launchpad.net raring Release.gpg  
Ign http://ports.ubuntu.com raring Release.gpg  
Hit http://ppa.launchpad.net raring Release  
Ign http://ports.ubuntu.com raring Release  
Ign http://ports.ubuntu.com raring/main Sources/DiffIndex  
Hit http://ppa.launchpad.net raring/main Sources  
Ign http://ports.ubuntu.com raring/universe Sources/DiffIndex  
Hit http://ppa.launchpad.net raring/main armhf Packages  
Ign http://ports.ubuntu.com raring/main armhf Packages/DiffIndex  
Hit http://ppa.launchpad.net raring/main/debug armhf Packages  
Ign http://ports.ubuntu.com raring/universe armhf Packages/DiffIndex  
Ign http://ppa.launchpad.net raring/main Translation-en  
Ign http://ppa.launchpad.net raring/main/debug Translation-en  
Ign http://ports.ubuntu.com raring/main Translation-en  
Ign http://ports.ubuntu.com raring/universe Translation-en  
Err http://ports.ubuntu.com raring/main Sources  
404 Not Found \[IP: 91.189.88.140 80\]  
Err http://ports.ubuntu.com raring/universe Sources  
404 Not Found \[IP: 91.189.88.140 80\]  
Err http://ports.ubuntu.com raring/main armhf Packages  
404 Not Found \[IP: 91.189.88.140 80\]  
Err http://ports.ubuntu.com raring/universe armhf Packages  
404 Not Found \[IP: 91.189.88.140 80\]  
W: Failed to fetch http://ports.ubuntu.com/ubuntu-ports/dists/raring/main/source/Sources 404 Not Found \[IP: 91.189.88.140 80\]

W: Failed to fetch http://ports.ubuntu.com/ubuntu-ports/dists/raring/universe/source/Sources 404 Not Found \[IP: 91.189.88.140 80\]

W: Failed to fetch http://ports.ubuntu.com/ubuntu-ports/dists/raring/main/binary-armhf/Packages 404 Not Found \[IP: 91.189.88.140 80\]

W: Failed to fetch http://ports.ubuntu.com/ubuntu-ports/dists/raring/universe/binary-armhf/Packages 404 Not Found \[IP: 91.189.88.140 80\]

E: Some index files failed to download. They have been ignored, or old ones used instead.
```

Eine Blick in die [Versionstabelle der Ubuntu Releases unter Wikipedia](https://de.wikipedia.org/wiki/Ubuntu_(Betriebssystem)#Versions%C3%BCberblick) zeigte, dass für die Raring-Ringteil Version 13.04 der Support abgelaufen war und deshalb die Packages in den .. verschoben wurden - die 13.04 hat einfach kein LTS = Long-Term-Support. Eine neuere Version für das Cubie-Truck-Nand gibt es leider noch nicht - 14.04 hätte LTS. Und wichtig - man sollte sich hüten, eine nicht NAND-Version ins Nand-Flash zu überspielen\!  
Es gibt Leute, [die biegen die URLs für APT um](http://vctechblog.wordpress.com/2014/08/08/ubuntu-13-04-raring-ringtail-still-getting-updates/), um die Fehlermeldungen zu umgehen. Dabei Frage ich mich schon, welchen Sinn das macht, wenn es für diese Pakete keinen Support, also Update, mehr gibt.  
Deswegen habe ich mich entschlossen, diese Version im NAND zu lassen, bis es eine NAND-Flash-Version für 14.04 gibt und das OS von SD-Karte zu booten.

```
sudo dd if=path\_of\_your\_image.img of=/dev/diskn bs=1M
```
