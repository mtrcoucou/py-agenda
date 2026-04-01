→ [INSTALLATION EN LIGNE DE COMMANDE:]

```
git clone https://github.com/mtrcoucou/py-agenda.git && cd py-agenda && python3 install-sftp.py
```


# py-agenda

Un agenda personnel en texte brut, auto-hébergé et léger — conçu pour Raspberry Pi et serveurs Linux.

Pas de base de données, pas d'interface web, pas de dépendance au cloud. Juste des fichiers texte, Python et SSH/SFTP ou WebDAV.

→ [Read in English](README.md)

---

## Fonctionnement

```
.py-agenda_systeme/     ← scripts (jamais exposés)
    calendrier.py
    reglages.py
    install-sftp.py

agenda/                 ← votre calendrier (exposé via SFTP ou WebDAV)
    __rdv__.txt         ← les N prochains jours (ouvrez ce fichier au quotidien)
    plus_tard_.txt      ← les dates futures
    2025/               ← jours passés archivés automatiquement
    2026/
```

`calendrier.py` tourne chaque matin via crontab. Il archive les jours passés, génère les nouveaux, et s'assure que le calendrier couvre toujours le nombre d'années configuré.

Le dossier `agenda/` est conçu pour être consulté directement depuis votre gestionnaire de fichiers — aucune application spéciale requise.

---

## Prérequis

- Python 3.6+
- Serveur Linux (Raspberry Pi, VPS, serveur personnel...)
- Accès SSH avec authentification par clé ed25519
- Client SFTP ou WebDAV sur vos appareils

---

## Installation

```bash
git clone https://github.com/mtrcoucou/py-agenda.git
cd py-agenda
python3 install-sftp.py
```

L'installateur va :
1. Vérifier votre connexion SSH
2. Écrire un fichier test pour que vous confirmiez l'accès SFTP depuis votre appareil
3. Poser quelques questions de configuration
4. Générer `reglages.py` et envoyer les deux scripts sur le serveur
5. Afficher la ligne crontab à copier-coller

---

## Accès client

### SFTP

| Appareil | Application | Notes |
|---|---|---|
| Android | **Material Files** (F-Droid) | ✅ Open source, support clé SSH |
| Linux | **Nautilus** (natif) | ✅ Intégré, aucune app supplémentaire |
| Mac | **Cyberduck** | ✅ Gratuit, open source |
| Windows | **SSHFS-Win** | ✅ Monte comme lecteur réseau dans l'explorateur |
| Windows | **WinSCP** | ✅ Open source, interface séparée |

**Android (Material Files) :**
1. Installez **Material Files** depuis F-Droid
2. Ajouter un stockage → SFTP
3. Entrez l'hôte, le port, l'utilisateur et votre clé privée
4. Naviguez vers `agenda/` et ouvrez `__rdv__.txt`

**Linux (Nautilus) :**
```
sftp://utilisateur@votre-serveur/chemin/vers/agenda
```

**Windows (SSHFS-Win) :**
1. Installez [SSHFS-Win](https://github.com/winfsp/sshfs-win)
2. Explorateur → clic droit sur "Ce PC" → "Connecter un lecteur réseau"
3. Entrez : `\\sshfs\utilisateur@votre-serveur\chemin\vers\agenda`

### WebDAV

Si vous exposez votre dossier `agenda/` via WebDAV (nécessite une configuration serveur WebDAV séparée) :

| Appareil | Application | Notes |
|---|---|---|
| Android | **Material Files** (F-Droid) | ✅ WebDAV supporté |
| Linux | **Nautilus** (natif) | ✅ Intégré |
| Mac | **Finder** (natif) | ✅ `⌘ + K` → `https://votre-url` |
| Windows | **Explorateur** (natif) | ✅ Connecter un lecteur réseau → URL WebDAV |

> ⚠️ Sous Windows, WebDAV en HTTPS peut nécessiter une modification du registre pour activer l'authentification Basic.
> Consultez la [documentation Microsoft](https://learn.microsoft.com/fr-fr/troubleshoot/windows-client/networking/cannot-connect-to-webdav-share) en cas de problème.

---

## Plateformes serveur supportées

| Serveur | Notes |
|---|---|
| ✅ Raspberry Pi | Recommandé |
| ✅ Fedora / Ubuntu / Debian | Recommandé |
| ✅ Mac Mini sous Linux | Testé |
| ✅ VPS (Hetzner, DigitalOcean...) | Recommandé |
| ⚠️ O2switch mutualisé | Liste blanche IP requise (max 5), problématique en mobilité |

---

## Configuration

Après installation, éditez `.py-agenda_systeme/reglages.py` sur le serveur :

| Paramètre | Défaut | Description |
|---|---|---|
| `dates` | 62 | Jours visibles dans le fichier principal (~2 mois) |
| `en_cours` | `__rdv__.txt` | Fichier calendrier principal |
| `suite` | `plus_tard_.txt` | Fichier des dates futures |
| `nb_annees` | 50 | Années pré-générées à l'avance |
| `chemin_agenda` | défini à l'install | Chemin de repli si aucun argument passé à calendrier.py |
| `largeur` | 40 | Largeur des séparateurs (augmentez pour les grands écrans) |

---

## Crontab

```
0 4 * * * python3 /chemin/.py-agenda_systeme/calendrier.py /chemin/agenda
```

Le second argument (`/chemin/agenda`) est optionnel — s'il est omis, `chemin_agenda` de `reglages.py` est utilisé.

---

## Licence

MIT
