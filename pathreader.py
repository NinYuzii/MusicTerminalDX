from pathlib import Path
import curses
import pygame


#Pedimos la ruta de la carpeta que tiene la musica y la imprimimos por pantalla

p = Path.home() / input("Input your music folder direction, starting in home: ")

print(p)
musiclist = []

#Vemos cada archivo en la carpeta y lo agregamos a la lista de reproduccion
for archivo in p.iterdir():
    if(archivo.name.find(".mp3") != -1):
        musiclist.append(archivo)

musiclist.sort()
for mp3 in musiclist:
    print(mp3.name[0:mp3.name.find(".mp3")])

print("Te gustaria reproducir la primer cancion de la lista?")
if(input("S/N ") == "S"):
    pygame.init()
    pygame.mixer.music.load(str(musiclist[0]))
    pygame.mixer.music.play()
    print("Reproduciendo: " + musiclist[0].name)
else:
    print("Fin")


print("Desea parar?")

if(input("S/N ") == "S"):
   pygame.mixer.stop()

