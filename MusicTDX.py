from pathlib import Path
import curses
import mpv
import time


#Inicializa el audio player(mpv) y tambien iniciamos la interfaz grafica de la terminal
player = mpv.MPV(video = False)
stdscr = curses.initscr()

def Get_Dir_Folder(stdsrc):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)
    
    #Pedimos la ruta de la carpeta que tiene la musica y la imprimimos por pantalla
    stdsrc.addstr(0,0,"Input your music folder direction, starting in home: ")
    path = Path.home() / stdscr.getstr().decode("utf-8")
    return path
    
def Reproducir_Musica(listaMusica, Index):
        player.play(str(listaMusica[Index]))
        stdscr.clear()
        stdscr.addstr(0,60,"Reproduciendo: " + listaMusica[Index].name)
        


def Ordenar_Musica(path):
    listaMusica = []
    #Vemos cada archivo en la carpeta y lo agregamos a la lista de reproduccion
    for archivo in path.iterdir():
        if(archivo.name.endswith(".mp3")):
            listaMusica.append(archivo)
    listaMusica.sort()
    return listaMusica


def Mostrar_Refrescar_Musica(stdscr, listaMusica):
    seleccion = 0
    # Al parecer cualquier funcion que ejecutemos desde esta podra usar la interfaz grafica sin pasarla como argumento

    stdscr.keypad(True)
    curses.cbreak()
    curses.noecho()
    stdscr.clear()
    while(True):
        #Conseguimos la maxima altura de la terminal y la maxima de ancho
        height , width = stdscr.getmaxyx()
        currentTrack = listaMusica[seleccion]
        #Por cada mp3 en musica lo imprimiremos en pantalla, y el seleccionado con efecto marcado
        for mp3 in listaMusica:
            if(mp3 == currentTrack):
                if(seleccion <= height - 1):
                    stdscr.addstr(seleccion,0,currentTrack.name[0:currentTrack.name.find(".mp3")], curses.A_REVERSE)
            else:
                if(listaMusica.index(mp3) <= height - 1):
                    stdscr.addstr(listaMusica.index(mp3),0,mp3.name[0:mp3.name.find(".mp3")])
        stdscr.refresh()
        key = stdscr.getch()
        if(key == curses.KEY_UP and seleccion > 0):
            seleccion -= 1
        elif(key == curses.KEY_DOWN and seleccion < len(listaMusica) - 1):
            seleccion += 1
        elif(key == 10):#* Tecla enter
            Reproducir_Musica(listaMusica, seleccion)
        elif(key == ord("q")):
            player.stop()
            break

    
                    
    

#Bloque donde ejecutamos las funciones (Aca empieza a ejecutarse el programa)

direccionCarpeta = curses.wrapper(Get_Dir_Folder) #* Prepara la terminal para usar la interfaz grafica
listaMusica = Ordenar_Musica(direccionCarpeta)#* Ordenamos la lista de reproduccion segun requiera el usuario
curses.wrapper(Mostrar_Refrescar_Musica, listaMusica)# *Se pone la funcion principal en la interfaz grafica donde el usuario va a interactuar 


    

#Por lo mientras no usare esta parte del codigo
def Show_Time():
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



