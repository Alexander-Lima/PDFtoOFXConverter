import re
from OFXConverter import ClassOFXConverter

class OFXConverterBB (ClassOFXConverter):
    def getStatements (self):
        try:
            linesCounter = self.countLines()
            results = []
            memoTest = re.compile(r'[a-zA-z\u00C0-\u00FF]')
            dateTest = re.compile(r'[0-9]+/[0-9]+/[0-9]+')
            with open(self.output_file_name, 'r') as opFile:
                for x in range(0,linesCounter):
                    readableLine = opFile.readline()
                    readableLine = readableLine.split('\t')

                    if readableLine.__len__() >= 6:
                        date = readableLine[0] if dateTest.findall(readableLine[0]) else None
                        memo = readableLine[3] if memoTest.findall(readableLine[3]) else readableLine[4]
                        value = readableLine[6] if readableLine[6] else None
                        if date and memo and value:
                            stmnt = self.Statement(date, self.getnormalizedMemo(memo), value)
                            results.append(stmnt)
                return results
        except:
            self.rootPane.hideModal()
            raise Exception(f'Erro ao processar arquivo {self.format.upper()}!')

    def getnormalizedMemo(self,memo):
        resultString = ''
        valueTest = re.compile(r'[a-zA-z\u00C0-\u00FF]+')
        check = valueTest.findall(memo)
        if check.__len__() > 0:
            for item in check:
                resultString = f'{resultString} {item}'.upper()
            return resultString
        else:
            return '' 

    def getConvertedValue (self, valueText):
        newValue = valueText.split(' ')
        minFields = 2
        if newValue.__len__() >= minFields:
            if newValue[1] == 'D':
                return '-' + newValue[0].replace('.','').replace(',','.')
            elif newValue[1] == 'C':
                return newValue[0].replace('.','').replace(',','.')
    
    def getConvertedDate (self, dateText):
        newDate = dateText.split('/')
        minFields = 3
        if newDate.__len__() >= minFields:
            newDate = f'{newDate[2]}{newDate[1]}{newDate[0]}'
            return newDate


