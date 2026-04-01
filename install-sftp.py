#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
textcal — installateur interactif / interactive installer v0.2
"""

import os
import sys
import datetime
import subprocess
import locale
import calendar

# ─────────────────────────────────────────────────────────────────────────────
# TRADUCTIONS
# ─────────────────────────────────────────────────────────────────────────────

T = {
	"bienvenue": {
		"FR": "\n  ╔══════════════════════════════════╗\n  ║  py-agenda — installateur SFTP   ║\n  ╚══════════════════════════════════╝\n",
		"EN": "\n  ╔══════════════════════════════════╗\n  ║  py-agenda — SFTP installer	  ║\n  ╚══════════════════════════════════╝\n",
	},
	"langue_prompt": {
		"FR": "\n  Choisissez votre langue / Choose your language [FR/EN] : ",
		"EN": "\n  Choisissez votre langue / Choose your language [FR/EN] : ",
	},
	"aide_dispo": {
		"FR": "  (tapez 'h' pour afficher l'aide)\n",
		"EN": "  (type 'h' for help)\n",
	},

	# ── SSH ──────────────────────────────────────────────────────────────────
	"ssh_deja": {
		"FR": "\n  Avez-vous déjà une connexion SSH configurée vers votre serveur ? [O/n] : ",
		"EN": "\n  Do you already have an SSH connection configured to your server? [Y/n]: ",
	},
	"ssh_guide_intro": {
		"FR": "\n  ── Guide de configuration SSH ─────────────────────────────────────────\n",
		"EN": "\n  ── SSH configuration guide ────────────────────────────────────────────\n",
	},
	"ssh_cle_existante": {
		"FR": "  ✓ Une clé ed25519 existe déjà : ~/.ssh/id_ed25519\n  Elle sera utilisée pour la connexion.\n",
		"EN": "  ✓ An ed25519 key already exists: ~/.ssh/id_ed25519\n  It will be used for the connection.\n",
	},
	"ssh_creation_cle": {
		"FR": (
			"  Aucune clé ed25519 trouvée. Création d'une nouvelle clé :\n\n"
			"  Exécutez cette commande dans votre terminal :\n"
			"	   ssh-keygen -t ed25519 -C \"py-agenda\"\n"
			"	   (appuyez sur Entrée pour accepter les valeurs par défaut)\n\n"
			"  Puis relancez cet installateur.\n"
			"  ───────────────────────────────────────────────────────────────────\n"
		),
		"EN": (
			"  No ed25519 key found. Please create one:\n\n"
			"  Run this command in your terminal:\n"
			"	   ssh-keygen -t ed25519 -C \"py-agenda\"\n"
			"	   (press Enter to accept defaults)\n\n"
			"  Then relaunch this installer.\n"
			"  ───────────────────────────────────────────────────────────────────\n"
		),
	},
	"ssh_guide": {
		"FR": (
			"  Copiez votre clé publique sur le serveur :\n"
			"	   ssh-copy-id utilisateur@votre-serveur\n\n"
			"  Testez la connexion :\n"
			"	   ssh utilisateur@votre-serveur\n\n"
			"  Une fois connecté, relancez cet installateur.\n"
			"  ───────────────────────────────────────────────────────────────────\n"
		),
		"EN": (
			"  Copy your public key to the server:\n"
			"	   ssh-copy-id user@your-server\n\n"
			"  Test the connection:\n"
			"	   ssh user@your-server\n\n"
			"  Once connected, relaunch this installer.\n"
			"  ───────────────────────────────────────────────────────────────────\n"
		),
	},

	# ── Connexion ────────────────────────────────────────────────────────────
	"q_hote": {
		"FR": "  Hôte ou IP du serveur : ",
		"EN": "  Server host or IP: ",
	},
	"q_port": {
		"FR": "  Port SSH (défaut : 22) : ",
		"EN": "  SSH port (default: 22): ",
	},
	"q_user": {
		"FR": "  Nom d'utilisateur SSH : ",
		"EN": "  SSH username: ",
	},
	"q_chemin": {
		"FR": "\n  Chemin distant du dossier agenda (ex: /home/user/agenda \n    Si vous comptez acceder au dossier agenda avec webdav, NE PAS EXPOSER TOUT /home/user en entier  :",
		"EN": "\n  Remote path for agenda folder (e.g. /home/user/agenda)\n    If you intend to access the agenda folder using WebDAV,DO NOT EXPOSE ENTIRE /home/user  : ",
	},
	"q_chemin_systeme": {
		"FR": "\n  Chemin distant du dossier système (défaut : {defaut})\n    Si vous comptez acceder au dossier agenda avec webdav, placez le dossier systeme à l'extrieur de celui-ci : ",
		"EN": "\n  Remote path for system folder (default: {defaut})\n  If you intend to access the agenda folder using WebDAV, place the system folder outside of it : ",
	},

	# ── Test connexion ───────────────────────────────────────────────────────
	"test_connexion": {
		"FR": "\n  ── Test de la connexion ───────────────────────────────────────────────\n",
		"EN": "\n  ── Connection test ────────────────────────────────────────────────────\n",
	},
	"test_creation_dossier": {
		"FR": "  Création du dossier distant et écriture du fichier test...\n",
		"EN": "  Creating remote folder and writing test file...\n",
	},
	"test_ok": {
		"FR": "  ✓ Fichier test écrit avec succès.\n",
		"EN": "  ✓ Test file written successfully.\n",
	},
	"test_erreur": {
		"FR": "  ✗ Erreur lors de la connexion SSH :\n",
		"EN": "  ✗ SSH connection error:\n",
	},
	"test_diagnostic": {
		"FR": (
			"\n  ── Diagnostic ─────────────────────────────────────────────────────────\n"
			"  Vérifiez :\n"
			"  - Que le serveur est accessible (ping {hote})\n"
			"  - Que le port {port} est ouvert\n"
			"  - Que votre clé SSH est bien autorisée sur le serveur\n"
			"  - Que le chemin distant existe ou que vous avez les droits de le créer\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
		"EN": (
			"\n  ── Diagnostic ─────────────────────────────────────────────────────────\n"
			"  Check:\n"
			"  - That the server is reachable (ping {hote})\n"
			"  - That port {port} is open\n"
			"  - That your SSH key is authorized on the server\n"
			"  - That the remote path exists or that you have rights to create it\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
	},
	"test_voir_fichier": {
		"FR": (
			"\n  Ouvrez maintenant votre application SFTP (ex: Material Files sur Android)\n"
			"  et vérifiez que vous voyez le fichier 'textcal_test.txt' dans :\n"
			"  {chemin}\n\n"
			"  Voyez-vous ce fichier ? [O/n] : "
		),
		"EN": (
			"\n  Now open your SFTP app (e.g. Material Files on Android)\n"
			"  and check that you can see 'textcal_test.txt' in:\n"
			"  {chemin}\n\n"
			"  Can you see this file? [Y/n]: "
		),
	},
	"test_invisible": {
		"FR": (
			"\n  ✗ Le fichier n'est pas visible. Vérifiez la configuration SFTP\n"
			"  de votre application cliente et relancez l'installateur.\n"
		),
		"EN": (
			"\n  ✗ File not visible. Check the SFTP configuration\n"
			"  of your client app and relaunch the installer.\n"
		),
	},
	"test_visible_ok": {
		"FR": "  ✓ Parfait, la connexion est opérationnelle !\n",
		"EN": "  ✓ Great, the connection is working!\n",
	},

	# ── Questions config ─────────────────────────────────────────────────────
	"q_jours": {
		"FR": "\n  Nombre de jours visibles dans le fichier principal (défaut : 62) : ",
		"EN": "\n  Number of visible days in the main file (default: 62): ",
	},
	"h_jours": {
		"FR": (
			"\n  [AIDE] 62 jours = environ 2 mois affichés dans votre fichier principal.\n"
			"  Les jours passés sont archivés automatiquement chaque matin par crontab.\n"
			"  Augmenter cette valeur affiche plus de jours mais rend le fichier plus long.\n"
		),
		"EN": (
			"\n  [HELP] 62 days ≈ 2 months displayed in your main file.\n"
			"  Past days are automatically archived every morning by crontab.\n"
			"  Increasing this value shows more days but makes the file longer.\n"
		),
	},
	"q_nom_encours": {
		"FR": "  Nom du fichier pour les {n} prochains jours (défaut : __rdv__.txt) : ",
		"EN": "  Name of the file for the next {n} days (default: __rdv__.txt): ",
	},
	"q_nom_suite": {
		"FR": "  Nom du fichier pour les jours au-delà des {n} prochains jours (défaut : plus_tard_.txt) : ",
		"EN": "  Name of the file for days beyond the next {n} days (default: plus_tard_.txt): ",
	},
	"q_annees": {
		"FR": "  Nombre d'années pré-générées (défaut : 50) : ",
		"EN": "  Number of pre-generated years (default: 50): ",
	},
	"h_annees": {
		"FR": (
			"\n  [AIDE] Le calendrier est pré-généré pour les {n} prochaines années.\n"
			"  Le script vérifie à chaque lancement que cette couverture est maintenue\n"
			"  et ajoute des dates si nécessaire. 50 ans est largement suffisant.\n"
		),
		"EN": (
			"\n  [HELP] The calendar is pre-generated for the next {n} years.\n"
			"  The script checks at each run that this coverage is maintained\n"
			"  and adds dates if needed. 50 years is more than enough.\n"
		),
	},

	# ── Fin ──────────────────────────────────────────────────────────────────
	"reglages_ok": {
		"FR": "\n  ✓ Fichier de réglages généré : {}\n",
		"EN": "\n  ✓ Settings file generated: {}\n",
	},
	"crontab": {
		"FR": (
			"\n  ── Crontab (archivage automatique chaque matin) ───────────────────────\n"
			"  Commande : crontab -e\n"
			"  Ajoutez cette ligne :\n\n"
			"  0 4 * * * python3 {chemin_systeme}/calendrier.py {chemin}\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
		"EN": (
			"\n  ── Crontab (automatic archiving every morning) ────────────────────────\n"
			"  Command: crontab -e\n"
			"  Add this line:\n\n"
			"  0 4 * * * python3 {chemin_systeme}/calendrier.py {chemin}\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
	},
	"sftp_tuto": {
		"FR": (
			"\n  ── Accès depuis Android ───────────────────────────────────────────────\n"
			"  1. Installez Material Files (F-Droid)\n"
			"  2. Ajouter un stockage → SFTP\n"
			"  3. Hôte : {hote}  Port : {port}  Utilisateur : {user}\n"
			"  4. Chemin : {chemin}\n"
			"  5. Ouvrez {en_cours} directement depuis l'app\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
		"EN": (
			"\n  ── Access from Android ────────────────────────────────────────────────\n"
			"  1. Install Material Files (F-Droid)\n"
			"  2. Add storage → SFTP\n"
			"  3. Host: {hote}  Port: {port}  User: {user}\n"
			"  4. Path: {chemin}\n"
			"  5. Open {en_cours} directly from the app\n"
			"  ───────────────────────────────────────────────────────────────────────\n"
		),
	},
	"termine": {
		"FR": "\n  ✓ Installation terminée. Bonne organisation !\n\n",
		"EN": "\n  ✓ Installation complete. Stay organized!\n\n",
	},
}

# ─────────────────────────────────────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────────────────────────────────────

locale_map = {"FR": "fr_FR.UTF-8", "EN": "en_US.UTF-8"}


def t(cle, lng, **kwargs):
	s = T[cle][lng]
	return s.format(**kwargs) if kwargs else s


def demander(prompt, defaut=None, aide=None, lng="EN"):
	if aide:
		print(T["aide_dispo"][lng], end="")
	while True:
		rep = input(prompt).strip()
		if rep.lower() == "h" and aide:
			print(aide)
			continue
		if rep == "" and defaut is not None:
			return defaut
		if rep != "":
			return rep


def oui(rep, lng):
	rep = rep.strip().lower()
	if lng == "FR":
		return rep in ("", "o", "oui", "y", "yes")
	return rep in ("", "y", "yes", "o", "oui")


# ─────────────────────────────────────────────────────────────────────────────
# ÉTAPES
# ─────────────────────────────────────────────────────────────────────────────

def choisir_langue():
	while True:
		rep = input(T["langue_prompt"]["FR"]).strip().upper()
		if rep in ("FR", "EN"):
			return rep
		if rep == "":
			return "EN"


def guide_ssh(lng):
	print(t("ssh_guide_intro", lng))
	cle = os.path.expanduser("~/.ssh/id_ed25519")
	if os.path.exists(cle):
		print(t("ssh_cle_existante", lng))
		print(t("ssh_guide", lng))
	else:
		print(t("ssh_creation_cle", lng))
		sys.exit(0)


def configurer_connexion(lng):
	hote   = demander(t("q_hote",  lng))
	port   = demander(t("q_port",  lng), defaut="22")
	user   = demander(t("q_user",  lng))
	chemin = demander(t("q_chemin", lng))
	parent  = "/".join(chemin.rstrip("/").split("/")[:-1])
	defaut_systeme = parent + "/.py-agenda_systeme"
	chemin_systeme = demander(t("q_chemin_systeme", lng, defaut=defaut_systeme), defaut=defaut_systeme)
	return {"hote": hote, "port": port, "user": user, "chemin": chemin, "chemin_systeme": chemin_systeme}


def tester_connexion(cnx, lng):
	print(t("test_connexion", lng))
	print(t("test_creation_dossier", lng))
	contenu = "textcal fonctionne !\\ntextcal works!\\n"
	cmd = (
		f"ssh -p {cnx['port']} {cnx['user']}@{cnx['hote']} "
		f"\"mkdir -p {cnx['chemin']} && "
		f"printf '{contenu}' > {cnx['chemin']}/textcal_test.txt\""
	)
	res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
	if res.returncode == 0:
		print(t("test_ok", lng))
		return True
	print(t("test_erreur", lng))
	print(f"  {res.stderr.strip()}\n")
	print(t("test_diagnostic", lng, hote=cnx["hote"], port=cnx["port"]))
	return False


def verifier_visibilite(cnx, lng):
	rep = input(t("test_voir_fichier", lng, chemin=cnx["chemin"]))
	if oui(rep, lng):
		print(t("test_visible_ok", lng))
		return True
	print(t("test_invisible", lng))
	return False


def questions_config(lng):
	# Nombre de jours
	rep = demander(t("q_jours", lng), defaut="62", aide=t("h_jours", lng), lng=lng)
	try:
		nb_jours = int(rep)
	except ValueError:
		nb_jours = 62

	# Noms de fichiers
	en_cours = demander(t("q_nom_encours", lng, n=nb_jours), defaut="__rdv__.txt")
	suite	= demander(t("q_nom_suite",   lng, n=nb_jours), defaut="plus_tard_.txt")

	# Années pré-générées
	rep = demander(t("q_annees", lng), defaut="50", aide=t("h_annees", lng, n=50), lng=lng)
	try:
		nb_annees = int(rep)
	except ValueError:
		nb_annees = 50

	return {"nb_jours": nb_jours, "en_cours": en_cours, "suite": suite, "nb_annees": nb_annees}


def generer_reglages(cnx, cfg, lng):
	locale.setlocale(locale.LC_TIME, locale_map.get(lng, ""))

	jours_bruts = [calendar.day_name[i] for i in range(7)]
	jours_bruts = [jours_bruts[6]] + jours_bruts[:6]  # dimanche en premier
	max_j = max(len(j) for j in jours_bruts)+4
	jours_repr = "[" + ", ".join(
		'"' + j.capitalize().ljust(max_j) + '"' for j in jours_bruts
	) + "]"

	mois_bruts = [calendar.month_name[i] for i in range(1, 13)]
	max_m = max(len(m) for m in mois_bruts)+2
	mois_repr = '"' + ",".join(
		(" " + m.capitalize()).ljust(max_m + 1) for m in mois_bruts
	) + '"'

	datdep = datetime.date.today().isoformat()
	datfin = str(datetime.date.today().year + cfg["nb_annees"]) + "-12-31"

	return f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Généré automatiquement par install.py — textcal
# Generated automatically by install.py — textcal

# ── Fichiers ──────────────────────────────────────────────────────────────────
en_cours	= "{cfg["en_cours"]}"
suite	   = "{cfg["suite"]}"
sauvegardes = "sauvegardes"

# ── Dates ─────────────────────────────────────────────────────────────────────
datdep	= "{datdep}"	  # date de début du calendrier
datfin	= "{datfin}"	  # recalculée automatiquement par le script
nb_annees = {cfg["nb_annees"]}			  # années pré-générées à maintenir

# ── Affichage ─────────────────────────────────────────────────────────────────
dates		 = {cfg["nb_jours"]}		   # jours visibles dans le fichier en cours
reglage_delta = -1			# décalage pour l'archivage (-1 = hier)

# Largeur des séparateurs (40 par défaut, optimisé pour grandes polices mobiles)
# Augmentez si vous lisez sur grand écran (ex: 40, 50, 60)
largeur	= 40
separateur = "_" * largeur + "\\n"

# ── Localisation (générée automatiquement selon la langue choisie) ─────────────
jours = {jours_repr}
mois  = {mois_repr}.split(",")

decoj = "------ "
decom = " #######"
decoa = decom * (largeur // 8) + "# "
'''


def generer_readme(cnx, cfg, lng):
	datfin = str(datetime.date.today().year + cfg["nb_annees"]) + "-12-31"
	if lng == "FR":
		return f"""# textcal

