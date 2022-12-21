"""
*
********************************************************************************************************************************
* Espaco_de_Tuplas_Info_User.py
*                        
*   ()[][]                                                                             
*   [][]                                 
*   [][][]                       
*   [][]   - Programação Paralela e Distribuida(PPD) - 2022.2 - Prof.Cidcley
*                                     
* Instituto Federal de Educação, Ciência e Tecnologia do Ceará - IFCE 
*    
******************************************************************************************************************************************************

*  *********************
*  Bibliotecas utilizada 
*  *********************
*
"""

import sys
import os
#import threading, time, random
import time, random

from xmlrpc.client import ServerProxy # <---- Usada para o Espião criar um Proxy que vai acessar o servidor RPC (RPC/RMI)
import ipaddress # <---- Usada aqui para checar a validade de um endereço IP

import linsimpy  # <---- Principal tecnologia do código! (Espaço de Tuplas) 

#Bibliotecas para manipulação e construção da interface gráfica no Tkinter:
from tkinter import *
from AnimatedGIF import *
from tkinter.scrolledtext import ScrolledText
from tkinter import Button, Label, PhotoImage, Tk
import tkinter.font as font
from PIL import Image, ImageTk
# Proxy para se comunicar com o servidor RPC 
proxy = None
# Lista que vai registrar o nome dos usuários criados e sua 'flags' de recebimento de novas msgs ('0' quando não detectou nenhuma msg nova e '1' quando detectou)
lista_registro_usuarios = []
# String que armazena a msg suspeita pra exibí-la na interface do espião
string_msg_SUSPEITA = "" 


class Users(object):

    def __init__(self):
        self.users = linsimpy.TupleSpaceEnvironment()

        self.usersList = []

        self.initUsers()

    def initUsers(self):
        self.users.out(("Users", tuple(self.usersList)))

    def createUser(self, name, nickname, coordinates):
        nicknameList = [nickname]
        coordinatesList = [coordinates]
        status = ["Online"]
        contacts = []

        userList = self.users.inp(("Users", object))
        aux = list(userList[1])
        aux.append(name)
        self.users.out(("Nick", name, tuple(nicknameList)))
        self.users.out(("Coordinates", name, tuple(coordinatesList)))
        self.users.out(("Status", name, tuple(status)))
        self.users.out(("Contacts", name, tuple(contacts)))
        self.users.out(("Users", tuple(aux)))

    def listUsers(self):
        lUsers = self.users.rdp(("Users", object))
        return list(lUsers[1])

    def addNickName(self, userName, newNick):
        nickList = self.users.inp(("Nick", userName, object))
        aux = list(nickList[2])
        aux.append(newNick)
        self.users.out(("Nick", userName, tuple(aux)))

    def listNickname(self, userName):
        listNick = self.users.rdp(("Nick", userName, object))
        return list(listNick[2])

    def changeCoordinates(self, userName, newCoordinates):
        coordinates = self.users.inp(("Coordinates", userName, object))
        aux = list(coordinates[2])
        aux.clear()
        aux.append(newCoordinates)
        self.users.out(("Coordinates", userName, tuple(aux)))

    def getCoordinates(self, userName):
        coordinates = self.users.rdp(("Coordinates", userName, object))
        aux = list(coordinates[2])
        return aux[0]


    def listLocalizador(self, userName):
        coordinates = self.users.rdp(("Coordinates", userName, object))
        return list(coordinates[2])


    def changeStatus(self, userName, status):
        statusList = self.users.inp(("Status", userName, object))
        aux = list(statusList[2])
        aux.clear()

        if status == 1:
            aux.append("Online")

        if status == 0:
            aux.append("Offline")

        self.users.out(("Status", userName, tuple(aux)))

    def getStatus(self, userName):
        status = self.users.rdp(("Status", userName, object))
        aux = list(status[2])

        if aux[0] == "Online":
            return 1
        else:
            return 0

    def addContacts(self, userName, newContact):
        contacts = self.users.inp(("Contacts", userName, object))
        aux = list(contacts[2])
        aux.append(newContact)
        self.users.out(("Contacts", userName, tuple(aux)))

    def listContacts(self, userName):
        contacts = self.users.rdp(("Contacts", userName, object))
        return list(contacts[2])
    

    


##########################################################################################################
##########################################################################################################




