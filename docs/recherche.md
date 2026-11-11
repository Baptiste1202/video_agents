# Recherche — outils, prix, règles, monétisation

> Synthèse de la recherche du 5 nov. 2026, complétée le 9 nov. Ce document sert de contexte : les règles techniques à appliquer sont dans `BRIEF.md`, les décisions dans `docs/decisions.md`.
> Les prix sont des ordres de grandeur, à recontrôler au moment de souscrire. [approximatif] / [estimation] = chiffre non vérifié.

## 1. Les 7 challenges de départ

1. **3 vidéos/jour dès le départ, c'est trop tôt.** Commencer à 1/jour avec validation humaine pendant 3-4 semaines. Le volume vient une fois que le pipeline sort une qualité stable. Instagram et YouTube pénalisent le contenu répétitif ou de faible effort (§5).
2. **Claude ne génère ni images ni vidéos.** Claude (ou ChatGPT) sert de "cerveau" : analyse des trends, scénarios, prompts, descriptions, contrôle qualité, orchestration. La génération visuelle passe par des modèles spécialisés (Veo, Kling, Seedance, Nano Banana…).
3. **Instagram ne paie quasiment pas à la vue.** Pour un compte en France, l'argent vient des partenariats de marque, de l'affiliation, des abonnements, ou d'un renvoi vers une autre plateforme. Il faut un modèle économique avant de produire 90 vidéos par mois.
4. **Un compte d'IA-girl doit être déclaré comme tel** (label Instagram depuis le 31 août 2026, AI Act depuis le 2 août 2026).
5. **On ne donne pas ses identifiants Instagram à un bot.** API officielle de Meta ou outil de planification agréé. Un bot qui se connecte comme un humain fait courir un risque de bannissement.
6. **L'API Instagram ne permet pas d'ajouter les musiques tendance** de la bibliothèque Instagram : la musique doit être intégrée au fichier vidéo avant l'envoi. Contrainte forte pour le format Reels.
7. **"Gratuit pour commencer" est réaliste pour le prototype, pas pour la production.** Compter ~40 à 120 $ par mois pour 1 vidéo par jour de bonne qualité (§8).

## 2. Mise en place du compte Instagram (fait en phase 0)

C'est l'humain qui crée le compte, puis donne aux agents un accès par l'API officielle, jamais son mot de passe.

1. Créer le compte avec un email dédié au projet, activer la double authentification.
2. Le passer en **compte professionnel Business** (la publication de Reels par API ne marche pas avec un compte Creator).
3. Le relier à une Page Facebook et à un compte Meta Business.
4. Activer dès le départ le label **"AI-generated profile"**.
5. Chauffer le compte à la main 1-2 semaines : photo de profil, bio, quelques posts, interactions.

Options d'accès pour les agents et contraintes de l'API : `BRIEF.md` §7.

## 3. Labels IA et cadre légal

- **Instagram :** depuis l'annonce du 31 août 2026, les profils centrés sur une personne générée par IA doivent activer le label "AI-generated profile". Sans label, la portée est limitée (Reels, Explorer, recommandations). Avec le label, aucune pénalité de portée ([TechRepublic](https://techrepublic.com/article/news-instagram-ai-generated-profile-label-recommendations/), [Implicator](https://www.implicator.ai/instagram-will-cut-the-reach-of-ai-personas-that-skip-its-new-label/)).
- **AI Act européen (article 50) :** obligations de transparence applicables depuis le 2 août 2026, dont l'obligation d'indiquer qu'un contenu de type deepfake est généré par IA. Amendes jusqu'à 15 M€ ou 3 % du CA mondial ([McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations)).
- **Loi française sur les influenceurs (2023) :** tout contenu commercial (placement, affiliation) porte la mention "Publicité" ou "Collaboration commerciale" ; les images retouchées ou générées par IA, la mention "Image virtuelle". [À vérifier avec un juriste avant le 1er partenariat]
- **TikTok :** étiquetage obligatoire du contenu IA réaliste.
- **Interdits à coder en dur dans l'agent Contrôle :** aucune ressemblance avec une personne réelle, aucun contenu suggérant une mineure, pas de faux avis ou fausses promesses produits.

