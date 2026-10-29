import json,pathlib,subprocess,sys,tempfile,unittest
from text_garden import analyze
class Garden(unittest.TestCase):
    def test_empty(self):self.assertEqual(analyze('')['words'],0);self.assertEqual(analyze('')['lines'],0)
    def test_unicode(self):
        r=analyze('Hello, café!\nHELLO 🌱\n');self.assertEqual(r['words'],3);self.assertEqual(r['unique_words'],2);self.assertEqual(r['lines'],2);self.assertGreater(r['bytes_utf8'],r['characters'])
    def test_contractions_and_punctuation(self):self.assertEqual(analyze("don't don't well-being")['words'],4)
    def test_stdin_json(self):
        p=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('text_garden.py')),'--json'],input='one two two',text=True,capture_output=True);self.assertEqual(p.returncode,0);self.assertEqual(json.loads(p.stdout)['top_words'][0],{'word':'two','count':2})
    def test_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'sample.txt';p.write_text('a\nb\n',encoding='utf-8');r=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('text_garden.py')),str(p),'--json'],capture_output=True,text=True);self.assertEqual(json.loads(r.stdout)['lines'],2)
    def test_crlf_file_preserves_counts(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'windows.txt';p.write_bytes(b'a\r\nb\r\n')
            r=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('text_garden.py')),str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0)
            result=json.loads(r.stdout)
            self.assertEqual(result['characters'],6)
            self.assertEqual(result['bytes_utf8'],6)
            self.assertEqual(result['lines'],2)
    def test_invalid_utf8_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/'invalid.txt';p.write_bytes(b'\xff')
            r=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('text_garden.py')),str(p),'--json'],capture_output=True,text=True)
            self.assertEqual(r.returncode,2)
            self.assertEqual(r.stdout,'')
            self.assertIn('text-garden:',r.stderr)
            self.assertNotIn('Traceback',r.stderr)
    def test_missing_file(self):
        p=subprocess.run([sys.executable,str(pathlib.Path(__file__).with_name('text_garden.py')),'/nonexistent/text-garden-fixture'],capture_output=True,text=True);self.assertEqual(p.returncode,2);self.assertIn('text-garden:',p.stderr)
if __name__=='__main__':unittest.main(verbosity=2)
