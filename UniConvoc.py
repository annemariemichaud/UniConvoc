# -*- coding: utf-8 -*-
import PyPDF2
import re

pdfOMFile = open('om.pdf', 'rb')
pdfOMReader = PyPDF2.PdfFileReader(pdfOMFile)

for pageNum in range(pdfOMReader.numPages):
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = pdfOMReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)
    contenu_page=pageObj.extractText()
    regexp='(Mme|M.)\\n-\\n[A-Z]*\\n-\\n[A-Z]*'
    result = re.search(regexp, contenu_page)
    if result:
        name_new_file = 'OM' + '_' + result.group(0).replace('\n-\n','_')+ '.pdf'
    else:
        name_new_file = 'OM' + '_' + str(pageNum+1) + '.pdf'
    pdfOutputFile = open(name_new_file, 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()

pdfOMFile.close()

