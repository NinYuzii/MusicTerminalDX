from pathlib import Path
import curses
import mpv
import time


#Inicializa el audio player(mpv) y tambien iniciamos la interfaz grafica de la terminal
player = mpv.MPV(video = False)

def Get_Dir_Folder(stdscr):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    
    #Pedimos la ruta de la carpeta que tiene la musica y la imprimimos por pantalla
    stdscr.addstr(0,0,"Input your music folder direction, starting in home: ")
    path = Path.home() / stdscr.getstr().decode("utf-8")
    return path
    
def Play_Music(stdscr, musicList, Index):
        player.play(str(musicList[Index]))
        stdscr.clear()
        stdscr.addstr(0,60,"Reproduciendo: " + musicList[Index].name)
        


def Sort_Playlist(path):
    musicList = []
    #Vemos cada archivo en la carpeta y lo agregamos a la lista de reproduccion
    for archivo in path.iterdir():
        if(archivo.name.endswith(".mp3")):
            musicList.append(archivo)
    musicList.sort()
    return musicList

def Print_MusicList(stdscr, musicList, selected):
    #DESASTRE DE IF'S, ELIF'S Y ELSE'S

    height , width = stdscr.getmaxyx() #Conseguimos la maxima altura de la terminal y la maxima de ancho
    currentTrack = musicList[selected] #La cancion actualmente seleccionada
    midTerminalPos = round(height/2 - 5) #La mitad de la altura de la terminal

    #Por cada mp3 en musica lo imprimiremos en pantalla, y el seleccionado con efecto marcado
    for index, mp3 in enumerate(musicList):
        distancia = abs(selected-index)
        if(distancia <= 8):
            indentation = abs(8 - distancia)
        else:
            indentation = 0
        if(index == selected):
            stdscr.addstr(midTerminalPos, indentation - 1,">" + "\u266a  " + currentTrack.name[0:currentTrack.name.find(".mp3")], curses.A_REVERSE)
        else:
            if(midTerminalPos + (index - selected) <= height - 1 and index > selected):
                stdscr.addstr(midTerminalPos + (index - selected), indentation, "\u266a " + mp3.name[0:mp3.name.find(".mp3")])  
            #Si el indice de la cancion es menor al seleccionado entonces
            elif(midTerminalPos - index <= height - 1 and index < selected):
                if(midTerminalPos - (selected - index)> -1):
                    stdscr.addstr(midTerminalPos - (selected - index), indentation, "\u266a " + mp3.name[0:mp3.name.find(".mp3")])
                 




#Por lo mientras no usare esta parte del codigo
def Show_Time():
        if player.time_pos is None or player.duration is None:
            return

        actualmin, actualsec = divmod(int(player.time_pos), 60)
        totalmin, totalsec = divmod(int(player.duration), 60)

        stdscr.addstr(5,60,f"{actualmin}:{actualsec:02}"f"{totalmin}:{totalsec:02}")


def Show_Redraw_Music(stdscr, musicList):
    selected = 0
    # Al parecer cualquier funcion que ejecutemos desde esta podra usar la interfaz grafica sin pasarla como argumento

    stdscr.keypad(True)
    curses.cbreak()
    curses.noecho()
    stdscr.clear()
    playlistLength = len(musicList)
    while(True):
        stdscr.clear()
        Print_MusicList(stdscr, musicList, selected)   
        stdscr.refresh()
        key = stdscr.getch()
        if(key == curses.KEY_UP and selected > 0):
            selected -= 1
        elif(key == curses.KEY_DOWN and selected < playlistLength - 1):
            selected += 1
        elif(key == 10):#* Tecla enter
            Play_Music(stdscr, musicList, selected)
        elif(key == ord("q")):
            player.stop()
            break

    
                    
    

#Bloque donde ejecutamos las funciones (Aca empieza a ejecutarse el programa)

direccionCarpeta = curses.wrapper(Get_Dir_Folder) #* Prepara la terminal para usar la interfaz grafica
musicList = Sort_Playlist(direccionCarpeta)#* Ordenamos la lista de reproduccion segun requiera el usuario
curses.wrapper(Show_Redraw_Music, musicList)# *Se pone la funcion principal en la interfaz grafica donde el usuario va a interactuar 


    


