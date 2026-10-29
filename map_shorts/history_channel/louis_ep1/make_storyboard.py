
from PIL import Image, ImageDraw, ImageFont
import textwrap
cap={
"C01":("0-8 s","Marcel. The ceiling is lovely. I am lower. DOWN. Good morning, Versailles.","tilt down from the ceiling, plume brushes the lens"),
"C02":("8-16 s","A hundred people watch me wake up. The French call it the lever. I call it a premiere.","static propped medium"),
"C03":("16-24 s","The doctor is here. The surgeon is here. Nobody is here to look at the doctor. Look at me.","same framing"),
"C04":("24-32 s","Now. The wig. At seventeen my hair started leaving. I took it personally. So I took a wig.","table height, close, valet finger"),
"C05":("32-40 s","It makes me taller. The Louvre says so. I did not ask.","tilt up, wide-angle distortion"),
"C06":("40-48 s","White. Grey. Powdered. Everyone will wear it one day. I am simply early.","wig fills the lens, rack focus"),
"C07":("48-56 s","Bow. Lower. Good.","floor-level low angle, a hand re-aims the phone"),
"C08":("56-64 s","A hundred people and only one of them is worth looking at.","slow push to an extreme close-up"),
"C09":("64-72 s","Lower... that is a hat. Eyes on me, not the hat.","wide vignetted view, swing to the reaction"),
"C10":("72-80 s","Red heels. A privilege of nobles. Only the ones I like.","foreground heel, rack focus to the face"),
"C12":("88-96 s","Venice sold mirrors. France made 357. I am in all of them.","backward-walk selfie, Hall of Mirrors"),
"C13":("96-104 s","Do not stand behind me. You ruin the reflection.","handheld halt at a mirror"),
"C14":("104-112 s","Tonight, I dine in public. You may watch. Do not stare. Well... a little. Subscribe to my stunning channel.","static propped medium, points at the lens"),
"C15":("112-120 s","Like it. Ring the bell. Anyway... do what you like. [haughty laugh] I am off to the table to feast!","haughty laugh, chin up, waves them off, strides to the table; mirror flash cut"),
}
F=lambda p,s: ImageFont.truetype(p,s)
SB="/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"; SR="/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"; SI="/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
BG=(243,234,211); INK=(40,28,22); BURG=(110,28,40); GOLD=(176,133,38)
def sheet(ids,name,cols,title,burst=False):
    tw,th=400,711; ch=210 if not burst else 70
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
            for ln in textwrap.wrap("\u201c"+l+"\u201d",38)[:3]:
                d.text((x,yy),ln,font=F(SR,25),fill=INK); yy+=29
            yy=y+th+ch-66
            for ln in textwrap.wrap(c,40)[:2]:
                d.text((x,yy),ln,font=F(SI,23),fill=GOLD); yy+=27
        else:
            d.text((x,y+th+8),["red heel","ringed hand","powder puff","gilded mirror","sun brooch","lace cravat","wig comb","embroidered cuff"][k],font=F(SI,26),fill=INK)
    s.save(name,quality=90); print(name,s.size)
sheet(["C01","C02","C03","C04","C05","C06","C07","C08"],"storyboard_1_takes1-3.jpg",4,"LOUIS XIV \u00b7 EP.1 \u201cMY MORNING\u201d \u00b7 storyboard 1/3 \u00b7 takes 1-3 (0-64 s)")
sheet(["C09","C10","C12","C13","C14","C15"],"storyboard_2_takes3-end.jpg",3,"LOUIS XIV \u00b7 EP.1 \u00b7 storyboard 2/3 \u00b7 64-120 s")
sheet(["B1","B2","B3","B4","B5","B6","B7","B8"],"storyboard_3_burst.jpg",4,"LOUIS XIV \u00b7 EP.1 \u00b7 storyboard 3/3 \u00b7 burst 80-88 s",burst=True)
