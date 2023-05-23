# ProjetEcom (ecommerce)
##### Ventalis, une entreprise avec les valeurs vertes.

## Mise en place de l'environnement de développement Python.
Mettez en place l'environnement de développement Python avec un environnement virtuel Python.
Si vous avez déjà configuré Python, exécutez les commandes suivantes (si vous êtes sur Windows, vous pouvez utiliser py ou py -3 à la place de python3 pour démarrer Python) :

## Installation
- Clonez ce dépôt sur votre machine locale :
   ```shell
   git clone https://github.com/Aleks512/ProjetEcom.git
- Créez et activez un environnement virtuel (facultatif) 
  ```shell
  python -m venv venv
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate  # Windows

- Installez les dépendances requises
  ```shell
  pip install -r requirements.txt
- Appliquez les migrations de la base de données
  ```shell
  python manage.py migrate
- Chargez les fixtures pour importer les données de base dans cet ordre precis :
  ```shell
  python manage.py loaddata fixtures/newuser.json
  python manage.py loaddata fixtures/consultant.json
  python manage.py loaddata fixtures/customer.json
  python manage.py loaddata fixtures/category.json
  python manage.py loaddata fixtures/product.json
  python manage.py loaddata fixtures/order.json
  python manage.py loaddata fixtures/cart.json
  python manage.py loaddata fixtures/comment.json
- Lancez le serveur de développement
  ```shell
  python manage.py runserver
- Accédez à l'application Ventalis dans votre navigateur à l'adresse suivante
  ```shell
  http://localhost:8000
N.B. Les mots de passe associés aux différents utilisateurs se trouvent dans le manuel d'utilisation joint en annexe de la copie rendue. Veuillez vous référer à ce manuel pour obtenir les mots de passe appropriés en fonction de rôle d'utilisateur (administrateur = superuser, customer, consultant).
