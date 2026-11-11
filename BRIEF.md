# BRIEF — Système d'agents IA de production vidéo

> Document de référence pour l'IA qui code le projet. À lire avant toute tâche.
> Version : 2026-11-11 (fusion de BRIEF, infos, decision, modeles, hebergement_model).
>
> Carte de la doc :
> - `ROADMAP.md` : les phases et l'avancement.
> - `docs/decisions.md` : décisions prises, journal daté, **questions ouvertes et incohérences**.
> - `docs/recherche.md` : benchmark des outils, prix, monétisation, business model, sources.
> - `docs/hebergement_gpu.md` : héberger un modèle vidéo soi-même (RTX 3050, GPU loué, LoRA).
> - `personas/ai_girl/persona.md` : fiche persona (lue par les agents).
> - `personas/ai_girl/refs/prompts.md` : prompts de génération (images de référence, scènes, séries vidéo).
> - `config/channels/ai_girl.yaml` : config de la chaîne 1.
>
> Les prix et les règles des plateformes changent souvent : à revérifier avant chaque décision.

## 1. Objectif

Construire un **moteur d'agents IA modulaire** qui produit et publie des vidéos courtes sur plusieurs comptes ("chaînes").

- **Chaîne 1 :** influenceuse virtuelle (persona IA, adulte, 22-28 ans) : Léna Reyes, Instagram Reels + TikTok.
- **Chaînes suivantes :** vidéos longues d'ambiance (pluie) sur YouTube, autres concepts (ex. niche utile « astuces » ou « faits »).
- Le moteur est commun ; tout ce qui est propre à une chaîne vit dans un **fichier de config**. Aucune logique spécifique à une chaîne dans le code du moteur.

## 2. Contraintes fortes

