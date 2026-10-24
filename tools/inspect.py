"""Decode the delivered MP4 in full and extract review frames without opening UI."""
import os,sys,pathlib,subprocess,re,json
root=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'.build/deps'))
import imageio_ffmpeg
ff=os.environ.get('FFMPEG') or imageio_ffmpeg.get_ffmpeg_exe(); video=root/'output/iap-ja.mp4'
r=subprocess.run([ff,'-hide_banner','-i',str(video),'-progress','pipe:1','-f','null','-'],text=True,capture_output=True,check=True)
assert 'Audio:' not in r.stderr and 'Video: h264' in r.stderr and '1280x720' in r.stderr and '30 fps' in r.stderr,r.stderr
assert 'Duration: 00:01:18.00' in r.stderr
frames=[int(x) for x in re.findall(r'^frame=(\d+)$',r.stdout,re.M)];assert frames[-1]==2340,frames
for t in [0,7,17,28,39,51,63,75,77.9]:
 subprocess.run([ff,'-hide_banner','-loglevel','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(root/f'output/decoded-{t:04.1f}.png')],check=True)
report={'result':'PASS','duration_seconds':78,'frames_decoded':frames[-1],'size':[1280,720],'fps':30,'codec':'h264','audio_tracks':0,'review_times':[0,7,17,28,39,51,63,75,77.9]}
(root/'output/verification.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))
