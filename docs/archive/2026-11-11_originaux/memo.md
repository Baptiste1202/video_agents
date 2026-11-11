# MEMO — Idées et infos clés du projet

> Notes de travail au 2026-11-05. Contexte complet : `BRIEF.md` ; étapes : `ROADMAP.md`.
> Les prix et les règles des plateformes changent souvent : à revérifier avant chaque décision.

[identifiants déplacés dans SECRETS.local.md à la racine]


## Phase 3 — Squelette du moteur en mode manuel (semaines 4-6)
 
- [ ] Initialiser le repo (structure du BRIEF, `.env.example`, tests)
- [ ] Modèle de job + statuts + stockage SQLite
- [ ] Chargement des configs de chaîne et des règles
- [ ] Interfaces `Provider` + providers `manual` (image, vidéo, publication)
- [ ] Agent Scénario (LLM)
- [ ] Montage FFmpeg (plans, sous-titres, musique)
- [ ] Agent Contrôle (vérifs automatiques) + bot Telegram de validation
- [ ] Suivi du budget et arrêt d'urgence
**Sortie :** une vidéo passe de l'idée à "prête à publier" avec seulement les générations faites à la main.
 
## Phase 4 — Boucle complète (semaines 6-8)
 
- [ ] Agent Trends (TikTok Creative Center, Apify, concurrents)
- [ ] Agent Analyse (stats des plateformes → mémoire → ajustements)
- [ ] Agent Règles (veille hebdomadaire, propositions à valider)
- [ ] Rythme : 1 vidéo par jour
**Sortie :** 30 jours de publication quotidienne, données de performance exploitables.
 
## Phase 5 — Passage aux API payantes (si ça prend)
 
Critère de déclenchement : au moins un format avec un bon taux de visionnage et une croissance régulière des abonnés.
 
- [ ] Brancher un provider vidéo API (Veo 3.1 Fast/Lite, Kling ou Seedance)
- [ ] Brancher un provider image API (Nano Banana API ou Flux + LoRA)
- [ ] Publication automatique (Meta Graph API ou outil tiers)
- [ ] Monter à 2 puis 3 vidéos par jour si la qualité tient
- [ ] Revoir le plafond de budget
## Phase 6 — Monétisation (mois 2-4)
 
- [ ] Liens d'affiliation dès le départ
- [ ] Liste email ou canal Telegram pour garder l'audience hors plateforme
- [ ] Offre d'abonnement si l'audience suit
- [ ] Premiers partenariats de marque vers 10 000 abonnés (mentions légales obligatoires)
## Phase 7 — Nouvelles chaînes (mois 3+)
 
- [ ] Créer `config/channels/rain_youtube.yaml` (vidéos longues 16:9, sans persona)
- [ ] Vérifier que le moteur tourne sans modification du code
- [ ] Bilan à 90 jours par chaîne : garder, ajuster ou arrêter
## Points d'étape
 
| Quand | Question | Si non |
| --- | --- | --- |
| Fin de la phase 2 | Au moins un format accroche-t-il ? | Changer de niche ou de format avant de coder plus |
| Mois 3 | Plus de 5 000 abonnés ou plus de 1 % d'engagement ? | Pivot de niche ou de format |
| Mois 6 | Les revenus couvrent-ils les coûts ? | Réduire la cadence, ou miser sur la vente du système (B2B) |
 
