"""Real ffmpeg regressions, isolated from the user's workspace and videos."""
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PIL import Image
from engine import topic
from engine.draw import W, H
from engine.topic import frame_count
from new_topic import create_topic
from render import render_video
from tools.verify_video import verify


class VideoIOTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.patcher = patch.object(topic, 'WORKSPACE', Path(self.tmp.name))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_failure_preserves_previous_artifacts_and_success_replaces_them(self):
        path = Path(self.tmp.name) / 'render-test'
        path.mkdir()
        meta = {'title': 'before', 'fps': 12}
        scenes = [(0, 2, 'test', '', 'test')]
        image = Image.new('RGB', (W, H), '#224466')
        module = SimpleNamespace(DURATION=2, SCENES=scenes, render=lambda t: image)
        render_video('render-test', path, meta, module, 12, 24)
        out = path / 'output'
        filenames = ('video.mp4', 'render.json', 'index.html')
        previous = {name: (out / name).read_bytes() for name in filenames}
        self.assertGreater(len(previous['video.mp4']), 100)
        real_popen = subprocess.Popen
        for error in (RuntimeError('scene failed'), KeyboardInterrupt()):
            processes = []

            def capture_process(*args, **kwargs):
                process = real_popen(*args, **kwargs)
                processes.append(process)
                return process

            def fail_after_one_second(t):
                if t >= 1:
                    raise error
                return image

            module.render = fail_after_one_second
            with patch('render.subprocess.Popen', side_effect=capture_process):
                with self.assertRaises(type(error)):
                    render_video('render-test', path, {'title': 'failed', 'fps': 12}, module, 12, 24)
            self.assertEqual(previous, {name: (out / name).read_bytes() for name in filenames})
            self.assertEqual(list(out.glob('.render-*')), [])
            self.assertEqual(len(processes), 1)
            self.assertIsNotNone(processes[0].poll())
            self.assertTrue(processes[0].stdin.closed)
        module.render = lambda t: Image.new('RGB', (W, H), '#bb7733')
        render_video('render-test', path, {'title': 'after', 'fps': 12}, module, 12, 24)
        for name in filenames:
            self.assertNotEqual(previous[name], (out / name).read_bytes())
        self.assertEqual(json.loads((out / 'render.json').read_text())['title'], 'after')
        self.assertEqual(list(out.glob('.render-*')), [])

    def test_strict_decode_rejects_concealed_corruption(self):
        create_topic('decode-test', 'decode test', 12)
        path, meta, module = topic.load_topic('decode-test')
        render_video('decode-test', path, meta, module, 12, frame_count(module.DURATION, 12))
        self.assertEqual(verify('decode-test')['frames_decoded'], 96)
        video = path / 'output/video.mp4'
        healthy = video.read_bytes()
        damaged = bytearray(healthy)
        # Locate the first IDR slice in MP4's length-prefixed H.264 media data.
        offset = 0
        while damaged[offset + 4:offset + 8] != b'mdat':
            size = int.from_bytes(damaged[offset:offset + 4], 'big')
            self.assertGreaterEqual(size, 8)
            offset += size
        offset += 8
        while True:
            size = int.from_bytes(damaged[offset:offset + 4], 'big')
            self.assertGreater(size, 0)
            if damaged[offset + 4] & 31 == 5:
                break
            offset += 4 + size
        start = offset + 4 + size // 2
        damaged[start:start + 50] = b'\xff' * 50
        video.write_bytes(damaged)
        loose = subprocess.run([topic.ffmpeg_exe(), '-hide_banner', '-i', str(video), '-progress', 'pipe:1', '-f', 'null', '-'], text=True, capture_output=True)
        self.assertEqual(loose.returncode, 0)
        self.assertIn('frame=96', loose.stdout)
        self.assertRegex(loose.stderr, r'(?i)error|corrupt')
        with self.assertRaises(subprocess.CalledProcessError):
            verify('decode-test')
        video.write_bytes(healthy)
        self.assertEqual(verify('decode-test')['frames_decoded'], 96)


if __name__ == '__main__':
    unittest.main()
