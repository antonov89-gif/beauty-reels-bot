import sys
from PIL import Image
ts=[float(x) for x in sys.argv[2:]]; W,H=960,540; rows=(len(ts)+1)//2
S=Image.new('RGB',(2*W,rows*H))
for i,t in enumerate(ts): S.paste(Image.open(f'stills/s_{t:06.1f}.jpg').resize((W,H)),(i%2*W,i//2*H))
S.save(sys.argv[1],quality=82)
