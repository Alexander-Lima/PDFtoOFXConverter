from time import sleep, time
import tkinter as tk
from tkinter import ttk
from OFXConverterBB import OFXConverterBB
from OFXConverterBrad import OFXConverterBrad

class Main():
    def __init__(self):
        self.rootPane = tk.Tk()
        self.rootPaneHeight = ''
        self.rootPaneWidth = ''
        self.rootPaneCenterX = ''
        self.rootPaneCenterY = ''
    
    def showPanel(self):
        self.modalWin.withdraw()
        self.rootPane.mainloop()

    def setRootGeometry(self, width, height):
        coord = self.setCenter(width, height)
        self.rootPaneCenterX = coord['x']
        self.rootPaneCenterY = coord['y']
        self.rootPane.geometry(f'{width}x{height}+{self.rootPaneCenterX}+{self.rootPaneCenterY}')

    def setModalGeometry(self, width, height):
        coord = self.setCenter(width, height)
        self.modalWin.geometry(f'{width}x{height}+{coord["x"]}+{coord["y"]}')

    def setModalConfigs(self):
        self.modalWin.title('')
        self.rootPane.config(bg='white')
        self.modalWin.resizable(width=0, height=0)
        self.modalWin.overrideredirect(1)

    def setRootConfigs(self):
        self.rootPane.title('CONVERSOR PDF -> OFX')
        self.rootPane.config(bg='white')
        self.rootPane.resizable(width=0, height=0)

    def setCenter(self, width, height):
        screenMedWidth = self.rootPane.winfo_screenwidth()/2
        screenMedheight = self.rootPane.winfo_screenheight()/2
        centerX = int(screenMedWidth - width/2)
        centerY = int(screenMedheight - height/2)
        return {'x':centerX, 'y': centerY}

    def hideRoot(self):
        self.rootPane.withdraw()

    def showRoot(self):
        self.modalWin.withdraw()
        self.rootPane.deiconify()
        self.rootPane.update()

    def createComponents(self):
        self.bradescoImg = tk.PhotoImage(file = r'./Images/Bradesco_logo.png')
        buttonBradesco = tk.Button(self.rootPane, image=self.bradescoImg, height=75, width=100, command=lambda: self.processPDF('Brad'))

        self.bbImg = tk.PhotoImage(file = r'./Images/BB_logo.png')
        buttonBB = tk.Button(self.rootPane, image=self.bbImg, height=75, width=100, command=lambda: self.processPDF('BB'))
        
        self.resultado_logo = tk.PhotoImage(file = r'./Images/Resultado_logo.png')
        header = tk.Label(self.rootPane, image=self.resultado_logo, height=100, width=300, bg='white')
        
        text = tk.Label(bg='white', height=2 ,text='SELECIONE O BANCO DE ORIGEM DO PDF:', font=('Arial', 10, 'bold'))

        self.modalWin = tk.Toplevel(self.rootPane)
        self.modalLabel = tk.Label(self.modalWin, text='AGUARDE,\nPROCESSANDO...',font=('Arial', 15, 'bold'))

        self.progressBar = ttk.Progressbar(self.modalWin, length=170, mode='determinate', maximum=100)

        header.place(x=0, y=0)
        text.place(x=25, y=110)
        buttonBradesco.place(x=40, y=180)
        buttonBB.place(x=180, y=180)
        self.modalLabel.place(x=15,y=15)
        self.progressBar.place(x=15, y=80)
       
    def startAll(self):
        self.setRootGeometry(320,300)
        self.setRootConfigs()
        self.createComponents()
        self.showPanel()

    def showModal(self):
        self.hideRoot()
        self.modalWin.deiconify()
        self.setModalGeometry(200,120)
        self.setModalConfigs()
        self.rootPane.update()

    def hideModal(self):
        self.modalWin.withdraw()

    def updateProgressBar(self,value):
        self.progressBar['value'] = value
        self.modalWin.update()
        sleep(0.5)
        self.progressBar['value'] = 0

    def processPDF(self, bank):
        if bank == 'BB':
            self.converter = OFXConverterBB(self)
            self.converter.processAll()
        elif bank == 'Brad':
            self.converter = OFXConverterBrad(self)
            self.converter.processAll()


main = Main()
main.startAll()









