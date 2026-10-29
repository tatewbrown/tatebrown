"""Generate the static GitHub Pages site. No third-party dependencies required."""
from pathlib import Path
from html import escape
from datetime import datetime
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/appearances.json').read_text())
EPISODES = sorted(DATA.get('episodes', []), key=lambda e: e.get('date', ''), reverse=True)
EMAIL = 'inquiries.tatebrown@hotmail.com'
NAV = [('index.html', 'Home'), ('films.html', 'Films'), ('writing.html', 'Writing'), ('travels.html', 'Travels'), ('newsletter.html', 'Africa Newsletter'), ('appearances.html', 'Appearances'), ('about.html', 'About'), ('contact.html', 'Contact')]

def e(value):
    return escape(str(value), quote=True)

def sidebar():
    archive_number = f'<p class="archive-count">{len(EPISODES)}</p><p>full episodes in the archive</p>' if EPISODES else '<p>Full-length broadcasts, all in one place.</p>'
    return f'''<aside class="sidebar column" aria-label="More from Tate">
      <div><a class="on-air" href="https://www.youtube.com/@TimcastIRL" target="_blank" rel="noopener noreferrer"><small>On air</small><strong>TIMCAST</strong><span>Presenting &amp; production</span></a>
      <section class="archive-callout"><h2 class="sidebar-title">APPEARANCES</h2>{archive_number}<a href="appearances.html">Watch the full shows →</a></section></div>
      <section><h2 class="sidebar-title">IN THE WORKS</h2><p class="notice"><strong>AFRICA NEWSLETTER</strong>A new newsletter about Africa.<br><em>Coming soon.</em><br><a href="newsletter.html">More information →</a></p>
      <p class="notice"><strong>FILMS &amp; WRITING</strong>Culture, travel &amp; world affairs.<br><em>Coming soon.</em></p></section>
      <section><h2 class="sidebar-title">THE NOTEBOOK</h2><table class="notebook-table"><caption class="eyebrow" style="color:var(--muted);caption-side:bottom;padding:7px 0">Books, films &amp; other interests</caption><tbody><tr><th scope="row">Book</th><td>Shantaram<small>Gregory David Roberts</small></td></tr><tr><th scope="row">Film</th><td>Nightcrawler<small>Dan Gilroy</small></td></tr><tr><th scope="row">Notes</th><td><a href="writing.html">Coming soon →</a></td></tr></tbody></table></section>
      <section class="elsewhere"><h2 class="sidebar-title">FIND ME ELSEWHERE</h2><div class="badge-links"><a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram ↗</a><a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">X / Twitter ↗</a><a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer" class="wide">TikTok ↗</a></div></section>
      <div class="contact-small"><strong>Enquiries</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </aside>'''

def document(filename, title, description, content, home=False):
    nav = ''.join(f'<a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{label}</a>' for url, label in NAV)
    canonical = 'https://tatebrown.com/' + ('' if filename == 'index.html' else filename)
    cls = 'archive-page' if filename == 'appearances.html' else ''
    markup = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)} — Tate Brown</title>
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#204d3c">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title)} — Tate Brown">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://tatebrown.com/images/tate-profile.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="assets/crest.svg">
  <link rel="stylesheet" href="assets/site.css">
  <script src="assets/site.js" defer></script>
</head>
<body class="{cls}" id="top">
<a class="skip-link" href="#main">Skip to content</a>
<div class="site">
  <header>
    <div class="topline"><span>The official website of Tate Brown</span><span class="top-extra">Culture · Travel · World Affairs</span><a href="contact.html">Enquiries ↗</a></div>
    <a class="masthead" href="index.html" aria-label="Tate Brown — home"><img class="crest" src="assets/crest.svg" alt="" width="78" height="78"><div class="brand"><span class="brand-name">Tate Brown</span><span class="brand-tagline">— At Home &amp; Abroad</span></div></a>
    <p class="strapline">Presenter &amp; producer · A curious eye on the world</p>
    <nav class="navigation" aria-label="Main navigation">{nav}</nav>
  </header>
  <main id="main" class="frame" tabindex="-1">{content}</main>
  <footer class="site-footer"><span>© 2026 Tate Brown · At Home &amp; Abroad</span><span class="footer-links"><a href="contact.html">Contact</a><a href="newsletter.html">Africa Newsletter</a><a href="#top">Back to top ↑</a></span></footer>
