#!/usr/bin/env python3
"""Render deterministic Pillow frames and stream them to ffmpeg."""
import argparse,importlib,pathlib,subprocess,sys,json,os,shutil
ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument('--topic',default='iap'); p.add_argument('--time',type=float); p.add_argument('--fps',type=int,default=30); a=p.parse_args()
if not a.topic.isidentifier() or not 1<=a.fps<=60: p.error('valid topic identifier and fps 1–60 required')
m=importlib.import_module(f'topics.{a.topic}.scenes'); out=ROOT/'output'; out.mkdir(exist_ok=True)
if a.time is not None:
 dest=out/f'{a.topic}-{a.time:05.1f}.png'; m.render(a.time).save(dest); print(dest); sys.exit()
ffmpeg=os.environ.get('FFMPEG') or shutil.which('ffmpeg')
if not ffmpeg:
 sys.path.insert(0,str(ROOT/'.build/deps'))
 try:
  import imageio_ffmpeg
  ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
 except ImportError: p.error('Set FFMPEG or install the pinned optional imageio-ffmpeg package; see README')
video=out/f'{a.topic}-ja.mp4'; frames=round(m.DURATION*a.fps)
cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(a.fps),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(video)]
proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
try:
 for i in range(frames):
  proc.stdin.write(m.render(i/a.fps).tobytes())
  if i%(a.fps*10)==0: print(f'{i/a.fps:.0f}/{m.DURATION}s',flush=True)
 proc.stdin.close()
 if proc.wait()!=0: raise RuntimeError('encoder failed')
except BaseException: proc.kill(); proc.wait(); raise
version=subprocess.check_output([ffmpeg,'-version'],text=True).splitlines()[0]
(out/f'{a.topic}-render.json').write_text(json.dumps({'duration':m.DURATION,'fps':a.fps,'frames':frames,'size':[1280,720],'audio':False,'engine':'Pillow + ffmpeg','python':sys.version.split()[0],'ffmpeg':version},indent=2)+'\n')
print(video)
