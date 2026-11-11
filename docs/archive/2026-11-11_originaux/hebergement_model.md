Héberger un modèle vidéo : parcours d'apprentissage
9 nov. 2026 · @Baptiste
La RTX 3050 sert de banc d'essai pour apprendre toute la chaîne ; le GPU loué prend le relais pour les gros modèles et l'entraînement.
Ce que la RTX 3050 peut faire
Tout dépend de sa VRAM (nvidia-smi pour la connaître).
VRAM
Possible
Usage
8 Go (PC fixe)
Wan 2.2 TI2V-5B en FP8 avec déchargement en RAM ; LTX-Video distillé ; Wan 14B quantifié en GGUF Q3/Q4 en 480p (lent)
Banc d'essai complet
4-6 Go (portable)
Génération d'images (SDXL, Flux quantifié) ; vidéo 5B en 480p très lent
Apprendre le pipeline, pas la vidéo
Sujets à creuser sur la 3050 :
• Le pipeline de Wan : encodeur de texte UMT5, DiT, VAE 3D. Décharger l'encodeur de texte en RAM libère beaucoup de VRAM.
• La quantification FP8 face au GGUF, et l'impact réel sur la qualité.
• Les accélérations de l'attention et la mise en cache entre étapes de débruitage (SageAttention, TeaCache), à mesurer soi-même.
• Le profilage : pic de VRAM, temps par image, goulots d'étranglement.
Week-end avec un GPU loué
Une RTX 4090 ou 5090 (24-32 Go), avec un volume réseau persistant pour ne pas retélécharger les poids (plusieurs dizaines de Go) à chaque session.
1. Image Docker avec ComfyUI sur RunPod ou Vast, les modèles sur le volume réseau.
2. Wan 2.2 14B image-to-video en FP8, en 720p : générer à partir des images de Léna et comparer avec Omni.
3. Pilotage par API : ComfyUI expose une API HTTP (/prompt pour envoyer un workflow exporté en JSON, puis récupération des sorties). Écrire un client Python : c'est le provider comfyui / wan_rented_gpu du BRIEF.md.
4. Automatisation du serveur : démarrage à la demande, traitement de la file de jobs, arrêt automatique après X minutes d'inactivité, suivi du coût par vidéo.
5. Bonus : tester LTX-2.3 pour le son généré avec la vidéo.
Étape suivante : un LoRA pour Léna
Le sujet le plus formateur, et celui qui règle la cohérence du visage.
• Jeu de données : 25 à 40 images validées de Léna (angles, lumières, tenues variées), légendées, avec un mot déclencheur du type lenareyes woman.
• Entraînement d'un LoRA Wan 2.2 : outils open source comme musubi-tuner, diffusion-pipe ou ai-toolkit. Il faut 24 Go de VRAM ou plus, donc sur le GPU loué.
• En option : un LoRA image (Flux ou équivalent) pour générer les images de départ sans dépendre de Gemini.
Les versions et options évoluent vite : vérifier la documentation de chaque outil au moment de l'installer.
Licences :
Modèle
Licence
Utilisable
Wan 2.2
Apache 2.0
Oui
LTX
Communautaire, gratuite sous 10 M$ de CA
Oui
HunyuanVideo 1.5
Exclut l'UE
Non
Plan semaine par semaine
Quand
Matériel
Objectif
Cette semaine
RTX 3050
Installer ComfyUI, faire tourner Wan 5B ou LTX, profiler, tester la quantification, écrire le client Python de l'API
Ce week-end
RTX 4090 louée
Wan 14B en 720p sur Léna, comparaison avec Omni, arrêt automatique, coût par clip
Semaine suivante
RTX 4090 louée
Constituer le jeu de données et entraîner le LoRA de Léna
Ensuite
Selon le volume
Provider wan_rented_gpu en production, ou achat d'une RTX 3090 d'occasion si le volume le justifie