class ServerScreen:

    def __init__(self, newServer):
        self.server = newServer
        self.numUser = 0
        self.maxUser = 6
        self.root = Tk()
        self.root.withdraw()

        self.path_img_bg_Insere_Dados_ServidorRPCRMI_asset = self.resource_path('recursos/bg_Insere_Dados_ServidorRPCRMI.png')
        self.img_bg_Insere_Dados_ServidorRPCRMI_asset = PhotoImage(file=self.path_img_bg_Insere_Dados_ServidorRPCRMI_asset, master=self.root)
        self.path_img_botao_Conectar_asset = self.resource_path('recursos/botao_Conectar.png')
        self.img_botao_Conectar_asset = PhotoImage(file=self.path_img_botao_Conectar_asset, master=self.root)

        self.mainScreen() #mudou

        self.root.mainloop()

    def resource_path(self, relative_path):
      try:
          base_path = sys._MEIPASS
      except Exception:
          base_path = os.path.abspath(".")

      return os.path.join(base_path, relative_path)
    

    def mainScreen(self):
        
        newWindow = Toplevel(self.root)
        newWindow.title("Sistema de Comunicação")
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.protocol("WM_DELETE_WINDOW", lambda:self.close(newWindow))
        
        gif_bg_asset_url = self.resource_path('recursos/gifs/chat_bubble_GIF.gif') 
        lbl_with_my_gif = AnimatedGif(newWindow, gif_bg_asset_url,0.30)
        lbl_with_my_gif.config(bg='#ffffff')
        lbl_with_my_gif.place(x=135, y=40)
        lbl_with_my_gif.start()

        lbltitle = Label(newWindow, text="Sistema   de   Comunicação \n baseado em Localização ", font='bold', background="#70ad47")
        lbltitle.place(x=60, y=180)

        btn = Button(newWindow, text="Adicionar User", command=lambda: self.addUserScreen(newWindow))
        btn.place(x=50, y=280)

        btn = Button(newWindow, text="Remover User", command=lambda: self.rmUserScreen(newWindow))
        btn.place(x=200, y=280)

        lUsers = self.server.listUsers() 
        yVal = 90

        if lUsers != []:
            for i in lUsers:
                yVal += 30
                self.addUserButton(newWindow, i, yVal)


    def addUserButton(self, Toplevel, nameUser, yAxis):
        btnUser = Button(Toplevel, text=nameUser, command=lambda: self.janela_Conectar_Servidor_RPCRMI(nameUser), width=35, height=1)
        btnUser.place(x=50, y=yAxis)






    def LocalizadorListScreen(self, nameUser):
        lLocalizador = self.server.listLocalizador(nameUser)
        yVal = 90

        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Localizador List")

        lbl = Label(newWindow, text = "Localizador", bg='#70ad47', font='bold')
        lbl.place(x=140, y=30)

        btn1 = Button(newWindow, text="Adicionar Localizador", command=lambda: self.addLocalizadorScreen(newWindow, nameUser))
        btn1.place(x=50, y=350)

        btn2 = Button(newWindow, text="Remover Localizador", command=lambda: self.rmLocalizadorScreen(newWindow, nameUser))
        btn2.place(x=200, y=350)

        if lLocalizador != []:
            for i in lLocalizador:
                yVal += 30
                self.addLocalizadorButton(newWindow, i, yVal)

    def addLocalizadorButton(self, Toplevel, btnName, yAxis):
        btnLocalizador = Button(Toplevel, text=btnName, command=lambda: self.StatusListScreen(btnName), width=35, height=1)
        btnLocalizador.place(x=40, y=yAxis)

    def StatusListScreen(self, nameLocalizador):
        lStatus = self.server.listStatus(nameLocalizador)
        yVal = 90

        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambiente: Status List")
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')

        lbl = Label(newWindow, text = "Status", bg='#70ad47', font='bold')
        lbl.place(x=140, y=30)

        btn1 = Button(newWindow, text="Adicionar Status", command=lambda: self.addStatusScreen(newWindow, nameLocalizador))
        btn1.place(x=120, y=310)

        btn2 = Button(newWindow, text="Remover Status", command=lambda: self.rmStatusScreen(newWindow, nameLocalizador))
        btn2.place(x=200, y=350)


        if lStatus != []:
            for i in lStatus:
                yVal += 30
                self.addStatusButton(newWindow, i, yVal)

    def addStatusButton(self, Toplevel, btnName, yAxis):
        btnLocalizador = Button(Toplevel, text=btnName, command=lambda: self.procListScreen(btnName), width=35, height=1)
        btnLocalizador.place(x=40, y=yAxis)


    def messageScreen(self, nameStatus, nameProc):
        lMessage = self.server.readMessages(nameProc)
        yVal = 50

        newWindow = Toplevel(self.root)
        newWindow.title("Messages")
        newWindow.geometry("330x400")

        lbl = Label(newWindow, text = "Messages",  bg='#70ad47', font='bold')
        lbl.place(x=130, y=30)

        btn = Button(newWindow, text="Send Message", command=lambda: self.sendMessageScreen(newWindow, nameStatus, nameProc))
        btn.place(x=20, y=350)

        if lMessage != []:
            for i in lMessage:
                yVal += 30
                self.messageLabel(newWindow, i, yVal)

    def messageLabel(self, Toplevel, message, yAxis):
        lbl = Label(Toplevel, text=message)
        lbl.place(x=50, y=yAxis)


