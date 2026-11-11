# Prompts — Images de référence, scènes et vidéos (Léna Reyes)

> Outils : Nano Banana (app Gemini) pour les images, Flow pour les vidéos (choix du modèle : `BRIEF.md` §5).
> `[BASE]` = le prompt de base (§0). Fiche persona : `../persona.md`.
> Règle d'or : on crée d'abord chaque élément **seul** (Léna, le chien, l'appartement, le café, les tenues), puis on les **assemble** dans des scènes en joignant leurs références.
> Quand plusieurs images sont jointes, les nommer dans le prompt : "the woman from image 1", "the dog from image 2", "the room from image 3". Maximum 3 images de référence par génération.

## 0. Prompt de base `[BASE]`

`[BASE]` = **BASE 3**, recopié dans `persona.md` §2 (seule version valable depuis le 11 nov. ; les anciennes versions sont dans `docs/archive/`).

```
24-year-old strikingly beautiful woman of predominantly Filipino and East Asian heritage with a subtle touch of French ancestry, fresh youthful face, harmonious symmetrical oval face, soft rounded high cheekbones, soft delicate jawline, striking piercing ice-blue almond-shaped eyes, very pale crystal-clear blue irises with a thin darker blue limbal ring, bright catchlights, an intense captivating gaze, the light eyes contrasting strongly with her warm golden skin and dark lashes, long dark lashes, softly arched dark eyebrows, small refined nose, full naturally shaped lips, long thick straight glossy dark brown hair, fair skin with a warm golden tan, smooth natural skin texture with a subtle healthy glow, exactly two beauty marks: one on the left cheekbone and one on the right side of the neck, no tattoos, athletic toned build with a fuller natural bust, narrow defined waist and very full round lifted glutes, 165 cm tall, light natural makeup
```

**À ajouter à chaque prompt :**

```
Her piercing ice-blue eyes are clearly visible, sharp and in focus.
```

**Retouche si les yeux ne sont pas bons** (joindre en image 2 une image où les yeux sont réussis) :

```
Make her eyes the same striking piercing ice-blue as image 2, clearly visible, keep everything else identical
```

## 1. Arborescence

Convention de nommage : `snake_case` anglais, `<sujet>_<détail>[_nn]`. Les références (`refs/`) sont jointes aux générations ; le contenu (`content/`) n'est jamais utilisé comme référence ; les inspirations (`inspiration/`) montrent de vraies personnes et ne sont **jamais** jointes.

```
personas/ai_girl/
  persona.md
  analytics/                exports TikTok
  refs/
    prompts.md
    lena/       face_master.jpg  face_master_alt.jpeg  face_left_profile.jpeg  face_three_quarter.jpeg
                expr_warm_smile  expr_laughing  expr_mysterious  expr_thoughtful
                body_sheet_bodysuit.jpeg  body_sheet_gym_grey.jpeg  archive/body_sheet_gym_black.jpeg
    dog/        praline_master.jpeg  praline_sheet.jpeg
    places/     apt_living.jpeg  apt_kitchen.jpeg   (à créer : apt_desk, cafe, gym)
    outfits/    outfit_casual_black_top_jeans  outfit_cosplay_elf_armor  outfit_evening_sage_slip_dress
                outfit_gym_brown_set  outfit_navy_slip_dress  outfit_preppy_brown_sweater
                outfit_pyjama_polka_dot  outfit_pyjama_white_romper  outfit_run_mauve_bra_white_shorts
                outfit_trench_leather_skirt
    series/     hi_there/base_black_knit.jpeg
  content/
    photos/     images générées (publiées ou à publier), ex. navy_dress_apt_01..07, cosplay_elf_armor_01..05
    broll/      plans sans le visage de Léna (café, chantier…)
    videos/raw/ clips Flow
inspiration/
  inbox/        captures Pinterest à traiter (tenues)
  archive/      captures déjà transformées en fiches outfits/
  ideas/        idées de formats et de poses (captures, enregistrements d'écran)
```

## 2. Léna — images de référence

### Portrait maître

```
High-end beauty portrait photo, head and shoulders, facing the camera, soft confident expression, [BASE], hair down over one shoulder, plain light grey background, soft flattering studio lighting with gentle rim light, sharp focus on the eyes, photorealistic, natural skin texture, editorial magazine quality, 85mm lens
```

### Planche corps 4 vues — joindre le portrait maître

```
Character reference sheet of the same woman as in the reference image, four full-body views side by side: front, three-quarter, side profile, back. [BASE], hair in a high ponytail, wearing a fitted black sports bra and high-waisted black compression leggings, barefoot, confident upright stance, shoulders back, arms relaxed, fit athletic figure with a defined waist and toned abs, plain light grey background, even studio lighting, photorealistic, fitness model reference photography, consistent face and proportions across all views
```

### 03 à 05. Gros plans visage — joindre le portrait maître ; un prompt par angle

(Noté « à faire » le 6 nov. ; `03_left_side` et `03_three_quarter` existent depuis.)

```
Close-up studio portrait of the same woman as in the reference image, [ANGLE: facing the camera / left side profile / three-quarter view turned right], neutral expression, [BASE], hair tied in a high ponytail so the face and ears are fully visible, plain light grey background, soft studio lighting, photorealistic, 85mm lens
```

### Plein pied

```
Full-body studio photo of the same woman as in the reference image, standing straight, facing the camera, [BASE], hair in a high ponytail, plain fitted grey tank top and black leggings, white sneakers, plain light grey background, even studio lighting, photorealistic, 50mm lens
```

### 08. Expressions — une ligne par image

```
Studio portrait of the same woman as in the reference image, [EXPRESSION: warm genuine smile / laughing / mysterious half-smile looking at the camera / thoughtful looking away], [BASE], plain light grey background, soft studio lighting, photorealistic
```

## 3. Le chien : Praline

Références : `dog/praline_master.jpeg` (portrait) et `dog/praline_sheet.jpeg` (planche 4 vues). Les joindre comme « image 2 » dans les scènes.

Description à insérer dans les prompts de scène :

```
the English Cocker Spaniel dog from image 2, golden red wavy coat, long feathered ears, dark brown eyes, sage green collar with a small gold tag
```

(Les prompts d'origine pour « Mochi », un Shiba Inu, sont abandonnés ; ils restent dans `docs/archive/`.)

## 4. Les lieux (sans Léna)

> Générer chaque lieu **vide**, puis s'en servir comme décor fixe. C'est ce qui rend son univers crédible et reconnaissable.

### 4a. Salon de l'appartement — aucune référence

```
Interior photo of a bright Parisian Haussmann apartment living room, tall windows with wrought-iron balconies overlooking Paris rooftops, herringbone oak parquet floor, white walls with ornate moldings, marble fireplace, cream bouclé sofa, sage green velvet armchair, light oak coffee table with architecture books, large green plants, a framed architectural blueprint on the wall, warm natural morning light, minimalist and elegant decor, photorealistic, wide angle, no people
```
→ `places/apt_living.jpeg` (existe)

### 4b. Cuisine — joindre : `apt_living`

```
Interior photo of the kitchen of the same Parisian Haussmann apartment as in the reference image, same parquet floor, same moldings and decor style, white marble countertop, light oak cabinets, brass fixtures, a small espresso machine, a bowl of fruit, tall window with morning light, photorealistic, no people
```
→ `places/apt_kitchen.jpeg` (existe)

### 4c. Bureau d'architecte à la maison — joindre : `apt_living`

```
Interior photo of a home office corner in the same Parisian Haussmann apartment as in the reference image, large light oak desk by a tall window, architectural drawings and sketches spread on the desk, a white cardboard architecture scale model of a modern building, drafting pencils, a laptop showing a 3D building model, a desk lamp, a coffee cup, plants, warm afternoon light, photorealistic, no people
```
→ `places/apt_desk.jpeg`

### 4d. Le café du Marais — aucune référence

```
Photo of a small cozy coffee shop in the Marais district of Paris, large front window facing a cobblestone street, small marble tables, bentwood chairs, light oak counter with pastries, specialty coffee machine, warm soft daylight, plants, minimalist Scandinavian-Parisian decor, photorealistic, no people
```
→ `places/cafe.jpeg`

### 4e. La salle de sport

Reprendre l'une des photos de salle réussies, ou générer :

```
Interior photo of a modern industrial-style gym, large tall windows with natural light, black squat racks, dumbbell rack, rubber floor, exposed concrete ceiling, warm golden light, clean and premium, photorealistic, no people
```
→ `places/gym.jpeg`

## 5. Les tenues (planches studio)

> Chaque tenue est générée une fois en studio, en pied. Ensuite, on la joint quand Léna la porte dans une scène.
> Joindre pour chaque tenue : portrait maître + planche corps.
> À terme, les tenues viennent de l'agent Style (`outfits/*.yaml`, `BRIEF.md` §6) et respectent ses règles (pas de moulant beige/nude, « thick opaque fabric » pour les bas).

Modèle commun :

```
Full-body studio photo of the same woman as in the reference images, [BASE], standing in a relaxed natural pose, wearing [TENUE], plain light grey background, soft even studio lighting, photorealistic, fashion lookbook style
```

Prompts d'origine (6 nov.). Les fichiers réellement générés dans `outfits/` ne correspondent pas tous à ces descriptions (ex. `outfit_trench_leather_skirt` : trench sur jupe en cuir et bottes) ; certains n'ont pas encore été générés (`work`, `cozy`, `gym_pink`).

| Fichier prévu | [TENUE] |
| --- | --- |
| `outfit_trench_01` | a beige trench coat open over a cream ribbed knit top, high-waisted straight blue jeans, white leather sneakers, small chocolate brown leather shoulder bag, hair down |
| `outfit_work_01` | a crisp white oversized shirt tucked into high-waisted chocolate brown tailored trousers, thin brown leather belt, beige loafers, minimal gold earrings, hair in a low sleek ponytail |
| `outfit_cozy_01` | an oversized cream cable-knit sweater, matching soft beige knit lounge shorts, fuzzy socks, hair in a messy bun |
| `outfit_run_01` | a pastel pink sports bra, opaque white high-waisted running shorts, light pink running jacket tied around the waist, white running shoes, black smartwatch on the left wrist, high ponytail |
| `outfit_gym_pink` | a pastel pink sports bra and opaque white high-waisted seamless leggings, white sneakers, black smartwatch on the left wrist, high ponytail |
| `outfit_gym_brown` | a matching chocolate brown ribbed sports bra and high-waisted seamless leggings, black smartwatch on the left wrist, high ponytail |
| `outfit_evening_01` | an elegant sage green satin midi slip dress with a light beige blazer over the shoulders, strappy nude heels, hair down in soft waves, subtle gold jewelry |

**Changer la tenue d'une image existante** (retouche) :

```
Change her outfit to a pastel pink sports bra and opaque white high-waisted seamless leggings, keep her face, hair, body shape, pose, lighting and background exactly identical
```

## 6. Scènes (assemblage)

> Ces images vont dans `content/`, pas dans `refs/`.

### 6a. Gabarit générique de scène — joindre : 3 images du visage (1, 2, 3) + planche corps (4)

```
The same woman from images 1, 2 and 3, with her exact face and piercing ice-blue eyes. Use image 4 only as a reference for her body shape and proportions. Vertical 3:4 photo, [BASE], [COIFFURE], wearing [TENUE], [ACTION ET LIEU], [REGARD], [LUMIÈRE], shot on a 35mm lens from about two meters away, natural perspective, no wide-angle distortion, photorealistic. Exactly two small beauty marks on her face and neck, no other marks. Her piercing ice-blue eyes are clearly visible, sharp and in focus.
```

⚠ Ce gabarit utilise 4 images jointes, au-delà de la règle « 3 max » de l'en-tête.

### 6b. Fitness lifestyle à la salle — joindre le portrait maître

```
Fitness lifestyle photo of the same woman as in the reference image, [BASE], wearing a matching sage green sports bra and high-waisted seamless scrunch leggings, standing in a three-quarter back view, looking over her shoulder at the camera with a confident captivating gaze, one hand on her hip, weight shifted onto one leg, athletic hourglass figure with a narrow waist, strong sculpted glutes and toned legs from glute training, toned arms and abs, slightly low camera angle, bright modern gym with natural window light, warm golden tones, shallow depth of field, photorealistic, high-end fitness magazine style
```

⚠ Vue de 3/4 dos : pour une vidéo, contraire à la règle d'accroche (visage face caméra dès la 1re seconde) si elle sert de première image.

### 6c. Matin dans l'appartement avec le chien
Joindre : portrait maître (image 1), chien (image 2), `apt_living` (image 3)

```
Photo of the woman from image 1 sitting on the cream sofa in the living room from image 3, with the English Cocker Spaniel dog from image 2 curled up next to her, [BASE], wearing an oversized cream cable-knit sweater and beige knit lounge shorts, hair in a messy bun, holding a cup of coffee, laughing softly while looking at the dog, warm morning light from the tall windows, candid lifestyle photography, photorealistic
```

### 6d. Architecte au travail (à la maison)
Joindre : portrait maître (image 1), `apt_desk` (image 2), `outfit_work_01` (image 3)

```
Photo of the woman from image 1 working at the desk from image 2, wearing the outfit from image 3, [BASE], sketching on an architectural drawing with a pencil, focused expression, slight smile, a white architecture scale model next to her, warm afternoon light from the window, candid lifestyle photography, photorealistic, shallow depth of field
```

### 6e. Au café du Marais
Joindre : portrait maître (image 1), `cafe` (image 2), `outfit_trench_01` (image 3)

```
Photo of the woman from image 1 sitting by the window at a small marble table in the coffee shop from image 2, wearing the outfit from image 3, [BASE], hair down, holding a cappuccino with latte art, sketchbook open on the table, looking out the window with a soft dreamy smile, warm natural daylight, candid Parisian lifestyle photography, photorealistic, 35mm lens
```

### 6f. Promenade avec le chien dans le Marais
Joindre : portrait maître (image 1), chien (image 2), `outfit_trench_01` (image 3)

```
Photo of the woman from image 1 walking the English Cocker Spaniel dog from image 2 on a leash on a cobblestone street in the Marais, Paris, wearing the outfit from image 3, [BASE], hair down moving slightly in the wind, glancing back over her shoulder at the camera with a warm smile, Parisian stone buildings and cafe terraces in the background, soft golden hour light, candid street photography, photorealistic
```

### 6g. Running sur les quais de Seine avec le chien
Joindre : portrait maître (image 1), chien (image 2), `outfit_run_01` (image 3)

```
Photo of the woman from image 1 jogging along the quays of the Seine in Paris with the English Cocker Spaniel dog from image 2 running beside her on a leash, wearing the outfit from image 3, [BASE], high ponytail, natural joyful expression, Eiffel Tower softly blurred in the distance, early morning golden light, dynamic motion, sports lifestyle photography, photorealistic
```

### 6h. Cuisine après la séance
Joindre : portrait maître (image 1), `apt_kitchen` (image 2), `outfit_gym_pink` (image 3)

```
Photo of the woman from image 1 in the kitchen from image 2, wearing the outfit from image 3, [BASE], making a smoothie bowl after her workout, high ponytail, relaxed happy expression, looking at the camera with a soft smile, bright morning light, candid lifestyle photography, photorealistic
```

## 7. Série « Hi there » (meilleur format, première série automatisée)

Principe : **une image de base fixe** (`series/hi_there/base_black_knit.jpeg`, Léna en haut noir côtelé devant le mur à lattes de bois) → **on change seulement la tenue** (tenues reprises de Pinterest, décrites en texte par l'agent Style) → **on anime** avec de légères variantes de mouvement → clip de 8 s, sans son (musique ajoutée dans TikTok).

### 7a. Image de base — joindre le portrait maître

```
Vertical 9:16 chest-up portrait of the same woman as in the reference image, [BASE], long straight glossy dark brown hair worn down, wearing a fitted black ribbed sleeveless mock-neck knit top, a gold square watch on her left wrist, thin gold bangle, small gold hoop earrings, a gold signet ring, standing against a warm brown vertical wooden slat wall, soft natural daylight, relaxed natural expression, looking slightly off-camera, realistic smartphone photo, sharp focus, high resolution, photorealistic
```

### 7b. Changer la tenue — joindre l'image de base

`[TENUE]` = la ligne « wearing … » de la fiche `outfits/<id>.yaml` (sans le mot « wearing »).

```
Keep this exact woman, face, ice-blue eyes, hair, pose, wooden slatted wall, lighting and chest-up framing unchanged. Change only her outfit: she is now [TENUE]. Remove the black ribbed top. Keep her gold watch and bracelet. Photorealistic, same smartphone photo look.
```

### 7c. Animation — prompt d'origine (vidéo qui a le mieux marché)

```
Animate this image as the exact first frame. One continuous single take, no cuts, same framing, same wooden wall, same outfit, chest-up shot. She moves smoothly and fluidly at natural speed like a relaxed photoshoot: first she runs both hands slowly through her hair with her eyes half-closed, then she tilts her head and looks into the camera with lips slightly parted, then she looks away over her shoulder and glances back with a subtle confident smile, then she tucks a strand of hair behind her ear and looks down softly. Realistic smartphone video, natural motion, consistent face, vertical 9:16, silent video with no audio
```

### 7d. Animation — version avec regard caméra dès la 1re seconde (règle d'accroche)

Exemple utilisé avec une tenue à manches cloche en voile et des lunettes de soleil sur la tête :

```
Animate this image as the exact first frame. One continuous single take, no cuts, same framing, same wooden wall, same outfit, chest-up shot. In the very first second she opens her eyes and looks straight into the lens. Then she moves smoothly and fluidly at natural speed like a relaxed photoshoot: she runs both hands slowly through her hair with her eyes half-closed, the sheer ruffled bell sleeves flowing gently, then she tilts her head and looks into the camera with lips slightly parted, then she looks away over her shoulder and glances back with a subtle confident smile, then she tucks a strand of hair behind her ear and looks down softly. The sunglasses stay on her head. Realistic smartphone video, natural motion, consistent face and ice-blue eyes, vertical 9:16, silent video with no audio.
```

Gabarit : remplacer « the sheer ruffled bell sleeves flowing gently » par `[DÉTAIL TENUE EN MOUVEMENT]` et « The sunglasses stay on her head. » par `[ACCESSOIRE QUI RESTE EN PLACE]` (ou supprimer).

### 7e. Variantes

- **Fond :** changer toutes les 2 ou 3 vidéos : mur de pierre, rideau de lin, porte cochère parisienne.
- **Mouvement :** gabarit portrait animé en plan fixe :

```
Static camera, waist-up portrait, vertical 9:16, soft natural daylight. She starts with her eyes closed, then slowly opens them and looks straight into the lens. She [GESTE: gently runs both hands through her hair / adjusts her earring / ties her hair up], glances to the side with a soft smile, then looks back at the camera with a calm, confident gaze. Subtle, natural, elegant movements. Her face, ice-blue eyes and outfit stay exactly the same. Silent video with no audio.
```

⚠ Ouverture yeux fermés : à vérifier face à la règle d'accroche (regard ou sourire dès la première image).

## 8. Contrôle avant de garder une image

- [ ] Même visage que le portrait maître (yeux bleus, 2 grains de beauté au bon endroit, aucun tatouage)
- [ ] Mains naturelles (5 doigts, pas crispées)
- [ ] Chien : conforme à sa planche de référence (pelage, marques, collier vert sauge)
- [ ] Décor cohérent avec la référence du lieu
- [ ] Aucun texte ou logo parasite dans l'image
