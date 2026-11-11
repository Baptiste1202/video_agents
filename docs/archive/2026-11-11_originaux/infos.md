# Brief projet — Agents IA de production vidéo (Instagram / YouTube)

Nov 5, 2026 · @Baptiste

## Le projet en une phrase

Un système d'agents IA, modulaire et réutilisable, qui produit et publie des vidéos courtes sur des comptes thématiques ("chaînes"). Premier cas d'usage : une influenceuse virtuelle sur Instagram Reels. Cas suivants : vidéos longues d'ambiance (pluie) sur YouTube, ou autres concepts.

**Rôle de ce document :** brief à donner à une IA (ou à un dev) pour qu'elle construise le système. Les sections marquées **\[À PRÉCISER\]** sont des décisions qui te reviennent avant de lancer.

### Mes 7 challenges principaux sur ta note initiale

1. **3 vidéos/jour dès le départ, c'est trop tôt.** Commence à 1/jour avec validation humaine pendant 3-4 semaines. Le volume vient une fois que le pipeline sort une qualité stable. Instagram et YouTube pénalisent désormais le contenu répétitif ou de faible effort (voir sections 4 et 7).
2. **Claude ne génère ni images ni vidéos.** Claude (ou ChatGPT) sert de "cerveau" : analyse des trends, scénarios, prompts, descriptions, contrôle qualité, orchestration. La génération visuelle passe par des modèles spécialisés (Veo, Kling, Seedance, Nano Banana…).
3. **Instagram ne paie quasiment pas à la vue.** Pour un compte en France, l'argent vient des partenariats de marque, de l'affiliation, des abonnements, ou d'un renvoi vers une autre plateforme. Il faut un modèle économique avant de produire 90 vidéos par mois.
4. **Un compte d'IA-girl doit être déclaré comme tel.** Depuis le 31 août 2026, Instagram limite la portée des profils de personnes générées par IA qui n'activent pas le label "AI-generated profile". L'AI Act européen impose aussi la transparence depuis le 2 août 2026.
5. **On ne donne pas ses identifiants Instagram à un bot.** On passe par l'API officielle de Meta (ou un outil de planification agréé). Un bot qui se connecte comme un humain fait courir un risque de bannissement.
6. **L'API Instagram ne permet pas d'ajouter les musiques tendance** de la bibliothèque Instagram. La musique doit être intégrée au fichier vidéo avant l'envoi. C'est une contrainte forte pour le format Reels.
7. **"Gratuit pour commencer" est réaliste pour le prototype, pas pour la production.** Compte environ 40 à 120 $ par mois pour 1 vidéo par jour de bonne qualité (détail en section 8).

## &#91;À PRÉCISER\] Ce que tu dois décider avant de lancer

Une IA qui construit le système sans ces réponses va les inventer. Remplis ce tableau, il deviendra le cœur du brief.

| Sujet | Question à trancher | Ma suggestion par défaut |
| --- | --- | --- |
| Persona | Nom, âge (clairement adulte, 22-28 ans), nationalité, personnalité, ton, histoire, ce qu'elle aime | Une fiche persona d'1 page, figée, que tous les agents lisent |
| Niche | De quoi parle-t-elle ? "Jolie fille" seul n'est pas une niche, c'est un physique | Choisir 1 niche monétisable : fitness, mode, voyage, beauté, gaming, lifestyle tech… |
| Langue et audience | Français, anglais, ou les deux ? Quel pays cible ? | Anglais pour la portée, ou FR pour une niche moins saturée |
| Monétisation | Comment gagnes-tu de l'argent, et à partir de combien d'abonnés ? | Affiliation dès le début, partenariats de marque après 10k abonnés |
| Ligne rouge contenu | Jusqu'où va le contenu (tenues, suggestivité) ? | Rester dans les règles Instagram ; décision à écrire noir sur blanc pour l'agent de contrôle |
| Formats vidéo | Vlog face caméra qui parle ? Plans esthétiques + texte à l'écran ? Tendances/danses ? | Commencer par plans esthétiques + texte + musique (le plus simple à rendre crédible) |
| Voix | Elle parle ou pas ? Quelle voix ? | Pas de voix au début ; voix clonée fixe (ElevenLabs) ensuite |
| Validation humaine | Quelles étapes passent par toi avant publication ? | Toi = validation finale pendant le 1er mois, puis seulement sur alerte |
| Budget | Combien par mois, et plafond d'alerte ? | 50 €/mois en test, plafond dur dans le code |
| KPI de succès | Qu'est-ce qui dit que ça marche à 30 et 90 jours ? | Taux de visionnage complet, partages, abonnés gagnés par vidéo |
| Statut juridique | Qui encaisse l'argent ? | Micro-entreprise suffit pour démarrer \[à vérifier avec un comptable\] |
| Hébergement | Où tourne le système ? | Ton PC au début, puis un petit serveur ou n8n cloud |

