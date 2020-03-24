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
    #afficher la fenêtre d'erreur
    tkMessageBox.showinfo("ALERTE", message)
    top.mainloop()

def trouver_nom_stage(pdfOMreader):
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
        dispositif = 'inconnu'
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
    return nom_repertoire

def creation_repertoire(nom_repertoire):
    try:
        os.mkdir(nom_repertoire)
        return False
    except OSError:
        #message_erreur = 'Le dossier ' + nom_repertoire + ' existe deja'
        #afficher_message_erreur(message_erreur)
        return True

def creation_fichiers_pdf(pdfOMReader,nom_repertoire):
    #création d'un compteur pour le cas ou nbre de pages # nbre de convocations
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
    files = os.listdir(nom_repertoire)
    for name in files:
        if name.find('.pdf')!=-1:
            nombre_fichiers_pdf = nombre_fichiers_pdf + 1
    if nombre_fichiers_pdf!=pdfOMReader.numPages:
        afficher_message_erreur("Le nombre de pages (stage : " + nom_repertoire + ") ne correspond pas aux nombres de fichiers PDF")

    

#initialisation de la liste des fichiers PDF
liste_fichiers_pdf = []
#ouverture du fichier pdf contenant toutes les convocations concaténées à la suite les unes des autres
files = os.listdir('.')
for name in files:
    if name.find('.pdf')!=-1:
            pdfOMFile = open(name, 'rb')
            liste_fichiers_pdf.append(pdfOMFile)
for fichier_pdf in liste_fichiers_pdf:
    pdfOMReader = PyPDF2.PdfFileReader(fichier_pdf)
    nouveau_repertoire = trouver_nom_stage(pdfOMReader)
    verification_repertoire_existant = creation_repertoire(nouveau_repertoire)
    if not(verification_repertoire_existant):
        creation_fichiers_pdf(pdfOMReader,nouveau_repertoire)
    fichier_pdf.close()




   
