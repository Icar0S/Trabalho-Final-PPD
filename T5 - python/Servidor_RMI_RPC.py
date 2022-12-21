"""
*
********************************************************************************************************************************
* Servidor_RMI_RPC.py                     
*                                                                           
*   ()[][]                                                                 
*   [][]                                                                    
*   [][][]                                                                  
*   [][]   - Programação Paralela e Distribuida(PPD) - 2022.2 - Prof.Cidcley
*                                                                           
*********************************************************************************************************************************
"""

"""
*
*  *********************
*  Bibliotecas utilizada
*  *********************
*
"""

from xmlrpc.server import SimpleXMLRPCServer # <---- Principal tecnologia do código! (RPC/RMI)
import paho.mqtt.client as mqtt # <---- Principal tecnologia do código! (MOM)

import socket, threading # <--- 'Socket' aqui é somente usada para conseguir o 'IP' da máquina em que esse Servidor vai estar conectado e executando!

#Bibliotecas para manipulação dos arquivos de imagem utilizados no código para poder compactá-los no arquivo .exe quando for construido:
import sys
import os

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.font as font

from AnimatedGIF import *


"""
*
*  ********************************************************
*  Funções Auxiliares para algumas 'funcionalidades extras'
*  ********************************************************
*
"""

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Método que utilizo para extrair o IP da máquina em que o Servidor está rodando, isso retorna uma string desse IP (Que é IPv4):
def extrai_IP_da_maquina():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP


"""Principais variáveis (GLOBAIS) utilizadas"""

IP_SERVIDOR =  str(extrai_IP_da_maquina()) 
PORTA_SERVIDOR = 12000
endereco_Broker = "mqtt.eclipseprojects.io" #Usa-se um broker simples para testes desses disponíveis Online!


"""
*
*  ********************
*  Parte com MOM
*  ********************
*
"""


client_subscriber_Envia_Mensagens_Suspeitas = mqtt.Client("lista_Mensagens_Suspeitas")
client_subscriber_Envia_Mensagens_Suspeitas.connect(endereco_Broker)
client_subscriber_Envia_Mensagens_Suspeitas.subscribe("guarda_mensagens/Suspeitas")
client_subscriber_Envia_Mensagens_Suspeitas.subscribe("guarda_Dados_Entrada/ServidorRPC")
client_subscriber_Envia_Mensagens_Suspeitas.publish("guarda_Dados_Entrada/ServidorRPC","Servidor RPC está Online!\n--------------------------------------------------------------\n [ *DADOS PARA CONEXÃO: ]\n\n - IP:"+IP_SERVIDOR+"\n - PORTA:"+str(PORTA_SERVIDOR))  


"""
*
*  **************************
*  Parte com RPC/RMI
*  **************************
*
"""

# Classe que vai oferecer o método para o espião enviar as msgs 'SUS' ao Tópico especificado
class metodos_Servidor_RPC:
    # Construtor da classe, basicamente vai definir as variavies 'de instancia' da classe que vão ser acessadas pelos métodos nela:
    def __init__(self,text_area):
        self.txt_area = text_area
    def envia_Msg_Suspeita(self,sala_do_chat,destinatário,remetente,msg_suspeita,lista_palavras_sus):
        global client_subscriber_Envia_Mensagens_Suspeitas
        client_subscriber_Envia_Mensagens_Suspeitas.publish("guarda_mensagens/Suspeitas","Mensagem SUSPEITA detectada:\n ''"+msg_suspeita+"''\n\nPalavras suspeitas: "+lista_palavras_sus+".\n\n**Enviada na sala de Chat: "+sala_do_chat+"\n*(Tupla)Remetente: "+remetente+"\n*(Tupla)Destinatário: "+destinatário+"\n--------------------------------------------------------------\n")  

# Função para criar e inicializar o Servidor RPC
def inicia_servidorRPC(text_area):
    global IP_SERVIDOR,PORTA_SERVIDOR

    #Criamos um objeto da classe que queremos usar na comunicação RPC dos jogadores(Nosso Clientes) com o servidor
    acessar_Metodos_ServidorRPC = metodos_Servidor_RPC(text_area)
    #definindo o servidor e o criando uma thread de sua inicialização que deve permanecer em loop para esperar chamadas remotas dos jogadores aos seus métodos:
    servidor_RPC = SimpleXMLRPCServer((IP_SERVIDOR,PORTA_SERVIDOR),logRequests=True,allow_none=True)
    #Registramos as funções que queremos que sejam acessadas via RPC na nossa instancia do servidor, aqui fez-se uma classe para facilitar nossa vida kkkkk
    servidor_RPC.register_instance(acessar_Metodos_ServidorRPC)

    text_area.insert(INSERT,"Servidor conectado!\n", 'dados__entrada_servidor')
    text_area.insert(INSERT, "\n>> [IP do Servidor]: "+IP_SERVIDOR+"\n>> [PORTA do Servidor]: "+str(PORTA_SERVIDOR)+"\n\n", 'dados__entrada_servidor')
    text_area.insert(INSERT,"-------------------------------------------------------------------\n\n", 'dados__entrada_servidor')
    text_area.tag_config('dados__entrada_servidor', background='red',foreground='black')

    threading.Thread(target=servidor_RPC.serve_forever()).start() #<---- THREAD 'servidor_RPC.serve_forever()' que vai colocá-lo para esperar acessos em loop

"""
*
*  ********************************************************
*  Construção de Interface Gráfica com a biblioteca Tkinter 
*  ********************************************************
*
"""

root = Tk()
root.withdraw()

path_img_bg_servidor_RPCRMI_asset = resource_path('recursos/bg_servidor_RPCRMI.png')
img_bg_servidor_RPCRMI_asset = PhotoImage(file=path_img_bg_servidor_RPCRMI_asset, master=root)

def fecha_APLICACAO(Toplevel):
    Toplevel.destroy()      
    Toplevel.quit()
    root. destroy()
    os._exit(1) 

def mostra_janela_SERVIDOR():
    newWindow = Toplevel(root)
    newWindow.title("RPC/RMI: Servidor")
    icone_asset_url = resource_path('recursos/icone.ico')
    newWindow.iconbitmap(icone_asset_url)
    newWindow.geometry("478x223")

    newWindow.protocol("WM_DELETE_WINDOW", lambda:fecha_APLICACAO(newWindow))

    bg_label = Label(newWindow,image = img_bg_servidor_RPCRMI_asset, width=475, height=222)
    bg_label.place(x=0, y=0)

    gif_bg_asset_url = resource_path('recursos/gifs/servidor_GIF.gif') 
    lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
    lbl_with_my_gif.config(bg='black')
    lbl_with_my_gif.place(x=16, y=137)
    lbl_with_my_gif.start()

    text_area_Janela_Servidor = ScrolledText(newWindow,wrap = WORD, width = 41,height = 6,font = ("Callibri",9))
    text_area_Janela_Servidor.place(x=145, y=99)
    text_area_Janela_Servidor.focus()

    inicia_servidorRPC(text_area_Janela_Servidor)

"""
*
*  *************************************
*  Inicializando a aplicação do Servidor
*  *************************************
*
"""

if __name__ == "__main__":
    threading.Thread(target=mostra_janela_SERVIDOR).start() #<---- THREAD 'mostra_janela_SERVIDOR' ***** 
    root.mainloop()

