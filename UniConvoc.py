# -*- coding: utf-8 -*-
import PyPDF2
import re
import os
import Tkinter
import tkMessageBox

def afficher_message_erreur(message):
    top = Tkinter.Tk()
    #centrer le message d'erreur sur l'écran
    top.eval('tk::PlaceWindow %s center' % top.winfo_pathname(top.winfo_id()))
    tkMessageBox.showinfo("ALERTE", message)
    top.mainloop()

#ouverture du fichier pdf contenant toutes les convocations concaténées à la suite les unes des autres
#le nom par défaut est om.pdf (généré automatiquemnt par GAIA)
pdfOMFile = open('om_essai.pdf', 'rb')
pdfOMReader = PyPDF2.PdfFileReader(pdfOMFile)

#extraction du numéro de dispositif, module et groupe
pageObj = pdfOMReader.getPage(0)
contenu_premiere_page=pageObj.extractText()
regExpDispositif = 'Dispositif:[A-Z0-9]{10}'
regExpModule = 'Module:[0-9]{5}'
regExpGroupe = 'Groupedesession:[0-9]{2}'
result_dispositif = re.search(regExpDispositif, contenu_premiere_page)
if result_dispositif:
    dispositif = result_dispositif.group(0).replace('Dispositif:','')
else:
    dipositif = 'inconnu'
result_module = re.search(regExpModule, contenu_premiere_page)
if result_module:
    module = result_module.group(0).replace('Module:','')
else:
    module = 'inconnu'
result_groupe = re.search(regExpGroupe, contenu_premiere_page)
if result_groupe:
    groupe=result_groupe.group(0).replace('Groupedesession:','')
else:
    groupe='inconnu'

nom_repertoire = dispositif + '_' + module + '_' + groupe

try:
    os.mkdir(nom_repertoire)
except OSError:
    afficher_message_erreur("Le répertoire des fichiers PDF existe déjà")

 #création d'un compteur pour le cas ou nbre de pages > nbre de convocations
compteur = 0

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
    #le nom du fichier est OMNumeroPage_Mme_NOM_PRENOM ou OM_M_Nom_PRENOM
        compteur = compteur + 1
        name_new_file = 'OM' + str(compteur) + '_' + result.group(0).replace('\n-\n','_').replace('.','')+ '.pdf'
        pdfOutputFile = open(nom_repertoire + '/' + name_new_file, 'wb')
        pdfWriter.write(pdfOutputFile)
        pdfOutputFile.close()

#test nombre de fichier créés = nombre de pages
nombre_fichiers_pdf = 0
for path, subdirs,files in os.walk(nom_repertoire):
    for name in files:
        if name.find('.pdf'):
            nombre_fichiers_pdf = nombre_fichiers_pdf + 1
if nombre_fichiers_pdf!=pdfOMReader.numPages:
    afficher_message_erreur("Le nombre de pages ne correspond pas aux nombres de fichiers PDF")

pdfOMFile.close()



   
