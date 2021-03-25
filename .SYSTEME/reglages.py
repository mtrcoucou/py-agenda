#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
#					REGLAGES MANUELS 									#

#	nombre de jours accessibles dans le fichier "en cours":
dates=70 # en cas de modification:
		# penser à modifier aussi les noms des fichiers (cf lignes 36 à 40)
#	nom du fichier en cours
en_cours=str(dates)+"_prochains_jours_.txt"
force_name_en_cours=0	# mettre =1 si necessaire

#	jours de décalage pour l'arcchivage'
reglage_delta=-1

#	nom de la suite du calendrier:
suite="plus_tard_.txt"

#	date de départ,date de fin
datdep="2020-01-01"
datfin="2100-12-31"

#	chemin vers les sauvegardes:
sauvegardes="sauvegardes"
ecriture_auto=1
#########################################################################
#					REGLAGES AVANCES									#
message="\n ne pas effacer :\n"
jours=["Dimanche ","lundi    ","mardi    ","mercredi ","jeudi    ","vendredi ","samedi   "]
mois=" Janvier   , Fevrier   , Mars      , Avril     , Mai       , Juin      , Juillet   , Aout      , Septembre , Octobre   , Novembre  , Decembre  ".split(",")
# les jours doivent faire 9 caractères , et les mois : 11 caractères
separateur="____________________________________\n"
decoj="------ "
decom=" #######"
decoa=decom*7+"### "
if force_name_en_cours==0:
	if 4<dates<9:en_cours="cette_semaine.txt"
	if 29<dates<38:en_cours="mois_en_cours.txt"
	if 85<dates<100:en_cours="ce_trimestre.txt"
	if 360<dates<400:en_cours="cette_annee.txt"
#########################################################################
