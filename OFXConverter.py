import tabula
import os
import traceback
from tkinter import filedialog
from tkinter import messagebox

class ClassOFXConverter:
    def __init__(self, format='tsv'):
        self.desktopPath = f'{os.environ["USERPROFILE"]}\Desktop'
        self.format = format
        self.output_file_name = self.desktopPath + r'\temporaryFile.' + format

    class Statement:
        def __init__(self, date, memo, value):
            self.date = date
            self.memo = memo
            self.value = value

    def getFormattedFile(self):
        file_path = filedialog.askopenfilename()
     
        if file_path:
            if file_path.find('.PDF') != -1 or file_path.find('.pdf') != -1:
                try:
                    tabula.convert_into(file_path, self.output_file_name, self.format, pages='all')
                    return True
                except:
                    messagebox.showerror('ERRO!','Algo errado aconteceu!\nNão foi possível converter o arquivo.')
            else:
                messagebox.showerror('ERRO!','Extensão de arquivo não suportada!')
        else:
            messagebox.showerror('ERRO!','Nenhum arquivo selecionado!')

    def countLines (self):
        with open(self.output_file_name, 'r') as opFile:
            texto = opFile.readlines()
            counter = len(texto)
            return counter

    def getStatements (self):
        pass

    def createOFX (self):
        statements = self.getStatements()
        filePath = self.desktopPath + '\ArquivoOFX.ofx'
        newOFXFile = open(filePath, 'w')
        newOFXFile.write('<OFX>\n')
        if statements.__len__() >=1:
            for stmnt in statements:
                    date = self.getConvertedDate(stmnt.date)
                    value = self.getConvertedValue(stmnt.value)
                    newOFXFile.write(
                        f'\t<STMTTRN>\n'+
                        f'\t    <TRNTYPE>{"DEBIT" if value[0] == "-" else "CREDIT"}</TRNTYPE>\n' + 
                        f'\t    <DTPOSTED>{date}</DTPOSTED>\n' + 
                        f'\t    <TRNAMT>{value}</TRNAMT>\n' + 
                        '\t    <FITID></FITID>\n' + 
                        '\t    <CHECKNUM></CHECKNUM>\n'+
                        f'\t    <MEMO>{stmnt.memo}</MEMO>\n' + 
                        '\t</STMTTRN>\n')
            newOFXFile.write('\n</OFX>')
            newOFXFile.close()
            messagebox.showinfo(message='Arquivo gerado com sucesso!')
        else:
            raise Exception('Algo errado aconteceu! \nNenhum lançamento foi gerado.')

    def getNormalizedMemo(self):
        pass
    
    def getConvertedDate (self, dateText):
        pass

    def getConvertedValue (self, valueText):
        pass

    def processAll (self):
        try:
            if self.getFormattedFile():
                self.getStatements()
                self.createOFX()
        except Exception as e:
            messagebox.showerror('ERRO!', 'Erro inesperado, verifique o log gerado.')
            with open(r'C:\Users\contabil\Desktop/log.txt', 'w') as log:
                log.write(traceback.format_exc())





