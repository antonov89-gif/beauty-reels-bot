import engine11 as E
def ts(x):
    h=int(x//3600); m=int(x%3600//60); s=x%60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s%1)*1000):03d}"
out=[]; n=1
for i,l in enumerate(E.LINES):
    w=l.split(); offs=E.TW[i]
    for c in range(0,len(w),6):
        a=E.starts[i]+offs[c]-0.05
        b=E.starts[i]+(offs[c+6]-0.05 if c+6<len(w) else E.D[i]+0.1)
        chunk=w[c:c+6]; txt=" ".join(chunk[:3])+("\n"+" ".join(chunk[3:]) if len(chunk)>3 else "")
        out.append(f"{n}\n{ts(a)} --> {ts(b)}\n{txt}\n"); n+=1
open("one_building.srt","w").write("\n".join(out))
print(n-1,"cues")
