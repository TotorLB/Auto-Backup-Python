#!/usr/bin/python
# -*- coding: utf-8 -*-

# Script proposé par V.L.B
# Script submitted by V.L.B

# Script de sauvegarde et de transfert sur un serveur distant.
# Backup script on the distant server.

# Les lignes suivantes seront commentées de manière à être comprises par chacun, peu importe le niveau de connaissance en python. La traduction vers l'anglais n'apporte aucune information supplémentaire et ne sert qu'à être accessible au plus nombre de personnes possible.
# The followings lines will be commented in a way meant to be understood by everyone. The french lines are only a translation from the english and don't bring any more information about the script itself.

# Objectif du script : Procéder à la sauvegarde d'une database (db) WordPress puis envoyer une archive de cette sauvegarde sur un serveur distant par SSH.
# Script's goal : Run a backup of a Wordpress database (db) then send an archive of this backup on a remote server by using SSH.

# Importation des modules nécessaires au script.
# Necessary modules are imported in order to use the script efficiency.

import os
# Permet l'importation des fonctionnalités récupérées grâce à l'OS (Système d'Exploitation). Cette importation servira lors des actions de préparation à la sauvegarde, de sauvegarde et de transfert sur le serveur distant.
# Allows to import functions from the actual OS (Operating System). This module will be used to prepare the database for the backup, the backup itself and the incremential backup on the distant server

import time
# Permet l'importation de données de temps nécessaires à l'utilisation de date et d'heure. Cette importation servira les deux lignes suivantes pour préparer la mise en place de la sauvegarde, celle-ci demandant une notation particulière durant la création du nom du fichier compressé.
# Allows to import time data. This will be used by the two right under lines to prepare the backup, this one asking some specific naming during the conception of the backup folder.

from datetime import datetime
# Permet l'importation du temps de manière à l'utiliser selon les besoins pour former des dates et gérer le temps en heures, minutes, secondes, ...
# Allows to import time in such way to make dates and manipulate time in hours, minutes, seconds, ...

from time import strftime
# Permet l'importation du temps de manière à en faire un argument clair. Il sera utilisé plus bas pour avoir une date formatée.
# Allows to import time to make it as an argument. It will be used later to get a formatted date.


# Établissement de classes concernant le temps.
# Time arguments used in the script.

d = datetime.now()
# Donne le temps à l'instant T. Cette fonction est possible grâce à l'importation de "datetime".
# Gives actual time. This is done because of the importation of "datetime".

date = d.strftime("%Y_%m_%d")
# Utilise la classe au-dessus pour créer une adresse selon un format précis de jour, mois, année. Cette fonction est possible grâce à l'importation de "strftime" ci-dessus.
# Uses the class defined above to give a formatted date like "day, month, year". The function is available because of the importation of "strftime".


# Définition d'un ensemble de paramètres nécessaires à l'exécution du script. Il est nécessaire d'adapter les noms de fichiers, de login, de mot de passe et autres informations selon le système utilisé. Dans cet exemple, les informations à changer et à adapter seront toutes montrées avec un ensemble de "X".
# These are the main parameters. It will be needed to change the informations below according to the needs of the used system (Folders path, login, password and any information related to the system using this script.) In this example, the informations who have to be changed will be named with a serie of "X".

Serveur_mere = {
	# Ceci est le nom du serveur possédant le WordPress. Il est le point d'origine de la sauvegarde et du transfert.
	# This is the main server owning Wordpress. It is the starting point of the backup and transfert. ("Serveur_mere" means "Main_server").

        'dir_wordpress' : '/XXX/XXX/XXX',
	# Ceci est le répertoire où est le Wordpress doit être trouvé.
	# This is the wordpress path can be found.
        'dir_to_backup' : '/XXX/XXX/XXX',
	# Ceci est le répertoire où doit être rangée la sauvegarde.
	# This is the storage location of the backup.
        'db_username' : 'XXX',
	# Ceci est le nom d'utilisateur de la base de données. Pour accéder à cette dernière, il est nécessaire de posséder les trois informations suivantes : Le nom d'utilisateur, le nom de la base de données et le mot de passe.
	# This is the database's login. In order to have access to it, it will be necessary to write down here the three needed informations : Login, Wordpress database's name and password.
        'db_name' : 'XXX',
	# Ceci est le nom de la base de données du WordPress.
	# This is the Wordpress' database's name.
        'db_password' : 'XXX',
	# Ceci est le mot de passe de la base de données.
	# This is the database's password. 
    }

