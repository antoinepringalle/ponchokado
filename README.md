# Tirage au sort cadeaux Ponchos Noël 2020

## Utilisation :

Remplir le fichier ponchos.csv avec les prénoms et les mails des participants (*séparateur virgule*). Ajouter si besoin
une troisième colonne **éviter** avec les noms des participants sur lesquels uen personne ne doit pas tomber.
Par exemple, si Antoine ne doit pas avoir Orlane et Baptiste, on écrira :

| prenom    | mail                              | eviter            |
|-----------|-----------------------------------|-------------------|
| Antoine   | mail@gmail.com                    | Orlane; Baptiste  |
| Orlane    | mail@gmail.com                    |                   | 
| Baptiste  | mail@gmail.com                    | Antoine           |
| ...       | ...                               | ...               |

Renseigner dans le fichier `main.py` l'adresse mail (`MY_ADRESS`) et le mot de passe (`PASSWORD`) du compte avec lequel on veut envoyer le mail.

Enfin, lancer le code avec la commande
```
$ python3 main.py
```