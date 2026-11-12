# ROADMAP — Système d'agents IA de production vidéo

> Feuille de route uniquement. Le contexte et l'architecture sont dans `BRIEF.md` ; les décisions et questions ouvertes dans `docs/decisions.md`.
> Principe : passer à la phase suivante seulement quand les critères de sortie sont remplis.
> Mise à jour : 2026-11-11.

## Phase 0 — Décisions et compte (semaine 1)

- [x] Choisir la niche, la langue et le public cible
- [x] Décider : contenu public ou adulte
- [x] Rédiger la fiche persona (`personas/ai_girl/persona.md`)
- [x] Créer le compte Instagram (email dédié, 2FA), le passer en compte Business, le relier à une Page Facebook + Meta Business, activer le label "AI-generated profile"
- [x] Créer le compte TikTok, activer l'étiquetage IA
- [x] Chauffer les comptes à la main 1-2 semaines (bio, photo, quelques posts, interactions)

**Sortie :** décisions écrites dans `config/channels/ai_girl.yaml`.

## Phase 1 — Personnage (semaine 2)

- [x] Générer 20-30 images de référence avec Gemini (Nano Banana) : face, profil, 3/4, plein pied, 3-4 tenues
- [x] Vérifier à la main la cohérence du visage
- [x] Ranger les références dans `personas/ai_girl/refs/`

**Sortie :** fiche personnage validée.

## Phase 2 — Production manuelle assistée (semaines 3-4)

- [x] Produire 10 vidéos "à la main" : scénario avec un LLM, génération dans Gemini / Flow, montage simple
- [x] Publier à la main, noter les résultats
- [x] Identifier les 2-3 formats qui marchent le mieux

**Sortie :** 10 vidéos publiées, formats gagnants identifiés.

**Bilan (exports TikTok au 11 nov., `personas/ai_girl/analytics/`) :** 10 vidéos publiées du 7 au 9 nov. sur @lena.reyes_only. 7 vidéos entre 830 et 950 vues, les 3 du 9 nov. autour de 265-295 vues. 14 abonnés. Taux de likes ~5 %. Formats en tête : « Hi there » (portrait regard caméra, 60 likes), « tenue du jour » / « Which one 1, 2 or 3 ? », « five more minutes ». Un public féminin qui accroche.

**Niche pas encore validée** (décision du 9 nov. ; au 11 nov. : outfit of the day, « Hi there », cosplay… en test, contenu FR et EN en test). Méthode de test : `docs/decisions.md` §3. Critères, sur 3 semaines de publication quotidienne (à poursuivre à la main pendant la phase 3) :

- [ ] Au moins 30 % des vidéos dépassent 1 000 vues
- [ ] Au moins 50 nouveaux abonnés par semaine
- [ ] Durée de visionnage moyenne supérieure à 60 % sur les meilleurs formats

## Phase 3 — Squelette du moteur en mode manuel (semaines 4-6)

- [x] Ranger le projet : structure du BRIEF, `personas/`, `config/channels/`, images renommées (11 nov.)
- [x] Initialiser le repo git + GitHub, `.gitignore`, venv, FFmpeg, `.env.example`, tests (12 nov.)
- [x] Socle Python : package `farm`, CLI `farm`, chargement et validation des configs de chaîne et des règles (12 nov.)
- [x] Modèle de job + statuts + stockage SQLite, CLI `farm job new/list/show/status` (12 nov.)
- [ ] Interfaces `Provider` + providers `manual` (image, vidéo, publication)
- [ ] Agent Scénario (LLM)
- [ ] Montage FFmpeg (plans, sous-titres, musique)
- [ ] Agent Contrôle (vérifs automatiques) + validation humaine en ligne de commande (bot Telegram plus tard)
- [ ] Suivi du budget et arrêt d'urgence

**Premier cas réel : la série « Hi there »** (`personas/ai_girl/refs/prompts.md` §7) : tenue Pinterest → fiche tenue → prompt de changement de tenue → image → prompt d'animation → clip → prêt à publier.

**Sortie :** une vidéo passe de l'idée à "prête à publier" avec seulement les générations faites à la main.

## Phase 4 — Boucle complète (semaines 6-8)

- [ ] Agent Trends (TikTok Creative Center, Apify, concurrents)
- [ ] Agent Analyse (stats des plateformes → mémoire → ajustements)
- [ ] Agent Règles (veille hebdomadaire, propositions à valider)
- [ ] Agent Style (inspirations → fiches `outfits/*.yaml`)
- [ ] Rythme : 1 vidéo par jour

**Sortie :** 30 jours de publication quotidienne, données de performance exploitables.

## Phase 5 — Passage aux API payantes (si ça prend)

Critère de déclenchement : au moins un format avec un bon taux de visionnage et une croissance régulière des abonnés.

- [ ] Test à ~20 $ sur l'API pour comparer la qualité et vérifier l'enchaînement
- [ ] Brancher un provider vidéo API (`gemini-omni-1.1-flash` : les Veo en préversion ont été retirés de l'API le 22 oct. 2026 ; ou Kling, Seedance ; ou `wan_rented_gpu`)
- [ ] Brancher un provider image API (Nano Banana API ou Flux + LoRA)
- [ ] Publication automatique (Meta Graph API ou outil tiers ; TikTok via un outil audité)
- [ ] Monter à 2 puis 3 vidéos par jour si la qualité et le taux de visionnage tiennent
- [ ] Revoir le plafond de budget

## Phase 6 — Monétisation (mois 2-4)

- [ ] Liens d'affiliation dès le départ
- [ ] Liste email ou canal Telegram pour garder l'audience hors plateforme
- [ ] Offre d'abonnement si l'audience suit
- [ ] Premiers partenariats de marque vers 10 000 abonnés (mentions légales obligatoires)
- [ ] Pour viser TikTok Creator Rewards : un format de plus de 60 s (ex. une journée de Léna en plusieurs plans)

## Phase 7 — Nouvelles chaînes (mois 3+)

- [ ] Créer `config/channels/rain_youtube.yaml` (vidéos longues 16:9, sans persona)
- [ ] Vérifier que le moteur tourne sans modification du code
- [ ] Bilan à 90 jours par chaîne : garder, ajuster ou arrêter

## Piste parallèle — Héberger un modèle vidéo

Apprentissage en parallèle des phases 3-5, détail dans `docs/hebergement_gpu.md` : ComfyUI + Wan 2.2 sur la RTX 3050, puis Wan 14B sur un GPU loué, puis entraînement d'un LoRA de Léna. Débouché : providers `comfyui_local` et `wan_rented_gpu`.

## Points d'étape

| Quand | Question | Si non |
| --- | --- | --- |
| Fin de la phase 2 | Au moins un format accroche-t-il ? | Changer de niche ou de format avant de coder plus |
| Après 3 semaines de publication quotidienne | Les 3 critères de validation de la niche (phase 2) sont-ils remplis ? | Changer de niche ou de format |
| Mois 3 | Plus de 5 000 abonnés ou plus de 1 % d'engagement ? | Pivot de niche ou de format |
| Mois 6 | Les revenus couvrent-ils les coûts ? | Réduire la cadence, ou miser sur la vente du système (B2B) |
