# Auto-Backup-Python
Backup script Python

You'll find an english traduction below the french one. Script will be translated in the same way in french and english.

Les lignes suivantes seront traduites en anglais mais n'apportent pas d'informations complémentaires.

   Français :
  
  Introduction :
  
  Ceci est un script d'automatisation d'une sauvegarde d'une database WordPress puis de son envoi sur un serveur distant.

  Ce script a bien entendu été testé et ne représente en aucun cas un danger pour la machine qui l'exécute. Néanmoins, assurez-vous de posséder une place suffisante pour pouvoir procéder à la sauvegarde et que vous détenez toutes les informations nécessaires pour accéder au WordPress et au site distant.

  Prérequis :
  
  - Python.
  - Avoir mysqldump, tar et scp. (Possiblité de vérifier leur présence avec la commande "whereis" (Exemple : "Whereis mysqldump".)
  - Avoir deux machines pour envoyer/recevoir la sauvegarde ayant la possibilité de se joindre entre eux.
  - Bien remplir les blancs avec les informations nécessaires sur le fichier "script.cfg"
  - Avoir correctement placé le fichier "script.cfg" fourni dans la liste dans le dossier /tmp. Attention, le dossier est supprimé au relancement. Il peut être placé ailleurs mais le chemin devra être modifié. (Voir dans le script).
  - Suivre le guide d'installation d'une clé de sécurité pour SSH. (ci-dessous)
  
  Clé de sécurité pour SSH :
  
  Sur la console, taper cette commande "ssh-keygen -t rsa". Presser entrée et tout laisser par défaut.
  Entrer cette commande : "ssh-copy-id USER@SERVER" (USER = nom d'utilisateur de la machine sur le serveur distant. SERVER = adresse IP du serveur distant.)
  Entrer le mot de passe du serveur distant.
  À partir de là, vous pourrez lancer le script sans avoir besoin d'entrer votre mot de passe. (Automatisation totale.)
  Note : Il est possible, pour des raisons de sécurité, de ne pas utiliser le générateur de clé si vous le souhaitez. Cependant, vous devrez entrer votre mot de passe à chaque utilisation du script.
  
  Installation :
  
  Une fois le script téléchargé sur votre machine, assurez-vous de posséder les droits pour son exécution. Pour lancer le script, la commande "./backup.py -f "NOM DU FICHIER"" doit être entrée.
  Si vous ne possédiez pas les droits nécessaires, rendez-vous dans le répertoire du fichier et utilisez la commande "chmod" pour modifier vos droits dessus.
  
  Informations à modifier :
  
  Pour ouvrir le fichier script, rendez-vous dans le répertoire correspondant avec la commande "cd" (Exemple : cd /etc/exemple). Utilisez nano, vi ou vim et entrez le nom du fichier. (Exemple : vim backup.py). Il ne vous restera qu'à modifier les valeurs ou attributs souhaités.
  Toutes les informations contenues dans les paramètres "serveur_mere" et "serveur_distant" doivent être convenablement remplies afin de permettre au script de fonctionner correctement.
  Pour l'utilisation de ce pour quoi le script a été conçu, changer les "X" des deux zones suffira à faire fonctionner le script et à obtenir une sauvegarde distante fonctionnelle.
  
  Action mannuelle à effectuer (SI VOUS N'AVEZ PAS UTILISÉ LE GÉNÉRATEUR DE CLÉS) :
  
  Durant l'exécution du script, vous serez amené, durant la dernière partie du script, à entrer le mot de passe de votre serveur distant. Si vous pouvez librement entrer le mot de passe dans le script afin d'entièrement l'automatiser, sachez que cela n'a pas été fait dans ce script afin de conserver une part de sécurité mais cela reste entièrement possible en utilisant le générateur de clés (ci-dessus).
  
  Résultat obtenu :
  
  Dans le répertoire que vous aurez assigné sur le script, vous retrouverez, sur le serveur distant, vos sauvegardes rangées selon leur nom avec la date.
  ATTENTION : Utilisant le même nom, la sauvegarde faite deux fois le même jour, pour X raison, mènerait à la perte de la première sauvegarde car celle-ci serait écrasée. Prenez donc soin de déplacer votre première sauvegarde si jamais vous souhaitiez en relancer une.
  
  Descriptif des commandes ligne par ligne :
  
  - "Import" (os, time, datetime, strftime) permet d'importer un module dans le script afin d'utiliser les fonctionnalités mises en place par ce module.
  d = datetime.now()
Donne le temps à l'instant T. Cette fonction est possible grâce à l'importation de "datetime".
  date = d.strftime("%Y_%m_%d")
Utilise la classe au-dessus pour créer une adresse selon un format précis d'année, mois, jour. Cette fonction est possible grâce à l'importation de "strftime" ci-dessus.
   - "Try" : La commande "try" permet d'essayer un ensemble de caractères afin d'y déceler une erreur. Si tel était le cas, la commande suivante "except" chercherait à indiquer l'origine de la faille. Si aucun problème n'est détecté, la commande entrée sera lancée.
   
   try:
    opts, args = getopt.getopt(argv[1:], "hf:", ["help", "fichier="])
    # Les paramètres sont listés.
except getopt.GetoptError, err:
    # S'il y a une erreur durant "try", "except" sera lancée.
    print str(err)
    # Affichage de l'erreur.
    show_usage()
    # Affiche l'aide.

if opts.__len__() == 0:
    # S'il n'y a aucun paramètre, erreur. Affiche l'aide.
    show_usage()

fichier = None
    # Création d'une variable vide.

for option, value in opts:	
     # Pour option, la valeur sera entre parenthèses dans les "if" suivants. C'est à dire que taper cette option aura pour effet de lancer la commande affichée en-dessous.
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
    # Au cas où le fichier demandé n'existe pas. Attention au bon placement des fichiers.

	# Attention à bien garder cette configuration (script.cfg) dans l'ordre afin de faire fonctionner le script.

conf = open(fichier,"r")	
    # Ouverture du fichier associé au script.

dir_to_backup = conf.readline()[16:-1]

dir_to_archive = conf.readline()[17:-1]

db_username = conf.readline()[14:-1]

db_name = conf.readline()[10:-1]

db_password = conf.readline()[14:-1]

dir_cible = conf.readline()[12:-1]

ip_cible = conf.readline()[11:-1]

login_cible = conf.readline()[14:-1]

conf.close()
   
  - if exists ('/usr/bin/mysqldump') == False: va vérifier si tel objet (mysqldump dans ce cas) n'existe pas. Si tout se passe bien, le script lancera le else avec un message indiquant la présence des éléments nécessaires.
  
  - os.system('rm -rf /etc/projet/archive/*') (ainsi que sa variante sauvegarde juste en-dessous) sert à vider les dossiers utilisés dans le script pour garantir le moins de conflits possible.
  
  - except BaseException as be:
			log.write(be)	# Écriture de l'erreur dans le log.
			os.system('rm -r /etc/projet/sauvegarde/*') # Suppression des fichiers commencés pour garder les dossiers propres.
			os.system('rm -r /etc/projet/archive/*')
			exit('1') # 1 signifie que le script s'arrête avec une erreur. Voir les logs.
   
  - os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_'+date+'.sql')
	
   Mysqldump est un programme de sauvegarde. Pour commencer, il est nécessaire de pouvoir s'y connecter.
	Sur la commande "mysqldump -u", le "-u" couplé à un nom, permet de se connecter à la base de données.
	Par la suite, le "-p" comprend la commande utilisée pour le mot de passe. Ainsi, on peut y comprendre : "Sur le serveur mère, le mot de passe est celui contenu dans les paramètres 'db_password'.
	"-d" produit la même action que "-p" mais pour le nom du WordPress.
	Enfin, la base de données pour le MySQLdump est créée, permettant de procéder à la sauvegarde.
   
  - os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_Update.sql')
	
	En reprenant la même logique de cheminement ci-dessus, la ligne permet de se connecter à la base de données puis de procéder à sa mise à jour, si nécessaire.
   
  - except BaseException as be:
    print(be)
	
   Si, pour quelque raison que ce soit, "try" venait à échouer, "except" serait lancée afin de tenter d'identifier la source de la faille.
	"BaseException" est un moyen de pouvoir placer la commande "as" qui sera vue dans la ligne suivante. En soi, depuis les versions récentes, "except" et "except BaseException" sont similaires dans leur utilisation.
	"as" permet de créer un alias. C'est à dire un nom à utilisation directe simplifiée. Ci-dessus, "be" prend le rôle de "BaseException". Ce faisant, dans la ligne "print(be). Print affichant quelque chose à l'écran, "be" affichera ce qu'aurait affiché "BaseException". L'utilisation de "as" est simplifiée par l'utilisation de ce procédé.
	"Print" retourne une information visible par l'utilisateur. Dans la configuration actuelle, celle-ci permet d'indiquer la faille qui empêche le bon déroulement de l'action entamée.
   
   - os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_'+date+'.tar.gz '+Serveur_mere['dir_to_backup'])
	
   "tar" lance une compression du fichier selon des options spécifiées par les lettres ajoutées derrière. Les lettres données derrière sont notées avec un "-" devant sauf dans le cas où plusieurs sont mises à la suite pour procéder à un enchaînement de caractères, dans ce cas, seule la première a un "-".
	"-c" signifie "Créer". Dans ce cas, le script procède à la création d'une archive .tar.
	"-v" signifie "verbose", soit un mode d'affichage détaillé pour l'utilisateur qui verra ce que la machine fait avec davantage d'informations.
	"-z" signifie que tar doit lire les fichiers grâce à gzip, lui permettant d'interagir avec différents types d'archives.
	"-f" signifie que tar agit sur tel ou tel fichier. Dans ce cas, il prend les renseignements sur la suite de la ligne.
	Le nom du fichier sera, grâce à "-f" : "/wordpress + "DATE DÉFINIE PRÉCÉDEMMENT" au format .tar.gz (type de compression.)
	Le fichier d'origine à copier étant trouvé sur 'dir_wordpress' défini précédemment et sera copié sur 'dir_to_backup'.
   
  - os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_save_Update.tar.gz '+Serveur_mere['dir_wordpress'])
	
   Comme pour le premier "try", cette ligne, similaire à la précédente, est en fait une mise à jour de la première afin d'être certain de posséder toutes les informations à jour.
	Like the first "try", this line, looking like the previous one, is an updating command used to get all last informations.
   
  - os.system('rsync -avrz '+Serveur_mere['dir_to_backup']+' '+Serveur_distant['login']+'@'+Serveur_distant['server']+':'+Serveur_distant['dir']+'/')
	
   "rsync" est un utilitaire de transfert et de synchronisation de fichiers. Comme pour tar, il a reçu un ensemble d'options définies par des lettres.
	"-a" désigne une archive puisqu'il s'agit d'un fichier .tar.gz (format compressé donc archive).
	"-v" signifie "verbose", soit un mode d'affichage détaillé pour l'utilisateur qui verra ce que la machine fait avec davantage d'informations.
	"-r" signifie "récurrence", soit la recherche de répétitions, points identiques dans le fichier. Cela est utilisé pour une sauvegarde incrémentielle.
	"-z" signifie que les fichiers envoyés seront compressés durant le transfert.
	La ligne veut donc dire : Synchronisation, avec les options sus-nommées, de cette zone : 'dir_to'backup' vers le serveur distant en utilisant le login + @ + adresse IP du serveur distant afin de pénétrer par SSH dans le répertoire 'dir' auquel on ajoute un "/" afin d'y placer la nouvelle sauvegarde. Donc, la sauvegarde sera ici : Serveur distant /dir/ (dir = Ce qui a été défini.)
  
-------------------------------------------------------------------------------------------------------------------------------

English :

  This is a script aiming to make an auto backup of a Wordpress' database then send it to the remote server.
Script itself had been commented in a way making it easy, even to a beginner, to modify, change it and adapt it to his needs.
  This is script, obviously, had been tested and won't cause problem to your machine. But, make sure you got enough space to make
the backup and that you own all necessary stuff to access to the WordPress and it remote server.

  Prerequisites :
  
  - Python.
  - To have mysqldump, tar et scp. (You can check if they're here with "whereis" (Example : "Whereis mysqldump".)
  - To have two machines to send/get the backup.
  - Fill the blanks space with the right informations in script.cfg.
  - Follow the keygenerator guide (right under)
  
  SSH key generator :
  
  On the console, use the following command "ssh-keygen -t rsa". Press enter and let by default.
  Enter this command : "ssh-copy-id USER@SERVER (USER = username of the remote server. SERVER = IP Address of the remote server.)
  Enter your password.
  From now, you won't need your password anymore to access via SSH your remote server.
  Note : You are free to not use this generator but you'll have to write down your password each time you use the script.
  
  Installation :
  
  Once script and "script.cfg" had been downloaded, make sure you've got all rights needed to make them run. Set "script.cfg" in the right folder (by default : /tmp/) (WARNING : /tmp/ are for temporary files. You can modify the path directly in the script if you want to make it permanent.) To execute the script, use the command : "./backup.py".
  If you didn't have the needed rights, go to the repertory where it is stored and use the command "chmod" to change yours rights.
  
  Informations to modify :
   
  To open the script, use "cd" command to go to the file (Example : cd /etc/backup) and use nano, vi or vim to open it. (Example : vim backup.py) You'll be able to change all informations you want from here.
  All informations in "serveur_mere" (main server) and "serveur_distant" (remote server) have to be filled to make work the script.
  If you just want to run it and use it for its initial goal, just fill the "X" in the two defined areas with the correct values and you'll get a backup to a remote server.
  To make any change easily, the script had been commented in english so you can locate what you would like to edit, remove or add.
  
  Manual operation needed (IF YOU DIDN'T USE THE KEY GENERATOR) :
  
  During the execution of the script, you'll be asked, at the last part, to type your password. This had been set for security reason defined in the script. Please, consider you may make this script totally working without any human touching. For this, just follow the key generator guide above.
  
  Expected result :
  
  In the defined repertory on the remote server, you'll find your backups according to their name and date.
  WARNING : Using the same name, two backups made the same day would go into conflict and the first one would be erased. Please, make sure to move your first backup somewhere else if you plan to make many backups the same date ! (If it's not on the same date, you won't have any problem with this).

   Description of each line :
   
   
  - "Import" (os, time, date, strftime) imports a module into the script in order to use its functionnalities in the script.
   d = datetime.now()
   Gives actual time. This is done because of the importation of "datetime".
   date = d.strftime("%Y_%m_%d")
   Uses the class defined above to give a formatted date like "year, month, day". The function is available because of the importation of "strftime".
  - "Try" command lets a block of characters to be used in order to detect troubles. If some troubles were detected, the following command "except" would give an error message. If nothing gone wrong, the command will be sent and actions will be done.
   
   try:
    opts, args = getopt.getopt(argv[1:], "hf:", ["help", "fichier="])
    # Parameters are listed.
except getopt.GetoptError, err:
    # If there's an error during "try", "except" will be launched.
    print str(err)
    # Error is displayed on monitor.
    show_usage()
    # Help is displayed.
    
if opts.__len__() == 0: 
    # If there's no parameter, error. Displays help.
    show_usage()

fichier = None 
    # Empty variable is created.

for option, value in opts:
	# For option, value will be in ( ) in the following "if". This means that if you use the script with the options defined below, you'll get a result according to the defined options. For example, "./backup.py -h" will display you all the help needed to make sure the script and the "script.cfg" run together right.
    if option in ('-h', '--help'):
        show_usage()
    elif option in ('-f', '--fichier'):
        fichier = value
    else:
        print "Unknown parameter used."
        show_usage()

if exists (fichier) == False:
    print "Le fichier de configuration n'existe pas. Configuration file does not exist."
    show_usage()

    # File configuration. Please, keep these lines in the same order as they appear in "script.cfg" to ensure everything is done with no trouble.
conf = open(fichier,"r")	# Ouverture du fichier associé au script. | File option is opened.
dir_to_backup = conf.readline()[16:-1]
dir_to_archive = conf.readline()[17:-1]
db_username = conf.readline()[14:-1]
db_name = conf.readline()[10:-1]
db_password = conf.readline()[14:-1]
dir_cible = conf.readline()[12:-1]
ip_cible = conf.readline()[11:-1]
login_cible = conf.readline()[14:-1]
conf.close()
   
   - if exists ('/usr/bin/mysqldump') == False: will check if something is missing. If none is missing, the monitor will display a message saying everything is here. If not, make sure the path aren't change on your computer.
  
  - os.system('rm -rf /etc/XXXX/XXXX*') (including the second one) will clear all the folders used in the script to make sure nothing will conflict with them.
  
  - except BaseException as be:
			log.write(be)	# Log writting
			os.system('rm -r /etc/projet/sauvegarde/*') # All files created during the script are deleted.
			os.system('rm -r /etc/projet/archive/*')
			exit('1') # 1 means the script stops because of an error. Check the logs.
   
  - os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_'+date+'.sql')
   
   Mysqldump is a program backup. To start, it needs to be connected on.
	On the command "mysqldump -u", "-u" used with a name, lets one to connect to the database.
	"-p" works for the password. The characters chain can be translated like : "On Serveur_mere (main server), password is the one stored in the parameter "db_password").
	"-d" words in the same way than "-p" but for the WordPress' name.
	Finally, the database dump is created, allowing to make the backup.
   
  - os.system('mysqldump -u '+Serveur_mere['db_username']+' -p'+Serveur_mere['db_password']+' -d '+Serveur_mere['db_name']+' > '+Serveur_mere['dir_to_backup']+'/db_wordpress_backup_Latest.sql')
   
   Using the same way of doing, database is updated if needed.
   
 -  except BaseException as be:
    print(be)
    
    If, for any reason, "try" wouldn't work properly, "except" would start working, looking for to identify the trouble's root.
	"BaseException" is a way to set up the command "as" which will be described below. Pratically speaking, "except" and "except BaseException" have no difference. They work in the same way.
	"as" allows to create an alias. This means a name with simplified using will be created. Above, "be" acts like "BaseException" because of "as". Then, in the line "print(be). Print monitoring something to the user, "be" will displays what "baseException" would have displayed. "as" using is made easier by this way.
	"Print" returns an information to the user so he can read it. In the script, this gives indication to the problem preventing the script to work properly.
   
  - os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_'+date+'.tar.gz '+Serveur_mere['dir_wordpress'])
   
   "tar" starts compressing file according to some specifics options with the letters added right after. Those letters are written with "-" before except in the case many letters are following each other (like in this script) where "-" will only be on the first letter.
	"-c" means "create". Tar is then working to create an archive .tar.
	"-v" means "verbose". It means that the computer will display more informations about the running actions for the user.
	"-z" means tar will read files through gzip, granting it to deal with many kinds of archives.
	"-f" means tar will work on a specified file. In this script, it uses informations given after.
	Because of "-f", tar archive will be : "/wordpress + "DATE DEFINED ABOVE" at .tar.gz format.
	File to copy and archive is found on 'dir_wordpress' already defined and will be saved on 'dir_to_backup'.
   
   - os.system('tar -cvzf '+Serveur_mere['dir_to_backup']+'/wordpress_save_Latest.tar.gz '+Serveur_mere['dir_to_backup'])
	Comme pour le premier "try", cette ligne, similaire à la précédente, est en fait une mise à jour de la première afin d'être certain de posséder toutes les informations à jour.
	Like the first "try", this line, looking like the previous one, is an updating command used to get all last informations.

   
  - os.system('rsync -avrz '+Serveur_mere['dir_to_backup']+' '+Serveur_distant['login']+'@'+Serveur_distant['server']+':'+Serveur_distant['dir']+'/')
   
   "rsync" is a utility to transfert and synchronise files. Like tar, it uses options defined by the letters after it.
	"-a" defines that rsync is working on a archive because the actual file is an .tar.gz (Compressed then archive).
	"-v" means "verbose". It means that the computer will display more informations about the running actions for the user.
	"-r" means "recursive", looking for some identical points in the origin file and the target repertory. It is used for an incremential backup.
	"-z" means files sent will be compressed during the transfert.
	This line literally means : Synchronise, with the options above, this area : 'dir_to_backup' to the remote server by using it's login + @ + IP address of the remote server in order to access it by SSH. By this way, get into "/dir" repertory, add "/" and set the backup here. (So the backup will be located here : On remote server /dir/ (dir = what was defined before).
	Note importante : Comme écrit au début, il est nécessaire d'entrer le mot de passe du serveur distant par mesures de sécurité.
	Important note : As said at the beginning, it will be asked to write down the password for security reasons. This script doesn't automatically bypass or takes the password.
   