Calendrier personnel en texte brut, auto-archivant.
Conçu pour Raspberry Pi et serveurs Linux. Client recommandé : Material Files (Android, F-Droid).

## Prérequis

- Python 3.6+
- Serveur Linux avec SSH activé
- Accès SFTP depuis votre appareil client

## Installation

```bash
python3 install.py
```

## Réglages (reglages.py)

| Paramètre | Valeur | Description |
|---|---|---|
| `dates` | {cfg["nb_jours"]} | Jours visibles dans le fichier principal |
| `en_cours` | {cfg["en_cours"]} | Fichier principal |
| `suite` | {cfg["suite"]} | Fichier des dates futures |
| `nb_annees` | {cfg["nb_annees"]} | Années pré-générées à maintenir |
| `datfin` | {datfin} | Recalculée automatiquement |
| `largeur` | 40 | Largeur des séparateurs — modifiable manuellement |

## Crontab

```
0 4 * * * python3 {cnx["chemin_systeme"]}/calendrier.py {cnx["chemin"]}
```

## Accès Android (Material Files)

1. Installez **Material Files** (F-Droid)
2. Ajouter un stockage → SFTP
3. Hôte : `{cnx["hote"]}` — Port : `{cnx["port"]}` — Utilisateur : `{cnx["user"]}`
4. Chemin : `{cnx["chemin"]}`
5. Ouvrez `{cfg["en_cours"]}` depuis l'app

