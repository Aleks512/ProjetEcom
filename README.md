# ProjetEcom (ecommerce)
## Ventalis, une entreprise avec les valeurs vertes.

### Mise en place de l'environnement de développement Python.
#### Mettez en place l'environnement de développement Python avec un environnement virtuel Python.
Si vous avez déjà configuré Python, exécutez les commandes suivantes (si vous êtes sur Windows, vous pouvez utiliser py ou py -3 à la place de python3 pour démarrer Python) :

## Installation
- Clonez ce dépôt sur votre machine locale :
   ```shell
   git clone https://github.com/Aleks512/ProjetEcom.git
- Installez les dépendances du projet à l'aide de gestionnaire de paquets (par exemple, pip) et exécutez les migrations de la base de données
    ```shell
    pip3 install -r requirements.txt
    python3 manage.py makemigrations
    python3 manage.py migrate
- Créer k'aadministrateur (superuser) du site et authentifiez vous via le login
    ```shell
    python3 manage.py createsuperuser
- Lancez le serveur de développement :
    ```shell
    python3 manage.py runserver
Ouvrez navigateur http://127.0.0.1:8000/admin/ to open the admin site