Serveur_distant = {
	# Ceci est le serveur distant sur lequel sera placée la sauvegarde lorsque transférée.
	# This is the remote server where the backup will be set up on. ("Serveur_distant" means "Remote_server").

        'dir' : '/XXX/XXX/XXX',
	# Ceci est le répertoire où sera placée la sauvegarde.
	# This is the folder path where the backup will be set.
        'server' : 'XXX.XXX.XXX.XXX',
	# Ceci est l'adresse IP du serveur distant afin qu'il puisse être contacté.
	# This is the IP address of the remote server in order to contact it.
        'login' : 'XXX',
	# Ceci est le login qui permet d'accéder au serveur distant. Le mot de passe devra être entré manuellement lors du transfert et, ce, pour des raisons de sécurité afin que tout le monde ne puisse pas écraser, modifier, corrompre ou abîmer une sauvegarde en cherchant volontairement à la modifier à sa base.
	# This is the login to have access to the remote server. Password will be asked later and will have to be manually typed. This is because of security reasons. None, except the administrator, should be able to save, modify, erase or corrupt the backup by specifically looking to change his database then send the new informations to the remote server.
    }

# Note : Ne pas supprimer les "," placées après chaque paramètre afin de garantir le bon fonctionnement du script.
# Note : Do not delete those "," set behind each parameter to make sure everything works properly.


# Script en lui-même utilisant les modules, classes et informations entrées ci-dessus.
# Core script using modules, classes and informations given above.

try:
	# La commande "try" permet d'essayer un ensemble de caractères afin d'y déceler une erreur. Si tel était le cas, la commande suivante "except" chercherait à indiquer l'origine de la faille. Si aucun problème n'est détecté, la commande entrée sera lancée.
	# "Try" command lets a block of characters to be used in order to detect troubles. If some troubles were detected, the following command "except" would give an error message. If nothing gone wrong, the command will be sent and actions will be done.
    os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_'+date+'.sql')
	# Mysqldump est un programme de sauvegarde. Pour commencer, il est nécessaire de pouvoir s'y connecter.
	# Sur la commande "mysqldump -u", le "-u" couplé à un nom, permet de se connecter à la base de données.
	# Par la suite, le "-p" comprend la commande utilisée pour le mot de passe. Ainsi, on peut y comprendre : "Sur le serveur mère, le mot de passe est celui contenu dans les paramètres 'db_password'.
	# "-d" produit la même action que "-p" mais pour le nom du WordPress.
	# Enfin, la base de données pour le MySQLdump est créée, permettant de procéder à la sauvegarde.
	# Mysqldump is a program backup. To start, it needs to be connected on.
	# On the command "mysqldump -u", "-u" used with a name, lets one to connect to the database.
	# "-p" works for the password. The characters chain can be translated like : "On Serveur_mere (main server), password is the one stored in the parameter "db_password").
	# "-d" words in the same way than "-p" but for the WordPress' name.
	# Finally, the database dump is created, allowing to make the backup.

    os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_Update.sql')
	# En reprenant la même logique de cheminement, la ligne permet de se connecter à la base de données puis de procéder à sa mise à jour, si nécessaire.
	# Using the same way of doing, database is updated if needed.

except BaseException as be:
    print(be)
	# Si, pour quelque raison que ce soit, "try" venait à échouer, "except" serait lancée afin de tenter d'identifier la source de la faille.
	# "BaseException" est un moyen de pouvoir placer la commande "as" qui sera vue dans la ligne suivante. En soi, depuis les versions récentes, "except" et "except BaseException" sont similaires dans leur utilisation.
	# "as" permet de créer un alias. C'est à dire un nom à utilisation directe simplifiée. Ci-dessus, "be" prend le rôle de "BaseException". Ce faisant, dans la ligne "print(be). Print affichant quelque chose à l'écran, "be" affichera ce qu'aurait affiché "BaseException". L'utilisation de "as" est simplifiée par l'utilisation de ce procédé.
	# "Print" retourne une information visible par l'utilisateur. Dans la configuration actuelle, celle-ci permet d'indiquer la faille qui empêche le bon déroulement de l'action entamée.
	# If, for any reason, "try" wouldn't work properly, "except" would start working, looking for to identify the trouble's root.
	# "BaseException" is a way to set up the command "as" which will be described below. Pratically speaking, "except" and "except BaseException" have no difference. They work in the same way.
	# "as" allows to create an alias. This means a name with simplified using will be created. Above, "be" acts like "BaseException" because of "as". Then, in the line "print(be). Print monitoring something to the user, "be" will displays what "baseException" would have displayed. "as" using is made easier by this way.
	# "Print" returns an information to the user so he can read it. In the script, this gives indication to the problem preventing the script to work properly.


