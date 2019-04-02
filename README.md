# Auto-Backup-Python
Backup script Python

You'll find an english traduction below the french one. Script will be translated in the same way in french and english.

Les lignes suivantes seront traduites en anglais mais n'apportent pas d'informations complémentaires. Ne pas être étonné que le script soit commenté dans les deux langues. Celles-ci disent la même chose.

   Français :
  
  Introduction :
  
  Ceci est un script d'automatisation d'une sauvegarde d'une database WordPress puis de son envoi sur un serveur distant.
Le script en lui-même a été commenté de manière à ce que même un débutant puisse modifier au besoin des éléments de ce script sans
difficulté.
  Ce script a bien entendu été testé et ne représente en aucun cas un danger pour la machine qui l'exécute. Néanmoins, assurez-vous de posséder une place suffisante pour pouvoir procéder à la sauvegarde et que vous détenez toutes les informations nécessaires pour accéder au WordPress et au site distant.

  Prérequis :
  
  - Python.
  - Avoir deux machines pour envoyer/recevoir la sauvegarde ayant la possibilité de se joindre entre eux.
  - Bien remplir les "X" avec les informations nécessaires.
  
  Installation :
  
  Une fois le script téléchargé sur votre machine, assurez-vous de posséder les droits pour son exécution. Pour lancer le script, la commande "./backup.py" doit être entrée.
  Si vous ne possédiez pas les droits nécessaires, rendez-vous dans le répertoire du fichier et utilisez la commande "chmod" pour modifier vos droits dessus.
  
  Informations à modifier :
  
  Pour ouvrir le fichier script, rendez-vous dans le répertoire correspondant avec la commande "cd" (Exemple : cd /etc/exemple). Utilisez nano, vi ou vim et entrez le nom du fichier. (Exemple : Vim backup.py). Il ne vous restera qu'à modifier les valeurs ou attributs souhaités.
  Toutes les informations contenues dans les paramètres "serveur_mère" et "serveur_distant" doivent être convenablement remplis afin de permettre au script de fonctionner correctement.
  Pour l'utilisation de ce pour quoi le script a été conçu, changer les "X" des deux zones suffira à faire fonctionner le script et à obtenir une sauvegarde distante fonctionnelle.
  Afin de faciliter les opérations de modification, le script a été entièrement commenté et détaillé pour fournir le plus de renseignements possibles sur chaque ligne.
  
  Action mannuelle à effectuer :
  
  Durant l'exécution du script, vous serez amené, durant la dernière partie du script, à entrer votre mot de passe de votre serveur distant. Si vous pouvez librement entrer le mot de passe dans le script afin d'entièrement l'automatiser, sachez que cela n'a pas été fait dans ce script afin de conserver une part de sécurité mais cela reste entièrement possible. Pour cela, il faudrait ajouter une catégorie mot de passe aux paramètres définis dans le serveur distant et ajouter cette variable sur la ligne adéquate (par défaut, le dernier "try" du script.)
  
  Résultat obtenu :
  
  Dans le répertoire que vous aurez assigné sur le script, vous retrouverez, sur le serveur distant, vos sauvegardes rangées selon leur nom avec la date.
  ATTENTION : Utilisant le même nom, la sauvegarde faite deux fois le même jour, pour X raison, mènera à la perte de la première sauvegarde car celle-ci serait écrasée. Prenez donc soin de déplacer votre première sauvegarde si jamais vous souhaitiez en relancer une.
  
-------------------------------------------------------------------------------------------------------------------------------

English :

  This is a script aiming to make an auto backup of a Wordpress' database then send it to the remote server.
Script itself had been commented in a way making it easy, even to a beginner, to modify, change it and adapt it to his needs.
  This is script, obviously, had been tested and won't cause problem to your machine. But, make sure you got enough space to make
the backup and that you own all necessary stuff to access to the WordPress and it remote server.

  Prerequisites :
  
  - Python
  - To own two machines able to send/receive the back and be able to reach each other.
  - To fill all "X" in the script to make it work properly.
  
  Installation :
  
  Once script had been doawnloaded, make sure you've got all rights needed to make it run. To execute the script, use the command : "./backup.py".
  If you didn't have the needed rights, go to the repertory where it is stored and use the command "chmod" to change yours rights.
  
  Informations to modify :
   
  To open the script, use "cd" command to go to the file (Example : cd /etc/backup) and use nano, vi or vim to open it. (Example : vim backup.py) You'll be able to change all informations you want from here.
  All informations in "serveur_mere" (main server) and "serveur_distant" (remote server) have to be filled to make work the script.
  If you just want to run it and use it for its initial goal, just fill the "X" in the two defined areas with the correct values and you'll get a backup to a remote server.
  To make any change easily, the script had been commented in english so you can locate what you would like to edit, remove or add.
  
  Manual operation needed :
  
  During the execution of the script, you'll be asked, at the last part, to type your password. This had been set for security reason defined in the script. Please, consider you may make this script totally working without any human touching. For this, just add to the remote server area a new parameter for password. This done, you just have to add this new argument to the last "try" line to make it auto fill with your password.
  
  Expected result :
  
  In the defined repertory on the remote server, you'll find your backups according to their name and date.
  WARNING : Using the same name, two backups made the same day would go into conflict and the first one would be erased. Please, make sure to move your first backup somewhere else if you plan to make many backups the same date ! (If it's not on the same date, you won't have any problem with this).
