#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# py-agenda — calendrier.py
# Script principal : archivage quotidien et maintenance du calendrier
# À placer dans .systeme/ et à lancer via crontab :
#   0 4 * * * python3 /chemin/.py-agenda_systeme/calendrier.py /chemin/agenda

import re
import sys
import os
from os import listdir
import shutil
import datetime
from datetime import date
from datetime import datetime as dat

# ─────────────────────────────────────────────────────────────────────────────
# CHEMINS
# ─────────────────────────────────────────────────────────────────────────────

# Chemin vers .systeme/ (dossier de ce script)
REP_S = os.path.dirname(os.path.abspath(__file__)) + "/"

# Chargement de reglages.py depuis .systeme/
sys.path.insert(0, REP_S)
from reglages import *

# Chemin vers l'agenda :
# - priorité à l'argument passé en ligne de commande (ex: crontab)
# - sinon fallback sur chemin_agenda défini dans reglages.py
REP_A = (sys.argv[1].rstrip("/") + "/") if len(sys.argv) > 1 else chemin_agenda.rstrip("/") + "/"

# ─────────────────────────────────────────────────────────────────────────────
# CALCUL DYNAMIQUE DE datfin
# Assure toujours nb_annees années de couverture à partir d'aujourd'hui
# ─────────────────────────────────────────────────────────────────────────────

aujourdhui  = dat.today().isoformat().split("T")[0]
an_courant  = int(aujourdhui.split("-")[0])
datfin	  = str(an_courant + nb_annees) + "-12-31"
an_min	  = datdep.split("-")[0]

# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────────────────────────────────────

def ajoute(st, destination):
	with open(REP_A + destination, "a", encoding="utf-8") as f:
		f.write(st)

def reecrit(st, destination):
	with open(REP_A + destination, "w", encoding="utf-8") as f:
		f.write(st)

def lit(cible):
	with open(REP_A + cible, "r", encoding="utf-8") as f:
		return f.read()

def dc(x):
	return ("0" * (int(x) < 10)) + str(int(x))

def stdate(st):
	if "/" in st:
		st = "-".join(reversed(st.split("/")))
	a, m, j = [int(i) for i in st.split("-")]
	return date(a, m, j)

def joursdelta(st, x):
	return (stdate(st) + datetime.timedelta(x)).isoformat().split("T")[0]

def jsm(st):
	return jours[(stdate(st).weekday() + 1) % 7]

def rep(st):
	return (
		joursdelta(st, 0).replace("-", "/")[0:-3]
		+ ")___"
		+ mois[stdate(joursdelta(st, 0)).month - 1].replace(" ", "")
		+ "_.txt"
	)

def datevide(st):
	dvid = ""
	a, m, j = st.split("-")
	if j == "01":
		if m == "01":
			dvid += decoa + " | " + a + " | \n"
		dvid += decom + " |" + mois[int(m) - 1] + a + " |" + decom + "\n" + separateur
	return (
		dvid
		+ decoj + " " + jsm(st) + j + mois[int(m) - 1]
		+ ("-" + str(st[0:4]) + "- ") * (jsm(st) == jours[0])
		+ decoj * (jsm(st) != jours[0])
		+ "\n=>\n\n"
		+ separateur
	)

def trouvesortie(an_min):
	annees_visibles = [i for i in listdir(REP_A) if i.isdigit()]
	annees_visibles.sort()
	while len(annees_visibles) > 2:
		shutil.move(
			REP_A + annees_visibles[0],
			REP_A + sauvegardes + "/" + annees_visibles.pop(0)
		)
	if not annees_visibles:
		annees_visibles.append(an_min)
	return annees_visibles.pop()

