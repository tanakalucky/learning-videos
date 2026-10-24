"""Small local topic contract: topic.json, scenes.py, DURATION, SCENES, render(t)."""
import importlib.util
import json
import math
from pathlib import Path
import re
import shutil
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / 'workspace'

def topic_path(name):
    if not re.fullmatch(r'[a-z][a-z0-9_-]*', name):
        raise ValueError('テーマ名は英小文字で始まる英数字・ハイフン・アンダースコアにしてください')
    path = WORKSPACE / name
    if path.resolve().parent != WORKSPACE.resolve():
        raise ValueError('テーマはworkspace直下に置いてください')
    return path

def load_topic(name):
    path = topic_path(name)
    meta = json.loads((path / 'topic.json').read_text())
    if not isinstance(meta.get('title'), str) or not meta['title'].strip():
        raise ValueError('titleが必要です')
    fps = meta.get('fps')
    if type(fps) is not int or not 1 <= fps <= 60:
        raise ValueError('fpsは1〜60の整数です')
    spec = importlib.util.spec_from_file_location('local_topic', path / 'scenes.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    duration = module.DURATION
    if not isinstance(duration, (int, float)) or not math.isfinite(duration) or duration <= 0:
        raise ValueError('DURATIONは正の有限秒数です')
    previous = 0
    for scene in module.SCENES:
        if len(scene) != 5:
            raise ValueError('SCENESは(start,end,title,tag,subtitle)の並びです')
        start, end, *_ = scene
        if not all(isinstance(x, (int, float)) and math.isfinite(x) for x in (start, end)) or start != previous or end <= start:
            raise ValueError('シーンは0秒から連続する正の区間にしてください')
        previous = end
    if not module.SCENES or previous != duration:
        raise ValueError('最終シーンの終了秒をDURATIONに合わせてください')
    return path, meta, module

def frame_count(duration, fps):
    count = round(duration * fps)
    if count < 1 or abs(count / fps - duration) > 1e-8:
        raise ValueError('DURATION × fpsが整数フレームになるようにしてください')
    return count

def ffmpeg_exe():
    executable = os.environ.get('FFMPEG') or shutil.which('ffmpeg')
    if executable:
        return executable
    sys.path.insert(0, str(ROOT / '.build/deps'))
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()