</div>
</body>
</html>
'''
    if filename == '404.html':
        markup = re.sub(r'((?:href|src)=\")(?!(?:[a-z]+:|/|#))', r'\1/', markup)
    return markup

def page(filename, title, intro, body, description=None):
    content = f'''<div class="inner-grid"><article class="page-content column"><header class="page-head"><p class="eyebrow">Tate Brown · At Home &amp; Abroad</p><h1>{title}</h1><p>{intro}</p></header>{body}</article>{sidebar()}</div>'''
    (ROOT / filename).write_text(document(filename, title.replace('&amp;', '&'), description or intro, content))

def home():
    count = f'{len(EPISODES)} full-length episodes' if EPISODES else 'Full-length episodes'
    content = f'''<div class="home-grid">
    <section class="poster-column column" aria-label="About Tate">
      <a class="poster" href="about.html"><p class="poster-kicker">Presenting · Production · Writing</p><p class="poster-name">TATE<br>BROWN</p><p class="poster-tagline">At Home &amp; Abroad</p><img src="images/tate-profile.jpg" alt="Tate on a steam locomotive during his travels" width="1536" height="2048" fetchpriority="high"><p class="poster-description">Culture. Travel.<br>World affairs.</p><span class="poster-foot">Meet the presenter →</span></a>
      <a class="small-ad" href="newsletter.html"><span class="eyebrow">In the works</span><strong>AFRICA NEWSLETTER</strong><p><em>Coming soon</em></p><span>Find out more →</span></a>
      <p class="profile-note">I'm Tate Brown, a presenter and producer at Timcast. Welcome to the home of my work, travels and interests.<br><a href="about.html">A little more about me →</a></p>
    </section>
    <section class="news-column column" aria-label="Latest updates"><p class="news-intro">All the latest from . . .</p><h1 class="news-title">TATE BROWN</h1><p class="eyebrow" style="color:var(--green);margin-top:8px">At home &amp; abroad</p><div class="double-rule"></div>
      <article class="news-item"><p class="news-meta">In the works · Newsletter</p><h2><a href="newsletter.html">A NEW NEWSLETTER ABOUT AFRICA</a></h2><p>Something new is taking shape. I'll be sharing more here as it comes together.</p><p class="status">Coming soon.</p></article>
      <article class="news-item"><p class="news-meta">On air · Appearances</p><h2><a href="appearances.html">TATE ON TIMCAST IRL</a></h2><p>{count} from the official Timcast IRL channel, collected in the appearances archive.</p></article>
      <article class="news-item"><p class="news-meta">From the road · Photographs</p><h2><a href="travels.html">A FEW PHOTOGRAPHS FROM AFRICA</a></h2><p>Scenes and small moments from my travels.</p></article>
      <article class="news-item"><p class="news-meta">Coming soon · Films</p><h2><a href="films.html">FILMS &amp; CONVERSATIONS</a></h2><p>People, places and a curious eye on the world. A new home for films and interviews.</p></article>
      <article class="news-item"><p class="news-meta">Coming soon · Writing</p><h2><a href="writing.html">FROM THE NOTEBOOK</a></h2><p>Writing on culture, travel and world affairs. Plus the books, films and other things that catch my attention.</p></article>
      <figure class="photo-teaser"><a href="travels.html"><img src="images/africa-4.jpg" alt="A view from a camel along the beach" width="1536" height="2048" loading="lazy"></a><figcaption>A moment from the road. <a href="travels.html">Open the photograph album →</a></figcaption></figure>
    </section>{sidebar()}</div>'''
    (ROOT / 'index.html').write_text(document('index.html', 'At Home & Abroad', 'The official website of Tate Brown. Presenting, culture, travel, world affairs and a forthcoming newsletter about Africa.', content, True))

home()

page('films.html', 'Films &amp; Conversations', 'People, places and a curious eye on the world.', '''
<section class="coming-soon"><p class="eyebrow">New work in the making</p><h2>Coming soon.</h2><p>A home for films, interviews and conversations about culture, travel and world affairs.</p><a class="text-link" href="appearances.html">In the meantime, watch my Timcast IRL appearances →</a></section>
<figure class="coming-photo"><img src="images/africa-3.jpg" alt="Tate visiting a roadside shoe market" width="1536" height="2048"><figcaption>From the road. <a href="travels.html">More photographs →</a></figcaption></figure>''')

page('writing.html', 'Writing &amp; Notes', 'Culture, travel, world affairs and other interests.', '''
<section class="coming-soon"><p class="eyebrow">From the notebook</p><h2>Coming soon.</h2><p>Essays, observations and notes on the things that catch my attention.</p><a class="text-link" href="newsletter.html">Read about the Africa newsletter →</a></section>
<section id="notebook"><h2>On the bookshelf &amp; on screen</h2><p>Books, films and a few diversions. Notes to follow.</p><div class="gallery"><figure><img src="images/shantaram-cover.jpg" alt="Cover of Shantaram by Gregory David Roberts" width="313" height="475" style="height:230px;object-fit:contain"><figcaption><strong>Shantaram</strong><br>Gregory David Roberts</figcaption></figure><figure><img src="images/nightcrawler-poster.jpg" alt="Poster for Nightcrawler, directed by Dan Gilroy" width="1536" height="2048" style="height:230px;object-fit:contain"><figcaption><strong>Nightcrawler</strong><br>Dan Gilroy</figcaption></figure></div></section>
<p style="margin-top:25px;font-size:12px"><a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">Earlier writing on Substack ↗</a></p>''')

