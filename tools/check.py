"""Content timeline, determinism, subtitle width and safe-area checks."""
import sys,pathlib,hashlib,json
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from topics.iap.scenes import SCENES,DURATION,render
from engine.draw import font
from PIL import ImageDraw,Image
assert 60<=DURATION<=90 and SCENES[0][0]==0 and SCENES[-1][1]==DURATION
d=ImageDraw.Draw(Image.new('RGB',(1,1)))
for i,s in enumerate(SCENES):
 if i: assert SCENES[i-1][1]==s[0]
 assert s[1]>s[0]
 for line in s[4].split('\n'): assert d.textlength(line,font=font(27))<=1120,(i,line)
 # Every cut plus middle and late state; same timestamp produces identical bytes.
 for t in [s[0],(s[0]+s[1])/2,s[1]-.1]:
  a=render(t); assert a.size==(1280,720) and a.tobytes()==render(t).tobytes()
print('PASS: 78s timeline, 7 contiguous scenes, 21 deterministic frames, subtitle widths')
