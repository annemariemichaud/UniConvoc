# -*- coding: utf-8 -*-
import PyPDF2

pdfOMFile = open('om.pdf', 'rb')
pdfOMReader = PyPDF2.PdfFileReader(pdfOMFile)


for pageNum in range(pdfOMReader.numPages):
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = pdfOMReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)
    name_new_file = 'OM' + '_' + str(pageNum+1) + '.pdf'
    pdfOutputFile = open(name_new_file, 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()

pdfOMFile.close()

