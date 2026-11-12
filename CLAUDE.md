# CLAUDE.md

Lis `BRIEF.md` et `ROADMAP.md` avant toute tâche.

- Décisions, journal et **questions ouvertes** : `docs/decisions.md`. Ne jamais trancher seul un point listé comme ouvert : demander.
- Recherche (outils, prix, monétisation, sources) : `docs/recherche.md`. Hébergement GPU : `docs/hebergement_gpu.md`.
- Persona et prompts : `personas/ai_girl/persona.md`, `personas/ai_girl/refs/prompts.md` (convention de nommage des images : §1 de ce fichier). Config de chaîne : `config/channels/ai_girl.yaml`.
- `SECRETS.local.md` contient des identifiants : ne jamais le lire sans demande explicite, ne jamais le commiter ni recopier son contenu.
- `docs/archive/` : copies des notes d'origine avant fusion (11 nov.), pour vérification uniquement.
- Commandes (depuis la racine) : activer le venv (`.venv/Scripts/activate`), puis `farm --help`, `farm config check`, `farm job list`, `pytest`. Code dans `src/farm/` ; jobs dans `data/farm.db` (fait foi) + `jobs/<id>/` (non versionnés).
- Langue : docs et messages en français ; code et commentaires en anglais.
- Commits : pas de ligne `Co-Authored-By` ni d'autre mention d'attribution à Claude.
