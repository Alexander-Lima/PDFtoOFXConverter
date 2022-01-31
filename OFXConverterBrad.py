from OFXConverter import ClassOFXConverter

class OFXConverterBrad (ClassOFXConverter):
    def getStatements (self):
        try:
            normalFields = 6
            date, memo, value, storedMemo = ('',)*4
            linesCounter = self.countLines()
            results = []

            with open(self.output_file_name, 'r') as opFile:
                for x in range(0,linesCounter):
                    readableLine = opFile.readline()
                    fields = readableLine.split('\t')
            
                    if fields.__len__() == normalFields:
                        date = fields[0] if (fields[0] and fields[0] != '""') else date

                        #get memo from 2 lined statements
                        if fields[1] and not fields[2]:
                            storedMemo = fields[1]

                        elif not fields[1] and fields[2]:
                            value = fields[3] if fields[3] else fields[4]
                            stmnt = self.Statement(date, storedMemo, value)
                            results.append(stmnt)
                
                        #get memo from 1 lined statements
                        elif fields[1] and fields[2]:
                            storedMemo = ''
                            memo = fields[1]
                            value = fields[3] if fields[3] else fields[4]
                            stmnt = self.Statement(date, memo, value)
                            results.append(stmnt)
                return results
        except:
            self.rootPane.hideModal()
            raise Exception(f'Erro ao processar arquivo {self.format.upper()}!')

    def getConvertedValue(self, valueText):
        newValue = valueText.replace('.','').replace(',','.')
        if newValue.find('.') == -1:
            return newValue + '.00'
        else:
            return newValue        

    def getConvertedDate (self, dateText):
        minDateFields = 3
        newDate = dateText.split('/')
        if newDate.__len__() == minDateFields:
            newDate = f'{newDate[2]}{newDate[1]}{newDate[0]}'
            return newDate







