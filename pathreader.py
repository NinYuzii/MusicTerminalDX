from pathlib import Path
import curses
import mpv
import time


#Inicializa el audio player(mpv) y tambien iniciamos la interfaz grafica de la terminal
player = mpv.MPV(video = False)
stdscr = curses.initscr()



musiclist = []

def Get_Dir_Folder(stdsrc):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    
    #Pedimos la ruta de la carpeta que tiene la musica y la imprimimos por pantalla
    stdsrc.addstr(0,0,"Input your music folder direction, starting in home: ")
    path = Path.home() / stdscr.getstr().decode("utf-8")
    return path
    
def Reproducir_Musica(Index):
        player.play(str(musiclist[Index]))
        stdscr.addstr(1,60,"Reproduciendo: " + musiclist[Index].name)
        


def Mostrar_Musica(stdscr, musiclist, path):
    stdscr.keypad(True)
    curses.cbreak()
    curses.noecho()
    musiclist.clear()
    #Vemos cada archivo en la carpeta y lo agregamos a la lista de reproduccion
    for archivo in path.iterdir():
        if(archivo.name.endswith(".mp3")):
            musiclist.append(archivo)
    musiclist.sort()
    stdscr.clear()
    #Conseguimos la maxima altura de la terminal y la maxima de ancho
    height , width = stdscr.getmaxyx()
    downcoordinate = 0
    for mp3 in musiclist:
        #Si intentamos esxribir mas de la cuenta se parara
        if(downcoordinate >= height - 1):
            break
        stdscr.addstr(downcoordinate,0,mp3.name[0:mp3.name.find(".mp3")])
        downcoordinate += 1
    stdscr.refresh()
    selected = 0
    stdscr.addstr(selected,0,musiclist[selected].name[0:musiclist[selected].name.find(".mp3")], curses.A_REVERSE)
    while(True):
        stdscr.refresh()
        currentTrack = musiclist[selected]
        stdscr.addstr(selected,0,currentTrack.name[0:currentTrack.name.find(".mp3")], curses.A_REVERSE)
        key = stdscr.getch()

        if(key == curses.KEY_UP and selected != 0):
            selected -= 1
        elif(key == curses.KEY_DOWN and selected < len(musiclist) - 1):
            selected += 1
        elif key in (10, 13, curses.KEY_ENTER):
            stdscr.addstr(0, 60, "ENTER DETECTADO")
            Reproducir_Musica(selected)
             
    


path = curses.wrapper(Get_Dir_Folder)#Prepara la terminal para usar la interfaz grafica
curses.wrapper(Mostrar_Musica, musiclist, path)


#Por lo mientras no usare esta parte del codigo
while(True):
    time.sleep(1)

    if player.time_pos is None or player.duration is None:
        continue

    actualmin, actualsec = divmod(int(player.time_pos), 60)
    totalmin, totalsec = divmod(int(player.duration), 60)

    print(
        f"{actualmin}:{actualsec:02}",
        f"{totalmin}:{totalsec:02}"
    )



