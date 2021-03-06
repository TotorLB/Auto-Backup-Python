#!/usr/bin/python
# -*- coding: utf-8 -*-

import os	# Fonctionnalités importées à partir de l'OS. | Imports OS functions to the script.
import sys	# Importe l'accès à certaines variables et paramètres. | Imports access to some variables and parameters.
import time	# Importe la notion de temps. | Imports time concept.
import getopt	# Importe la notion de création de paramètre. | Imports concept of parameter creation.
from os.path import exists # Importe le module nécessaire pour vérifier l'existence d'un fichier. | Imports module necessary to check file's existence.
from datetime import datetime	# Importe le temps de sorte à l'utiliser en heure, minutes, secondes. | Imports time in order to use it as hours, minutes and seconds.
from time import strftime	# Importe le temps de sorte à en faire un argument formaté. | Imports time in order to use it as a formatted argument.
from sys import argv		# Importe le nécessaire pour lister des paramètres. | Imports necessary options to list parameters.

def show_usage():	# Variable d'aide finissant sur une erreur. | Defines help then closes on error.
    print """
    Sauvegarde d'un site Wordpress sur un serveur distant.

    --- Un fichier de configuration sous la forme suivante doit exister pour le bon fonctionnement du script:
    dir_to_backup = /etc/dossier_sauvegarde_mysqldump
    dir_to_archive = /etc/dossier_sauvegarde_archive_tar
    db_username = username_database
    db_name = nom_database
    db_password = mot_de_passe_database
    dir_cible = /etc/dossier_destination_sauvegarde
    ip_cible = adresse_ip_serveur_distant
    login_cible = login_serveur_distant

    --- Le script attend le paramètre suivant:
        -f fichier - i.e. /etc/mon_fichier_de_configuration

    Wordpress backup on a remote server.

    --- A configuration file should exist. It should have the following aspect:
    dir_to_backup = /etc/mysqldump_backup_repertory
    dir_to_archive = /etc/tar_archive_backup_repertory
    db_username = username_database
    db_name = name_database
    db_password = password_database
    dir_cible = /etc/backup_destination_repertory
    ip_cible = ip_adress_remote_server
    login_cible = login_remote_server

    --- Script expect the following parameter:
        -f fichier - i.e. /etc/configuration_file
    """
    exit(1)


try:
    opts, args = getopt.getopt(argv[1:], "hf:", ["help", "fichier="]) # Liste de paramètres. | Parameters are listed.
except getopt.GetoptError, err:	# S'il y a une erreur durant "try", "except" sera lancée. | If there's an error during "try", "except" will be launched.
    print str(err)
    show_usage()

if opts.__len__() == 0: # S'il n'y a aucun paramètre, erreur. Affiche l'aide. | If there's no parameter, error. Displays help.
    show_usage()

fichier = None 	# Création d'une variable vide. | Empty variable is created.

for option, value in opts:	# Pour option, la valeur sera entre parenthèses dans les "if" suivants. | For option, value will be in ( ) in the following "if".
    if option in ('-h', '--help'):
        show_usage()
    elif option in ('-f', '--fichier'):
        fichier = value
    else:
        print "Paramètre inconnu. Unknown parameter used."
        show_usage()

if exists (fichier) == False:
    print "Le fichier de configuration n'existe pas. Configuration file does not exist."
    show_usage()

#fichier conf
conf = open(fichier,"r")	# Ouverture du fichier associé au script. | File option is opened.
dir_to_backup = conf.readline()[16:-1]
dir_to_archive = conf.readline()[17:-1]
db_username = conf.readline()[14:-1]
db_name = conf.readline()[10:-1]
db_password = conf.readline()[14:-1]
dir_cible = conf.readline()[12:-1]
ip_cible = conf.readline()[11:-1]
login_cible = conf.readline()[14:-1]
conf.close()

d = datetime.now()	# Variable donnant le temps à l'instant T | Parameter giving the actual T time.
date = d.strftime("%Y_%m_%d")	# Variable utilisant "d" pour en faire un format clair. | Parameter using "d" to make a formatted date.
chemin="/etc/projet/logs/"	# Chemin absolu des logs | Path for the logs.
log = open(chemin+"log.log", "w")	# Création des logs | Creation of logs.


serveur_mere = {	# serveur_mere means main_server
	'dir_to_backup' : dir_to_backup,	# Où mysqldump va sauvegarder son dump. | Where mysqldump will save its dump.
	'dir_to_archive' : dir_to_archive,	# Où tar va sauvegarder son archive. | Where tar will save its archive.
	'db_username' : db_username,			# Username de la database Wordpress. | Wordpress database's username.
	'db_name' : db_name,				# Nom de la database Wordpress. | Wordpress database's name.
	'db_password' : db_password,			# Mot de passe de la database Wordpress. | Wordpress database's password.
	}

serveur_distant = {	# serveur_distant means remote_server
	'dir' : dir_cible,			# Répertoire où va être stocké la sauvegarde. | Repertory where the archive will be sent.
	'server' : ip_cible,			# Adresse IP du serveur distant. | IP address of the remote server.
	'login' : login_cible,				# Login du serveur distant. | Remote server's login.
	}

if exists ('/usr/bin/mysqldump') == False:		# Les "if" suivants vont vérifier si les éléments nécessaires sont bien présents pour le script. | "If" will check if all elements are here.
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
	# La deuxième ligne crée un deuxième dump pour avoir toujours un fichier le plus à jour possible peu importe la date. À chaque sauvegarde, il sera remis à jour.
	# The second line will create a second dump to always have a file updated, the latest one. At each backup, it is updated.
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
			os.system('rm -r /etc/projet/sauvegarde/*') # Suppression des fichiers commencés pour garder les dossiers propres. | Documents created are deleted to clean the folders.
			os.system('rm -r /etc/projet/archive/*')
			exit('1') # 1 signifie que le script s'arrête avec une erreur. Voir les logs. | 1 means script stopped working because of an error. Check the logs.
	except BaseException as be:
		log.write(be)	# Écriture de l'erreur dans le log. | Log is written.
		os.system('rm -r /etc/projet/sauvegarde/*')
		os.system('rm -r /etc/projet/archive/*')
		exit(1)

except BaseException as be:
	log.write(be)	# Écriture de l'erreur dans le log. | Log is written.
	os.system('rm -r /etc/projet/sauvegarde/*')
	os.system('rm -r /etc/projet/archive/*')
	sys.exit(1)

log.close() # Fermeture du fichier log. | Log's file is closed
sys.exit(0) # 0 signifie que tout s'est déroulé correctement. | 0 means everything went right.