photos = [('africa-1.jpg', 'Sculptures under an open sky.', 'Sculptures in a dry landscape beneath a wide, clouded sky'), ('africa-2.jpg', 'A pause for lunch.', 'Lunch at a wooden table overlooking the sea through tropical plants'), ('africa-3.jpg', 'At the roadside market.', 'Tate looking at shoes at a roadside market'), ('africa-4.jpg', 'Along the coast.', 'A view from a camel walking along a beach')]
gallery = ''.join(f'''<figure><a href="images/{name}" data-lightbox="{e(caption)}"><img src="images/{name}" alt="{e(alt)}" width="1536" height="2048" loading="lazy"></a><figcaption><span class="photo-number">0{i}.</span>{caption}</figcaption></figure>''' for i, (name, caption, alt) in enumerate(photos, 1))
page('travels.html', 'Photographs from the Road', 'A few scenes from my travels in Africa.', f'<div class="gallery">{gallery}</div><p class="photo-tip">Select a photograph to take a closer look.</p><div class="double-rule"></div><p>There\'s more on the way. I\'m also working on a <a href="newsletter.html">newsletter about Africa</a>.</p>')

page('newsletter.html', 'Africa Newsletter', 'A new project by Tate Brown.', '''
<section class="coming-soon"><p class="newsletter-label">A NEWSLETTER BY TATE BROWN</p><h2 class="newsletter-title">AFRICA<br>NEWSLETTER</h2><p class="newsletter-coming">Coming soon.</p><p>I'm working on a newsletter about Africa.<br>More details to follow.</p><a class="text-link" href="travels.html">In the meantime, a few photographs from my travels →</a></section>
<figure class="coming-photo"><img src="images/africa-3.jpg" alt="Tate at a roadside market during his travels in Africa" width="1536" height="2048"><figcaption>A scene from my travels in Africa.</figcaption></figure>''', 'Tate Brown is working on a newsletter about Africa. Coming soon.')

