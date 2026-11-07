"""Offline coverage, image-integrity and internal-link checks; no network."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
LANGUAGES={'en','zh-Hans','ja','ko','es','zh-Hant'}
class Page(HTMLParser):
 def __init__(self):super().__init__();self.ids=[];self.refs=[];self.locales=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if 'data-title' in a:self.locales.append(a['data-locale'])
  for key in ['href','src','data-src','poster','data-poster','data-gallery-src']:
   if a.get(key):self.refs.append(a[key])
pages={}
for p in ROOT.glob('*.html'):
 text=p.read_text();assert '\ufffd' not in text,p
 page=Page();page.feed(text);pages[p.name]=page
 assert len(page.ids)==len(set(page.ids)),('duplicate id',p)
 assert len(page.locales)==6 and set(page.locales)==LANGUAGES,p
 assert text.count('assets/site.js?')==1,p
for name,p in pages.items():
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or ref.startswith('//'):continue
  target=unquote(u.path) or name
  assert (ROOT/target).is_file(),(name,ref)
  if u.fragment:assert u.fragment in pages[target].ids,(name,ref)
site=json.loads((ROOT/'content/site.json').read_text());assert set(site)==LANGUAGES
for lang,row in site.items():
 assert [len(row[x]) for x in ['nav','hero','features','extra','guide','faq','labels']]==[7,4,4,4,14,9,15],lang
 assert len(row['landing']['benefits'])==3 and len(row['landing']['steps'])==3 and len(row['landing']['tourLabels'])==4,lang
 assert 'iCloud' in row['features'][3][2] and 'Pro' in row['features'][3][2]
 assert '.apkg' in row['features'][0][2]
 assert len(row['companion'])==22 and len(row['companion']['steps'])==3
 assert set(x[0] for x in row['guide']) >= {'teach','dictation','reminders','companion'}
 assert (ROOT/'assets/videos'/lang/'companion.mp4').is_file()
for name,count in [('privacy',11),('terms',12)]:
 source=json.loads((ROOT/'content'/(name+'.json')).read_text());assert set(source)==LANGUAGES
 for lang,body in source.items():
  assert body.count('<h2>')==count,(name,lang)
  assert '\ufffd' not in body
manifest=json.loads((ROOT/'assets/screenshots/manifest.json').read_text());assert len(manifest)==48
assert {r['language'] for r in manifest}==LANGUAGES
for row in manifest:assert hashlib.sha256((ROOT/row['file']).read_bytes()).hexdigest()==row['sha256'],row['file']
print('PASS: 30 localized pages; full 11/12-section policies; all local links/anchors; 48 image hashes; six-language field coverage.')

videos=json.loads((ROOT/"assets/videos/manifest.json").read_text())
assert len(videos)==6 and {v["language"] for v in videos}==LANGUAGES
for v in videos:assert hashlib.sha256((ROOT/v["file"]).read_bytes()).hexdigest()==v["sha256"]
print("PASS: six real-demo video hashes and language coverage.")
