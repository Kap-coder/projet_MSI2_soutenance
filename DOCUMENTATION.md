# 📚 Tutore2 - Système de Gestion d'Emplois de Temps Académiques

## 🚀 Démarrage Rapide

### 1. Installation
```bash
# Cloner le repository
git clone <repository_url>
cd Tutore2

# Activer l'environnement virtuel
.\venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Configuration de la Base de Données
```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 3. Lancer le serveur
```bash
# Double-cliquer sur run.bat ou
python manage.py runserver
```

L'application sera accessible à `http://127.0.0.1:8000/`

## 📁 Structure du Projet

```
Tutore2/
├── users/              # Gestion des utilisateurs et authentification
├── courses/            # Gestion des cours/matières
├── rooms/              # Gestion des salles de classe
├── timetables/         # Gestion des emplois du temps
├── schedules/          # Gestion des créneaux horaires
├── availability/       # Gestion des disponibilités enseignants
├── Tutore2/            # Configuration du projet
└── venv/               # Environnement virtuel
```

## 🔑 Applications Django

### 1. **Users** (Gestion des Utilisateurs)
- Modèle utilisateur personnalisé avec rôles (ADMIN, TEACHER, STUDENT)
- API REST pour la gestion des utilisateurs
- **Endpoints:**
  - `GET/POST /api/users/` - Lister/Créer les utilisateurs
  - `GET/PUT/DELETE /api/users/{id}/` - Récupérer/Modifier/Supprimer un utilisateur

### 2. **Courses** (Gestion des Cours)
- Modèle pour les matières/cours
- Code unique pour chaque cours
- **Endpoints:**
  - `GET/POST /api/courses/` - Lister/Créer les cours
  - `GET/PUT/DELETE /api/courses/{id}/` - Gérer un cours

### 3. **Rooms** (Gestion des Salles)
- Types de salles : Salle de classe, Laboratoire, Amphithéâtre
- Gestion de la capacité et localisation
- **Endpoints:**
  - `GET/POST /api/rooms/` - Lister/Créer les salles
  - `GET/PUT/DELETE /api/rooms/{id}/` - Gérer une salle

### 4. **Timetables** (Emplois du Temps)
- Gestion des emplois du temps complets
- Statuts : DRAFT, PUBLISHED, ARCHIVED
- Année académique et semestre
- **Endpoints:**
  - `GET/POST /api/timetables/` - Lister/Créer les emplois du temps
  - `GET/PUT/DELETE /api/timetables/{id}/` - Gérer un emploi du temps

### 5. **Schedules** (Créneaux Horaires)
- Lie un cours, un enseignant, une salle et des horaires
- Validation des horaires
- Contraintes d'unicité
- **Endpoints:**
  - `GET/POST /api/schedules/` - Lister/Créer les créneaux
  - `GET/PUT/DELETE /api/schedules/{id}/` - Gérer un créneau

### 6. **Availability** (Disponibilités Enseignants)
- Gestion des disponibilités par jour de la semaine
- Horaires flexibles
- **Endpoints:**
  - `GET/POST /api/availability/` - Lister/Créer les disponibilités
  - `GET/PUT/DELETE /api/availability/{id}/` - Gérer une disponibilité

## 🔐 Authentification

L'API utilise l'authentification de session Django. Pour accéder aux endpoints :

1. Se connecter à l'administration Django (`/admin/`)
2. Ou utiliser les identifiants du superutilisateur

## 📊 Accès à l'Administration

L'interface d'administration Django est accessible à :
```
http://127.0.0.1:8000/admin/
```

## 🛠️ Technologies Utilisées

- **Django 6.0.1** - Framework web Python
- **Django REST Framework 3.14** - API REST
- **SQLite** - Base de données (développement)
- **Python 3.13**

## 📝 Notes de Développement

- Tous les modèles incluent les timestamps `created_at` et `updated_at`
- Les validations sont intégrées au niveau des modèles
- Les permissions sont basées sur l'authentification
- Pagination activée (20 items par page)
- Filtrage, recherche et tri disponibles sur tous les endpoints

## 🚀 Prochaines Étapes

1. Ajouter une API d'authentification (JWT/Token)
2. Créer des algorithmes de résolution de conflits d'horaires
3. Développer une interface web (Frontend)
4. Ajouter des tests unitaires
5. Configurer un système de notification
6. Déployer en production

## 📧 Support

Pour toute question ou problème, consultez la documentation Django officielle ou contactez l'équipe de développement.
