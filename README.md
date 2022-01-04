# Développement de chatbot
## Principe
Notre application permet aux robots (pepper/NAO) d'interagir avec leurs interlocuteurs et de leur offrir différents services tels que la récupération de leur propre emploi du temps, ainsi que la traduction de phrases du français à l'anglais ou encore la définition de mots, via des API REST.
## Fonctionnement
Le système est basé sur deux composants :
Le premier composant qui permet le devellopement du chatbot en utilisant Rasa et qui se pose sur 4 principaux fichier:
- `nlu.yml` : ce fichier contient une liste de questions courantes et dialogue que les utilisateurs sont susceptibles de poser,et qui contient aussi les intentions,les entités, que l'assistant doit extraire de l'exemple donné par l'utilisateur.
- `domaine.yml` : contient les différentes réponses que le chatbot peut utiliser,les actions à effectuer ainsi que les informations à retenir dans des slots pour pouvoir les utiliser dans l'exécution des actions. Des formes on été utilisé lors de la récupération de slots ce qui permet de stocker des informations qui ne sont pas définie dans les fichiers d'entraînement ce qui est pratique pour le cas de traduction des phrases et la définition des mots.
- `stories.yml` : contient des conversations simulées de bout en bout, dans un premier temps ces histoires ont été écrites à la main pour initialiser un modèle.
- `actions.py` : Ce script contient les differents  actions personnalisées pour le chatbot afin de répondre aux besoins du client,`ActionSchedule` permet de recuperer les informations relatives au filière de l'utilisateur afin de récuperer l'emplois du temps en utilisant l'API fourni par CERI.`ActionDefinition` permet de recuperer le mot enregistrer dans le slot word et le traduire en utilisant le dictionnaire LAROUSSE.`ActionTranslation` cette fonction est la responsable sur la traduction des phrases du français en anglais.
- `rules.yml` : Les règles sont un type de données d'entraînement utilisées pour entraîner le modèle de gestion du dialogue. Les règles décrivent de courts morceaux de conversations qui doivent toujours suivre le même chemin et dont lequel nous avons definie les regles concernant les boucles de Form qui consiste a stocker des informations qui ne sont pas définie dans les fichiers d'entraînement ce qui est pratique pour le cas de traduction des phrases et la définition des mots.
Le deuxieme composant s'agit du choregraphe qui permet de tenir des conversations vocales avec l'utilisateur. Ceci est fait grâce au graphe du chorégraphe `NaoRasaASRProject.pml` qui consiste à récupérer la parole de l'utilisateur sous forme d'un fichier sous extension wave, le convertir en un fichier json qui contient les mots à l'aide de la bibliothèque GoogleSpeech, ce fichier json est traité ensuite par le modèle rasa afin de concevoir une réponse appropriée à celui-ci. Il est indispensable de connecter le robot et l'ordinateur contenant le chatbot ainsi que le chorégraphe sur le même réseau.

## Configuration
Nous avons conservé la configuration par défaut fournie avec la commande Rasa init puisque le modèle était correctement entraîné sans oublier l'utilisation de l'apprentissage interactif sur rasax qui nous a permis de corriger le comportement du bot et d'améliorer ses performances.
Après avoir défini les adresses IP de chaque composant, le chatbot doit être lancé par \textbf{rasa shell}, ce qui place celui-ci en attente du discours provenant de l'utilisateur à l'aide du chorégraphe qui orchestre la scène.
## Entrainement Model
Apres la definition des données d'entrainement du bot, l'entrainement de ce dernier est lancé avec la commande rasa train ce qui permet d'entrainer le nlu model et le core model.
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/nlu_model_train.png?raw=true)
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/core_model_train.png?raw=true)

Apres le bot est entrainer, on lance l'apprentissage interactive en utilisant la commande rasa x ce qui ouvre une page web qui permet d'interagir avec le bot en temps réel tout en lui corrigant les actions au cas ou il se trompe.
il faut lancer le script actions/actions.py avant de commencer une conversation avec le chatbot ce qui permet d'initiliaser le serveur dédié a l'execution des differents actions définies.
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/run_action_server.png?raw=true)
### exemples usage 
Notre modèle a réussi à tenir une conversation correcte après le renforcement de ce dernier grâce à RasaX, il est maintenant capable de récupérer auprès de l'utilisateur sa section et son groupe afin de lui fournir sa prochaine session ainsi que de lui rappeler la date du prochain examen afin de bien se préparer.
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/interactif_learning_rasax_1.png?raw=true)

Parmi les services fournis par notre robot, l'utilisateur peut demander une définition de n'importe quel mot en français, et notre robot est capable de fournir cette définition sans avoir besoin de se former sur ce mot en particulier.
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/interactif_learning_rasax_2.png?raw=true)


Et le dernier service dans lequel notre robot est doué est la traduction de toutes les phrases du français vers l'anglais sans aucune condition sur la taille et la grammaire de la phrase.
![alt text](https://github.com/anashaddad123/Chat_bot/blob/main/images/interactif_learning_rasax_3.png?raw=true)

