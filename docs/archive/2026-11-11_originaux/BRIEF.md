# BRIEF — Système d'agents IA de production vidéo
 
> Document de référence pour l'IA qui code le projet. À lire avant toute tâche.
> Version : 2026-11-08. La feuille de route est dans `ROADMAP.md`.
 
## 1. Objectif
 
Construire un **moteur d'agents IA modulaire** qui produit et publie des vidéos courtes sur plusieurs comptes ("chaînes").
 
- **Chaîne 1 :** influenceuse virtuelle (persona IA, adulte, 22-28 ans), Instagram Reels + TikTok.
- **Chaînes suivantes :** vidéos longues d'ambiance (pluie) sur YouTube, autres concepts.
- Le moteur est commun ; tout ce qui est propre à une chaîne vit dans un **fichier de config**. Aucune logique spécifique à une chaîne dans le code du moteur.
## 2. Contraintes fortes
 
1. **Budget quasi nul au départ.** Phase de test = offres gratuites + abonnement Google AI Pro (étudiant), utilisé **à la main** (pas d'API incluse). Le code doit donc supporter une **étape de génération manuelle** (voir §5).
2. **Fournisseurs interchangeables.** LLM, image, vidéo, voix, publication = adaptateurs derrière une interface commune, choisis dans la config. Passer de "manuel" à "API payante" = changer une ligne de config.
3. **Humain dans la boucle.** Validation obligatoire avant publication au début ; désactivable par chaîne plus tard.
4. **Plafond de dépenses dur** par jour et par mois. Arrêt automatique si dépassé.
5. **Pas d'identifiants de compte dans le code.** Publication uniquement via API officielle ou outil de publication tiers. Secrets dans `.env`, jamais commités.
6. **Conformité :** label IA obligatoire (Instagram "AI-generated profile", étiquette IA TikTok, AI Act art. 50), mention "Publicité" / "Image virtuelle" sur tout contenu commercial (loi influenceurs FR). Aucune ressemblance avec une personne réelle, aucune apparence juvénile.
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
 
## 4. Les agents (entrées / sorties)
 
| Agent | Entrée | Sortie | Notes |
| --- | --- | --- | --- |
| 1 Trends | config chaîne, historique des résultats | 5 idées classées / jour (JSON) | Sources : TikTok Creative Center, scrapers Apify, comptes concurrents listés dans la config. Optionnel par chaîne. |
| 2 Scénario | idée, fiche persona, règles | script, liste de plans, prompts image/vidéo, texte à l'écran, légende, hashtags | Respecte la durée et le format de la plateforme. |
| 3 Production | prompts, images de référence du personnage | vidéo finale 9:16 (ou 16:9) | Image de réf. → image de scène → vidéo (image-to-video) → montage FFmpeg (plans, sous-titres, musique libre de droits intégrée au fichier). |
| 4 Contrôle | vidéo, légende, règles | `approved` / `rejected` + motifs | Vérifs : format, durée, cohérence du visage, texte, labels, mots interdits. Puis envoi à l'humain (bot Telegram : Valider / Refaire). |
| 5 Publication | vidéo approuvée, légende | URL du post | Instagram : compte Business, vidéo sur URL publique, max 100 posts API / 24 h, **pas de musique Instagram via API**. Heure de publication optimale. |
| 6 Analyse | stats plateformes | rapport + ajustements pour 1 et 2 | Vues, temps de visionnage, partages, sauvegardes, abonnés gagnés, coût par vidéo. |
| 7 Règles | pages officielles des plateformes | propositions de modif de `rules/*.yaml` | Hebdomadaire. **Ne modifie rien seul** : propose, l'humain valide. |
| 8 Style | captures d'inspiration déposées dans `inspiration/inbox/` | une fiche `outfits/<id>.yaml` par tenue + image studio de la persona dans cette tenue | Décrit **uniquement la tenue** (jamais la personne). Voir §6 bis. |
 
**Ajout à l'agent Scénario :** il choisit une tenue dans `outfits/` en respectant la catégorie de la scène (sport, travail, soirée…), le public visé par le format et le dosage de contenu de la chaîne (`spicy_mix`). Il injecte le champ `prompt` de la fiche dans le prompt de scène et joint `ref_image` comme référence.
 
**Règle d'accroche (agents Scénario et Contrôle) :** les 3 premières secondes de chaque vidéo doivent accrocher. Dès la première image, le visage de la persona est visible, tourné vers la caméra, avec un regard ou un sourire. Jamais d'ouverture de dos, de cadre vide ou de longue mise en place. Si le format repose sur une révélation (entrée dans une pièce, changement de tenue…), on ouvre sur un flash de 0,5 à 1 s du plan final, puis on revient au début. Le Contrôle rejette une vidéo dont la première seconde ne montre pas le visage.
 
**Ajout à l'agent Analyse :** il suit aussi la **répartition hommes / femmes** de l'audience et les performances par format et par public visé, pour orienter le choix des formats.
 
## 5. Mode manuel (phase de test)
 
L'abonnement Google AI Pro ne donne pas d'API : la génération image/vidéo se fait à la main dans l'app Gemini ou Google Flow.
 
Le provider `manual` doit :
1. écrire les prompts dans `jobs/<id>/prompts.md` (prêts à copier-coller) ;
2. passer le job en `awaiting_assets` et notifier l'humain ;
3. surveiller `jobs/<id>/inbox/` ; dès que les fichiers attendus y sont déposés, reprendre le pipeline (montage, contrôle, etc.).
Même logique possible pour la publication (`publisher: manual` = prépare vidéo + légende, l'humain poste).
 
## 6 bis. Bibliothèque de tenues (agent Style)
 
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
## 6. Config d'une chaîne (exemple)
 
```yaml
# config/channels/ai_girl.yaml
id: ai_girl
enabled: true
platforms: [instagram_reels, tiktok]
language: fr            # TO DECIDE
niche: "TO DECIDE"      # e.g. fitness, fashion, travel
persona_file: personas/ai_girl/persona.md
reference_images: personas/ai_girl/refs/
content_rating: public  # public | adult (adult channels never publish to IG/TikTok/YouTube)
format: { aspect: "9:16", min_s: 8, max_s: 30 }
cadence: { per_day: 1 }
agents: [trends, scenario, production, control, publication, analysis]
providers:
  llm: claude           # claude | openai | gemini
  image: manual         # manual | nano_banana_api | flux_lora
  video: manual         # manual | veo_api | kling_api | seedance_api
  voice: none
  publisher: manual     # manual | meta_graph | third_party
human_review: required  # required | on_doubt | off
budget: { daily_usd: 2, monthly_usd: 50 }
competitors: []         # accounts to watch
outfits_dir: outfits/
spicy_mix: { level_0_1: 0.7, level_2: 0.3 }
audience_targets:       # share of formats aimed at each audience, tuned by the Analysis agent
  male: 0.5
  female: 0.3
  both: 0.2
```
 
## 7. Stack suggérée
 
- **Python 3.11+**, un module par agent, une interface `Provider` par type (llm, image, video, voice, publisher).
- **Orchestration :** script CLI + planificateur (cron / APScheduler) au départ ; n8n possible plus tard.
- **Stockage :** SQLite + dossiers `jobs/` ; Google Sheets en export lecture seule si utile.
- **Montage :** FFmpeg.
- **Notifications / validation :** bot Telegram.
- **Logs :** chaque appel de provider enregistre modèle, prompt, coût, durée.
Structure de repo proposée :
 
```
config/channels/   personas/   rules/   jobs/   outfits/   inspiration/{inbox,archive}/
src/agents/   src/providers/{llm,image,video,voice,publisher}/   src/core/{pipeline,budget,storage,notify}/
tests/   .env.example   BRIEF.md   ROADMAP.md
```
 
## 8. Fournisseurs à prévoir (à brancher plus tard)
 
- **LLM :** Claude, OpenAI, Gemini (API).
- **Image :** Nano Banana (API Gemini), Flux + LoRA (fal.ai / Replicate).
- **Vidéo :** Veo 3.1 / 3.1 Fast / Lite (API Gemini / Vertex), Kling 3.0, Seedance 2.0 (via fal.ai ou équivalent). Sora : fermé, ne pas intégrer.
- **Publication :** Meta Graph API (compte Business + app validée), ou outil tiers avec API.
- **Trends :** Apify (scrapers Instagram / TikTok).
## 9. Décisions encore ouvertes (ne pas inventer : demander)
 
- ~~Niche, langue, nom et fiche de la persona~~ → décidé : Léna Reyes, voir `personas/ai_girl/persona.md`.
- Public ou adulte (change plateformes, providers et règles).
- Mode de monétisation prioritaire.
- Hébergement final (PC local vs serveur).
## 10. Règles de code
 
- Commentaires de code en anglais ; docs et messages utilisateur en français.
- Aucun secret dans le repo ; `.env.example` à jour.
- Chaque agent testable seul avec un job factice.
- Commencer petit : pipeline de bout en bout en mode `manual` avant tout provider payant.
 