page('about.html', 'About Tate', 'Presenter, producer and a curious eye on the world.', f'''
<img class="about-portrait" src="images/tate-profile.jpg" alt="Tate Brown on a steam locomotive" width="1536" height="2048">
<div class="about-copy"><p>I'm <strong>Tate Brown</strong>, a presenter and producer at Timcast, with an interest in culture, travel and world affairs.</p><p>This is the home for my work, photographs and notes from the road.</p><p>I'm also developing a <a href="newsletter.html">newsletter about Africa</a>. Films and new writing are on the way.</p><p>You can find full-length Timcast IRL broadcasts featuring me in the <a href="appearances.html">appearances archive</a>.</p><p>For presenting, production and other enquiries, <a href="mailto:{EMAIL}">get in touch</a>.</p></div>
<div class="about-links"><a class="text-link" href="appearances.html">Watch my appearances →</a><a class="text-link" href="travels.html">Photographs from the road →</a></div>''')

page('contact.html', 'Get in Touch', 'For presenting, production and other enquiries.', f'''
<div class="contact-box"><p class="eyebrow">Contact Tate Brown</p><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a><div class="contact-actions"><a class="button-link" href="mailto:{EMAIL}">Send an email ↗</a><button type="button" class="plain-button" data-copy-email="{EMAIL}" hidden>Copy email address</button></div><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p></div>
<h2>Elsewhere</h2><p>You can also find me on <a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a>, <a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">X</a> and <a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a>.</p><p><a class="text-link" href="appearances.html">Browse my full-show appearances →</a></p>''')

def date_label(value):
    try:
        d = datetime.strptime(value, '%Y-%m-%d')
        return f'{d.day} {d.strftime("%b")} <span>{d.year}</span>'
    except ValueError:
        return e(value)

def runtime(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600}:{seconds % 3600 // 60:02}:{seconds % 60:02}'

rows = ''
for episode in EPISODES:
    url = 'https://www.youtube.com/watch?v=' + episode['id']
    rows += f'''<tr data-appearance><td class="table-date"><time datetime="{e(episode['date'])}">{date_label(episode['date'])}</time></td><td><a class="episode-title" href="{url}" target="_blank" rel="noopener noreferrer">{e(episode['title'])}</a><span class="episode-label">Timcast IRL · Full episode</span></td><td>{runtime(episode['duration'])}</td><td><a class="table-watch" href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch {e(episode['title'])}">Watch ↗</a></td></tr>'''

archive = f'''<div class="archive-summary"><strong id="appearance-count" role="status" aria-live="polite">{len(EPISODES)} full episodes</strong><span>Most recent first · Official YouTube videos</span></div><div class="archive-search"><label for="appearance-search">Find an episode</label><input id="appearance-search" type="search" placeholder="Search titles or dates…" autocomplete="off"></div><table class="appearances-table"><thead><tr><th scope="col" class="date-col">Date</th><th scope="col">Episode</th><th scope="col" class="time-col">Length</th><th scope="col" class="watch-col">Watch</th></tr></thead><tbody>{rows}</tbody></table><p id="no-appearances" class="no-results" hidden>No matching episodes. Try another title or date.</p><p class="archive-note">Full-length shows from the official Timcast IRL channel with Tate credited in the episode description. {e(DATA.get('scope', ''))}</p>'''
if not EPISODES:
    archive = '<section class="coming-soon"><h2>Appearances</h2><p>The full-show archive is being assembled.</p><a class="text-link" href="https://www.youtube.com/@TimcastIRL/streams" target="_blank" rel="noopener noreferrer">Browse Timcast IRL on YouTube ↗</a></section>'
page('appearances.html', 'Appearances', 'Full-length Timcast IRL shows featuring Tate Brown.', archive, 'Watch Tate Brown in full-length Timcast IRL broadcasts. Browse the appearances archive by date and episode title.')

page('404.html', 'A Wrong Turn', 'The page you are looking for could not be found.', '<section class="coming-soon"><h2>Back on the road.</h2><p>Head back to the homepage to find the latest work, photographs and appearances.</p><a class="button-link" href="/">Return home →</a></section>')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>https://tatebrown.com/{"" if url == "index.html" else url}</loc></url>\n' for url, _ in NAV) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sitemap)
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://tatebrown.com/sitemap.xml\n')
print(f'Built {len(NAV) + 1} pages with {len(EPISODES)} verified appearances.')