## 4. Benchmark des IA

Il faut 4 familles d'outils : un cerveau (texte), un générateur d'images, un générateur de vidéo, et en option de la voix. Les prix bougent tous les mois : changer de fournisseur doit se faire par configuration.

### Le cerveau : Claude, ChatGPT, Gemini

Ils se valent pour écrire scénarios, prompts et descriptions. Claude est particulièrement bon pour l'orchestration d'agents et le code du pipeline. Coût par vidéo via API : quelques centimes. Gratuit possible au début via les offres gratuites, ~20 $/mois en abonnement [approximatif].

### Vidéo (le poste le plus cher)

| Modèle | Prix indicatif | Points forts | Remarques |
| --- | --- | --- | --- |
| `gemini-omni-1.1-flash` (API Gemini) | ~0,10 $/s en 720p | Remplace les Veo en préversion dans l'API | Info du 9 nov. (Layer3 Labs, Developers Digest) |
| Google Veo 3.1 Lite | ~0,03 $/s (720p, sans audio) | Le moins cher listé | Idéal pour prototyper ([CometAPI](https://www.cometapi.com/ai-video-api-pricing/)). ⚠ Préversions retirées de l'API le 22 oct. 2026 |
| Google Veo 3.1 Fast | 0,10 $/s ; 0,15 $/s avec audio | Bon compromis qualité/prix | Tarifs Vertex AI ([EvoLink](https://evolink.ai/blog/best-sora-2-alternatives-2026)) |
| Google Veo 3.1 | 0,20 $/s ; 0,40 $/s avec audio | Meilleure qualité globale, audio natif | Image de référence pour garder le visage |
| Kling 3.0 (Kuaishou) | ~0,07 $/s selon fournisseur | Très bon rapport qualité/prix, offre gratuite avec crédits | Très utilisé pour la publication quotidienne ([Fluxnote](https://fluxnote.io/guides/ai-video-model-pricing-comparison-2026)) |
| Seedance 2.0 (ByteDance) | dès ~0,04 $/s (version Fast) | Peu cher, beaucoup de contrôle créatif | Via API tierces (fal.ai, Atlas Cloud…) |
| Wan 2.x (Alibaba, open source) | Gratuit si GPU perso, sinon quelques centimes | Aucun abonnement | Carte graphique puissante ou GPU loué : `docs/hebergement_gpu.md` |
| Runway Gen-4.5 | Abonnement | Contrôle fin du mouvement | Plus orienté création manuelle |
| OpenAI Sora 2 | — | — | **Fermé** : app arrêtée en avril 2026, API le 24 septembre 2026 ([Rangy](https://rangy.ai/blog/ai-video-generators-compared-2026)). À écarter |

Ordre de grandeur : un Reel de 15 s coûte 0,50 à 6 $ selon le modèle, avant les ratés. Compter 2 à 3 générations par plan retenu.

Dans l'app Flow (crédits de l'abonnement), voir le tableau « Quel modèle utiliser dans Flow » de `BRIEF.md` §5.

### Images et cohérence du physique

On crée une **fiche personnage** (visage de face, profil, 3/4, plein pied, 3-4 tenues), puis chaque vidéo part d'une image générée à partir de ces références (image-to-video). La fiche personnage (images + description textuelle précise), lue par tous les agents, est l'actif le plus précieux du projet.

| Approche | Outil | Coût | Quand l'utiliser |
| --- | --- | --- | --- |
| Références sans entraînement | Nano Banana 2 / Pro (Google Gemini), Seedream (ByteDance) | Gratuit en quantité limitée (Google AI Studio), puis quelques centimes par image [approximatif] | Pour démarrer : une à trois images de référence suffisent ([RunDiffusion](https://www.rundiffusion.com/nano-banana-2-consistent-character-images)) |
| Modèle entraîné sur le personnage (LoRA) | Flux + LoRA via fal.ai, Replicate ou ComfyUI ; LoRA Wan 2.2 (`docs/hebergement_gpu.md`) | Quelques dollars par entraînement | Si le visage dérive malgré les références, ou pour un contrôle total |
| Studio tout-en-un | Higgsfield, OpenArt | Abonnement ~10-30 $/mois [approximatif] | Interface plutôt que code (§7) |

### Voix et lip-sync (si elle parle)

- **Voix :** ElevenLabs (offre gratuite limitée, puis ~5-22 $/mois [approximatif]). Une seule voix figée pour la persona.
- **Synchronisation labiale :** Veo 3.1 et Seedance génèrent l'audio avec la vidéo ; sinon HeyGen ou Hedra pour faire parler une image.
- **Montage :** FFmpeg (gratuit) pour assembler plans, sous-titres, musique et texte à l'écran ; CapCut pour retoucher à la main.

### Agrégateurs

fal.ai, Replicate ou OpenRouter donnent accès à la plupart de ces modèles avec **une seule clé API et une seule facture** : changer de modèle = changer une ligne de config.

## 5. Outils existants pour chaque étape

Ne pas recoder ce qui existe : la plupart des briques coûtent quelques dollars par mois.

| Étape | Outil | Coût | Commentaire |
| --- | --- | --- | --- |
| Trends | Tableau de bord professionnel Instagram (audios tendance, statistiques) | Gratuit | À consulter à la main au début |
| Trends | TikTok Creative Center (hashtags, sons, vidéos tendance par pays) | Gratuit | Les tendances TikTok arrivent souvent sur Reels quelques jours après |
| Trends | Scrapers Apify (Instagram Reels, audio Instagram, TikTok Creative Center) | ~2 $ pour 1 000 résultats ([Apify](https://apify.com/kinaesthetic_millionaire/instagram-reels-audio-scraper)) | Branchables sur Claude via MCP : l'agent Trends peut les appeler seul |
| Trends | Google Trends | Gratuit | Pour les sujets, pas pour les formats |
| Trends | Veille de comptes concurrents | Gratuit (manuel) ou Apify | Lister 10-20 comptes IA et humains de la niche ; l'agent analyse leurs Reels les plus vus |
| Orchestration | n8n | Gratuit en auto-hébergé, ~20 €/mois en cloud [approximatif] | Enchaîne les étapes visuellement, planifie, gère les erreurs |
| Orchestration | Make / Zapier | Offre gratuite limitée | Plus simple que n8n, plus cher à volume |
| Orchestration | Claude Agent SDK / Claude Code + scripts Python | Coût API seulement | Plus flexible, demande du code |
| Publication | Metricool, Buffer, Later | Offre gratuite ou ~10-20 €/mois [approximatif] | Planification + statistiques ; vérifier qu'ils ont une API |
| Publication | Postproxy, Publora, bundle.social | Abonnement API | Conçus pour être appelés par un programme |
| Publication | Blotato | Abonnement | Outil TikTok déjà audité : publication publique par API |
| Analyse | API Instagram Insights (via l'app ou l'outil de publication) | Gratuit | Vues, temps de visionnage, partages, sauvegardes, abonnés gagnés |
| Stockage | Google Sheets ou Airtable comme tableau de bord du pipeline | Gratuit | Une ligne par vidéo : idée, statut, coût, URL, résultats |
| Validation | Bot Telegram ou Slack avec boutons Valider / Refaire | Gratuit | Le plus simple pour garder un humain dans la boucle depuis son téléphone |

**Raccourci possible :** les plateformes "tout-en-un" d'influenceurs IA (Higgsfield, services de création d'avatar) vont plus vite mais enferment. Pour un système qui doit aussi faire de la pluie sur YouTube, une architecture maison avec des briques interchangeables est préférable.

## 6. Monétisation

Instagram ne paie presque rien à la vue : il sert à construire une audience monétisée ailleurs. YouTube paie à la vue, mais les seuils sont hauts et le contenu IA répétitif est exclu.

### Instagram

- **Pas de paiement direct à la vue pour la plupart des créateurs** : le programme de bonus Reels a pris fin en 2023 ; ce qui reste est limité et sur invitation ([Stack Influence](https://stackinfluence.com/how-to-get-paid-on-instagram-reels/), [Lilach Bullock](https://www.lilachbullock.com/does-instagram-pay-creators-for-reels/)).
- **Ce qui rapporte :** partenariats de marque, affiliation, abonnements payants, cadeaux (Gifts), vente ou renvoi vers une autre plateforme.
- Ordre de grandeur en Europe de l'Ouest : 150 à 800 € par post sponsorisé ([Fluxnote](https://fluxnote.io/guides/instagram-earnings-europe-2026)). Les marques sont souvent plus prudentes avec un influenceur IA.
- Beaucoup de comptes d'IA-girls renvoient vers des plateformes d'abonnement externes. Si c'est le plan, le décider explicitement : cela change la ligne éditoriale, les risques de bannissement et le cadre légal.

### YouTube

| Élément | Aujourd'hui | À partir du 1er février 2027 |
| --- | --- | --- |
| Entrée dans le Programme Partenaire (pubs) | 1 000 abonnés + 4 000 h de visionnage sur 12 mois, ou 10 M de vues Shorts sur 90 jours | 1 000 abonnés + 8 000 h, ou 20 M de vues Shorts sur 90 jours |
| Revenus Shorts | 45 % de sa part du pot publicitaire Shorts | Maintenir 10 M de vues Shorts sur 90 jours glissants pour toucher la part Shorts chaque mois |
| Revenus vidéos longues | 55 % des revenus pub de la vidéo [connaissance générale] | Inchangé |

Sources : [AIR Media-Tech](https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide), [Elev8or](https://www.elev8or.io/blog/bio/youtube-shorts-creator-pool-2027). Les seuils doublent début 2027 ; la monétisation des Shorts devient très difficile pour un petit compte. Les vidéos longues sont plus accessibles.

**Alerte "bruit de pluie" :** YouTube exclut de la monétisation le contenu "inauthentique" : vidéos génériques, répétitives ou basées sur des modèles quasi identiques, produites en masse par IA ([TechRepublic](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)). Des chaînes de pluie de 10 h quasi identiques sont exactement dans la cible. Pour passer : ambiances distinctes, séries thématiques, visuels soignés, apport humain visible. Ces règles changent souvent : l'agent Analyse les revérifie chaque trimestre.

### TikTok Creator Rewards

- Ne paie que les vidéos de **plus d'une minute**, à partir de **10 000 abonnés et 100 000 vues sur 30 jours**, avec du contenu original. Les clips de 8 s ne rapportent rien.
- France : ~0,60 $ pour 1 000 vues qualifiées, soit ~400-600 $ pour 1 million de vues ([Elev8or](https://www.elev8or.io/tools/tiktok-creator-rewards-calculator), TT Calculator).
- [À vérifier : TikTok peut exclure du Creator Rewards un contenu entièrement IA jugé "non original"]
- Pour le viser : un format de plus de 60 s (ex. une journée de Léna en plusieurs plans).

### Quelle plateforme est la plus rentable ?

Aucune ne rend riche par les vues seules. Pour une IA-girl, la vue paie peu partout ; la vraie rentabilité vient de ce qu'on vend à l'audience.

| Plateforme | Paiement aux vues | Ce qu'il faut pour être payé | 1 M de vues rapporte environ | Rôle dans le projet |
| --- | --- | --- | --- | --- |
| TikTok | Oui, France éligible (Creator Rewards) | 10 000 abonnés, vidéos de **plus de 60 s**, contenu original | ~400-600 $ en France | Meilleur canal de découverte ; paie le mieux à la vue si format > 1 min |
| YouTube (vidéos longues) | Oui | 1 000 abonnés + 4 000 h (8 000 h dès février 2027) | Très variable, souvent plusieurs centaines à milliers de $ | Le plus solide sur la durée, adapté à la pluie |
| YouTube Shorts | Oui | 1 000 abonnés + 10 M de vues Shorts / 90 jours | ~10-50 $ ([Vidpros](https://vidpros.com/youtube-shorts-monetization-in-2026)) | Faible ; seuil très haut |
| Instagram Reels | Quasiment non en France | Programmes sur invitation | ~0 $ en direct | Vitrine pour les marques et pour renvoyer vers les offres |

**Verdict :** TikTok + Instagram pour l'audience de l'IA-girl, YouTube long pour la pluie. Publier la même vidéo sur les trois ne coûte presque rien en plus : le système doit être **multi-plateforme dès le départ**.

### Plateformes d'abonnement : le contenu IA est-il autorisé ?

| Plateforme | Persona 100 % IA autorisée ? | Conditions | Commission |
| --- | --- | --- | --- |
| [Fanvue](https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue) | Oui | Indiquer clairement que c'est de l'IA ; vérification d'identité (KYC) de l'opérateur ; aucune ressemblance avec une personne réelle sans consentement | 20 % (80 % pour le créateur) ([AI Creator Ops](https://ai-creator-ops.vercel.app/platforms/fanvue)) |
| OnlyFans | Non | L'IA n'est permise que si le contenu montre le créateur vérifié lui-même ([Aruna Talent](https://arunatalent.com/blog/onlyfans-ai-content-policy-2026)) | 20 % |
| Fansly | Non pour l'IA photoréaliste | Interdite depuis juin 2025 ([Sirency](https://www.sirency.com/blog/fanvue-alternatives-for-creators)) | 20 % |
| Patreon | Non pour l'IA hyperréaliste sur les pages adultes | Les personnages IA illustrés ou animés sont acceptés | ~10 % selon offre |

- Fanvue autorise aussi le contenu adulte dans des espaces réservés aux abonnés vérifiés : c'est le modèle de la plupart des comptes d'IA-girls qui gagnent de l'argent. Un abonnement "tout public" (photos exclusives, coulisses, messages) est possible aussi.
- Un compte qui renvoie vers du contenu adulte ne décroche presque pas de partenariats grand public, et Instagram/TikTok surveillent de près les liens vers ces sites. (Décision prise : public, voir `docs/decisions.md`.)
- Si un jour adulte : règles plus strictes partout (aucune apparence juvénile, aucune ressemblance avec une vraie personne), déclaration des revenus, image publique à assumer.
- Le chat avec les abonnés est souvent la première source de revenus sur ces plateformes. Fanvue propose des outils IA pour ça ; OnlyFans interdit les chatbots en messages privés.

## 7. Business model

Scénario le plus probable : la première année coûte plus qu'elle ne rapporte, et seule une petite minorité de comptes dépasse 1 000 $ par mois. Plus de 200 000 comptes d'influenceurs IA actifs sur Instagram et TikTok, dont moins de 2 000 dépassent 1 000 $ par mois (HypeAuditor 2026, cité par [Oakgen](https://oakgen.ai/blog/ai-influencer-monetization-guide)). Les chiffres "20 000 $/mois" qui circulent viennent surtout de vendeurs d'outils.

### Les sources de revenus, par ordre d'arrivée

| Source | À partir de | Ordre de grandeur | Remarque |
| --- | --- | --- | --- |
| Affiliation (mode, beauté, outils IA) | Dès le début | 5-30 % de commission par vente | Fonctionne même avec peu d'abonnés si la niche achète |
| Abonnement payant (Fanvue, Instagram Abonnements, Patreon) | ~1 000-5 000 abonnés | 5-15 €/mois par abonné, 80 % pour le créateur | Taux de conversion réaliste : 0,2 à 1 % de l'audience [estimation] |
| TikTok Creator Rewards | 10 000 abonnés + vidéos > 1 min | ~0,6 $ pour 1 000 vues qualifiées en France | Complément, pas un modèle |
| Partenariats de marque | ~10 000 abonnés avec 2 %+ d'engagement | 150-800 € par post en Europe de l'Ouest | Plus difficile si le compte renvoie vers de l'adulte |
| YouTube (chaîne pluie, longues vidéos) | 1 000 abonnés + 4 000 h | Variable | Lent mais durable, si le contenu passe la règle "inauthentique" |
| **Vendre le système lui-même** | Dès qu'il marche | Prestation ou abonnement B2B | Probablement le meilleur actif |

### Trois scénarios à 12 mois (estimations)

Hypothèses : 1 compte IA-girl tout public, Instagram + TikTok, 1 puis 3 vidéos/jour, coûts de 100 à 250 €/mois.

| Scénario | Abonnés à 12 mois | Revenus mensuels au mois 12 | Résultat sur l'année | Probabilité |
| --- | --- | --- | --- | --- |
| Pessimiste | < 5 000 | 0-200 € | Perte de 1 500 à 2 500 € | Le cas le plus fréquent |
| Réaliste (bonne exécution) | 10 000-50 000 | 300-1 500 € | Autour de l'équilibre | Possible avec une niche claire et de la régularité |
| Optimiste (top ~1 %) | 100 000+ | 3 000-10 000 € et plus | Nettement positif | Rare : vrai succès viral et persona forte |

Exemple pour l'abonnement : 30 000 abonnés × 0,3 % convertis × 8 € × 80 % = ~580 € par mois.

### Le business model proposé

1. **Un moteur, un portefeuille de chaînes.** Plutôt que tout miser sur une IA-girl, lancer 2-3 chaînes à coût marginal faible (IA-girl, pluie/ambiance sur YouTube, une niche utile type "astuces" ou "faits"). Garder celles qui décollent, couper les autres après 90 jours.
2. **Audience gratuite → offre payante.** TikTok et Instagram attirent, un lien en bio renvoie vers une offre contrôlée : abonnement, affiliation, produits numériques.
3. **Capter l'audience hors plateforme dès le début** (liste email ou canal Telegram) : une plateforme peut supprimer un compte du jour au lendemain.
4. **Vendre le système.** Un pipeline qui produit 3 vidéos/jour de qualité constante pour ~5 € pièce intéresse marques et créateurs. Revenu le moins risqué : il ne dépend pas de l'algorithme.
5. **Règle de pilotage :** budget plafonné à 250 €/mois ; point d'étape à 3 mois (5 000 abonnés ou 1 % d'engagement, sinon pivot).

### Plateformes d'avatar type Higgsfield : gratuites ?

Non. Higgsfield a une offre gratuite **sans crédits de génération** et sans droit d'usage commercial ([Creatify](<https://creatify.ai/blog/is-higgsfield-free-free-plan-trials-and-promo-codes-explained-(2026)>)). Offres payantes, vérifiées en octobre 2026 ([HeyGen](https://www.heygen.com/blog/higgsfield-pricing)) :

| Offre | Prix mensuel | Prix annuel (par mois) |
| --- | --- | --- |
| Starter | 19 $ | — |
| Plus | 59 $ | 47 $ |
| Ultra | 129 $ | 99 $ |

Les crédits ne se reportent pas, les prix varient selon le pays. Higgsfield donne accès à Kling 3.0, Veo 3.1, Seedance 2.0 et Nano Banana Pro dans une seule interface, avec un outil de personnage constant (Soul ID). Utile pour prototyper vite à la main pendant 1 mois ; pour l'automatisation, les API (fal.ai, Google) restent moins chères et plus flexibles. Alternatives : OpenArt, ImagineArt (à partir d'environ 9 $/mois).

## 8. Budget estimé

Pour 1 Reel/jour de bonne qualité : ~40 à 120 $/mois ; pour 3/jour : ~120 à 350 $. Hypothèses : Reel de 15 s, 2,5 générations par plan retenu, modèles entre Veo 3.1 Lite (0,03 $/s) et Kling 3.0 (~0,07 $/s). Estimations, pas des devis.

| Poste | 1 vidéo/jour | 3 vidéos/jour |
| --- | --- | --- |
| Génération vidéo | 35-80 $ | 100-240 $ |
| Génération d'images | 0-10 $ | 5-20 $ |
| Cerveau (Claude/ChatGPT par API) | 5-15 $ | 10-30 $ |
| Trends (Apify) | 0-5 $ | 5-10 $ |
| Publication + analyse (outil tiers) | 0-20 $ | 0-20 $ |
| Voix (si elle parle) | 0-5 $ | 5-22 $ |
| **Total indicatif** | **~40-120 $/mois** | **~120-350 $/mois** |

Estimation du 9 nov. avec `gemini-omni-1.1-flash` : ~25-50 $ pour 30 vidéos de 8 s par mois (un essai raté inclus).

**Version 100 % gratuite pour le prototype :** crédits gratuits Kling, Google AI Studio pour les images, offres gratuites des LLM, publication manuelle. Suffisant pour 5-10 vidéos de test, pas pour un rythme quotidien. En pratique : abonnement Google AI Pro étudiant (Gemini + Flow à la main).

## 9. Sources

- [Meta : Instagram Content Publishing](https://developers.facebook.com/documentation/instagram-platform/content-publishing)
- [Postproxy : guide de publication de Reels par API](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)
- [TechRepublic : label "AI-generated profile" sur Instagram](https://techrepublic.com/article/news-instagram-ai-generated-profile-label-recommendations/)
- [Implicator : portée des personas IA sans label](https://www.implicator.ai/instagram-will-cut-the-reach-of-ai-personas-that-skip-its-new-label/)
- [McCann FitzGerald : AI Act article 50, obligations des déployeurs](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations)
- [CometAPI : prix des API vidéo](https://www.cometapi.com/ai-video-api-pricing/)
- [EvoLink : tarifs Veo 3.1 sur Vertex AI](https://evolink.ai/blog/best-sora-2-alternatives-2026)
- [Fluxnote : comparatif des prix vidéo IA](https://fluxnote.io/guides/ai-video-model-pricing-comparison-2026)
- [Rangy : comparatif des générateurs vidéo 2026](https://rangy.ai/blog/ai-video-generators-compared-2026)
- [RunDiffusion : cohérence de personnage avec Nano Banana 2](https://www.rundiffusion.com/nano-banana-2-consistent-character-images)
- [Apify : scraper audio Instagram Reels](https://apify.com/kinaesthetic_millionaire/instagram-reels-audio-scraper)
- [Stack Influence : rémunération des Reels après la fin des bonus](https://stackinfluence.com/how-to-get-paid-on-instagram-reels/)
- [Lilach Bullock : Instagram paie-t-il les Reels ?](https://www.lilachbullock.com/does-instagram-pay-creators-for-reels/)
- [Fluxnote : revenus Instagram en Europe](https://fluxnote.io/guides/instagram-earnings-europe-2026)
- [AIR Media-Tech : conditions du Programme Partenaire YouTube](https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide)
- [Elev8or : seuil de 10 M de vues Shorts en 2027](https://www.elev8or.io/blog/bio/youtube-shorts-creator-pool-2027)
- [TechRepublic : règles YouTube sur le contenu IA inauthentique](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)
- [Elev8or : calculateur TikTok Creator Rewards](https://www.elev8or.io/tools/tiktok-creator-rewards-calculator)
- [Vidpros : revenus YouTube Shorts 2026](https://vidpros.com/youtube-shorts-monetization-in-2026)
- [Fanvue : le contenu IA est-il autorisé ?](https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue)
- [AI Creator Ops : fiche Fanvue](https://ai-creator-ops.vercel.app/platforms/fanvue)
- [Aruna Talent : politique IA d'OnlyFans 2026](https://arunatalent.com/blog/onlyfans-ai-content-policy-2026)
- [Sirency : alternatives à Fanvue et règles IA](https://www.sirency.com/blog/fanvue-alternatives-for-creators)
- [Oakgen : guide de monétisation des influenceurs IA](https://oakgen.ai/blog/ai-influencer-monetization-guide)
- [Creatify : Higgsfield est-il gratuit ?](<https://creatify.ai/blog/is-higgsfield-free-free-plan-trials-and-promo-codes-explained-(2026)>)
- [HeyGen : prix de Higgsfield (octobre 2026)](https://www.heygen.com/blog/higgsfield-pricing)
- Sources du 9 nov. (sans lien dans la note d'origine) : Developers Digest (modèles vidéo de l'API Gemini et dates de retrait), Layer3 Labs (prix de Veo et `gemini-omni-1.1-flash`), TikTok for Developers (Direct Post et clients non audités), Ayrshare (audit de l'API TikTok), Blotato (outil de publication TikTok audité), TT Calculator (conditions de Creator Rewards).