try:
    os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_'+date+'.tar.gz '+Serveur_mere['dir_wordpress'])
	# "tar" lance une compression du fichier selon des options spécifiées par les lettres ajoutées derrière. Les lettres données derrière sont notées avec un "-" devant sauf dans le cas où plusieurs sont mises à la suite pour procéder à un enchaînement de caractères, dans ce cas, seule la première a un "-".
	# "-c" signifie "Créer". Dans ce cas, le script procède à la création d'une archive .tar.
	# "-v" signifie "verbose", soit un mode d'affichage détaillé pour l'utilisateur qui verra ce que la machine fait avec davantage d'informations.
	# "-z" signifie que tar doit lire les fichiers grâce à gzip, lui permettant d'interagir avec différents types d'archives.
	# "-f" signifie que tar agit sur tel ou tel fichier. Dans ce cas, il prend les renseignements sur la suite de la ligne.
	# Le nom du fichier sera, grâce à "-f" : "/wordpress + "DATE DÉFINIE PRÉCÉDEMMENT" au format .tar.gz (type de compression.)
	# Le fichier d'origine à copier étant trouvé sur 'dir_wordpress' défini précédemment et sera copié sur 'dir_to_backup'.
	# "tar" starts compressing file according to some specifics options with the letters added right after. Those letters are written with "-" before except in the case many letters are following each other (like in this script) where "-" will only be on the first letter.
	# "-c" means "create". Tar is then working to create an archive .tar.
	# "-v" means "verbose". It means that the computer will display more informations about the running actions for the user.
	# "-z" means tar will read files through gzip, granting it to deal with many kinds of archives.
	# "-f" means tar will work on a specified file. In this script, it uses informations given after.
	# Because of "-f", tar archive will be : "/wordpress + "DATE DEFINED ABOVE" at .tar.gz format.
	# File to copy and archive is found on 'dir_wordpress' already defined and will be saved on 'dir_to_backup'.
    os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_save_Update.tar.gz '+Serveur_mere['dir_wordpress'])
	# Comme pour le premier "try", cette ligne, similaire à la précédente, est en fait une mise à jour de la première afin d'être certain de posséder toutes les informations à jour.
	# Like the first "try", this line, looking like the previous one, is an updating command used to get all last informations.

except BaseException as be:
    print(be)
	# Si, pour quelque raison que ce soit, "try" venait à échouer, "except" serait lancée afin de tenter d'identifier la source de la faille.
        # "BaseException" est un moyen de pouvoir placer la commande "as" qui sera vue dans la ligne suivante. En soi, depuis les versions récentes, "except" et "except BaseException" sont similaires dans leur utilisation.
        # "as" permet de créer un alias. C'est à dire un nom à utilisation directe simplifiée. Ci-dessus, "be" prend le rôle de "BaseException". Ce faisant, dans la ligne "print(be). Print affichant quelque chose à l'écran, "be" affichera ce qu'aurait affiché "BaseException". L'utilisation de "as" est simplifiée par l'utilisation de ce procédé.
        # "Print" retourne une information visible par l'utilisateur. Dans la configuration actuelle, celle-ci permet d'indiquer la faille qui empêche le bon déroulement de l'action entamée.
        # If, for any reason, "try" wouldn't work properly, "except" would start working, looking for to identify the trouble's root.
        # "BaseException" is a way to set up the command "as" which will be described below. Pratically speaking, "except" and "except BaseException" have no difference. They work in the same way.
        # "as" allows to create an alias. This means a name with simplified using will be created. Above, "be" acts like "BaseException" because of "as". Then, in the line "print(be). Print monitoring something to the user, "be" will displays what "baseException" would have displayed. "as" using is made easier by this way.
        # "Print" returns an information to the user so he can read it. In the script, this gives indication to the problem preventing the script to work properly.


