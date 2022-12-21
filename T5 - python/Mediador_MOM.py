"""
*
********************************************************************************************************************************
* Mediador_MOM.py
* 
*   ()[][]   
*   [][]     
*   [][][]   
*   [][]   - Programação Paralela e Distribuida(PPD) - 2022.2 - Prof.Cidcley
*                                          
********************************************************************************************************************************
*
* *********************
* Bibliotecas utilizada
* *********************
*
"""

import paho.mqtt.client as mqtt # <---- Principal tecnologia do código! (MOM)
from queue import Queue # Usada para se criar uma estrutura de dados que amazene as msgs pegues dos tópicos assinados

#Bibliotecas para manipulação dos arquivos de imagem utilizados no código para poder compactá-los no arquivo .exe quando for construido:
import sys
import os

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

from AnimatedGIF import *

"""Principais variáveis (GLOBAIS) utilizadas"""
endereco_Broker = "mqtt.eclipseprojects.io" # Broker online para testes
mensagens_recebidas = Queue() # Armazena as mensagens numa 'Queue' que é 'thread safe' já que usamos muitas threads nesse projeto

"""
*
* ********************************************************
* Funções Auxiliares para algumas 'funcionalidades extras'
* ********************************************************
*
"""

# Método que éc hamado quando o Cliente recebe uma mensagem do seu tópico inscrito
def on_message(client, userdata, message):
    global mensagens_recebidas
    print(str(mensagens_recebidas))
    mensagens_recebidas.put(str(message.payload.decode("utf-8")) + "\n--------------------------------------------------------------\n*Tópico: " + str(message.topic))

# usada para a criação do .EXE
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

"""
*
*  *********************************************************
*  Construção de Interface Gráfica com a biblioteca Tkinter
*  *********************************************************
*
"""

root = Tk()
root.withdraw()

# ABAIXO, AS TELAS DO MEDIADOR - MOM:
path_img_bg_mediador_MOM_asset = resource_path('recursos/bg_mediador_MOM.png')
img_bg_mediador_MOM_asset = PhotoImage(file=path_img_bg_mediador_MOM_asset, master=root)

def fecha_APLICACAO(Toplevel):
    Toplevel.destroy()      
    Toplevel.quit()
    root. destroy()
    os._exit(1) 

def janela_Mediador():
    global endereco_Broker
    
    newWindow = Toplevel(root)
    newWindow.title("MOM: Mediador")
    icone_asset_url = resource_path('recursos/icone.ico')
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("375x426")

    newWindow.protocol("WM_DELETE_WINDOW", lambda:fecha_APLICACAO(newWindow))

    bg_label = Label(newWindow,image = img_bg_mediador_MOM_asset, width=371, height=425)
    bg_label.place(x=0, y=0)

    gif_bg_asset_url = resource_path('recursos/gifs/mediador_GIF.gif') 
    lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
    lbl_with_my_gif.config(bg='black')
    lbl_with_my_gif.place(x=22, y=20)
    lbl_with_my_gif.start()

    text_area = ScrolledText(newWindow,wrap = WORD, width = 39,height = 13,font = ("Callibri",9))
    text_area.place(x=37, y=174)
    text_area.focus()

    text_area.insert(INSERT,"[ ! ] Mediador conectado!\n\n", 'dados__entrada_mediador')
    text_area.insert(INSERT,"--------------------------------------------------------------\n\n ...\n\n\n\n\n\n\n\n\n", 'dados__entrada_mediador')
    text_area.tag_config('dados__entrada_mediador', background='black',foreground='lime')

    # *Parte que usa MQTT
    client_subscriber_Mediador = mqtt.Client("Mediador")
    client_subscriber_Mediador.connect(endereco_Broker)
    client_subscriber_Mediador.is_connected()
    client_subscriber_Mediador.subscribe("guarda_mensagens/Suspeitas") # <---- Tópico exclusivo para armazenar as mensagens enviadas pelo espião
    client_subscriber_Mediador.loop_start()
    client_subscriber_Mediador.on_message=on_message
    newWindow.after(1,lambda:checa_Recebidos_no_Topico(newWindow,text_area))

# Checa se há mensagens no Tópico assinado
def checa_Recebidos_no_Topico(newWindow,text_area):
    global mensagens_recebidas
                               
    if mensagens_recebidas.empty() == True:
        pass  # Link que ajudou nesse trecho: https://realpython.com/python-pass/
    else:
        text_area.insert(INSERT,"--------------------------------------------------------------\n", 'dados_recebidos_tipicos')
        text_area.insert(INSERT,"[ ! ]MENSAGEM RECEBIDA DO ESPIÃO:\n--------------------------------------------------------------\n", 'dados_recebidos_tipicos')
        text_area.insert(INSERT,mensagens_recebidas.get(), 'dados_recebidos_tipicos')
        text_area.insert(INSERT,"\n\n--------------------------------------------------------------", 'dados_recebidos_tipicos')
        text_area.insert(INSERT,"\n...\n", 'dados_recebidos_tipicos')
        text_area.tag_config('dados_recebidos_tipicos', background='black',foreground='lime')
        
    newWindow.after(1,lambda:checa_Recebidos_no_Topico(newWindow,text_area))

"""
*
*  **************************************
*  Inicializando a aplicação do Mediador
*  **************************************
*
"""

if __name__ == "__main__":
    janela_Mediador()
    root.mainloop()

