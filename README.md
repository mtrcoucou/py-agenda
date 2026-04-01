
→ [COMMAND LINE INSTALLATION:]

```
git clone https://github.com/mtrcoucou/py-agenda.git && cd py-agenda && python3 install-sftp.py
```

# py-agenda

A lightweight, self-hosted, plain-text personal calendar — designed for Raspberry Pi and Linux servers.

No database, no web interface, no cloud dependency. Just text files, Python, and SSH/SFTP or WebDAV.

→ [Lire en français](README.fr.md)

---

## How it works

```
.py-agenda_systeme/     ← scripts (never exposed)
    calendrier.py
    reglages.py
    install-sftp.py

agenda/                 ← your calendar (exposed via SFTP or WebDAV)
    __rdv__.txt         ← next N days (open this daily)
    plus_tard_.txt      ← future dates
    2025/               ← auto-archived past days
    2026/
```

`calendrier.py` runs every morning via crontab. It archives past days, generates new ones, and ensures your calendar always covers the configured number of years ahead.

The `agenda/` folder is designed to be accessed directly from your file manager — no special app needed.

---

## Requirements

- Python 3.6+
- Linux server (Raspberry Pi, VPS, home server...)
- SSH access with ed25519 key authentication
- SFTP or WebDAV client on your devices

---

## Installation

```bash
git clone https://github.com/mtrcoucou/py-agenda.git
cd py-agenda
python3 install-sftp.py
```

The installer will:
1. Verify your SSH connection
2. Write a test file so you can confirm SFTP access from your device
3. Ask a few configuration questions
4. Generate `reglages.py` and send both scripts to the server
5. Display the crontab line to copy-paste

---

## Client access

### SFTP

| Device | App | Notes |
|---|---|---|
| Android | **Material Files** (F-Droid) | ✅ Open source, SSH key support |
| Linux | **Nautilus** (native) | ✅ Built-in, no extra app needed |
| Mac | **Cyberduck** | ✅ Free, open source |
| Windows | **SSHFS-Win** | ✅ Mounts as a network drive in Explorer |
| Windows | **WinSCP** | ✅ Open source, separate interface |

**Android (Material Files):**
1. Install **Material Files** from F-Droid
2. Add storage → SFTP
3. Enter host, port, username and private key
4. Navigate to `agenda/` and open `__rdv__.txt`

**Linux (Nautilus):**
```
sftp://user@your-server/path/to/agenda
```

**Windows (SSHFS-Win):**
1. Install [SSHFS-Win](https://github.com/winfsp/sshfs-win)
2. Open Explorer → right-click "This PC" → "Map network drive"
3. Enter: `\\sshfs\user@your-server\path\to\agenda`

### WebDAV

If you expose your `agenda/` folder via WebDAV (requires a separate WebDAV server setup):

| Device | App | Notes |
|---|---|---|
| Android | **Material Files** (F-Droid) | ✅ WebDAV supported |
| Linux | **Nautilus** (native) | ✅ Built-in |
| Mac | **Finder** (native) | ✅ `⌘ + K` → `https://your-url` |
| Windows | **Explorer** (native) | ✅ Map network drive → WebDAV URL |

> ⚠️ On Windows, WebDAV over HTTPS may require a registry edit to enable Basic Authentication.
> See [Microsoft documentation](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/cannot-connect-to-webdav-share) if you encounter issues.

---

## Supported server platforms

| Server | Notes |
|---|---|
| ✅ Raspberry Pi | Recommended |
| ✅ Fedora / Ubuntu / Debian | Recommended |
| ✅ Mac Mini on Linux | Tested |
| ✅ VPS (Hetzner, DigitalOcean...) | Recommended |
| ⚠️ O2switch mutualisé | IP whitelist required (max 5), problematic on mobile |

---

## Configuration

After installation, edit `.py-agenda_systeme/reglages.py` on the server:

| Parameter | Default | Description |
|---|---|---|
| `dates` | 62 | Visible days in main file (~2 months) |
| `en_cours` | `__rdv__.txt` | Main calendar file |
| `suite` | `plus_tard_.txt` | Future dates file |
| `nb_annees` | 50 | Years pre-generated ahead |
| `chemin_agenda` | set at install | Fallback path if no argument passed to calendrier.py |
| `largeur` | 40 | Separator width (increase for larger screens) |

---

## Crontab

```
0 4 * * * python3 /path/.py-agenda_systeme/calendrier.py /path/agenda
```

The second argument (`/path/agenda`) is optional — if omitted, `chemin_agenda` from `reglages.py` is used.

---

## License

MIT
