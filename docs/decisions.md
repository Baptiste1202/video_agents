# Décisions — Léna Reyes / moteur d'agents

> Ce qui est décidé, quand et pourquoi, et ce qui reste à trancher.
> Contexte : `BRIEF.md` ; étapes : `ROADMAP.md` ; recherche et chiffres : `docs/recherche.md`.

## 1. Tableau des décisions

Grille issue du brief initial (5 nov.) : une IA qui construit le système sans ces réponses va les inventer.

| Sujet | Question | Suggestion initiale (5 nov.) | État au 11 nov. |
| --- | --- | --- | --- |
| Persona | Nom, âge (clairement adulte, 22-28 ans), nationalité, personnalité, ton, histoire | Une fiche d'1 page, figée, lue par tous les agents | ✅ Léna Reyes, 24 ans : `personas/ai_girl/persona.md` ; prompt de base = BASE 3 ; chien = Praline (cocker) |
| Niche | De quoi parle-t-elle ? "Jolie fille" seul n'est pas une niche | 1 niche monétisable : fitness, mode, voyage, beauté, gaming, lifestyle tech… | 🧪 **En test** (11 nov.) : outfit of the day, « Hi there », cosplay, fitness, Paris life. Méthode : §3 |
| Langue et audience | FR, EN ou les deux ? Quel pays ? | Anglais pour la portée, ou FR pour une niche moins saturée | 🧪 **En test** : audience à ~60 % française ; on compare FR et EN |
| Public ou adulte | Tout public ou renvoi vers de l'adulte ? Change plateformes, providers, règles | Rester dans les règles Instagram | ✅ Public (persona §7, `content_rating: public`). Tout contenu adulte = chaîne et comptes séparés, jamais liés |
| Monétisation | Comment, à partir de combien d'abonnés ? | Affiliation dès le début, partenariats après 10k | 🟡 Plan dans la persona §7 ; mode prioritaire encore ouvert |
| Ligne rouge contenu | Jusqu'où vont tenues et suggestivité ? | Rester dans les règles Instagram, écrit noir sur blanc pour le Contrôle | ✅ ~30 % de contenu osé (niveau 2), dans les règles des plateformes : persona §8 |
| Formats vidéo | Face caméra qui parle ? Plans esthétiques + texte ? Tendances ? | Plans esthétiques + texte + musique | ✅ Persona §5 ; « Hi there » = meilleur format, première série automatisée |
| Voix | Elle parle ? | Pas de voix au début ; voix clonée fixe (ElevenLabs) ensuite | ✅ Pas de voix au départ |
| Validation humaine | Quelles étapes passent par toi ? | Validation finale le 1er mois, puis sur alerte | ✅ `human_review: required`, en ligne de commande (Telegram plus tard) |
| Budget | Combien par mois, plafond ? | 50 €/mois en test, plafond dur dans le code | ✅ 2 $/jour, 50 $/mois (`ai_girl.yaml`). Plafond global de pilotage : 250 €/mois |
| KPI de succès | Qu'est-ce qui dit que ça marche à 30 et 90 jours ? | Taux de visionnage complet, partages, abonnés gagnés par vidéo | ✅ Critères du 9 nov. (§3) + points d'étape de la ROADMAP |
| Statut juridique | Qui encaisse l'argent ? | Micro-entreprise [à vérifier avec un comptable] | ❓ Ouvert |
| Hébergement | Où tourne le système ? | Le PC au début, puis petit serveur ou n8n cloud | ✅ PC local, hors OneDrive ; code sur GitHub, dépôt **public** (choix du 12 nov.). Serveur : plus tard. GPU : `docs/hebergement_gpu.md` |
| Musique | D'où vient-elle ? | Libre de droits, intégrée au fichier | ✅ Son tendance ajouté dans l'app TikTok au moment de publier ; le pipeline sort des vidéos muettes |
| LLM | Quel cerveau pour les agents ? | Claude par API | ✅ Claude par API (clé disponible ; facturée à part de l'abonnement claude.ai) |

## 2. Journal

### 2026-11-05 — Brief initial

Les 7 challenges sur la note de départ (détail dans `docs/recherche.md` §1) : commencer à 1 vidéo/jour, Claude = cerveau et pas générateur, Instagram ne paie pas à la vue, label IA obligatoire, jamais d'identifiants donnés à un bot, pas de musique Instagram via API, "gratuit" tient pour le prototype seulement.

### 2026-11-08 — BRIEF v2

Ajout de l'agent Style (bibliothèque de tenues), de la règle d'accroche des 3 premières secondes, du suivi hommes/femmes par l'agent Analyse.

### 2026-11-09 — Passage à l'automatisation

En résumé : on garde l'offre Gemini étudiante, on produit en mode manuel assisté, on publie TikTok en semi-automatique, et la niche n'est pas encore validée.

1. **Passer à Claude Code : oui.** La conversation ne se transfère pas, mais l'essentiel est dans les fichiers. Mettre BRIEF.md, ROADMAP.md, memo.md, persona.md et ai_girl.yaml dans le dossier VS Code aux emplacements prévus ; créer `CLAUDE.md` (« Lis BRIEF.md et ROADMAP.md avant toute tâche ») ; premier message : « On attaque la phase 3 de ROADMAP.md : squelette du moteur en mode manuel. Propose-moi un plan avant de coder. »
2. **Louer de la RAM ou du CPU : non.** La génération vidéo tourne sur la carte graphique (VRAM), pas sur le processeur. Il faudrait louer un GPU (RTX 4090 à ~0,35 $/h), mais à ce stade l'installation est lourde et la qualité inférieure à Google. (Repris ensuite comme piste d'apprentissage : `docs/hebergement_gpu.md`.)
3. **Abonnement Flow plus cher : non.** L'offre étudiante Pro est gratuite : on la garde pour produire à la main. L'offre Ultra coûte 100 $/mois ou plus. Aucun abonnement ne donne accès à l'API, celle dont les agents ont besoin.

   | Modèle API | Prix | Clip de 8 s | 30 vidéos / mois (avec un essai raté) |
   | --- | --- | --- | --- |
   | `gemini-omni-1.1-flash` (remplace les Veo en préversion, retirés le 22 octobre 2026) | ~0,10 $/s en 720p | ~0,80 $ | ~25 à 50 $ |