def trouvedate(lignes):
	j_lst = re.findall(r"-+ +[A-Za-z]+ +(\d{2}) [A-Za-z]+ +-\d*-+", lignes)
	m_lst = re.findall(r"-+ +[A-Za-z]+ +\d{2}( [A-Za-z]+ +)-\d*-+", lignes)
	if not j_lst or not m_lst:
		return None
	j   = j_lst[0]
	m_s = m_lst[0]
	mois_strip = [mo.strip() for mo in mois]
	try:
		m = dc(mois_strip.index(m_s.strip()) + 1)
	except ValueError:
		return None
	a = trouvesortie(an_min)
	annee_explicite = re.findall(r"-+ +[A-Za-z]+ +\d{2} [A-Za-z]+ +-(\d+)-+", lignes)
	if annee_explicite:
		a = annee_explicite[0]
	return "-".join([a, m, j])

# ─────────────────────────────────────────────────────────────────────────────
# CRÉATION D'UN NOUVEAU CALENDRIER (premier lancement)
# ─────────────────────────────────────────────────────────────────────────────

def nouveau_calendrier():
	datecur, calend, calendfin = datdep, "", ""
	dateinterm = joursdelta(datecur, dates)
	while datecur < dateinterm:
		calend	+= datevide(datecur)
		datecur	= joursdelta(datecur, 1)
	while datecur <= datfin:
		calendfin += datevide(datecur)
		datecur	= joursdelta(datecur, 1)
	ajoute(calend,	en_cours)
	reecrit(calendfin, suite)

# ─────────────────────────────────────────────────────────────────────────────
# ARCHIVAGE D'UN JOUR PASSÉ
# ─────────────────────────────────────────────────────────────────────────────

def archive():
	encm = lit(en_cours).split(separateur)
	plt  = lit(suite).split(separateur)
	fini = separateur

	# En-tête d'année
	if re.findall(r" *\#+ +\| +\w+ +\d+ +\|", encm[0]):
		anneelue = re.findall(r" *\#+ +\| +\w+ +(\d+) +\|", encm[0])[0]
		if anneelue not in listdir(REP_A):
			os.mkdir(REP_A + anneelue)
		fini += encm.pop(0)

	while encm and encm[0] == "":
		encm.pop(0)

	if not encm:
		return None

	date_trouvee = trouvedate(encm[0])
	if date_trouvee:
		dest = encm.pop(0)
		fini += dest
		while len(encm) <= dates:
			if not plt:
				break
			encm.append(plt.pop(0))
		ajoute(fini, rep(date_trouvee))
		anneecur = date_trouvee.split("-")[0]
		ajoute(fini, anneecur + "/TOUT_" + anneecur + "_.txt")
		reecrit(separateur.join(encm), en_cours)
		reecrit(separateur.join(plt),  suite)
		return date_trouvee
	return None

# ─────────────────────────────────────────────────────────────────────────────
# MAINTENANCE DE plus_tard_.txt
# Vérifie que la couverture atteint datfin et complète si nécessaire
# ─────────────────────────────────────────────────────────────────────────────

def maintenir_couverture():
	contenu = lit(suite)
	blocs   = contenu.split(separateur)
	derniere_date = None
	for bloc in reversed(blocs):
		if bloc.strip():
			d = trouvedate(bloc)
			if d:
				derniere_date = d
				break
	if derniere_date is None:
		return
	if derniere_date < datfin:
		extension = ""
		datecur   = joursdelta(derniere_date, 1)
		while datecur <= datfin:
			extension += datevide(datecur)
			datecur	= joursdelta(datecur, 1)
		ajoute(extension, suite)

# ─────────────────────────────────────────────────────────────────────────────
# PROGRAMME PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

# Dossiers nécessaires
if sauvegardes not in listdir(REP_A):
	os.mkdir(REP_A + sauvegardes)

an_min = trouvesortie(an_min)
if an_min not in listdir(REP_A):
	os.mkdir(REP_A + an_min)

# Premier lancement
if suite not in listdir(REP_A) and en_cours not in listdir(REP_A):
	nouveau_calendrier()

# Maintenance de la couverture
maintenir_couverture()

# Archivage des jours passés
hier		 = joursdelta(aujourdhui, reglage_delta)
premieredate = lit(en_cours)
ref		  = trouvedate(premieredate)

while ref and ref <= hier:
	ref = archive()
	if ref and ref >= hier:
		break