1. **Budget quasi nul au départ.** Phase de test = offres gratuites + abonnement Google AI Pro (offre étudiante, gratuite), utilisé **à la main** : aucun abonnement Gemini / Flow ne donne accès à l'API. Le code doit donc supporter une **étape de génération manuelle** (voir §5).
2. **Fournisseurs interchangeables.** LLM, image, vidéo, voix, publication = adaptateurs derrière une interface commune, choisis dans la config. Passer de "manuel" à "API payante" = changer une ligne de config.
3. **Humain dans la boucle.** Validation obligatoire avant publication au début ; désactivable par chaîne plus tard (puis seulement quand l'agent Contrôle a un doute).
4. **Plafond de dépenses dur** par jour et par mois. **Arrêt d'urgence** automatique si le budget du jour est dépassé **ou si 2 publications d'affilée échouent**.
5. **Pas d'identifiants de compte dans le code.** On ne donne jamais un mot de passe à un bot (risque de bannissement). Publication uniquement via API officielle ou outil de publication tiers. Secrets dans `.env`, jamais commités.
6. **Conformité :** label IA obligatoire (Instagram "AI-generated profile", étiquette IA TikTok, AI Act art. 50), mention "Publicité" / "Collaboration commerciale" et "Image virtuelle" sur tout contenu commercial (loi influenceurs FR, 2023). Aucune ressemblance avec une personne réelle, aucune apparence juvénile, pas de faux avis ni de fausses promesses produits. Détail et sources : `docs/recherche.md` §3.

## 3. Architecture

```
            config/channels/<channel>.yaml   +   rules/<platform>.yaml
                              │
  ┌──────────┐   ┌───────────┐   ┌────────────┐   ┌──────────┐   ┌─────────────┐   ┌─────────┐
  │ 1 Trends │ → │ 2 Scénario│ → │ 3 Production│ → │ 4 Contrôle│ → │ 5 Publication│ → │ 6 Analyse│
  └──────────┘   └───────────┘   └────────────┘   └──────────┘   └─────────────┘   └─────────┘
        ↑                                    (+ validation humaine)                     │
        └───────────────────────── boucle d'apprentissage ──────────────────────────────┘
                              │
                 Mémoire partagée (SQLite au départ) : 1 ligne par vidéo
  7 Agent Règles (transversal, hebdomadaire) : maintient rules/*.yaml
  8 Agent Style (transversal, à la demande) : inspiration/inbox/ → outfits/*.yaml → refs/outfits/*.png
                                              └──────────► bibliothèque lue par l'agent Scénario
```

Chaque vidéo = un **job** (fichier JSON + dossier d'assets) qui passe d'étape en étape. Statuts : `idea → scripted → awaiting_assets → produced → in_review → approved → published → analyzed` (+ `rejected`, `failed`).

**Principes :**

- **Chaque agent = un module indépendant** avec une entrée et une sortie claires (le JSON du job). On peut en remplacer un sans toucher aux autres.
- **Une étape peut être sautée ou faite à la main** : la chaîne pluie n'a pas besoin de l'agent Trends au quotidien, ni de fiche personnage.
- **Chaque vidéo est tracée** : idée d'origine, prompts utilisés, modèle, coût, statut, résultats. Indispensable pour apprendre et maîtriser le budget.
- La **mémoire partagée** permet à l'agent Analyse de dire aux autres ce qui a marché.

## 4. Les agents (entrées / sorties)

| Agent | Entrée | Sortie | Notes |
| --- | --- | --- | --- |
| 1 Trends | config chaîne, historique des résultats | 5 idées classées / jour (JSON) | Sources : TikTok Creative Center, scrapers Apify (branchables via MCP), comptes concurrents listés dans la config. Optionnel par chaîne. |
| 2 Scénario | idée, fiche persona, règles, bibliothèque de tenues | script, liste de plans, prompts image/vidéo, texte à l'écran, légende, hashtags | Respecte la durée et le format de la plateforme. |
| 3 Production | prompts, images de référence du personnage | vidéo finale 9:16 (ou 16:9) | Image de réf. → image de scène → vidéo (image-to-video) → montage FFmpeg (plans, texte à l'écran ; musique selon `format.music` : ajoutée dans l'app au moment de publier pour la chaîne 1). |
| 4 Contrôle | vidéo, légende, règles | `approved` / `rejected` + motifs | Vérifs : format, durée, cohérence du visage, texte, labels, mots interdits, lignes rouges de la persona. Puis envoi à l'humain : validation en ligne de commande au départ, bot Telegram (Valider / Refaire) plus tard. Blocage et alerte si doute. |
| 5 Publication | vidéo approuvée, légende | URL du post | Contraintes par plateforme : §7. Heure de publication optimale. |
| 6 Analyse | stats plateformes | rapport + ajustements pour 1 et 2 | Vues, temps de visionnage, partages, sauvegardes, abonnés gagnés, coût par vidéo. Vérifie aussi chaque trimestre les règles de monétisation des plateformes cibles. |
| 7 Règles | pages officielles des plateformes | propositions de modif de `rules/*.yaml` | Hebdomadaire. **Ne modifie rien seul** : propose, l'humain valide. |
| 8 Style | captures d'inspiration déposées dans `inspiration/inbox/` | une fiche `outfits/<id>.yaml` par tenue + image studio de la persona dans cette tenue | Décrit **uniquement la tenue** (jamais la personne). Voir §6. |

**Agent Scénario — choix de la tenue :** il choisit une tenue dans `outfits/` en respectant la catégorie de la scène (sport, travail, soirée…), le public visé par le format et le dosage de contenu de la chaîne (`spicy_mix`). Il injecte le champ `prompt` de la fiche dans le prompt de scène et joint `ref_image` comme référence.

**Règle d'accroche (agents Scénario et Contrôle) :** les 3 premières secondes de chaque vidéo doivent accrocher. Dès la première image, le visage de la persona est visible, tourné vers la caméra, avec un regard ou un sourire. Jamais d'ouverture de dos, de cadre vide ou de longue mise en place. Si le format repose sur une révélation (entrée dans une pièce, changement de tenue…), on ouvre sur un flash de 0,5 à 1 s du plan final, puis on revient au début. Le Contrôle rejette une vidéo dont la première seconde ne montre pas le visage.

**Agent Analyse — audience :** il suit aussi la **répartition hommes / femmes** de l'audience et les performances par format et par public visé, pour orienter le choix des formats.

**Agent Règles — détail :**

- **Veille hebdomadaire :** relit les pages officielles (règles Instagram, TikTok, YouTube, Fanvue, AI Act, loi influenceurs) et signale tout changement. Les règles des plateformes ont changé plusieurs fois en 2026 ; sans cet agent, le système se met en infraction sans le savoir.
- **Un fichier de règles par plateforme** (`rules/<platform>.yaml`) : format, durée, labels IA obligatoires, mentions "Publicité" / "Image virtuelle", sujets interdits, lignes rouges fixées par l'humain.
- **Il propose, l'humain valide** : évite qu'un agent assouplisse ses propres limites.
- **Limite :** ce n'est pas un juriste. Avant le premier partenariat payant ou toute activité adulte, faire valider par un professionnel.

## 5. Mode manuel (phase de test)

L'abonnement Google AI Pro ne donne pas d'API : la génération image/vidéo se fait à la main dans l'app Gemini ou Google Flow.

Répartition des rôles :
- **Le système** génère les prompts, choisit les tenues, écrit les textes à l'écran et les légendes ; puis monte (texte, musique, coupe), range et prépare la publication.
- **L'humain** génère images et vidéos dans Gemini et Flow, puis les dépose dans un dossier.

Le provider `manual` doit :
1. écrire les prompts dans `jobs/<id>/prompts.md` (prêts à copier-coller) ;
2. passer le job en `awaiting_assets` et notifier l'humain ;
3. surveiller `jobs/<id>/inbox/` ; dès que les fichiers attendus y sont déposés, reprendre le pipeline (montage, contrôle, etc.).

Même logique pour la publication (`publisher: manual` = prépare vidéo + légende + hashtags, l'humain poste). Pour TikTok, mode **semi-automatique** : l'humain programme la semaine dans TikTok Studio (~15 min / semaine).

**Quel modèle utiliser dans Flow** (à indiquer dans `prompts.md`) :

| Modèle | À utiliser pour | Coût en crédits Flow |
| --- | --- | --- |
| Veo 3.1 Lite | Brouillons : vérifier qu'un mouvement fonctionne | Le moins cher |
| Veo 3.1 Fast | Vidéos du quotidien : bon réalisme pour un coût raisonnable | ~20 crédits par génération (source tierce) |
| Veo 3.1 Quality | Vidéo finale d'un plan déjà validé avec Fast | ~100 crédits par génération (même source) |
| Omni 1.1 Flash | Combiner plusieurs images de référence (Léna + chien + décor) ou modifier une vidéo existante | À vérifier dans Flow |

Étape suivante prévue : un test à ~20 $ sur l'API pour comparer la qualité et vérifier l'enchaînement automatique (voir §9).

## 6. Bibliothèque de tenues (agent Style)

**Pourquoi :** les tenues décrites à la main sont trop génériques. L'humain collecte des inspirations réelles (Instagram, Pinterest), l'agent Style les transforme en fiches réutilisables.

**Règle absolue :** une photo d'inspiration montre une **vraie personne**. Elle n'est **jamais** jointe à une génération d'image ou de vidéo (risque de reprendre son visage, blocage « personnalité » de Flow). Seule la **description texte** de la tenue est utilisée.

**Fonctionnement :**
1. L'humain dépose une capture dans `inspiration/inbox/`.
2. L'agent Style l'envoie au LLM multimodal avec le prompt ci-dessous.
3. Il crée `outfits/<id>.yaml` et déplace la capture dans `inspiration/archive/`.
4. Il prépare (ou génère, selon le provider) l'image studio de la persona dans la tenue → `personas/<channel>/refs/outfits/<id>.png`, statut `awaiting_validation` jusqu'à validation humaine.

**Prompt de description (vision) :**

```
Describe ONLY the outfit worn in this image, for use in an image-generation prompt. Ignore the person entirely: no face, hair, body, skin, pose or background. List each garment with its exact color, fabric, cut, fit, length and details (trim, straps, seams, texture), then shoes and accessories. Output one single English line starting with "wearing", plus a short list of 2-3 palette colors and a category (sport, casual, work, evening, lounge). If brands or logos are visible, do not mention them.
```

**Format d'une fiche :**

```yaml
# outfits/cream_pilates_set.yaml
id: cream_pilates_set
category: sport            # sport | casual | work | evening | lounge
palette: [cream, black]
prompt: >
  wearing a cream sports bra with thin black contrast trim and spaghetti straps,
  high-waisted cream ribbed flared lounge pants, grey socks, a thin gold ring
audience: female           # female | male | both
spicy_level: 1             # 0 = sage, 1 = séduisant, 2 = osé
source: inspiration/archive/2026-11-08_pilates.jpg
shop_link: ""              # lien d'affiliation vers une pièce similaire (rempli par l'humain)
ref_image: personas/ai_girl/refs/outfits/cream_pilates_set.png
status: validated          # awaiting_validation | validated | retired
used_count: 0              # mis à jour à chaque utilisation, pour éviter les répétitions
```

**Règles de choix (agent Scénario) :**
- Ne pas réutiliser la même tenue plus d'une fois sur 7 jours glissants.
- Respecter le dosage `spicy_mix` de la chaîne (ex. 70 % niveau 0-1, 30 % niveau 2).
- Bas et jupes : toujours ajouter « thick opaque fabric » dans le prompt.
- Pas de vêtement moulant couleur peau (beige, nude, sable) : les modérations automatiques le prennent pour de la nudité. Pour un legging ou une brassière, préférer le noir, le marine, le gris foncé, le bordeaux ou le vert.
- Cadrage : le bas de l'image ne doit jamais couper au niveau de l'entrejambe. On cadre au-dessus de la taille ou en pied entier.
- Si `shop_link` est rempli, proposer une légende qui le mentionne (avec la mention « Publicité » si le lien est affilié).

## 7. Configs de chaîne et contraintes des plateformes

### Configs

La config de référence de la chaîne 1 est `config/channels/ai_girl.yaml`. Elle n'est pas recopiée ici pour éviter les versions divergentes. Champs clés : plateformes, format, cadence, agents actifs, `human_review`, providers et leurs réglages, budget, trends, conformité, légendes, `outfits_dir`, `spicy_mix`, `audience_targets`.

Chaîne 2 (plus tard), pour vérifier que le moteur n'est pas rigide :

| Champ | Chaîne 1 : IA-girl | Chaîne 2 : pluie |
| --- | --- | --- |
| Plateforme | Instagram Reels + TikTok | YouTube (vidéos longues) |
| Format | 9:16, 8-30 s | 16:9, 1-10 h |
| Rythme | 1/jour, puis 2-3/jour | 2-3/semaine |
| Persona | Fiche personnage + images de référence | Aucune |
| Agents actifs | Les 6 | Scénario, Production, Contrôle, Publication, Analyse |
| Modèle vidéo | Manuel (Flow), puis API (suggestion initiale : Kling 3.0 ou Veo 3.1 Fast) | Boucle courte générée puis répétée au montage |
| Audio | Son tendance ajouté dans l'app TikTok/Instagram au moment de publier | Sons de pluie libres de droits ou générés |
| Validation humaine | Oui | Oui |

⚠ Chaîne pluie : YouTube exclut de la monétisation le contenu "inauthentique" (vidéos génériques, répétitives, produites en masse). Chaque vidéo doit avoir une valeur propre : ambiances distinctes, séries thématiques, visuels soignés, apport humain visible.

### Instagram (Reels)

- Publication par API uniquement avec un **compte professionnel Business** (pas Creator), relié à une Page Facebook et à un compte Meta Business.
- Deux voies : **Meta Graph API** (gratuit, contrôle total, mais revue de l'app par Meta ~2-4 semaines et vidéo à héberger sur une **URL publique**) ou **outil tiers avec API** (Postproxy, Publora, bundle.social, Metricool, Buffer… : immédiat, mais abonnement et dépendance). Recommandation : outil tiers pour démarrer, API officielle quand le projet tient.
- Max **100 publications API sur 24 h glissantes** par compte.
- **Pas de musique de la bibliothèque Instagram via l'API** (ni sons tendance, ni catalogue) : musique libre de droits intégrée au fichier, ou publication manuelle des Reels sur un son tendance (choix actuel de la chaîne 1 : son ajouté dans l'app).
- Format Reels : 9:16, **5 à 90 s**, MP4/MOV H.264, **100 Mo max**. En dehors, la vidéo est publiée comme simple post vidéo.
- Légende : 2 200 caractères maximum (la config vise 300 : les légendes courtes marchent mieux).
- Label "AI-generated profile" obligatoire depuis le 31 août 2026, sinon portée limitée.
- Un compte neuf qui publie plusieurs Reels/jour par API paraît suspect : chauffer à la main d'abord (fait en phase 0).

### TikTok

- **API officielle :** tant que l'application n'a pas passé l'audit de TikTok, toutes les publications restent **privées**. Une application à usage interne ne passe pas cet audit.
- Donc : **semi-automatique maintenant** (le système prépare vidéo, légende, hashtags ; l'humain programme la semaine dans TikTok Studio, gratuit) ; **outil tiers déjà audité** (ex. Blotato) quand le volume le justifie (abonnement, publication publique dès le premier envoi).
- Étiquetage IA obligatoire pour le contenu IA réaliste.
- Creator Rewards ne paie que les vidéos de **plus de 60 s** (détail : `docs/recherche.md`).

## 8. Stack et structure du repo

- **Python 3.11+**, un module par agent, une interface `Provider` par type (llm, image, video, voice, publisher, notifier).
- **Orchestration :** script CLI + planificateur (cron / APScheduler) au départ ; n8n possible plus tard.
- **Stockage :** SQLite + dossiers `jobs/` ; Google Sheets en export lecture seule si utile.
- **Montage :** FFmpeg.
- **Notifications / validation :** ligne de commande au départ ; bot Telegram plus tard.
- **Logs :** chaque appel de provider enregistre modèle, prompt, coût, durée.

Structure de repo proposée :

```
config/channels/   personas/   rules/   jobs/   outfits/   inspiration/{inbox,archive,ideas}/   workflows/
src/agents/   src/providers/{llm,image,video,voice,publisher}/   src/core/{pipeline,budget,storage,notify}/
tests/   docs/   .env.example   CLAUDE.md   BRIEF.md   ROADMAP.md
```


## 9. Fournisseurs à prévoir (à brancher plus tard)

- **LLM :** Claude, OpenAI, Gemini (API). Rôle de "cerveau" uniquement : Claude ne génère ni images ni vidéos.
- **Image :** Nano Banana (API Gemini), Flux + LoRA (fal.ai / Replicate), `comfyui_local`.
- **Vidéo :**
  - API Gemini : `gemini-omni-1.1-flash` (~0,10 $/s en 720p, ~0,80 $ le clip de 8 s, ~25-50 $ pour 30 vidéos/mois avec un essai raté). Il **remplace les modèles Veo en préversion, retirés de l'API le 22 octobre 2026** : la mention "Veo 3.1 API" est donc à revérifier avant de coder `veo_api`.
  - Kling 3.0, Seedance 2.0 (via fal.ai ou équivalent).
  - Auto-hébergé : `comfyui_local` (ComfyUI + Wan 2.2 sur la RTX 3050) et `wan_rented_gpu` (RunPod / Vast, RTX 4090, arrêt auto). Client Python de l'API HTTP ComfyUI (`/prompt` + récupération des sorties). Détail : `docs/hebergement_gpu.md`.
  - Sora : fermé (app arrêtée en avril 2026, API le 24 septembre 2026), ne pas intégrer.
- **Agrégateurs :** fal.ai, Replicate, OpenRouter (une seule clé API et une seule facture).
- **Voix (plus tard) :** ElevenLabs (une voix figée). Lip-sync : Veo / Seedance génèrent l'audio ; sinon HeyGen ou Hedra.
- **Publication :** Meta Graph API (compte Business + app validée), outil tiers avec API, TikTok Studio (semi-auto), outil TikTok audité (Blotato).
- **Trends :** Apify (scrapers Instagram / TikTok, ~2 $ / 1 000 résultats), TikTok Creative Center, Google Trends.

## 10. Décisions encore ouvertes (ne pas inventer : demander)

La liste à jour est dans `docs/decisions.md` (section « Questions ouvertes »). Ne rien inventer sur ces points.

## 11. Règles de code

- Commentaires de code en anglais ; docs et messages utilisateur en français.
- Aucun secret dans le repo ; `.env.example` à jour.
- Chaque agent testable seul avec un job factice.
- Commencer petit : pipeline de bout en bout en mode `manual` avant tout provider payant.