# Transfert du fichier précédémment établi sur le serveur distant.
# File created is now sent to the remote server.

try:
    os.system('rsync -avrz '+Serveur_mere['dir_to_backup']+' '+Serveur_distant['login']+'@'+Serveur_distant['server']+':'+Serveur_distant['dir']+'/')
	# "rsync" est un utilitaire de transfert et de synchronisation de fichiers. Comme pour tar, il a reçu un ensemble d'options définies par des lettres.
	# "-a" désigne une archive puisqu'il s'agit d'un fichier .tar.gz (format compressé donc archive).
	# "-v" signifie "verbose", soit un mode d'affichage détaillé pour l'utilisateur qui verra ce que la machine fait avec davantage d'informations.
	# "-r" signifie "récurrence", soit la recherche de répétitions, points identiques dans le fichier. Cela est utilisé pour une sauvegarde incrémentielle.
	# "-z" signifie que les fichiers envoyés seront compressés durant le transfert.
	# La ligne veut donc dire : Synchronisation, avec les options sus-nommées, de cette zone : 'dir_to'backup' vers le serveur distant en utilisant le login + @ + adresse IP du serveur distant afin de pénétrer par SSH dans le répertoire 'dir' auquel on ajoute un "/" afin d'y placer la nouvelle sauvegarde. Donc, la sauvegarde sera ici : Serveur distant /dir/ (dir = Ce qui a été défini.
	# "rsync" is a utility to transfert and synchronise files. Like tar, it uses options defined by the letters after it.
	# "-a" defines that rsync is working on a archive because the actual file is an .tar.gz (Compressed then archive).
	# "-v" means "verbose". It means that the computer will display more informations about the running actions for the user.
	# "-r" means "recursive", looking for some identical points in the origin file and the target repertory. It is used for an incremential backup.
	# "-z" means files sent will be compressed during the transfert.
	# This line literally means : Synchronise, with the options above, this area : 'dir_to_backup' to the remote server by using it's login + @ + IP address of the remote server in order to access it by SSH. By this way, get into "/dir" repertory, add "/" and set the backup here. (So the backup will be located here : On remote server /dir/ (dir = what was defined before).
	# Note importante : Comme écrit au début, il est nécessaire d'entrer le mot de passe du serveur distant par mesures de sécurité.
	# Important note : As said at the beginning, it will be asked to write down the password for security reasons. This script doesn't automatically bypass or takes the password.

    print("Sauvegarde incrémentielle effectuée avec succès.")
	# "Print" retourne une information visible par l'utilisateur. Cette phrase confirme le succès de la sauvegarde et peut être librement changée.
	# "Print" returns an information to the user so he can read it. It can be freely changed to any sentence to confirm the success of the script. Actually, in french, it says : "Incremential backup had been done with success."

except BaseException as be:
    print(be)
	# Si, pour quelque raison que ce soit, "try" venait à échouer, "except" serait lancée afin de tenter d'identifier la source de la faille.
        # "BaseException" est un moyen de pouvoir placer la commande "as" qui sera vue dans la ligne suivante. En soi, depuis les versions récentes, "except" et "except BaseException" sont similaires dans leur utilisation.
        # "as" permet de créer un alias. C'est à dire un nom à utilisation directe simplifiée. Ci-dessus, "be" prend le rôle de "BaseException". Ce faisant, dans la ligne "print(be). Print affichant quelque chose à l'écran, "be" affichera ce qu'aurait affiché "BaseException". L'utilisation de "as" est simplifiée par l'utilisation de ce procédé.
        # "Print" retourne une information visible par l'utilisateur. Dans la configuration actuelle, celle-ci permet d'indiquer la faille qui empêche le bon déroulement de l'action entamée.
        # If, for any reason, "try" wouldn't work properly, "except" would start working, looking for to identify the trouble's root.
        # "BaseException" is a way to set up the command "as" which will be described below. Pratically speaking, "except" and "except BaseException" have no difference. They work in the same way.
        # "as" allows to create an alias. This means a name with simplified using will be created. Above, "be" acts like "BaseException" because of "as". Then, in the line "print(be). Print monitoring something to the user, "be" will displays what "baseException" would have displayed. "as" using is made easier by this way.
        # "Print" returns an information to the user so he can read it. In the script, this gives indication to the problem preventing the script to work properly.