## Accès Linux (Nautilus)

```
sftp://{cnx["user"]}@{cnx["hote"]}{cnx["chemin"]}
```

## Accès Mac

Utilisez **Cyberduck** → Nouvelle connexion → SFTP.

## Plateformes supportées

| Serveur | Client |
|---|---|
| ✅ Raspberry Pi | ✅ Android (Material Files) |
| ✅ Fedora / Ubuntu / Debian | ✅ Linux (Nautilus) |
| ✅ Mac Mini sous Linux | ⚠️ Mac (Cyberduck, non officiel) |
| | ❌ iOS / Windows (non supporté) |
"""
	else:
		return f"""# textcal

Personal plain-text self-archiving calendar.
Designed for Raspberry Pi and Linux servers. Recommended client: Material Files (Android, F-Droid).

## Requirements

- Python 3.6+
- Linux server with SSH enabled
- SFTP access from your client device

## Installation

```bash
python3 install.py
```

## Settings (reglages.py)

| Parameter | Value | Description |
|---|---|---|
| `dates` | {cfg["nb_jours"]} | Visible days in main file |
| `en_cours` | {cfg["en_cours"]} | Main file |
| `suite` | {cfg["suite"]} | Future dates file |
| `nb_annees` | {cfg["nb_annees"]} | Pre-generated years to maintain |
| `datfin` | {datfin} | Recalculated automatically |
| `largeur` | 40 | Separator width — manually adjustable |