4. **Automatiser la publication TikTok.** Avec l'API officielle, tant que l'application n'a pas passé l'audit de TikTok, toutes les publications restent privées ; une application à usage interne ne passe pas cet audit.

   | Option | Coût | Quand |
   | --- | --- | --- |
   | Semi-automatique : le système prépare vidéo, légende et hashtags ; programmation de la semaine dans TikTok Studio (15 min) | Gratuit | Maintenant |
   | Outil tiers déjà audité par TikTok, publication publique dès le premier envoi | Abonnement | Quand le volume le justifie |

5. **Rémunération à la vue : un complément, pas un modèle.** Creator Rewards ne paie que les vidéos de plus d'une minute, à partir de 10 000 abonnés et 100 000 vues sur 30 jours, avec du contenu original. Les clips de 8 s ne rapportent rien. France : ~0,60 $ pour 1 000 vues qualifiées, soit ~600 $ pour 1 million de vues par mois. Meilleure piste : vendre le système à d'autres créateurs. Pour viser Creator Rewards, il faut un format de plus de 60 s (ex. une journée de Léna en plusieurs plans).
6. **Produire sans API payante : le mode manuel.** Le système génère les prompts, choisit les tenues, écrit les textes à l'écran et les légendes. L'humain génère images et vidéos dans Gemini et Flow, puis les dépose dans un dossier. Le système monte (texte, musique, coupe), range et prépare la publication. Étape suivante : un test à 20 $ sur l'API pour comparer la qualité et vérifier l'enchaînement.
7. **La niche n'est pas encore validée.** État : 8 abonnés, 900 vues au maximum. Signaux encourageants : 5 % de likes, un public féminin qui accroche, le format « tenue du jour » devant. Critères de validation : voir §3.

Sources du 9 nov. : Developers Digest (modèles vidéo de l'API Gemini et dates de retrait), Layer3 Labs (prix de Veo et `gemini-omni-1.1-flash`), TikTok for Developers (Direct Post et clients non audités), Ayrshare (audit de l'API TikTok), Blotato (outil de publication TikTok audité), TT Calculator (conditions de Creator Rewards).

### 2026-11-09 — Héberger un modèle vidéo

La RTX 3050 sert de banc d'essai pour apprendre toute la chaîne ; le GPU loué prend le relais pour les gros modèles et l'entraînement. Détail : `docs/hebergement_gpu.md`.

### 2026-11-11 — Fusion de la doc et arbitrages

