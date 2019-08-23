# -*- coding: utf-8 -*-
import PyPDF2
import re

#ouverture du fichier pdf contenant toutes les convocations concaténées à la suite les unes des autres
#le nom par défaut est om.pdf (généré automatiquemnt par GAIA)
pdfOMFile = open('om.pdf', 'rb')
pdfOMReader = PyPDF2.PdfFileReader(pdfOMFile)

#création des fichiers PDF à une seule page
for pageNum in range(pdfOMReader.numPages):
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = pdfOMReader.getPage(pageNum)
    pdfWriter.addPage(pageObj)
    contenu_page=pageObj.extractText()
    #Expression régulière qui cherche chaînes contenant Mme ou M. suivi d'un ensemble de caractères majuscules
    #ou tirets séparés par un retour chariot tiret retour chariot 
    regexp='(Mme|M.)\\n-\\n[A-Z\-]*\\n-\\n[A-Z\-]*'
    result = re.search(regexp, contenu_page)
    if result:
    #le nom du fichier est OM_Mme_NOM_PRENOM ou OM_M_Nom_PRENOM
        name_new_file = 'OM' + '_' + result.group(0).replace('\n-\n','_').replace('.','')+ '.pdf'
    pdfOutputFile = open(name_new_file, 'wb')
    pdfWriter.write(pdfOutputFile)
    pdfOutputFile.close()

pdfOMFile.close()

