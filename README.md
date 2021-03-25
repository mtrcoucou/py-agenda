
BONJOUR !

-l'initialisation de l'agenda se fait en executant la meme commande que pour le mettre à jour:

			python3 /..emplacement../py-agenda/.SYSTEME/misajour.py

Pour maintenir l'agenda à jour, cette commande doit être executée chaque jours, par exemple à l'allumage de l'ordinateur ou avec cron
les journées écoulées sont archivées à la date de la veille



il est configuré pour afficher rapidement:
-les 65 prochains jours dans un petit fichier texte 
-les jours qui suivent dans un fichier texte plus gros
-les archives classées par années et par mois
-l'année en cours

les fichiers ont des noms intuitifs mais pour modifier :
editez le fichier de reglages /.SYSTEME/reglages.py


avec nano:
			sudo nano /..emplacement../py-agenda/.SYTEME/reglages.py

