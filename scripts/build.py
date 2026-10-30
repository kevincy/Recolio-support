"""Build the six-language static GitHub Pages site from reviewed content."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'content/site.json').read_text())
LANGS=['en','zh-Hans','ja','ko','es','zh-Hant']
NAMES=['English','简体中文','日本語','한국어','Español','繁體中文']
E=lambda s:html.escape(s,quote=True)
def localized(fn):return ''.join(f'<span data-locale="{l}">{fn(D[l])}</span>' for l in LANGS)
def chrome(page):
 nav=''.join(f'<a href="{p}.html"'+(' aria-current="page"' if page==p else '')+'>'+localized(lambda d,i=i:d['nav'][i])+'</a>' for i,p in enumerate(['guide','support','privacy']))
 options=''.join(f'<option value="{l}">{n}</option>' for l,n in zip(LANGS,NAMES))
 return f'''<header class="site-header"><div class="nav"><a class="brand" href="index.html"><img src="assets/app-icon.png" width="36" height="36" alt="">Recolio</a><nav class="nav-links">{nav}</nav><label class="language-picker">{localized(lambda d:d['nav'][4])}<select id="language" name="language">{options}</select></label></div></header>'''
def footer():
 return '<footer class="site-footer"><div class="footer-inner"><a class="brand" href="index.html">Recolio</a><span>© 2026 Recolio</span><nav>'+''.join(f'<a href="{p}.html">'+localized(lambda d,i=i:d['nav'][i])+'</a>' for i,p in [(0,'guide'),(1,'support'),(2,'privacy'),(3,'terms')])+'</nav></div></footer>'
def screenshot(lang,role,alt,eager=False):
 src=f'assets/screenshots/{lang}/{role}.webp'
 return f'<img data-src="{src}"'+(f' src="{src}"' if lang=='en' else '')+f' alt="{E(alt)}" loading="'+('eager' if eager else 'lazy')+'" decoding="async" width="'+('1100' if role.startswith('ipad') else '840')+'" height="'+('1467' if role.startswith('ipad') else '1821')+'">'
def home(lang,d):
 n,h,f,x,g,q,L=[d[k] for k in ['nav','hero','features','extra','guide','faq','labels']]
 store='<a class="button" href="https://apps.apple.com/app/id6823991638">'+E(n[5])+' <span aria-hidden="true">↗</span></a>'
 s=f'''<section class="hero"><div class="hero-grid"><div><p class="eyebrow">{E(h[0])}</p><h1>{E(h[1]).replace(chr(10),'<br>')}</h1><p class="hero-copy">{E(h[2])}</p><div class="hero-actions">{store}<a class="text-link" href="#tour-{lang}">{E(n[6])} ↓</a></div><p class="quiet">{E(h[3])}</p></div><figure class="hero-visual">{screenshot(lang,'02-search',f[1][3],True)}</figure></div></section>'''
 t=d['landing']
 s+='<div class="benefits section">'+''.join('<span><b aria-hidden="true">✓</b> '+E(v)+'</span>' for v in t['benefits'])+'</div>'
 s+='<section class="section start-steps"><p class="eyebrow">.apkg → Recolio</p><div class="step-grid">'+''.join(f'<a href="guide.html#{lang}-{anchor}"><span class="step-number">0{i+1}</span><h2>{E(title)}</h2><span aria-hidden="true">→</span></a>' for i,(title,anchor) in enumerate(zip(t['steps'],['start','preview','review'])))+'</div></section>'
 roles=['03-import','02-search','ipad-05-organize','ipad-01-study']
 s+=f'<section class="section tour" id="tour-{lang}" data-gallery><h2>{E(t["tourTitle"])}</h2><p>{E(t["tourSubtitle"])}</p><div class="tour-controls" role="group" aria-label="{E(t["tourTitle"])}">'
 for i,label in enumerate(t['tourLabels']):
  s+=f'<button type="button" data-gallery-src="assets/screenshots/{lang}/{roles[i]}.webp" data-gallery-alt="{E(f[i][3])}" data-gallery-copy="{E(f[i][2])}" aria-pressed="{str(i==1).lower()}">{E(label)}</button>'
 s+=f'</div><div class="tour-stage"><div><p class="eyebrow">Recolio / iPhone + iPad</p><p data-gallery-caption aria-live="polite">{E(f[1][2])}</p><a class="text-link" href="guide.html">{E(L[5])} →</a></div><figure>{screenshot(lang,"02-search",f[1][3])}</figure></div></section>'
 for i,role in enumerate(['03-import','02-search','ipad-05-organize']):
  a=f[i]
  s+=f'<section class="feature section" id="'+('features-'+lang if i==0 else ['','search-','folders-'][i]+lang)+f'"><div class="feature-copy"><p class="eyebrow">0{i+1} / {E(a[0])}</p><h2>{E(a[1])}</h2><p>{E(a[2])}</p><a class="text-link" href="guide.html#{lang}-'+['start','search','structure'][i]+f'">{E(L[5])} →</a></div><figure class="feature-visual {"tablet" if i==2 else ""}">{screenshot(lang,role,a[3])}</figure></section>'
 a=f[3]
 s+=f'<section class="sync section" id="sync-{lang}"><div class="sync-intro"><p class="eyebrow">04 / {E(a[0])}</p><h2>{E(a[1])}</h2><p>{E(a[2])}</p><a class="text-link" href="guide.html#{lang}-sync">{E(L[5])} →</a></div><div class="sync-gallery"><figure>{screenshot(lang,"01-study",a[3])}<figcaption>iPhone</figcaption></figure><div class="sync-symbol" aria-hidden="true">↔<small>iCloud</small></div><figure>{screenshot(lang,"ipad-01-study",a[3])}<figcaption>iPad</figcaption></figure></div><p class="sync-badge">{E(L[10])}</p></section>'
 s+='<section class="section extras">'+''.join(f'<article><h2>{E(x[i])}</h2><p>{E(x[i+1])}</p></article>' for i in [0,2])+'</section>'
 s+=f'<section class="section resources"><p class="eyebrow">{E(L[0])}</p><h2>{E(L[1])}</h2><div class="cards">'+''.join(f'<article class="card"><h3>{E(n[i])}</h3><p>{E(L[i+2])}</p><a href="{p}.html">{E(L[i+5])} →</a></article>' for i,p in enumerate(['guide','support','privacy']))+f'</div><p class="quiet">{E(L[9])}</p></section>'
 s+=f'<section class="section home-faq"><h2>{E(t["faqTitle"])}</h2>'+''.join(f'<details><summary>{E(title)}</summary><p>{E(answer)}</p></details>' for title,answer in [q[0],q[1],q[3],q[4]])+'</section>'
 s+=f'<section class="section final-cta"><h2>{E(t["ctaTitle"])}</h2><p>{E(h[3])}</p>{store}</section>'
 return s

def document(page,lang,d):
 n,L=d['nav'],d['labels'];title=n[['guide','support','privacy','terms'].index(page)]
 desc={'guide':L[2],'support':L[3],'privacy':L[4],'terms':'Recolio'}[page]
 s=f'<header class="page-hero"><p class="eyebrow">Recolio</p><h1>{E(title)}</h1><p>{E(desc)}</p>'+ (f'<p class="meta">{E(L[13])}</p>' if page in ['privacy','terms'] else '')+'</header><article class="document">'
 if page=='guide':
  # Keep legacy en/zh anchor prefixes usable with ?lang=zh; new anchors use locale IDs.
  s+='<nav class="toc">'+''.join(f'<a href="#{lang}-{x[0]}">{E(x[1])}</a>' for x in d['guide'])+'</nav>'
  for ident,title,body in d['guide']:
   aliases=[]
   if lang=='zh-Hans':aliases=['zh-'+ident]
   if ident=='start':aliases += [lang+'-import']
   if ident=='search':aliases += [lang+'-browser']
   if ident=='review':aliases += [lang+'-study',lang+'-fsrs']
   s+=''.join(f'<span id="{a}" class="anchor"></span>' for a in aliases)
   s+=f'<h2 id="{lang}-{ident}">{E(title)}</h2><p>{E(body)}</p>'
 elif page=='support':
  s+=''.join(f'<details{ " open" if i==0 else ""}><summary>{E(q)}</summary><p>{E(a)}</p></details>' for i,(q,a) in enumerate(d['faq']))
 else:s+=json.loads((ROOT/'content'/(page+'.json')).read_text())[lang]
 if page=='terms':s+='<p><a href="privacy.html">'+E(n[2])+'</a> · <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Apple EULA</a></p>'
 s+=f'<div class="contact-box"><h2>{E(L[8])}</h2><p><a href="mailto:hikevincheng@gmail.com">{E(L[11])}: hikevincheng@gmail.com</a></p><p><a href="https://github.com/kevincy/Recolio-support/issues/new">{E(L[12])} ↗</a></p></div></article>'
 return s

def build():
 for page in ['index','guide','support','privacy','terms']:
  body=''
  for lang in LANGS:
   d=D[lang];title='Recolio — '+(d['hero'][1].replace('\n',' ') if page=='index' else d['nav'][['guide','support','privacy','terms'].index(page)])
   desc=d['hero'][2] if page=='index' else d['labels'][2 if page=='guide' else 3 if page=='support' else 4]
   body+=f'<div data-locale="{lang}" data-title="{E(title)}" data-description="{E(desc)}">'+(home(lang,d) if page=='index' else document(page,lang,d))+'</div>'
  title='Recolio — '+('Flashcards for iPhone & iPad' if page=='index' else D['en']['nav'][['guide','support','privacy','terms'].index(page)])
  description=D['en']['hero'][2] if page=='index' else D['en']['labels'][2 if page=='guide' else 3 if page=='support' else 4]
  alternates=''.join(f'<link rel="alternate" hreflang="{lang}" href="https://kevincy.github.io/Recolio-support/{page}.html?lang={lang}">' for lang in LANGS)
  output=f'''<!doctype html>
<html lang="en" data-language="en"><head><meta charset="utf-8"><script src="assets/site.js?v=20261030-tour"></script><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="{E(description)}">{alternates}<meta name="theme-color" content="#faf8f4"><title>{E(title)}</title><link rel="icon" href="assets/app-icon.png"><link rel="stylesheet" href="assets/styles.css?v=20261030-tour"></head><body>{chrome(page)}<main>{body}</main>{footer()}</body></html>\n'''
  (ROOT/(page+'.html')).write_text(output)
 print('Built 5 pages × 6 complete languages')
if __name__=='__main__':build()
