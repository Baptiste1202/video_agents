Léna Reyes — Passage à l'automatisation : décisions
9 nov. 2026 · @Baptiste
On garde l'offre Gemini étudiante, on produit en mode manuel assisté, on publie TikTok en semi-automatique, et la niche n'est pas encore validée.
1. Passer à Claude Code : oui
La conversation ne se transfère pas, mais l'essentiel est déjà dans les fichiers.
1. Mettre BRIEF.md, ROADMAP.md, memo.md, persona.md et ai_girl.yaml dans le dossier VS Code, aux emplacements prévus par le brief.
2. Créer CLAUDE.md avec une ligne : « Lis BRIEF.md et ROADMAP.md avant toute tâche. »
3. Premier message : « On attaque la phase 3 de ROADMAP.md : squelette du moteur en mode manuel. Propose-moi un plan avant de coder. »
2. Louer de la RAM ou du CPU : non
La génération vidéo tourne sur la carte graphique (VRAM), pas sur le processeur. Il faudrait louer un GPU (RTX 4090 à ~0,35 $/h), mais à ce stade l'installation est lourde et la qualité inférieure à Google.
3. Abonnement Flow plus cher : non
• L'offre étudiante Pro est gratuite : on la garde pour produire à la main.
• L'offre Ultra coûte 100 $/mois ou plus.
• Aucun abonnement ne donne accès à l'API, celle dont les agents ont besoin.
Modèle API
Prix
Clip de 8 s
30 vidéos / mois (avec un essai raté)
gemini-omni-1.1-flash (remplace les Veo en préversion, retirés le 22 octobre 2026)
~0,10 $/s en 720p
~0,80 $
~25 à 50 $
4. Automatiser la publication TikTok
Avec l'API officielle, tant que l'application n'a pas passé l'audit de TikTok, toutes les publications restent privées. Une application à usage interne ne passe pas cet audit.
Option
Coût
Quand
Semi-automatique : le système prépare vidéo, légende et hashtags ; programmation de la semaine dans TikTok Studio (15 min)
Gratuit
Maintenant
Outil tiers déjà audité par TikTok, publication publique dès le premier envoi
Abonnement
Quand le volume le justifie
5. Rémunération à la vue : un complément, pas un modèle
• Creator Rewards ne paie que les vidéos de plus d'une minute, à partir de 10 000 abonnés et 100 000 vues sur 30 jours, avec du contenu original.
• Les clips de 8 s ne rapportent rien.
• France : ~0,60 $ pour 1 000 vues qualifiées, soit ~600 $ pour 1 million de vues par mois.
• Meilleure piste : vendre le système à d'autres créateurs. Pour viser Creator Rewards, il faut un format de plus de 60 s (par exemple, une journée de Léna en plusieurs plans).
6. Produire sans API payante : le mode manuel
• Le système génère les prompts, choisit les tenues, écrit les textes à l'écran et les légendes.
• L'humain génère images et vidéos dans Gemini et Flow, puis les dépose dans un dossier.
• Le système monte (texte, musique, coupe), range et prépare la publication.
• Étape suivante : un test à 20 $ sur l'API pour comparer la qualité et vérifier l'enchaînement.
7. La niche n'est pas encore validée
État actuel : 8 abonnés, 900 vues au maximum. Signaux encourageants : 5 % de likes, un public féminin qui accroche, le format « tenue du jour » devant.
Critères de validation, sur 3 semaines de publication quotidienne :
[ ] Au moins 30 % des vidéos dépassent 1 000 vues
[ ] Au moins 50 nouveaux abonnés par semaine
[ ] Durée de visionnage moyenne supérieure à 60 % sur les meilleurs formats
Sources
• Developers Digest : modèles vidéo de l'API Gemini et dates de retrait
• Layer3 Labs : prix de Veo et gemini-omni-1.1-flash
• TikTok for Developers : Direct Post et clients non audités
• Ayrshare : audit de l'API TikTok
• Blotato : outil de publication TikTok audité
• TT Calculator : conditions de Creator Rewards