##########################################################################################################
##########################################################################################################


    def addUserScreen(self, oldWindow):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambientes: Criar User")
        newWindow.geometry("330x250")
        newWindow.config(bg='#70ad47')

        lblNome = Label(newWindow, text = "Digite os Nomes", font='bold', bg='#70ad47')
        lblNome.place(x=20, y=15)

        lblUser = Label(newWindow, text = "User:",  font='bold', background="#70ad47")
        lblUser.place(x=20, y=50)
        userName = Entry(newWindow)
        userName.place(x=100, y=50, width=180, height=20)

        lblLocalizador = Label(newWindow, text="Localizador:",  font='bold', background="#70ad47")
        lblLocalizador.place(x=20, y=80)
        nomeLocalizador = Entry(newWindow)
        nomeLocalizador.place(x=100, y=80, width=180, height=20)

        lblStatus = Label(newWindow, text="Status:",  font='bold', background="#70ad47")
        lblStatus.place(x=20, y=110)
        nomeStatus = Entry(newWindow)
        nomeStatus.place(x=100, y=110, width=180, height=20)


        btnUser = Button(newWindow, text="Criar", command=lambda: self.newUser( oldWindow,userName.get(), nomeLocalizador.get(), nomeStatus.get(), newWindow), width=10, height=1)
        btnUser.place(x=200, y=180)

    def rmUserScreen(self, oldWindow):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.title("Ambientes: Remover User")
        newWindow.geometry("330x250")
        newWindow.config(bg='#70ad47')

        lblUser = Label(newWindow, text = "Nome User", bg='#70ad47')
        lblUser.place(x=20, y=50)
        userName = Entry(newWindow)
        userName.place(x=100, y=50, width=180, height=20)

        btnUser = Button(newWindow, text="Remover", command=lambda: self.rmUser( oldWindow, userName.get(), newWindow), width=10, height=1)
        btnUser.place(x=200, y=180)

    def addLocalizadorScreen(self, oldWindow, userName):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Criar Localizador")

        lblLocalizador = Label(newWindow, text="Nome Localizador",  bg='#70ad47', font='bold')
        lblLocalizador.place(x=20, y=50)
        nomeLocalizador = Entry(newWindow)
        nomeLocalizador.place(x=110, y=50, width=180, height=20)

        btnLocalizador = Button(newWindow, text="Adicionar", command=lambda: self.newLocalizador(userName, nomeLocalizador.get(), newWindow, oldWindow), width=10, height=1)
        btnLocalizador.place(x=200, y=180)

    def rmLocalizadorScreen(self, oldWindow, userName):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Remover Localizador")

        lblLocalizador = Label(newWindow, text="Nome Localizador",  bg='#70ad47', font='bold')
        lblLocalizador.place(x=20, y=50)
        nomeLocalizador = Entry(newWindow)
        nomeLocalizador.place(x=110, y=50, width=180, height=20)

        btnLocalizador = Button(newWindow, text="Remover", command=lambda: self.rmLocalizador(userName, nomeLocalizador.get(), newWindow, oldWindow), width=10, height=1)
        btnLocalizador.place(x=200, y=180)


    def addStatusScreen(self, oldWindow, nameLocalizador):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Criar Status")

        lblStatus = Label(newWindow, text="Nome Status",  bg='#70ad47', font='bold')
        lblStatus.place(x=20, y=50)
        nomeStatus = Entry(newWindow)
        nomeStatus.place(x=100, y=50, width=180, height=20)

        btnStatus = Button(newWindow, text="Adicionar", command=lambda: self.newStatus(nameLocalizador, nomeStatus.get(), newWindow, oldWindow), width=10, height=1)
        btnStatus.place(x=200, y=180)

    def rmStatusScreen(self, oldWindow, nameLocalizador):
        newWindow = Toplevel(self.root)
        icone_asset_url = self.resource_path('recursos/icone.ico')   
        newWindow.iconbitmap(icone_asset_url) 
        newWindow.geometry("330x400")
        newWindow.config(bg='#70ad47')
        newWindow.title("Ambiente: Remover Status")

        lblStatus = Label(newWindow, text="Nome Status",  bg='#70ad47', font='bold')
        lblStatus.place(x=20, y=50)
        nomeStatus = Entry(newWindow)
        nomeStatus.place(x=100, y=50, width=180, height=20)

        btnStatus = Button(newWindow, text="Remover", command=lambda: self.rmStatus(nameLocalizador, nomeStatus.get(), newWindow, oldWindow), width=10, height=1)
        btnStatus.place(x=200, y=180)

  
    def sendMessageScreen(self, oldWindow, nameStatus, userName):
        newWindow = Toplevel(self.root)
        newWindow.title("Send Message")
        newWindow.geometry("330x250")

        lblUser2 = Label(newWindow, text="De " + userName + " para")
        lblUser2.place(x=20, y=50)
        userName2 = Entry(newWindow)
        userName2.place(x=100, y=50, width=180, height=20)

        lblMessage = Label(newWindow, text="Message")
        lblMessage.place(x=20, y=80)
        message = Entry(newWindow)
        message.place(x=100, y=80, width=180, height=20)

        btnMessage = Button(newWindow, text="Send", command=lambda: self.sendMessage(nameStatus,  userName2.get(), message.get(), newWindow, oldWindow), width=10, height=1)
        btnMessage.place(x=200, y=180)

    def newUser(self, TopLevel, userName, nameLocalizador, nameStatus,  oldWindow):
        if(self.numUser < self.maxUser):
            self.numUser += 1
            self.server.createUser(userName, nameLocalizador, nameStatus)
            print(self.server.listUsers())

        self.closeTab(oldWindow)
        self.closeTab(TopLevel)
        self.mainScreen()

    def rmUser(self, TopLevel, userName, oldWindow):
        if self.server.deleteUser(userName):
            self.numUser -= 1
            self.closeTab(oldWindow)
            self.closeTab(TopLevel)
            self.mainScreen()
        else:
            self.closeTab(oldWindow)

    def newLocalizador(self, userName, nameLocalizador, oldWindow, newWindow):
        if self.server.addNewLocalizador(userName, nameLocalizador):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.LocalizadorListScreen(userName)
        else:
            self.closeTab(oldWindow)

    def rmLocalizador(self, userName, nameLocalizador, oldWindow, newWindow):
        if self.server.deleteLocalizador(userName, nameLocalizador):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.LocalizadorListScreen(userName)
        else:
            self.closeTab(oldWindow)

   

    def newStatus(self, nameLocalizador, nameStatus, oldWindow, newWindow):
        if self.server.addNewStatus(nameLocalizador, nameStatus):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.StatusListScreen(nameLocalizador)
            print(self.server.getStatus())
        else:
            self.closeTab(oldWindow)

    def rmStatus(self, nameLocalizador, nameStatus, oldWindow, newWindow):
        if self.server.deleteStatus(nameLocalizador, nameStatus):
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.StatusListScreen(nameLocalizador)
        else:
            self.closeTab(oldWindow)


    def sendMessage(self, nameStatus, nameProdSender, nameProcReceiver, message, oldWindow, newWindow):
        lProc = self.server.listProc(nameStatus)
        ok = False

        for i in lProc:
            if i == nameProcReceiver:
                ok = True

        if ok:
            self.server.sendMessage(nameProdSender, nameProcReceiver, message)
            self.closeTab(oldWindow)
            self.closeTab(newWindow)
            self.messageScreen(nameStatus, nameProdSender)
        else:
            self.closeTab(oldWindow)


    def close(self, TopLevel):
        TopLevel.destroy()
        TopLevel.quit()
        self.root.destroy()

    def closeTab(self, TopLevel):
        TopLevel.destroy()
    











   

    



    def janela_Erro_PORTA_INVALIDA(self):
        newWindow = Toplevel(self.root)
        newWindow.title("**Conexão: Erro!")
        icone_asset_url = self.resource_path('recursos/icone.ico')    
        newWindow.iconbitmap(icone_asset_url)
        newWindow.geometry("338x183")

        self.path_img_bg_PORTA_SERVIDOR_RPC_INVALIDA_warning_asset = self.resource_path('recursos/bg_PORTA_SERVIDOR_RPC_INVALIDA_warning.png')
        self.img_bg_PORTA_SERVIDOR_RPC_INVALIDA_warning_asset = PhotoImage(file=self.path_img_bg_PORTA_SERVIDOR_RPC_INVALIDA_warning_asset, master=self.root)

        bg_label = Label(newWindow,image = self.img_bg_PORTA_SERVIDOR_RPC_INVALIDA_warning_asset, width=334, height=178)
        bg_label.place(x=0, y=0)

        self.path_img_botao_Ok_asset = self.resource_path('recursos/botao_Ok.png')
        self.img_botao_Ok_asset = PhotoImage(file=self.path_img_botao_Ok_asset, master=self.root)

        ok_button = Button(newWindow, image=self.img_botao_Ok_asset,command=lambda:self.closeTab(Toplevel))
        ok_button.place(x=107, y=127)

    def janela_Erro_IP_INVALIDO(self):
        newWindow = Toplevel(self.root)
        newWindow.title("**Conexão: Erro!")
        icone_asset_url = self.resource_path('recursos/icone.ico')    
        newWindow.iconbitmap(icone_asset_url)
        newWindow.geometry("338x183")

        path_img_botao_Ok_asset = self.resource_path('recursos/botao_Ok.png')
        self.img_botao_Ok_asset = PhotoImage(file=path_img_botao_Ok_asset, master=self.root)

        path_img_bg_IP_SERVIDOR_RPC_INVALIDO_warning_asset = self.resource_path('recursos/bg_IP_SERVIDOR_RPC_INVALIDO_warning.png')
        self.img_bg_IP_SERVIDOR_RPC_INVALIDO_warning_asset = PhotoImage(file=path_img_bg_IP_SERVIDOR_RPC_INVALIDO_warning_asset, master=self.root)

        bg_label = Label(newWindow,image = self.img_bg_IP_SERVIDOR_RPC_INVALIDO_warning_asset, width=334, height=178)
        bg_label.place(x=0, y=0)

        ok_button = Button(newWindow, image=self.img_botao_Ok_asset,command=lambda:self.close(newWindow))
        ok_button.place(x=107, y=127)



    # Janela que recebe os dados para se conectar ao servidor RPC/RMI (IP e PORTA)
    def janela_Conectar_Servidor_RPCRMI(self, nameUser):
        newWindow = Toplevel(self.root)
        newWindow.title("**Conexão: Erro!")
        icone_asset_url = self.resource_path('recursos/icone.ico')    
        newWindow.iconbitmap(icone_asset_url)
        newWindow.geometry("338x183")

        bg_label = Label(newWindow, image = self.img_bg_Insere_Dados_ServidorRPCRMI_asset, width=334, height=178)
        bg_label.place(x=0, y=0)

        IP_input = Entry(newWindow)
        IP_input.place(x=21, y=87,width = 145,height = 26)

        PORTA_input = Entry(newWindow)
        PORTA_input.place(x=181, y=87,width = 145,height = 26)

        

        conectar_button = Button(newWindow, image=self.img_botao_Conectar_asset,command=lambda:self.checa_Dados(str(IP_input.get()),PORTA_input.get()))
        conectar_button.place(x=107, y=127)

    # Checa a validade dos dados recebidos de IP e PORTA e guarda eles se forem válidos
    def checa_Dados(self, endereco_ip,porta):
        try:
            int(porta)
        except Exception as erro:
            self.janela_Erro_PORTA_INVALIDA()
        else:
            try:
                ipaddress.ip_address(endereco_ip)
            except Exception as erro:
                self.janela_Erro_IP_INVALIDO()
            else:
                print("IP e PORTA atualizados no proxy de conexão!")
                self.config_Proxy_RPC(endereco_ip,porta)

    # Usa os dados válidos para criar uma conexão 'proxy' com o servidor RPC/RMI
    def config_Proxy_RPC(self, endereco_ip,porta):
        global proxy
        try:
            proxy = ServerProxy('http://'+endereco_ip+':'+str(porta),allow_none=True)
        except Exception as erro:
            print("*Ops! Houve algum erro de conexão com o Servidor RPC!")
    





if __name__ == "__main__":
    server = Users()
    ServerScreen(server)
    