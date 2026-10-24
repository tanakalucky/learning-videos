from PIL import Image,ImageDraw,ImageFont
from functools import lru_cache
import os,math
W,H=1280,720
BG='#0b1425'; INK='#f1f5fc'; MUTED='#aabbd4'; BLUE='#72b6ff'; GREEN='#65e0bd'; RED='#ff9eaa'; GOLD='#ffd487'
@lru_cache(None)
def font(n): return ImageFont.truetype(os.environ.get('VIDEO_FONT','/System/Library/Fonts/ヒラギノ角ゴシック W4.ttc'),n)
def progress(t,start=0,duration=1.5): return max(0,min(1,(t-start)/duration))
class Canvas:
 def __init__(self): self.im=Image.new('RGB',(W,H),BG); self.d=ImageDraw.Draw(self.im)
 def text(self,x,y,s,n=28,color=INK,anchor=None): self.d.text((x,y),s,font=font(n),fill=color,anchor=anchor)
 def box(self,x,y,w,h,color=BLUE): self.d.rounded_rectangle((x,y,x+w,y+h),radius=20,fill='#15233a',outline=color,width=2)
 def card(self,x,y,w,h,title,body='',color=BLUE):
  self.box(x,y,w,h,color); self.text(x+22,y+22,title,31,color)
  for i,line in enumerate(body.split('\n')): self.text(x+22,y+82+i*40,line,25,MUTED)
 def arrow(self,x1,y1,x2,y2,p=1,color=BLUE):
  self.d.line((x1,y1,x2,y2),fill='#31435f',width=4); p=max(0,min(1,p)); x=x1+(x2-x1)*p; y=y1+(y2-y1)*p; a=math.atan2(y2-y1,x2-x1)
  self.d.line((x1,y1,x,y),fill=color,width=5)
  self.d.polygon([(x,y),(x-16*math.cos(a-.5),y-16*math.sin(a-.5)),(x-16*math.cos(a+.5),y-16*math.sin(a+.5))],fill=color)
  self.d.ellipse((x-6,y-6,x+6,y+6),fill=color)
 def pill(self,x,y,s,color=GREEN):
  w=self.d.textlength(s,font=font(24))+32; self.box(x,y,w,44,color); self.text(x+16,y+8,s,24,color)
 def person(self,x,y,label,color=BLUE):
  self.d.ellipse((x+28,y,x+72,y+44),outline=color,width=4); self.d.rounded_rectangle((x+10,y+53,x+90,y+104),radius=20,outline=color,width=4); self.text(x+50,y+123,label,28,color,'mt')
 def frame(self,index,title,tag,subtitle,t,duration):
  self.text(48,25,'LEARNING NOTES   /   GOOGLE CLOUD',19,MUTED); self.text(1232,25,f'{index:02d} / 07',19,MUTED,'rt'); self.text(48,78,title,43); self.text(48,143,tag,22,BLUE)
  self.d.rounded_rectangle((48,588,1232,680),radius=18,fill='#1d2e49')
  for i,line in enumerate(subtitle.split('\n')): self.text(640,603+i*35,line,27,INK,'mt')
  self.d.rectangle((48,703,1232,706),fill='#263954'); self.d.rectangle((48,703,48+1184*t/duration,706),fill=BLUE)