## Architecture : un moteur, plusieurs chaînes

Pour éviter un système rigide, sépare le **moteur** (les 6 agents, communs) de la **config de chaîne** (ce qui change d'un compte à l'autre). L'IA-girl sur Instagram et la pluie sur YouTube sont deux configs du même moteur.

&#91;embedded content: pipeline d'agents · 6 étapes en boucle\]

Le contrôle est la seule étape où tu interviens au début ; la mémoire partagée permet à l'agent Analyse de dire aux autres ce qui a marché.

### Principes à donner à l'IA qui construira le système

- **Chaque agent = un module indépendant** avec une entrée et une sortie claires (un fichier JSON par vidéo qui passe d'étape en étape). On peut en remplacer un sans toucher aux autres.
- **Les fournisseurs d'IA sont interchangeables** : le modèle vidéo, le modèle image et le LLM sont choisis dans la config, pas codés en dur.
- **Une étape peut être sautée ou faite à la main** : par exemple, la pluie YouTube n'a pas besoin de l'agent Trends au quotidien, ni de la fiche personnage.
- **Chaque vidéo est tracée** : idée d'origine, prompts utilisés, modèle, coût, statut, résultats. Indispensable pour apprendre et maîtriser le budget.
- **Plafond de dépenses et arrêt d'urgence** : le système s'arrête seul si le budget du jour est dépassé ou si 2 publications d'affilée échouent.
- **Validation humaine activable par chaîne** : obligatoire au début, puis seulement quand l'agent Contrôle a un doute.

### Agent transversal : l'agent Règles

Un 7e agent, hors de la boucle, tient à jour un **fichier de règles** que l'agent Contrôle applique à chaque vidéo. Les règles des plateformes ont changé plusieurs fois en 2026 ; sans cet agent, le système se met en infraction sans le savoir.

- **Veille hebdomadaire :** relit les pages officielles (règles Instagram, TikTok, YouTube, Fanvue, AI Act, loi influenceurs) et signale tout changement.
- **Fichier de règles par plateforme :** format, durée, labels IA obligatoires, mentions "Publicité" / "Image virtuelle", sujets interdits, ligne rouge que tu as fixée.
- **Contrôle avant publication :** légende, hashtags, liens et visuel vérifiés contre ce fichier ; blocage et alerte si doute.
- **Il propose, tu valides :** toute modification du fichier de règles passe par toi, pour éviter qu'un agent assouplisse ses propres limites.
- **Limite à connaître :** ce n'est pas un juriste. Avant le premier partenariat payant ou toute activité adulte, faire valider par un professionnel.

### Exemple de config de chaîne (à compléter)

| Champ | Chaîne 1 : IA-girl | Chaîne 2 : pluie (plus tard) |
| --- | --- | --- |
| Plateforme | Instagram Reels | YouTube (vidéos longues) |
| Format | 9:16, 8-30 s | 16:9, 1-10 h |
| Rythme | 1/jour, puis 3/jour | 2-3/semaine |
| Persona | Fiche personnage + images de référence | Aucune |
| Agents actifs | Les 6 | Scénario, Production, Contrôle, Publication, Analyse |
| Modèle vidéo | Kling 3.0 ou Veo 3.1 Fast | Boucle courte générée puis répétée au montage |
| Audio | Musique libre de droits intégrée | Sons de pluie libres de droits ou générés |
| Validation humaine | Oui | Oui |

## Compte Instagram, accès des bots et règles

Oui, c'est toi qui crées le compte, puis tu donnes aux agents un accès par l'API officielle, jamais ton mot de passe.

### Mise en place du compte

1. Créer le compte Instagram avec un email dédié au projet, et activer la double authentification.
2. Le passer en **compte professionnel Business** : la publication de Reels par API ne fonctionne qu'avec un compte Business, pas Creator ([Postproxy](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)).
3. Le relier à une Page Facebook et à un compte Meta Business.
4. Activer dès le départ le label **"AI-generated profile"** dans les paramètres du profil.
5. Chauffer le compte manuellement 1-2 semaines : photo de profil, bio, quelques posts, interactions. Un compte neuf qui publie 3 Reels/jour par API paraît suspect.

### Deux façons de donner l'accès aux agents

| Option | Comment | Pour | Contre |
| --- | --- | --- | --- |
| API officielle Meta (Graph API) | Créer une app Meta, demander les permissions de publication, stocker un token | Gratuit, contrôle total | Revue de l'app par Meta (environ 2-4 semaines), vidéo à héberger sur une URL publique |
| Outil de publication tiers avec API | Connecter le compte à un outil (Postproxy, Publora, bundle.social, Metricool, Buffer…) que tes agents appellent | Immédiat, pas de revue Meta | Abonnement mensuel, dépendance à un tiers |

Recommandation : outil tiers pour démarrer vite, API officielle quand le projet tient la route.

### Contraintes techniques de l'API à connaître

- Limite de **100 publications par API sur 24 h glissantes** par compte : largement suffisant ([doc Meta](https://developers.facebook.com/documentation/instagram-platform/content-publishing)).
- **Pas de musique de la bibliothèque Instagram via l'API** (ni sons tendance, ni catalogue) : la musique doit être intégrée dans le fichier avant l'envoi ([Postproxy](https://postproxy.dev/blog/instagram-reels-api-publishing-guide/)). Conséquence : musique libre de droits, ou publication manuelle des Reels sur son tendance.
- Format Reels : 9:16, 5 à 90 secondes, MP4/MOV H.264, 100 Mo max. En dehors, la vidéo est publiée comme simple post vidéo.
- Légende : 2 200 caractères maximum.

### Labels IA et cadre légal

- **Instagram :** depuis l'annonce du 31 août 2026, les profils centrés sur une personne générée par IA doivent activer le label "AI-generated profile". Sans label, la portée est limitée (Reels, Explorer, recommandations). Avec le label, aucune pénalité de portée ([TechRepublic](https://techrepublic.com/article/news-instagram-ai-generated-profile-label-recommendations/), [Implicator](https://www.implicator.ai/instagram-will-cut-the-reach-of-ai-personas-that-skip-its-new-label/)).
- **AI Act européen (article 50) :** les obligations de transparence s'appliquent depuis le 2 août 2026, y compris l'obligation d'indiquer qu'un contenu de type deepfake est généré par IA. Amendes jusqu'à 15 M€ ou 3 % du CA mondial ([McCann FitzGerald](https://www.mccannfitzgerald.com/knowledge/data-privacy-and-cyber-risk/ai-transparency-european-commissions-guidelines-on-article-50-part-2-deployer-obligations)).
- **Loi française sur les influenceurs (2023) :** tout contenu commercial (placement, affiliation) doit porter la mention "Publicité" ou "Collaboration commerciale", et les images retouchées ou générées par IA la mention "Image virtuelle". \[À vérifier avec un juriste avant le 1er partenariat\]
- **Interdits à coder en dur dans l'agent de contrôle :** aucune ressemblance avec une personne réelle, aucun contenu suggérant une mineure, pas de faux avis ou fausses promesses produits.

## Benchmark des IA : qui fait quoi, à quel prix

Il faut 4 familles d'outils, pas une seule IA : un cerveau (texte), un générateur d'images, un générateur de vidéo, et en option de la voix. Les prix bougent tous les mois : l'agent doit pouvoir changer de fournisseur par simple configuration.

### Le cerveau : Claude, ChatGPT, Gemini

Claude, ChatGPT et Gemini se valent pour écrire scénarios, prompts et descriptions. Claude est particulièrement bon pour l'orchestration d'agents et le code du pipeline. Coût par vidéo via API : quelques centimes. Gratuit possible au début via les offres gratuites, environ 20 $/mois en abonnement \[approximatif\].

### Vidéo (le poste le plus cher)

| Modèle | Prix indicatif | Points forts | Remarques |
| --- | --- | --- | --- |
| Google Veo 3.1 Lite | \~0,03 $/s (720p, sans audio) | Le moins cher listé | Idéal pour prototyper ([CometAPI](https://www.cometapi.com/ai-video-api-pricing/)) |
| Google Veo 3.1 Fast | 0,10 $/s ; 0,15 $/s avec audio | Bon compromis qualité/prix | Tarifs Vertex AI ([EvoLink](https://evolink.ai/blog/best-sora-2-alternatives-2026)) |
| Google Veo 3.1 | 0,20 $/s ; 0,40 $/s avec audio | Meilleure qualité globale, audio natif | Image de référence pour garder le visage |
| Kling 3.0 (Kuaishou) | \~0,07 $/s selon fournisseur | Très bon rapport qualité/prix, offre gratuite avec crédits | Très utilisé pour la publication quotidienne ([Fluxnote](https://fluxnote.io/guides/ai-video-model-pricing-comparison-2026)) |
| Seedance 2.0 (ByteDance) | dès \~0,04 $/s (version Fast) | Peu cher, beaucoup de contrôle créatif | Via API tierces (fal.ai, Atlas Cloud…) |
| Wan 2.x (Alibaba, open source) | Gratuit si GPU perso, sinon quelques centimes | Aucun abonnement | Demande une carte graphique puissante ou un GPU loué |
| Runway Gen-4.5 | Abonnement | Contrôle fin du mouvement | Plus orienté création manuelle |
| OpenAI Sora 2 | — | — | **Fermé** : app arrêtée en avril 2026, API arrêtée le 24 septembre 2026 ([Rangy](https://rangy.ai/blog/ai-video-generators-compared-2026)). À écarter |

Ordre de grandeur : un Reel de 15 s coûte 0,50 à 6 $ selon le modèle, avant les ratés. Compte 2 à 3 générations par plan retenu.

### Images et cohérence du physique

Ton idée de générer d'abord des images de référence est la bonne : on crée une **fiche personnage** (visage de face, profil, 3/4, plein pied, 3-4 tenues), puis chaque vidéo part d'une image générée à partir de ces références (image-to-video).

| Approche | Outil | Coût | Quand l'utiliser |
| --- | --- | --- | --- |
| Références sans entraînement | Nano Banana 2 / Pro (Google Gemini), Seedream (ByteDance) | Gratuit en quantité limitée (Google AI Studio), puis quelques centimes par image \[approximatif\] | Pour démarrer : une à trois images de référence suffisent ([RunDiffusion](https://www.rundiffusion.com/nano-banana-2-consistent-character-images)) |
| Modèle entraîné sur le personnage (LoRA) | Flux + LoRA via fal.ai, Replicate ou ComfyUI | Quelques dollars par entraînement | Si le visage dérive malgré les références, ou pour un contrôle total |
| Studio tout-en-un | Higgsfield, OpenArt | Abonnement \~10-30 $/mois \[approximatif\] | Si tu veux une interface plutôt que du code |

**\[À PRÉCISER\]** Stocke la fiche personnage (images + description textuelle précise) dans un dossier que tous les agents lisent. C'est l'actif le plus précieux du projet.

### Voix et lip-sync (si elle parle)

- **Voix :** ElevenLabs (offre gratuite limitée, puis \~5-22 $/mois \[approximatif\]). Une seule voix figée pour la persona.
- **Synchronisation labiale :** Veo 3.1 et Seedance génèrent l'audio avec la vidéo ; sinon HeyGen ou Hedra pour faire parler une image.
- **Montage automatique :** FFmpeg (gratuit) pour assembler plans, sous-titres, musique et texte à l'écran ; CapCut si tu retouches à la main.

### Passer par un agrégateur

fal.ai, Replicate ou OpenRouter donnent accès à la plupart de ces modèles avec **une seule clé API et une seule facture**. C'est ce qui rend le système non rigide : changer de modèle = changer une ligne de config.

## Outils existants pour chaque étape

Ne recode pas ce qui existe : la plupart des briques s'achètent quelques dollars par mois. Les prix ci-dessous sont des ordres de grandeur, à recontrôler au moment de souscrire.

| Étape | Outil | Coût | Commentaire |
| --- | --- | --- | --- |
| Trends | Tableau de bord professionnel Instagram (audios tendance, statistiques) | Gratuit | À consulter à la main au début |
| Trends | TikTok Creative Center (hashtags, sons, vidéos tendance par pays) | Gratuit | Les tendances TikTok arrivent souvent sur Reels quelques jours après |
| Trends | Scrapers Apify (Instagram Reels, audio Instagram, TikTok Creative Center) | \~2 $ pour 1 000 résultats ([Apify](https://apify.com/kinaesthetic_millionaire/instagram-reels-audio-scraper)) | Branchables directement sur Claude via MCP : l'agent "Trends" peut les appeler seul |
| Trends | Google Trends | Gratuit | Pour les sujets, pas pour les formats |
| Trends | Veille de comptes concurrents | Gratuit (manuel) ou Apify | Lister 10-20 comptes IA et humains de ta niche ; l'agent analyse leurs Reels les plus vus |
| Orchestration | n8n | Gratuit en auto-hébergé, \~20 €/mois en cloud \[approximatif\] | Enchaîne les étapes visuellement, planifie, gère les erreurs |
| Orchestration | Make / Zapier | Offre gratuite limitée | Plus simple que n8n, plus cher à volume |
| Orchestration | Claude Agent SDK / Claude Code + scripts Python | Coût API seulement | Plus flexible, demande du code |
| Publication | Metricool, Buffer, Later | Offre gratuite ou \~10-20 €/mois \[approximatif\] | Planification + statistiques ; vérifier qu'ils ont une API |
| Publication | Postproxy, Publora, bundle.social | Abonnement API | Conçus pour être appelés par un programme |
| Analyse | API Instagram Insights (via ton app ou l'outil de publication) | Gratuit | Vues, temps de visionnage, partages, sauvegardes, abonnés gagnés |
| Stockage | Google Sheets ou Airtable comme tableau de bord du pipeline | Gratuit | Une ligne par vidéo : idée, statut, coût, URL, résultats |
| Validation | Bot Telegram ou Slack qui t'envoie la vidéo avec boutons Valider / Refaire | Gratuit | Le moyen le plus simple de garder un humain dans la boucle depuis ton téléphone |

**Raccourci possible :** des plateformes "tout-en-un" d'influenceurs IA existent (Higgsfield, ou des services de création d'avatar). Elles vont plus vite mais t'enferment. Pour un système qui doit aussi faire de la pluie sur YouTube, une architecture maison avec des briques interchangeables est préférable.

## Monétisation : Instagram vs YouTube

Instagram ne te paiera presque rien à la vue : il sert à construire une audience que tu monétises ailleurs. YouTube paie à la vue, mais les seuils sont hauts et le contenu IA répétitif est exclu.

### Instagram

- **Pas de paiement direct à la vue pour la plupart des créateurs** : le programme de bonus Reels a pris fin en 2023 et ce qui reste est limité et sur invitation ([Stack Influence](https://stackinfluence.com/how-to-get-paid-on-instagram-reels/), [Lilach Bullock](https://www.lilachbullock.com/does-instagram-pay-creators-for-reels/)).
- **Ce qui rapporte vraiment :** partenariats de marque, affiliation (liens produits), abonnements payants, cadeaux (Gifts), et vente ou renvoi vers une autre plateforme.
- Ordre de grandeur en Europe de l'Ouest : 150 à 800 € par post sponsorisé selon l'audience ([Fluxnote](https://fluxnote.io/guides/instagram-earnings-europe-2026)). Les marques sont souvent plus prudentes avec un influenceur IA.
- Beaucoup de comptes d'IA-girls renvoient vers des plateformes d'abonnement externes. Si c'est ton plan, décide-le explicitement : cela change la ligne éditoriale, les risques de bannissement et le cadre légal. **\[À PRÉCISER\]**

### YouTube

| Élément | Aujourd'hui | À partir du 1er février 2027 |
| --- | --- | --- |
| Entrée dans le Programme Partenaire (pubs) | 1 000 abonnés + 4 000 h de visionnage sur 12 mois, ou 10 M de vues Shorts sur 90 jours | 1 000 abonnés + 8 000 h, ou 20 M de vues Shorts sur 90 jours |
| Revenus Shorts | 45 % de ta part du pot publicitaire Shorts | Il faut maintenir 10 M de vues Shorts sur 90 jours glissants pour toucher la part Shorts chaque mois |
| Revenus vidéos longues | 55 % des revenus pub de la vidéo \[connaissance générale\] | Inchangé |

Sources : [AIR Media-Tech](https://air.io/en/monetization/youtube-partner-program-requirements-2026-the-complete-guide), [Elev8or](https://www.elev8or.io/blog/bio/youtube-shorts-creator-pool-2027). Conclusion : les seuils doublent début 2027, la monétisation des Shorts devient très difficile pour un petit compte. Les vidéos longues sont plus accessibles.

### Alerte sur ton idée "bruit de pluie"

YouTube exclut de la monétisation le contenu "inauthentique" : vidéos génériques, répétitives ou basées sur des modèles quasi identiques, produites en masse par IA ([TechRepublic](https://techrepublic.com/article/news-youtube-ai-video-monetization-rules)). Des chaînes de pluie de 10 h quasi identiques sont exactement dans la cible. Pour passer, chaque vidéo doit avoir une vraie valeur propre : ambiances distinctes, séries thématiques, visuels soignés, et un apport humain visible.

**Précision utile pour l'IA qui construira le projet :** ces règles changent souvent. L'agent "Analyse" doit vérifier chaque trimestre les règles de monétisation des plateformes cibles.

### Quelle plateforme est la plus rentable ?

Aucune ne rend riche par les vues seules. Pour une IA-girl, la vue à la vue paie peu partout ; la vraie rentabilité vient de ce que tu vends à l'audience. Les plateformes servent surtout à attirer du monde.

| Plateforme | Paiement aux vues | Ce qu'il faut pour être payé | 1 M de vues rapporte environ | Rôle dans ton projet |
| --- | --- | --- | --- | --- |
| TikTok | Oui, France éligible (Creator Rewards) | 10 000 abonnés, vidéos de **plus de 60 s** uniquement, contenu original | \~400-600 $ en France ([Elev8or](https://www.elev8or.io/tools/tiktok-creator-rewards-calculator)) | Meilleur canal de découverte ; paie le mieux à la vue si format > 1 min |
| YouTube (vidéos longues) | Oui | 1 000 abonnés + 4 000 h (8 000 h dès février 2027) | Très variable, souvent plusieurs centaines à milliers de $ | Le plus solide sur la durée, adapté à la pluie |
| YouTube Shorts | Oui | 1 000 abonnés + 10 M de vues Shorts / 90 jours | \~10-50 $ ([Vidpros](https://vidpros.com/youtube-shorts-monetization-in-2026)) | Faible ; seuil très haut |
| Instagram Reels | Quasiment non en France | Programmes sur invitation | \~0 $ en direct | Vitrine pour les marques et pour renvoyer vers tes offres |

**Verdict :** TikTok + Instagram pour l'audience de l'IA-girl, YouTube long pour la pluie. Publier la même vidéo sur les trois coûte presque rien en plus : le système doit être **multi-plateforme dès le départ**. TikTok exige aussi d'étiqueter le contenu IA réaliste. \[À vérifier : TikTok peut exclure du Creator Rewards un contenu entièrement IA jugé "non original"\]

### Plateformes d'abonnement : le contenu IA est-il autorisé ?

OnlyFans : non pour une persona 100 % IA. Fanvue : oui, c'est la plateforme qui s'est positionnée sur les créateurs IA.

| Plateforme | Persona 100 % IA autorisée ? | Conditions | Commission |
| --- | --- | --- | --- |
| [Fanvue](https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue) | Oui | Indiquer clairement que c'est de l'IA ; vérification d'identité (KYC) de toi, l'opérateur ; aucune ressemblance avec une personne réelle sans consentement | 20 % (tu gardes 80 %) ([AI Creator Ops](https://ai-creator-ops.vercel.app/platforms/fanvue)) |
| OnlyFans | Non | L'IA n'est permise que si le contenu montre le créateur vérifié lui-même ([Aruna Talent](https://arunatalent.com/blog/onlyfans-ai-content-policy-2026)) | 20 % |
| Fansly | Non pour l'IA photoréaliste | Interdite depuis juin 2025 ([Sirency](https://www.sirency.com/blog/fanvue-alternatives-for-creators)) | 20 % |
| Patreon | Non pour l'IA hyperréaliste sur les pages adultes | Les personnages IA illustrés ou animés sont acceptés | \~10 % selon offre |

**Ce que ça implique pour toi :**

- Fanvue autorise aussi le contenu adulte dans des espaces réservés aux abonnés vérifiés. C'est le modèle de la plupart des comptes d'IA-girls qui gagnent de l'argent. Ce n'est pas une obligation : un abonnement "tout public" (photos exclusives, coulisses, messages) est possible aussi.
- **Décision à prendre \[À PRÉCISER\] : adulte ou tout public.** Elle change tout le reste. Un compte qui renvoie vers du contenu adulte ne décrochera presque pas de partenariats de marque grand public, et Instagram/TikTok surveillent de près les liens vers ces sites.
- Si tu vas vers l'adulte : règles plus strictes partout (aucune apparence juvénile, aucune ressemblance avec une vraie personne), déclaration des revenus, et image publique à assumer.
- Le chat avec les abonnés est souvent la première source de revenus sur ces plateformes. Fanvue propose des outils IA pour ça ; OnlyFans interdit les chatbots en messages privés.

## Business model

Scénario le plus probable : la première année coûte plus qu'elle ne rapporte, et seule une petite minorité de comptes dépasse 1 000 $ par mois. Le marché est saturé : plus de 200 000 comptes d'influenceurs IA actifs sur Instagram et TikTok, dont moins de 2 000 dépassent 1 000 $ par mois, selon une analyse HypeAuditor 2026 citée par [Oakgen](https://oakgen.ai/blog/ai-influencer-monetization-guide). Les chiffres "20 000 $/mois" qui circulent viennent surtout de vendeurs d'outils.

### Les sources de revenus, par ordre d'arrivée

| Source | À partir de | Ordre de grandeur | Remarque |
| --- | --- | --- | --- |
| Affiliation (liens produits : mode, beauté, outils IA) | Dès le début | 5-30 % de commission par vente | Fonctionne même avec peu d'abonnés si la niche achète |
| Abonnement payant (Fanvue, Instagram Abonnements, Patreon) | \~1 000-5 000 abonnés | 5-15 €/mois par abonné, 80 % pour toi | Taux de conversion réaliste : 0,2 à 1 % de l'audience \[estimation\] |
| TikTok Creator Rewards | 10 000 abonnés + vidéos > 1 min | \~0,6 $ pour 1 000 vues qualifiées en France | Complément, pas un modèle |
| Partenariats de marque | \~10 000 abonnés avec 2 %+ d'engagement | 150-800 € par post en Europe de l'Ouest | Plus difficile si le compte renvoie vers de l'adulte |
| YouTube (chaîne pluie, longues vidéos) | 1 000 abonnés + 4 000 h | Variable | Revenus lents mais durables, si le contenu passe la règle "inauthentique" |
| **Vendre le système lui-même** | Dès qu'il marche | Prestation ou abonnement B2B | Voir ci-dessous : c'est peut-être ton meilleur actif |

### Trois scénarios à 12 mois (estimations)

Hypothèses : 1 compte IA-girl tout public, publié sur Instagram + TikTok, 1 puis 3 vidéos/jour, coûts de 100 à 250 €/mois.

| Scénario | Abonnés à 12 mois | Revenus mensuels au mois 12 | Résultat sur l'année | Probabilité |
| --- | --- | --- | --- | --- |
| Pessimiste | < 5 000 | 0-200 € | Perte de 1 500 à 2 500 € | Le cas le plus fréquent |
| Réaliste (bonne exécution) | 10 000-50 000 | 300-1 500 € | Autour de l'équilibre | Possible avec une niche claire et de la régularité |
| Optimiste (top \~1 %) | 100 000+ | 3 000-10 000 € et plus | Nettement positif | Rare : demande un vrai succès viral et une persona forte |

Exemple de calcul pour l'abonnement : 30 000 abonnés × 0,3 % convertis × 8 € × 80 % = environ 580 € par mois.

### Le business model cohérent que je te propose

1. **Un moteur, un portefeuille de chaînes.** Plutôt que tout miser sur une IA-girl, lancer 2-3 chaînes à coût marginal faible (IA-girl, pluie/ambiance sur YouTube, une niche utile type "astuces" ou "faits"). On garde celles qui décollent, on coupe les autres après 90 jours.
2. **Audience gratuite → offre payante.** TikTok et Instagram attirent, un lien en bio renvoie vers une offre que tu contrôles : abonnement, affiliation, produits numériques.
3. **Capter l'audience hors plateforme dès le début** (liste email ou canal Telegram) : une plateforme peut supprimer un compte du jour au lendemain.
4. **Vendre le système.** Si ton pipeline produit 3 vidéos par jour de qualité constante pour 5 € pièce, des marques et des créateurs paieront pour ça. C'est le revenu le moins risqué : il ne dépend pas de l'algorithme.
5. **Règle de pilotage :** budget plafonné à 250 €/mois ; point d'étape à 3 mois. Si aucune chaîne n'a dépassé 5 000 abonnés ou 1 % d'engagement, on change de niche ou de format.

### Plateformes d'avatar type Higgsfield : gratuites ?

Non, pas vraiment. Higgsfield a une offre gratuite **sans crédits de génération** et sans droit d'usage commercial ([Creatify](<https://creatify.ai/blog/is-higgsfield-free-free-plan-trials-and-promo-codes-explained-(2026)>)). Les offres payantes, vérifiées en octobre 2026 ([HeyGen](https://www.heygen.com/blog/higgsfield-pricing)) :

| Offre | Prix mensuel | Prix annuel (par mois) |
| --- | --- | --- |
| Starter | 19 $ | — |
| Plus | 59 $ | 47 $ |
| Ultra | 129 $ | 99 $ |

Les crédits ne se reportent pas d'un mois à l'autre, et les prix varient selon le pays. Higgsfield donne accès à Kling 3.0, Veo 3.1, Seedance 2.0 et Nano Banana Pro dans une seule interface, avec un outil de personnage constant (Soul ID). **Mon avis :** utile pour prototyper vite à la main pendant 1 mois ; pour l'automatisation, passer directement par les API (fal.ai, Google) reste moins cher et plus flexible. Alternatives comparables : OpenArt, ImagineArt (à partir d'environ 9 $/mois).

## Budget estimé et plan de démarrage

Pour 1 Reel par jour de bonne qualité, compte environ 40 à 120 $ par mois ; pour 3 par jour, environ 120 à 350 $. Hypothèses : Reel de 15 s, 2,5 générations par plan retenu, modèles vidéo entre Veo 3.1 Lite (0,03 $/s) et Kling 3.0 (\~0,07 $/s). Ce sont des estimations, pas des devis.

| Poste | 1 vidéo/jour | 3 vidéos/jour |
| --- | --- | --- |
| Génération vidéo | 35-80 $ | 100-240 $ |
| Génération d'images | 0-10 $ | 5-20 $ |
| Cerveau (Claude/ChatGPT par API) | 5-15 $ | 10-30 $ |
| Trends (Apify) | 0-5 $ | 5-10 $ |
| Publication + analyse (outil tiers) | 0-20 $ | 0-20 $ |
| Voix (si elle parle) | 0-5 $ | 5-22 $ |
| **Total indicatif** | **\~40-120 $/mois** | **\~120-350 $/mois** |

**Version 100 % gratuite possible pour le prototype :** crédits gratuits Kling, Google AI Studio pour les images, offres gratuites des LLM, publication manuelle. Suffisant pour produire 5-10 vidéos de test, pas pour tenir un rythme quotidien.

### Plan de démarrage proposé

1. **Semaine 1 : fondations.** Remplir le tableau "À préciser", rédiger la fiche persona, créer le compte et commencer à le chauffer.
2. **Semaine 2 : personnage.** Générer la fiche personnage (20-30 images de référence), valider à la main la cohérence du visage.
3. **Semaines 3-4 : production manuelle assistée.** Produire 10 vidéos "à la main" avec l'aide de l'IA, pour savoir ce qui marche avant d'automatiser.
4. **Semaines 5-6 : automatisation.** Brancher les agents un par un (trends → scénario → production → contrôle), toi en validation finale. 1 vidéo/jour.
5. **Mois 2-3 : boucle d'apprentissage.** L'agent Analyse compare les résultats et ajuste les scénarios. Monter à 2 puis 3 vidéos/jour seulement si le taux de visionnage tient.
6. **Ensuite : nouvelle chaîne.** Réutiliser le même moteur avec une nouvelle config (ex. pluie sur YouTube) pour valider que le système n'est pas rigide.

## Sources

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

* [Elev8or : calculateur TikTok Creator Rewards](https://www.elev8or.io/tools/tiktok-creator-rewards-calculator)
* [Vidpros : revenus YouTube Shorts 2026](https://vidpros.com/youtube-shorts-monetization-in-2026)
* [Fanvue : le contenu IA est-il autorisé ?](https://help.fanvue.com/en/articles/9538738-is-ai-content-allowed-on-fanvue)
* [AI Creator Ops : fiche Fanvue](https://ai-creator-ops.vercel.app/platforms/fanvue)
* [Aruna Talent : politique IA d'OnlyFans 2026](https://arunatalent.com/blog/onlyfans-ai-content-policy-2026)
* [Sirency : alternatives à Fanvue et règles IA](https://www.sirency.com/blog/fanvue-alternatives-for-creators)
* [Oakgen : guide de monétisation des influenceurs IA](https://oakgen.ai/blog/ai-influencer-monetization-guide)
* [Creatify : Higgsfield est-il gratuit ?](<https://creatify.ai/blog/is-higgsfield-free-free-plan-trials-and-promo-codes-explained-(2026)>)
* [HeyGen : prix de Higgsfield (octobre 2026)](https://www.heygen.com/blog/higgsfield-pricing)