## Crontab

```
0 4 * * * python3 {cnx["chemin_systeme"]}/calendrier.py {cnx["chemin"]}
```

## Android access (Material Files)

1. Install **Material Files** (F-Droid)
2. Add storage → SFTP
3. Host: `{cnx["hote"]}` — Port: `{cnx["port"]}` — User: `{cnx["user"]}`
4. Path: `{cnx["chemin"]}`
5. Open `{cfg["en_cours"]}` from the app

## Linux access (Nautilus)

```
sftp://{cnx["user"]}@{cnx["hote"]}{cnx["chemin"]}
```

## Mac access

Use **Cyberduck** → New connection → SFTP.

## Supported platforms

| Server | Client |
|---|---|
| ✅ Raspberry Pi | ✅ Android (Material Files) |
| ✅ Fedora / Ubuntu / Debian | ✅ Linux (Nautilus) |
| ✅ Mac Mini on Linux | ⚠️ Mac (Cyberduck, unofficial) |
| | ❌ iOS / Windows (not supported) |
"""


def ecrire_fichiers(cnx, cfg, lng, reglages, readme):
	chemin_systeme = cnx["chemin_systeme"]

	def ssh_run(commande):
		cmd = f"ssh -p {cnx['port']} {cnx['user']}@{cnx['hote']} '{commande}'"
		subprocess.run(cmd, shell=True)

	def scp(contenu, chemin_complet):
		cmd = f"ssh -p {cnx['port']} {cnx['user']}@{cnx['hote']} 'cat > {chemin_complet}'"
		subprocess.run(cmd, input=contenu, shell=True, text=True)

	# Création des dossiers distants
	ssh_run(f"mkdir -p {chemin_systeme} {cnx['chemin']}/sauvegardes")

	# Lecture de calendrier.py depuis le dossier local de install.py
	rep_install = os.path.dirname(os.path.abspath(__file__))
	chemin_calendrier_local = os.path.join(rep_install, "calendrier.py")
	if not os.path.exists(chemin_calendrier_local):
		print("  ✗ calendrier.py introuvable à côté de install.py — abandon." if lng == "FR"
			  else "  ✗ calendrier.py not found next to install.py — aborting.")
		sys.exit(1)
	with open(chemin_calendrier_local, "r", encoding="utf-8") as f:
		calendrier = f.read()

	# Envoi des fichiers dans .systeme/
	scp(reglages,   chemin_systeme + "/reglages.py")
	scp(calendrier, chemin_systeme + "/calendrier.py")
	nom_readme = "README.fr.md" if lng == "FR" else "README.en.md"
	scp(readme, cnx["chemin"] + "/" + nom_readme)
	print(t("reglages_ok", lng).format(chemin_systeme + "/reglages.py"))
	msg_cal = "  ✓ calendrier.py envoyé : " if lng == "FR" else "  ✓ calendrier.py sent: "
	print(msg_cal + chemin_systeme + "/calendrier.py")


# ─────────────────────────────────────────────────────────────────────────────
# PROGRAMME PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def main():
	print(T["bienvenue"]["FR"], end="")
	lng = choisir_langue()
	print(t("bienvenue", lng))

	# SSH configuré ?
	rep = input(t("ssh_deja", lng)).strip()
	if not oui(rep, lng):
		guide_ssh(lng)
		return

	# Paramètres de connexion + test
	cnx = configurer_connexion(lng)
	while True:
		ok = tester_connexion(cnx, lng)
		if not ok:
			invite = "  Réessayer ? [O/n] : " if lng == "FR" else "  Retry? [Y/n]: "
			if not oui(input(invite).strip(), lng):
				sys.exit(1)
			cnx = configurer_connexion(lng)
			continue
		break

	# Vérification visuelle
	if not verifier_visibilite(cnx, lng):
		sys.exit(1)

	# Questions de configuration
	cfg = questions_config(lng)

	# Génération et envoi des fichiers
	reglages = generer_reglages(cnx, cfg, lng)
	readme   = generer_readme(cnx, cfg, lng)
	ecrire_fichiers(cnx, cfg, lng, reglages, readme)

	# Instructions finales
	print(t("crontab",   lng, chemin_systeme=cnx["chemin_systeme"], chemin=cnx["chemin"]))
	print(t("sftp_tuto", lng,
			hote=cnx["hote"], port=cnx["port"],
			user=cnx["user"], chemin=cnx["chemin"],
			en_cours=cfg["en_cours"]))
	print(t("termine", lng))


if __name__ == "__main__":
	main()
