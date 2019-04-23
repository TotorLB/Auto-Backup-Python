#!/usr/bin/python
# -*- coding: utf-8 -*-

import os	# Fonctionnalités importées à partir de l'OS. | Imports OS functions to the script.
import time	# Importe la notion de temps. | Imports time concept.
from os.path import exists # Importe le module nécessaire pour vérifier l'existence d'un fichier. | Imports module necessary to check file's existence.
from datetime import datetime	# Importe le temps de sorte à l'utiliser en heure, minutes, secondes. | Imports time in order to use it as hours, minutes and seconds.
from time import strftime	# Importe le temps de sorte à en faire un argument formaté. | Imports time in order to use it as a formatted argument.

d = datetime.now()	# Variable donnant le temps à l'instant T | Parameter giving the actual T time.
date = d.strftime("%Y_%m_%d")	# Variable utilisant "d" pour en faire un format clair. | Parameter using "d" to make a formatted date.
chemin="/etc/projet/logs/"	# Chemin absolu des logs | Path for the logs.
log = open(chemin+"log.log", "w")	# Création des logs | Creation of logs.
serveur_mere = {	# serveur_mere means main_server
	'dir_wordpress' : '/XXX/XXX/XXX/',	# Où trouver le répertoire wordpress. | Where to find the wordpress repertory.
	'dir_to_backup' : '/XXX/XXX/XXX',	# Où mysqldump va sauvegarder son dump. | Where mysqldump will save its dump.
	'dir_to_archive' : '/XXX/XXX/XXX',	# Où tar va sauvegarder son archive. | Where tar will save its archive.
	'db_username' : 'XXX',			# Username de la database Wordpress. | Wordpress database's username.
	'db_name' : 'XXX',				# Nom de la database Wordpress. | Wordpress database's name.
	'db_password' : 'XXX',			# Mot de passe de la database Wordpress. | Wordpress database's password.
	}

serveur_distant = {	# serveur_distant means remote_server
	'dir' : '/XXX/XXX',			# Répertoire où va être stocké la sauvegarde. | Repertory where the archive will be sent.
	'server' : 'XXX.XXX.XXX.XXX',			# Adresse IP du serveur distant. | IP address of the remote server.
	'login' : 'XXX',				# Login du serveur distant. | Remote server's login.
	}

if exists ('/usr/bin/mysqldump') == False:		# Les "if" suivants vont vérifier si les éléments nécessaires sont bien présents pour le script. | "If" will check if all elements are here.
	print('Mysqldump est manquant. Mysqldump is missing.')	# Si ce n'est pas le cas, un message s'affichera à l'écran indiquant quel fichier manque. | If not, it will be displayed which is one missing.
	exit('1')					# Il se peut que les fichiers aient été déplacé. Attention à bien vérifier leur chemin. | Check their path if not found.
	if exists ('/usr/lib/tar') == False:
		print('Tar est manquant. Tar is missing.')
		exit('1')
		if exists ('/usr/bin/scp') == False:
			print('Scp est manquant. Scp is missing.')
			exit('1')
else:
	print('Mysqldump, Tar et Scp sont présents. Mysqldump, Tar and Scp are here.')

os.system('rm -rf /etc/projet/archive/*')		# Purge des dossiers utilisés afin de garantir une sauvegarde propre. | Used files are cleaned to ensure safe and good backup.
os.system('rm -rf /etc/projet/sauvegarde/*')		# ATTENTION : Tous les fichiers contenus dans les dossiers seront supprimés. | WARNING : All documents inside those files will be erased.

try:
	os.system('mysqldump -u'+serveur_mere['db_username']+' -p'+serveur_mere['db_password']+' -d'+serveur_mere['db_name']+' > '+serveur_mere['dir_to_backup']+'/db_wordpress_backup_'+date+'.sql')
	os.system('mysqldump -u'+serveur_mere['db_username']+' -p'+serveur_mere['db_password']+' -d'+serveur_mere['db_name']+' > '+serveur_mere['dir_to_backup']+'/db_wordpress_backup_Latest.sql')
	# Création du dump pour la sauvegarde et la sauvegarde la plus récente. | Dump creation for the back and the latest backup.

	try:
		os.system('tar -cvzf '+serveur_mere['dir_to_archive']+'/wordpress_'+date+'.tar.gz '+serveur_mere['dir_to_backup'])

		os.system('tar -cvzf '+serveur_mere['dir_to_archive']+'/wordpress_save_Latest.tar.gz '+serveur_mere['dir_to_backup'])
		# Mise en archive du dump préparé précédemment. | Dump is archived into a tar.

		try:
			os.system('scp -r '+serveur_mere['dir_to_archive']+' '+serveur_distant['login']+'@'+serveur_distant['server']+':'+serveur_distant['dir']+'/')
			print("Sauvegarde effectuée avec succès.")
			# L'archive est envoyée via SCP sur le serveur distant grâce à la clé générée dans les prérequis. | Archive is sent to the remote server via the key generated before.

		except BaseException as be:
			log.write(be)	# Écriture de l'erreur dans le log. | Log is written.
			os.system('rm -r /etc/projet/sauvegarde/*') # Suppression des fichiers commencés pour garder les dossiers propres. | Documents created are deleted to clean the folders.
			os.system('rm -r /etc/projet/archive/*')
			exit('1') # 1 signifie que le script s'arrête avec une erreur. Voir les logs. | 1 means script stopped working because of an error. Check the logs.
	except BaseException as be:
		log.write(be)	# Écriture de l'erreur dans le log. | Log is written.
		os.system('rm -r /etc/projet/sauvegarde/*')
		os.system('rm -r /etc/projet/archive/*')
		exit('1')

except BaseException as be:
	log.write(be)	# Écriture de l'erreur dans le log. | Log is written.
	os.system('rm -r /etc/projet/sauvegarde/*')
	os.system('rm -r /etc/projet/archive/*')
	exit('1')

log.close() # Fermeture du fichier log. | Log's file is closed
exit('0') # 0 signifie que tout s'est déroulé correctement. | 0 means everything went right.
