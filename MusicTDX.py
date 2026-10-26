from pathlib import Path
import curses
import mpv
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3


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
    
def Play_Music(playWin, musicList, Index):
        player.play(str(musicList[Index]))
        mp3info = MP3(musicList[Index], ID3 = ID3)
        playWin.clear()
        playWin.addstr(0,0,"Playing: " + str(mp3info.tags["TIT2"]))#Titulo
        playWin.addstr(1,0,"Artist: " + str(mp3info.tags["TPE1"]))#Artista
        playWin.refresh()
        return Index


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
    midTerminalPos = round(height/2 - 5) #La mitad de la altura de la terminal menos un ajuste para que se vea bien

    #Por cada mp3 en musica lo imprimiremos en pantalla, y el seleccionado con efecto marcado
    for index, mp3 in enumerate(musicList):
        distance = abs(selected-index)#Determinamos la distance entre el seleccionado y la cancion analizada

        #//Determinar Sangria//#
        if(distance <= 8):
            indentation = abs(8 - distance)
        else:
            indentation = 0

        #//Imprimir canciones//#
        if(index == selected):#Si el index coincide con la cancion seleccionada entonces la imprimiremos con efecto revertido
            stdscr.addstr(midTerminalPos, indentation - 1,">" + "\u266a  " + currentTrack.name[0:currentTrack.name.find(".mp3")], curses.A_REVERSE)
        else:
            if(midTerminalPos + distance <= height - 1 and index > selected):#Aqui con (index > selected) vemos si la cancion analizada esta adelante en la lista
                stdscr.addstr(midTerminalPos + distance, indentation, "\u266a " + mp3.name[0:mp3.name.find(".mp3")])# Y lo imprimimos abajo

            elif(midTerminalPos - distance <= height - 1 and index < selected): #Lo que estamos haciendo con (index < selected) 
                if(midTerminalPos - distance > -1):                              #es ver si la cancion esta antes de la seleccionada
                    stdscr.addstr(midTerminalPos - distance, indentation, "\u266a " + mp3.name[0:mp3.name.find(".mp3")])#para despues imprimirlos arriba
                 
        #Aqui le hice una modificacion bien chida y simplifique el codigo como un pro (Con distance)




#Por lo mientras no usare esta parte del codigo
def Show_Time():
        if player.time_pos is None or player.duration is None:
            return

        actualmin, actualsec = divmod(int(player.time_pos), 60)
        totalmin, totalsec = divmod(int(player.duration), 60)

        stdscr.addstr(5,60,f"{actualmin}:{actualsec:02}"f"{totalmin}:{totalsec:02}")


def Show_Redraw_Music(stdscr, musicList):
    stdscr.clear()
    stdscr.refresh()
    selected = 0
    songEnded = False
    # Al parecer cualquier funcion que ejecutemos desde esta podra usar la interfaz grafica sin tener que usar wrapper
    height , width = stdscr.getmaxyx()
    musicListWin = curses.newwin(height, round(width/2), 0, 0)
    playWin = curses.newwin(height, round(width/2), 0, round(width/2))
    musicListWin.keypad(True)
    curses.cbreak()
    curses.noecho()
    playlistLength = len(musicList) 
    @player.event_callback("end-file")
    def On_End_File(event):
        nonlocal songEnded
        reason = event.data.reason
        if(reason == 0):
            songEnded = True

    while(True):

        musicListWin.clear()
        Print_MusicList(musicListWin, musicList, selected)
        musicListWin.refresh()
        musicListWin.timeout(500)
        #Se pide un input para poder seguir y si no consigue uno en 500 ms entonces pasara -1 (Leer documentacion es util)
        key = musicListWin.getch()
        if(key == curses.KEY_UP and selected > 0):
            selected -= 1
        elif(key == curses.KEY_DOWN and selected < playlistLength - 1):
            selected += 1
        elif(key == 10):#* Tecla enter
            indOfSong = Play_Music(playWin, musicList, selected)
        elif(key == ord("q")):
            player.stop()
            break
        elif(key == -1 ):
            if(songEnded):
                nextSong = indOfSong + 1
                if(nextSong < playlistLength - 1):
                    indOfSong = Play_Music(playWin, musicList, nextSong)
                    songEnded = False
                    selected = indOfSong


                           
                    
    
                    
    

#Bloque donde ejecutamos las funciones (Aca empieza a ejecutarse el programa)

direccionCarpeta = curses.wrapper(Get_Dir_Folder) #* Prepara la terminal para usar la interfaz grafica
musicList = Sort_Playlist(direccionCarpeta)#* Ordenamos la lista de reproduccion segun requiera el usuario
curses.wrapper(Show_Redraw_Music, musicList)# *Se pone la funcion principal en la interfaz grafica donde el usuario va a interactuar 


    