- Doc fusionnée (8 notes → `BRIEF`, `ROADMAP`, `docs/`), assets rangés et renommés (`personas/`, `inspiration/`, `config/channels/`), identifiants sortis dans `SECRETS.local.md`.
- Niche et langue restent **en test** ; contenu osé ~30 % ; chien = Praline ; prompt de base = BASE 3 ; musique ajoutée dans l'app ; Telegram reporté ; projet déplacé hors OneDrive + dépôt GitHub privé.
- Première série à automatiser : **« Hi there »** (image de base fixe, tenues Pinterest, animation avec variantes).

### 2026-11-12 — Outils

- LLM : **Claude Opus 5.5** par API (`claude-opus-5-5`, effort `medium`).
- Prompt de base : **BASE 3 gardé tel quel** pour l'instant (y compris « fresh youthful face », à surveiller).
- FFmpeg 9.0.2 installé (winget). Dépôt GitHub : `Baptiste1202/video_agents`.
- Le dépôt **reste public** (choix de l'utilisateur ; il contient la doc, les refs de la persona et les exports d'analytics, jamais les identifiants ni `inspiration/`). Remplace « dépôt privé » du 11 nov.
- Jobs : **SQLite fait foi** (`data/farm.db`, une ligne par vidéo avec la fiche complète en JSON) ; `jobs/<id>/job.json` en est une copie lisible, réécrite à chaque sauvegarde ; dépôts manuels dans `jobs/<id>/inbox/`. Id : `<AAAAMMJJ>-<chaîne>-<NNN>`. Chaque changement de statut est tracé (date, motif, forcé ou non) ; un passage hors circuit demande `--force`.

## 3. Critères de validation de la niche

Sur 3 semaines de publication quotidienne :

- [ ] Au moins 30 % des vidéos dépassent 1 000 vues
- [ ] Au moins 50 nouveaux abonnés par semaine
- [ ] Durée de visionnage moyenne supérieure à 60 % sur les meilleurs formats

**Comment savoir qu'une niche a pris (méthode de test) :**

1. **Étiqueter chaque vidéo** (le job le fera automatiquement) : niche, format/série, langue (FR/EN), niveau de contenu (0-1-2), heure de publication.
2. **Comparer par lots** : au moins 8-10 vidéos par niche avant de conclure ; une vidéo seule ne dit rien (l'algorithme est très variable).
3. **Regarder les bons indicateurs**, dans cet ordre :
   - **Taux de visionnage complet / durée moyenne** : le signal que l'algorithme regarde en premier. Sur un clip de 8 s, viser > 60-70 %.
   - **Abonnés gagnés pour 1 000 vues** : c'est lui qui dit si les gens veulent *revoir* Léna, pas juste regarder une fois.
   - **Partages et sauvegardes pour 1 000 vues** : signal fort de valeur.
   - Les vues brutes viennent en dernier (elles dépendent beaucoup du hasard de la distribution).
4. **Une niche « prend »** quand, sur son lot, la médiane des vues monte d'un lot à l'autre (pas seulement un pic), que les abonnés/1 000 vues dépassent nettement les autres niches, et que les vues des vidéos suivantes restent hautes (l'audience revient). On garde les 1-2 meilleures, on coupe le reste.
5. **Même logique pour la langue** : alterner FR et EN sur une même série (ex. « Hi there ») pour que seule la langue change.

## 4. Questions ouvertes et incohérences

> Relevées lors de la fusion des docs le 11 nov. À trancher par l'humain : l'IA ne doit pas choisir à sa place.

### Décisions encore ouvertes

- Mode de monétisation prioritaire.
- Hébergement final : PC local pour l'instant ; serveur à décider plus tard.
- Statut juridique (micro-entreprise ?).
- Lien en bio (`link_in_bio`) et liste des 10-20 comptes concurrents (`competitors`).

### Incohérences entre les fichiers

Relevées le 11 nov. et **toutes tranchées le jour même** : niche et langue en test (pas une incohérence mais une phase), audience qui suit la niche, ~30 % de contenu osé, chien = Praline, prompt de base = BASE 3, images renommées, dossier `personas/`, config dans `config/channels/`, `gemini-omni-1.1-flash` pour l'API vidéo (Veo 3.1 reste dans Flow). Détail dans `docs/archive/` si besoin.

Point d'attention restant : BASE 3 contient « fresh youthful face », à surveiller face à la ligne rouge « jamais d'apparence juvénile » (persona §8).
