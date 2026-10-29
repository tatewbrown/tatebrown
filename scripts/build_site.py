"""Build the static Tate Brown website. Run with Python 3; no dependencies."""
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/appearances.json').read_text())
EPISODES = sorted(DATA['episodes'], key=lambda episode: episode['date'], reverse=True)
EMAIL = 'inquiries.tatebrown@hotmail.com'
NAV = [('index.html', 'Home'), ('films.html', 'Films'), ('writing.html', 'Writing'), ('travels.html', 'Travels'), ('newsletter.html', 'Africa Newsletter'), ('appearances.html', 'Appearances'), ('about.html', 'About'), ('contact.html', 'Contact')]


def e(value):
    return escape(str(value), quote=True)


def runtime(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600}:{seconds % 3600 // 60:02}:{seconds % 60:02}'


def date_label(value):
    date = datetime.strptime(value, '%Y-%m-%d')
    return f'{date.day} {date.strftime("%b")} <span>{date.year}</span>'


def sidebar():
    recent = ''
    for episode in EPISODES[:5]:
        date = datetime.strptime(episode['date'], '%Y-%m-%d')
        label = f'{date.day} {date.strftime("%B %Y")}'
        recent += f'''<div class="recent-show"><a href="{e(episode['source_url'])}" target="_blank" rel="noopener noreferrer"><time datetime="{e(episode['date'])}">{label}</time></a><br><span class="runtime">Timcast IRL ({runtime(episode['duration'])})</span></div>'''
    years = Counter(episode['date'][:4] for episode in EPISODES)
    stats = ''.join(f'<tr><th scope="row">{year}</th><td>{count}</td></tr>' for year, count in sorted(years.items(), reverse=True))
    return f'''<aside aria-label="More from Tate">
      <p class="timcast-logo"><a href="https://www.youtube.com/@TimcastIRL" target="_blank" rel="noopener noreferrer">TIMCAST IRL</a></p>
      <h2 class="sidebar-title">RECENT APPEARANCES</h2>
      {recent}
      <p class="archive-link"><a href="appearances.html">All {len(EPISODES)} full shows</a></p>
      <h2 class="sidebar-title">THE ARCHIVE</h2>
      <table class="stats-table" border="1"><caption>Full shows with me in them</caption><thead><tr><th scope="col">Year</th><th scope="col">Episodes</th></tr></thead><tbody>{stats}<tr><th scope="row">Total</th><td>{len(EPISODES)}</td></tr></tbody></table>
      <h2 class="sidebar-title">LINKS</h2>
      <p class="sidebar-links"><a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">Twitter / X</a><br><a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a><br><a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a><br><a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">Substack</a><br><a href="contact.html">Email me</a></p>
      <h2 class="sidebar-title">BOOKS &amp; FILMS</h2>
      <p class="interests"><a href="writing.html#books"><img src="images/shantaram-cover.jpg" alt="Shantaram" width="313" height="475" loading="lazy"></a> <a href="writing.html#books"><img src="images/nightcrawler-poster.jpg" alt="Nightcrawler" width="1536" height="2048" loading="lazy"></a></p>
    </aside>'''


def document(filename, title, description, content):
    nav = ' '.join(f'<a href="{url}"' + (' aria-current="page"' if url == filename else '') + f'>{label}</a>' for url, label in NAV)
    canonical = 'https://tatebrown.com/' + ('' if filename == 'index.html' else filename)
    page_class = 'archive-page' if filename == 'appearances.html' else ''
    title_text = 'The Tate Brown website' if filename == 'index.html' else title + ' - Tate Brown'
    markup = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title_text)}</title>
  <meta name="description" content="{e(description)}">
  <meta name="theme-color" content="#ff7800">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{e(title_text)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="https://tatebrown.com/images/tate-profile.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/svg+xml" href="assets/crest.svg">
  <link rel="stylesheet" href="assets/site.css?v=1998">
  <script src="assets/site.js" defer></script>
</head>
<body class="{page_class}" id="top">
<a class="skip-link" href="#main">Skip to content</a>
<div class="site">
  <header>
    <a class="masthead" href="index.html" aria-label="Tate Brown - home"><img src="assets/masthead.svg" alt="Tate Brown - the website" width="1080" height="78"></a>
    <nav class="navigation" aria-label="Main navigation">{nav}</nav>
  </header>
  <main id="main" class="main-wrap" tabindex="-1">{content}</main>
  <footer class="site-footer"><p><a href="index.html">Home</a> | <a href="contact.html">Email me</a> | <a href="#top">Back to top</a></p><p>Thanks for visiting.<br>© 2026 Tate Brown</p></footer>
</div>
</body>
</html>
'''
    if filename == '404.html':
        markup = re.sub(r'((?:href|src)=\")(?!(?:[a-z]+:|/|#))', r'\1/', markup)
    return markup


def page(filename, title, intro, body, description=None):
    intro_markup = f'<p>{intro}</p>' if intro else ''
    content = f'''<table class="layout-table inner-table" border="1" width="1000" role="presentation"><tbody><tr><td class="page-content" width="700" valign="top"><header class="page-head"><h1>{title}</h1>{intro_markup}</header><div class="page-copy">{body}</div></td><td class="sidebar" width="300" valign="top">{sidebar()}</td></tr></tbody></table>'''
    (ROOT / filename).write_text(document(filename, title.replace('&amp;', '&'), description or intro, content))


def home():
    content = f'''<table class="layout-table home-table" border="1" width="1080" role="presentation"><tbody><tr>
    <td class="portrait-column" width="320" bgcolor="#BCC3E3" valign="top">
      <h2 class="portrait-heading">TATE<br>BROWN</h2>
      <a href="about.html"><img class="portrait-image" src="images/tate-profile.jpg" alt="Tate on a steam locomotive" width="1536" height="2048" fetchpriority="high"></a>
      <p class="portrait-job">Presenter &amp; producer<br><strong>Timcast</strong></p>
      <p class="portrait-note"><a href="about.html">A bit about me</a><br><a href="contact.html">Get in touch</a></p>
      <div class="newsletter-ad"><h2><a href="newsletter.html">AFRICA NEWSLETTER</a></h2><p><b><i>Coming soon</i></b></p></div>
      <a href="travels.html"><img class="side-photo" src="images/africa-3.jpg" alt="Shoe shopping in Africa" width="1536" height="2048" loading="lazy"></a>
      <p class="portrait-note"><a href="travels.html">Photos from Africa</a></p>
    </td>
    <td class="news-column" width="460" bgcolor="#F9BD8C" valign="top">
      <p class="news-intro">Welcome to the website of . . .</p>
      <h1 class="news-title">TATE BROWN</h1>
      <p class="welcome">I'm Tate. You might know me from Timcast.<br>I wanted somewhere to put my writing, films and photos.<br>So here it is.</p>
      <div class="news-item"><h2><a href="newsletter.html">AFRICA NEWSLETTER</a></h2><p>I'm working on a newsletter about Africa. More on that soon.</p></div>
      <div class="news-item"><h2><a href="appearances.html">TIMCAST IRL APPEARANCES</a></h2><p>{len(EPISODES)} full episodes, with dates and links.</p></div>
      <div class="news-item"><h2><a href="travels.html">PHOTOS FROM AFRICA</a></h2><p>A few photos from my travels. Click to enlarge.</p></div>
      <div class="news-item"><h2><a href="films.html">FILMS</a></h2><p>Coming soon.</p></div>
      <div class="news-item"><h2><a href="writing.html">WRITING</a></h2><p>Coming soon.</p></div>
      <div class="news-item"><h2><a href="writing.html#books">BOOKS &amp; FILMS</a></h2><p>A couple of things I like.</p></div>
      <figure class="photo-teaser"><a href="travels.html"><img src="images/africa-4.jpg" alt="A view from a camel on the beach" width="1536" height="2048" loading="lazy"></a><figcaption><a href="travels.html">More photos</a></figcaption></figure>
    </td>
    <td class="sidebar" width="300" valign="top">{sidebar()}</td>
    </tr></tbody></table>'''
    (ROOT / 'index.html').write_text(document('index.html', 'Home', 'Tate Brown. Writing, films, photos and Timcast appearances.', content))


home()

page('films.html', 'Films', '', '''
<div class="coming-soon"><p><b>Coming soon.</b></p></div>
<p>In the meantime, here are some <a href="appearances.html">Timcast IRL shows I've been on</a>.</p>
''', 'Films by Tate Brown. Coming soon.')

page('writing.html', 'Writing', '', '''
<div class="coming-soon"><p><b>Coming soon.</b></p></div>
<p>I'm working on a <a href="newsletter.html">newsletter about Africa</a>. More on that soon.</p>
<p><a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">My Substack</a></p>
<hr>
<section id="books"><h2>Books &amp; films</h2><p>A couple of things I like.</p><div class="interests-gallery"><figure><img src="images/shantaram-cover.jpg" alt="Cover of Shantaram" width="313" height="475"><figcaption><b>Shantaram</b><br>Gregory David Roberts</figcaption></figure><figure><img src="images/nightcrawler-poster.jpg" alt="Poster for Nightcrawler" width="1536" height="2048"><figcaption><b>Nightcrawler</b><br>Dan Gilroy</figcaption></figure></div></section>
''', 'Writing by Tate Brown, and a few books and films.')

photos = [
    ('africa-1.jpg', 'Sculptures.', 'Sculptures in a dry landscape beneath a cloudy sky'),
    ('africa-2.jpg', 'Lunch.', 'Lunch at a wooden table overlooking the sea'),
    ('africa-3.jpg', 'Shoe shopping.', 'Tate looking at shoes at a roadside market'),
    ('africa-4.jpg', 'On a camel.', 'A view from a camel walking along a beach'),
]
gallery = ''.join(f'<figure><a href="images/{name}" data-lightbox="{e(caption)}"><img src="images/{name}" alt="{e(alt)}" width="1536" height="2048" loading="lazy"></a><figcaption>{caption}</figcaption></figure>' for name, caption, alt in photos)
page('travels.html', 'Travels', 'A few photos from Africa. Click to enlarge.', f'<div class="gallery">{gallery}</div>', 'Photos from Tate Brown\'s travels in Africa.')

page('newsletter.html', 'Africa Newsletter', '', '''
<div class="coming-soon"><p><b>Coming soon.</b></p></div>
<p>I'm working on a newsletter about Africa. More on that soon.</p>
<figure class="coming-photo"><a href="travels.html"><img src="images/africa-3.jpg" alt="Tate looking at shoes at a roadside market" width="1536" height="2048"></a><figcaption><a href="travels.html">More photos from Africa</a></figcaption></figure>
''', 'Tate Brown\'s newsletter about Africa. Coming soon.')

page('about.html', 'About me', '', f'''
<img class="about-portrait" src="images/tate-profile.jpg" alt="Tate Brown on a steam locomotive" width="1536" height="2048">
<div class="about-copy"><p>I'm Tate Brown. I'm a presenter and producer at Timcast.</p><p>I'm interested in culture, travel and what's going on elsewhere in the world. I'd like to do more of that here.</p><p>I like football and old websites.</p><p>I'm working on a <a href="newsletter.html">newsletter about Africa</a>. I'll also be putting my films and writing here.</p><p>If you've seen me on Timcast IRL, you can find the <a href="appearances.html">full shows here</a>.</p><p>You can email me at <a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
''', 'About Tate Brown, presenter and producer at Timcast.')

page('contact.html', 'Contact', '', f'''
<p>If you'd like to get in touch, email me.</p>
<p><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a></p>
<button type="button" data-copy-email="{EMAIL}" hidden>Copy email address</button><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p>
<p>I'm also on <a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">Twitter / X</a>, <a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a> and <a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a>.</p>
''', 'Contact Tate Brown.')

rows = ''
for episode in EPISODES:
    url = e(episode['source_url'])
    rows += f'''<tr data-appearance><td class="table-date"><time datetime="{e(episode['date'])}">{date_label(episode['date'])}</time></td><td><a class="episode-title" href="{url}" target="_blank" rel="noopener noreferrer">{e(episode['title'])}</a></td><td>{runtime(episode['duration'])}</td><td class="watch-cell"><a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch {e(episode['title'])}">Watch</a></td></tr>'''
archive = f'''<div class="archive-summary"><b id="appearance-count" role="status" aria-live="polite">{len(EPISODES)} full episodes</b><p>Newest first.</p></div><div class="archive-search"><label for="appearance-search">Find an episode: </label><input id="appearance-search" type="search" placeholder="Title or date" autocomplete="off"></div><table class="appearances-table" border="1"><thead><tr><th scope="col" class="date-col">Date</th><th scope="col">Episode</th><th scope="col" class="time-col">Length</th><th scope="col" class="watch-col">Watch</th></tr></thead><tbody>{rows}</tbody></table><p id="no-appearances" class="no-results" hidden>No matches. Try another title or date.</p><p class="archive-note">These are full shows from the official Timcast IRL channel. I'm credited in each episode's description. {e(DATA['scope'])}</p>'''
page('appearances.html', 'Appearances', "Here are some of the Timcast IRL shows I've been on. You can watch the full episodes below.", archive, 'Tate Brown on Timcast IRL. Full episodes, dates and watch links.')

page('404.html', 'Page not found', '', '<p>This page isn\'t here. <a href="/">Back to the homepage</a>.</p>', 'Page not found.')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>https://tatebrown.com/{"" if url == "index.html" else url}</loc></url>\n' for url, _ in NAV) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sitemap)
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://tatebrown.com/sitemap.xml\n')
print(f'Built {len(NAV) + 1} pages with {len(EPISODES)} verified appearances.')
