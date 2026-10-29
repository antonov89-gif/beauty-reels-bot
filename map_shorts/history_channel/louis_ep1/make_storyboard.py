
from PIL import Image, ImageDraw, ImageFont
import textwrap
cap={
"C01":("0-14 s","Oops, the ceiling. There. Welcome to Versailles. Yes, I'm that handsome. Try not to faint.","tilt down from the ceiling, plume brushes the lens"),
"C02":("14-22 s","Some mornings, a hundred people watch me wake up. The ceremony is called the rising. I call it opening night.","static propped medium"),
"C03":("22-30 s","The doctor's here, the surgeon's here, and nobody came to see them. Everyone came to see me. Naturally.","same framing"),
"C04":("30-38 s","Now, the wig. My hair started falling out at seventeen. I took it personally, so I got a wig.","table height, close, valet finger"),
"C05":("38-46 s","It makes me look taller, they say. I wouldn't know. I never look down.","tilt up, wide-angle distortion"),
"C06":("46-54 s","White, grey, a little powder. One day, everybody will wear this. I'm just early.","wig fills the lens, rack focus"),
"C07":("54-62 s","Bow. Lower. Good. Yes, this is the new wig. Take notes.","floor-level low angle, a hand re-aims the phone"),
"C08":("62-70 s","A hundred people here, and none may speak before me. I love listening. To myself, mostly.","slow push to an extreme close-up"),
"C09":("70-78 s","Lower. Lower. Careful, that's a hat. Eyes on me, not on the hat.","wide vignetted view, swing to the reaction"),
"C10":("78-86 s","Red heels. Nobles only, and only the ones I like. Mine are the tallest, of course.","foreground heel, rack focus to the face"),
"C12":("94-102 s","Venice sold us mirrors. Now we have 357 of our own, and I'm in every single one.","backward-walk selfie, Hall of Mirrors"),
"C13":("102-110 s","Don't stand behind me, you're ruining my reflection. Go. Over there. Further.","handheld halt at a mirror"),
"C14":("110-118 s","Tonight I dine in public. You may watch, but don't stare. Well... a little. Subscribe to my stunning channel.","static propped medium, points at the lens"),
"C15":("118-128 s","Hit like. Ring the bell. Anyway, do what you like. [haughty laugh] I'm off to the table to feast!","haughty laugh, chin up, waves them off, strides to the table; mirror flash cut"),
}
F=lambda p,s: ImageFont.truetype(p,s)
SB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SR="/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"; SI="/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
BG=(243,234,211); INK=(40,28,22); BURG=(110,28,40); GOLD=(176,133,38)
def sheet(ids,name,cols,title,burst=False):
    tw,th=400,711; ch=260 if not burst else 70
    rows=(len(ids)+cols-1)//cols
    W=cols*(tw+24)+24; H=90+rows*(th+ch+24)+24
    s=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(s)
    d.text((24,18),title,font=F(SB,40),fill=BURG)
    for k,i in enumerate(ids):
        x=24+(k%cols)*(tw+24); y=90+(k//cols)*(th+ch+24)
        im=Image.open(f"frames/{i}.jpg").convert("RGB").resize((tw,th),Image.LANCZOS); s.paste(im,(x,y))
        d.rectangle([x-2,y-2,x+tw+2,y+th+2],outline=GOLD,width=3)
        d.rectangle([x,y,x+90,y+40],fill=INK); d.text((x+8,y+3),i,font=F(SB,30),fill=BG)
        if not burst:
            t,l,c=cap[i]; d.text((x,y+th+10),t,font=F(SB,26),fill=BURG)
            yy=y+th+44
            for ln in textwrap.wrap("\u201c"+l+"\u201d",35)[:4]:
                d.text((x,yy),ln,font=F(SR,25),fill=INK); yy+=29
            yy=y+th+ch-66
            for ln in textwrap.wrap(c,40)[:2]:
                d.text((x,yy),ln,font=F(SI,23),fill=GOLD); yy+=27
        else:
            d.text((x,y+th+8),["red heel","ringed hand","powder puff","gilded mirror","sun brooch","lace cravat","wig comb","embroidered cuff"][k],font=F(SI,26),fill=INK)
    s.save(name,quality=90); print(name,s.size)
sheet(["C01","C02","C03","C04","C05","C06","C07","C08"],"storyboard_1_takes1-3.jpg",4,"LOUIS XIV \u00b7 EP.1 \u201cMY MORNING\u201d \u00b7 storyboard 1/3 \u00b7 takes 1-3 (0-70 s)")
sheet(["C09","C10","C12","C13","C14","C15"],"storyboard_2_takes3-end.jpg",3,"LOUIS XIV \u00b7 EP.1 \u00b7 storyboard 2/3 \u00b7 70-128 s")
sheet(["B1","B2","B3","B4","B5","B6","B7","B8"],"storyboard_3_burst.jpg",4,"LOUIS XIV \u00b7 EP.1 \u00b7 storyboard 3/3 \u00b7 burst 86-94 s",burst=True)
