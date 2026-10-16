import urllib.request, math, time, os
def fetch(lon,lat,d,out,w,h,tries=5):
    dlon=d*(w/h)/math.cos(math.radians(lat))
    u=f"https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/export?bbox={lon-dlon},{lat-d},{lon+dlon},{lat+d}&bboxSR=4326&imageSR=4326&size={w},{h}&format=jpg&f=image"
    for a in range(tries):
        try:
            open(out,"wb").write(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"curl/8.5.0"}),timeout=120).read()); return
        except Exception as e:
            print("retry",out,a,str(e)[:60]); time.sleep(4)
    raise SystemExit("fail "+out)
SP={"S1":(-80.1300,25.7790,0.0060),"S2":(-80.1700,25.7790,0.0090),"S3":(-80.1881,25.7814,0.0030),
    "S4":(-80.1930,25.7745,0.0040),"S5":(-80.1993,25.8011,0.0030),"S6":(-80.1600,25.7915,0.0120)}
if __name__=="__main__":
    from PIL import Image, ImageDraw
    for k,(lon,lat,d) in SP.items():
        if not os.path.exists(f"sat/{k}.jpg"): fetch(lon,lat,d,f"sat/{k}.jpg",1620,2880)
    sh=Image.new("RGB",(360*6,640))
    for i,k in enumerate(SP):
        im=Image.open(f"sat/{k}.jpg").resize((360,640)); dr=ImageDraw.Draw(im); dr.line((180,0,180,640),fill=(255,0,0),width=1); dr.line((0,320,360,320),fill=(255,0,0),width=1); sh.paste(im,(i*360,0))
    sh.save("sat/check.jpg",quality=88); print("ok")
