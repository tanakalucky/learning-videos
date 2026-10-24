"""Small synthetic topics only; no real educational content is committed."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from engine import topic
from engine.preview import write_preview
from new_topic import create_topic

class ToolboxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.patcher = patch.object(topic, 'WORKSPACE', Path(self.tmp.name))
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_scaffold_refuses_overwrite_and_bad_paths(self):
        path = create_topic('sample', '試作', 12)
        before = {p.name: p.read_bytes() for p in path.iterdir()}
        with self.assertRaises(FileExistsError):
            create_topic('sample', '変更', 24)
        self.assertEqual(before, {p.name: p.read_bytes() for p in path.iterdir()})
        for name in ['../outside', '/tmp/outside', 'x/y', '']:
            with self.assertRaises(ValueError):
                create_topic(name, '試作', 12)

    def test_duration_fps_and_timeline(self):
        path = create_topic('sample', '試作', 12)
        _, meta, module = topic.load_topic('sample')
        self.assertEqual(topic.frame_count(module.DURATION, meta['fps']), 96)
        with self.assertRaises(ValueError):
            topic.frame_count(1.01, 12)
        (path / 'scenes.py').write_text('DURATION=2\nSCENES=[(0,1,"a","b","c")]\n')
        with self.assertRaises(ValueError):
            topic.load_topic('sample')
        for fps in [0, 61, True]:
            with self.assertRaises(ValueError):
                create_topic('invalid', '試作', fps)

    def test_preview_uses_topic_metadata(self):
        path = create_topic('sample', '<試作>', 12)
        _, meta, module = topic.load_topic('sample')
        write_preview(path / 'preview.html', meta, module.SCENES, module.DURATION)
        text = (path / 'preview.html').read_text()
        self.assertIn('&lt;試作&gt;', text)
        self.assertIn('8秒', text)
        self.assertIn('video.mp4', text)

if __name__ == '__main__':
    unittest.main()
