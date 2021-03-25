#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reglages import *
#########################################################################
#					REGLAGES AUTOMATIQUES								#
import re
import sys
import os
from os import listdir
import shutil
import datetime
from datetime import date
from datetime import datetime as dat
misaj=str(sys.argv[0])
an_min=datdep.split("-")[0]
#	chemin vers ce fichier:
REP_A="/".join(misaj.split("/")[0:-2]+[""])
print(REP_A)
aujourdhui=dat.today().isoformat().split("T")[0]  # remettre -1 pour la mise en service
def trouvesortie(an_min):
	annees_visibles=[]
	for i in listdir(REP_A):
		if i.isdigit():annees_visibles.append(i)
	annees_visibles.sort()
	while len(annees_visibles)>2:shutil.move(REP_A+annees_visibles[0],REP_A+sauvegardes+"/"+annees_visibles.pop(0))
	if annees_visibles==[]:annees_visibles.append(an_min)
	return(annees_visibles.pop())
#########################################################################
#					FONCTIONS DU MODULE									#
def ajoute(st,destination):
	ajout=open(REP_A+destination,"a")
	ajout.write(st)
	ajout.close()
def reecrit(st,destination):
	ajout=open(REP_A+destination,"w")
	ajout.write(st)
	ajout.close()
def lit(cible):
	lecture=open(REP_A+cible,"r")
	st=lecture.read()
	lecture.close()
	return(st)
def dc(x):return("0"*(int(x)<10)+str(int(x)))
def stdate(st):
	if "/"in st:st="-".join(reversed(st.split("/")))
	a,m,j=[int(i)for i in st.split("-")]
	return(date(a,m,j))
def joursdelta(st,x):return((stdate(st)+datetime.timedelta(x)).isoformat().split("T")[0])
def jsm(st):return(jours[(stdate(st).weekday()+1)%7])
def rep(st):return(joursdelta(st,-0).replace("-","/")[0:-3]+")___"+mois[stdate(joursdelta(st,0)).month-1].replace(" ","")+"_.txt")
def datevide(st):
	dvid=""
	a,m,j=st.split("-")
	if j=="01":
		if m=="01":dvid+=decoa+" | "+a+" | \n"
		dvid+=decom+" |"+mois[int(m)-1]+a+" |"+decom+"\n"+separateur
	return(dvid+decoj+" "+jsm(st)+j+mois[int(m)-1]+("-"+str(st[0:4])+"- ")*(jsm(st)=="Dimanche ")+decoj*(jsm(st)!="Dimanche ")+"\n=>\n\n"+separateur)
def trouvedate(lignes):
	#if re.findall("\s*\#+\s+\|\s+\w+\s+\d+\s+\|",lignes)!=[]:return(re.findall("\s*\#+\s+\|\s+\w+\s+\d+\s+\|",lignes)[0])
	if 1:
		j=re.findall("\-+\s+[A-Za-z]+\s+(\d{2})\s[A-Za-z]+\s+\-\d*\-+",lignes)[0]
		m=dc(mois.index(re.findall("\-+\s+[A-Za-z]+\s+\d{2}(\s[A-Za-z]+\s+)\-\d*\-+",lignes)[0])+1)
		a=trouvesortie(an_min)
		if re.findall("\-+\s+[A-Za-z]+\s+\d{2}\s[A-Za-z]+\s+\-(\d+)\-+",lignes)!=[]:
			a=re.findall("\-+\s+[A-Za-z]+\s+\d{2}\s[A-Za-z]+\s+\-(\d+)\-+",lignes)[0]
		return("-".join([a,m,j]))
def nouveau_calendrier():
	datecur,calend,calendfin=datdep,"",""
	dateinterm=joursdelta(datecur,dates)
	while datecur<dateinterm:
		calend+=datevide(datecur)
		datecur=joursdelta(datecur,1)
	while datecur<datfin:
		calendfin+=datevide(datecur)
		datecur=joursdelta(datecur,1)	
	ajoute(calend,en_cours)
	reecrit(calendfin,suite)
def archive():
	encm=lit(en_cours).split(separateur)
	plt=lit(suite).split(separateur)
	fini=separateur
	if re.findall("\s*\#+\s+\|\s+\w+\s+\d+\s+\|",encm[0])!=[]:
		anneelue=re.findall("\s*\#+\s+\|\s+\w+\s+(\d+)\s+\|",encm[0])[0]
		if not anneelue in listdir(REP_A):os.mkdir(REP_A+anneelue)	
		fini+=encm.pop(0)
	while encm[0]=="":encm.pop(0)
	if trouvedate(encm[0])!="":
		dest=encm.pop(0)
		fini+=dest
		while len(encm)<=dates:encm.append(plt.pop(0))
		ajoute(fini,rep(trouvedate(dest)))
		anneecur=trouvedate(dest).split("-")[0]
		ajoute(fini,anneecur+"/TOUT_"+anneecur+"_.txt")
		reecrit(separateur.join(encm),en_cours)
		reecrit(separateur.join(plt),suite)
		return(trouvedate(dest))
########################################################################Fin des fonctions################		
an_min=trouvesortie(an_min)
if not sauvegardes in listdir(REP_A):os.mkdir(REP_A+"/"+sauvegardes)
if not suite in listdir(REP_A) and not en_cours in listdir(REP_A):nouveau_calendrier()###################
an_min=trouvesortie(an_min)
if not an_min in listdir(REP_A):os.mkdir(REP_A+an_min)
hier=joursdelta(aujourdhui,-1) #####################################################################Debug
premieredate=lit(en_cours)
ref=trouvedate(premieredate)
while ref<=hier:
	ref=archive()
	#print(ref)################ A virer pour mise en service
	if ref>=hier:break
