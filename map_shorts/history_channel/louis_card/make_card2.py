"""Character card for Louis XIV (history POV channel, brand DRAFT): our own layout, cream parchment + gold, serif display, AI mark.
Images: A_face, B_mirror, C_full_v2, D_bed (Nano Banana 2.1, 28.10.2026). Output louis_xiv_character_card_v2.png (2400x2350)."""
from PIL import Image, ImageDraw, ImageFont

BG, INK, GOLD, BURG = (243, 234, 211), (40, 28, 22), (176, 133, 38), (110, 28, 40)
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SBO = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F = lambda p, s: ImageFont.truetype(p, s)
W, H = 2400, 3000
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
d.rectangle([20, 20, W - 21, H - 21], outline=GOLD, width=6)
d.rectangle([36, 36, W - 37, H - 37], outline=GOLD, width=2)
d.text((90, 70), "LOUIS XIV  ·  THE SUN KING", font=F(SB, 72), fill=BURG)
d.text((92, 168), "Character card v2 (hype · extravagant · documentary vlog look)  ·  series “A Morning with Louis XIV”  ·  Versailles, c. 1685", font=F(SI, 38), fill=INK)
# AI mark
mk = "AI-GENERATED CHARACTER"; mf = F(SBO, 36); mw = int(d.textlength(mk, font=mf))
d.rounded_rectangle([W - 90 - mw - 50, 78, W - 90, 148], radius=12, fill=INK)
d.text((W - 90 - mw - 25, 92), mk, font=mf, fill=BG)
# images
files = [("A2_face.jpg", "THE SELFIE"), ("B2_mirror.jpg", "THE MIRROR"), ("C2_full.jpg", "THE HALL · RED HEELS"), ("D2_morning.jpg", "THE MORNING")]
th, gap = 880, 40
tw = int(768 * th / 1376)
x0, y0 = (W - (4 * tw + 3 * gap)) // 2, 250
for i, (f, lab) in enumerate(files):
    t = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    x = x0 + i * (tw + gap)
    im.paste(t, (x, y0))
    d.rectangle([x - 3, y0 - 3, x + tw + 3, y0 + th + 3], outline=GOLD, width=3)
    d.rectangle([x, y0 + th - 54, x + tw, y0 + th], fill=INK)
    d.text((x + 16, y0 + th - 46), lab, font=F(SBO, 34), fill=BG)
by = y0 + th + 60
d.line([90, by - 20, W - 90, by - 20], fill=GOLD, width=3)
colw = (W - 180 - 2 * 60) // 3
rows = [
 [("PERSONALITY", ["The Sun, in person.", "Obsessed with his looks.", "Vain. Self-loving. Arrogant.", "Everything he does is a performance."]),
  ("MANNERISMS", ["Eyes half-closed, looks down his nose", "into the lens. Checks the gilded hand mirror", "before every line. Fixes a curl with a", "ringed hand. Treats the page as a", "lighting technician."]),
  ("CATCHPHRASES", ["“Bow. Lower. Good.”", "“Look. Do not stare.”", "“Marcel, my left side. MY left.”", "“The sun is never late.”"])],
 [("FACE & STYLING", ["Man of about 46, heavy-lidded eyes, long nose,", "thin curled moustache, black beauty patch by", "the mouth, painted arched brows, rouged cheeks,", "powdered pale skin, a smug half-smile."]),
  ("WARDROBE · DAY", ["Towering dark-chestnut wig to the chest, scarlet", "velvet coat embroidered with gold suns, a jewelled", "sun brooch, a mountain of lace, a ring on every", "finger, diamond-buckled black shoes, scarlet", "heels, a plumed hat."]),
  ("WARDROBE · MORNING", ["Smaller curled wig, gold silk dressing gown over", "a lace nightshirt, powder and rouge already on,", "gilded hand mirror, three wigs on stands, a", "valet and a physician at the bed."])],
 [("DOCUMENTARY LOOK", ["Raw documentary-vlog frames: phone front camera,", "ultra-wide with distortion, handheld, window and", "candle light, visible pores and powder, real", "fabric. Same grammar as the Elizabeth channel;", "our own character, palette (scarlet, gold, cream)."]),
  ("FACT ANCHORS (28.10, 2 sources each)", ["Wore heels to the end of his life; Rigaud’s 1701", "state portrait shows them. Red heels: a court", "privilege of nobles, 1670s. Hair loss from about", "1655 (age ~17): wigs. At 14 he danced the sun god", "Apollo (1653). Doctor and surgeon were in the room", "at the morning ritual before he got up."]),
  ("RULES", ["Comedy reconstruction in the voice of Louis XIV;", "dialogue and styling (patch, rouge, tower wig) are", "exaggeration, not claims. AI visuals and voice,", "marked on screen, in the description and the", "platform flag. No gore, no jokes about illness.", "Not Elizabeth’s face: no rotten teeth, no “peasants”.", "Brand: DRAFT 0.1."])],
]
y = by
for r, row in enumerate(rows):
    for i, (t, ls) in enumerate(row):
        x = 90 + i * (colw + 60)
        d.text((x, y), t, font=F(SB, 32), fill=BURG)
        yy = y + 54
        for ln in ls:
            d.text((x, yy), ln, font=F(SR, 32), fill=INK)
            yy += 41
    y += 54 + 41 * max(len(ls) for _, ls in row) + 50
im = im.crop((0, 0, W, min(H, y + 30)))
d = ImageDraw.Draw(im)
d.rectangle([20, 20, W - 21, im.height - 21], outline=GOLD, width=6)
d.rectangle([36, 36, W - 37, im.height - 37], outline=GOLD, width=2)
im.save("louis_xiv_character_card_v2.png")
print(im.size)
