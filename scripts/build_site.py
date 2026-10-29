"""Build the static Tate Brown website. Run with Python 3; no dependencies."""
from collections import Counter
from datetime import datetime
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/appearances.json').read_text())
EDITORIAL = json.loads((ROOT / 'data/editorial.json').read_text())
FEATURED = json.loads((ROOT / 'data/featured-appearances.json').read_text())
EPISODES = sorted(DATA['episodes'], key=lambda episode: episode['date'], reverse=True)
EPISODES_BY_ID = {episode['id']: episode for episode in EPISODES}
EMAIL = 'inquiries.tatebrown@hotmail.com'
NAV = [('index.html', 'Home'), ('films.html', 'Films'), ('writing.html', 'Writing'), ('travels.html', 'Travels'), ('newsletter.html', 'Africa Newsletter'), ('appearances.html', 'Appearances'), ('about.html', 'About'), ('contact.html', 'Contact')]
EXTRA_PAGES = ['books.html', 'links.html'] + [article['slug'] + '.html' for article in EDITORIAL['articles']]
NAV_PARENT = {article['slug'] + '.html': 'writing.html' for article in EDITORIAL['articles']}
NAV_PARENT['books.html'] = 'writing.html'


def e(value):
    return escape(str(value), quote=True)


def runtime(seconds):
    seconds = int(seconds)
    return f'{seconds // 3600}:{seconds % 3600 // 60:02}:{seconds % 60:02}'


def date_text(value, short=False):
    date = datetime.strptime(value, '%Y-%m-%d')
    return f'{date.strftime("%b")} {date.day}' if short else f'{date.day} {date.strftime("%B %Y")}'


def date_label(value):
    date = datetime.strptime(value, '%Y-%m-%d')
    return f'{date.day} {date.strftime("%b")} <span>{date.year}</span>'


def shelf():
    return '''<section class="shelf"><h2 class="sidebar-title">READING &amp; WATCHING</h2><div class="shelf-links"><figure><a href="books.html#shantaram"><img src="images/shantaram-cover.jpg" alt="Shantaram" width="313" height="475" loading="lazy"></a><figcaption><a href="books.html#shantaram">Shantaram</a></figcaption></figure><figure><a href="books.html#nightcrawler"><img src="images/nightcrawler-poster.jpg" alt="Nightcrawler" width="1536" height="2048" loading="lazy"></a><figcaption><a href="books.html#nightcrawler">Nightcrawler</a></figcaption></figure></div></section>'''


def sidebar():
    recent = ''
    for episode in EPISODES[:2]:
        recent += f'''<div class="recent-show"><a href="{e(episode['source_url'])}" target="_blank" rel="noopener noreferrer"><time datetime="{e(episode['date'])}">{date_text(episode['date'])}</time></a><br><span class="runtime">Timcast IRL ({runtime(episode['duration'])})</span></div>'''
    return f'''<aside aria-label="More from Tate">
      <section class="sidebar-section"><h2 class="sidebar-title"><a href="newsletter.html">AFRICA NEWSLETTER</a></h2><p class="newsletter-status">Coming soon.</p><p class="sidebar-copy">I'm working on a newsletter about Africa.<br><a href="newsletter.html">A bit of background</a></p></section>
      <section class="sidebar-section"><h2 class="sidebar-title">A FEW LINKS</h2><ul class="link-list"><li><a href="https://www.braintreetownfc.org.uk/" target="_blank" rel="noopener noreferrer">Braintree Town FC</a><br>The website that started this.</li><li><a href="books.html">Books &amp; films</a></li><li><a href="links.html">More links</a></li></ul></section>
      <section class="sidebar-section"><h2 class="sidebar-title">RECENT APPEARANCES</h2>{recent}<p class="archive-link"><a href="appearances.html#start-here">Three shows to start with</a><br><a href="appearances.html#archive">All {len(EPISODES)} full episodes</a></p></section>
      <section class="sidebar-section"><h2 class="sidebar-title">FIND ME ELSEWHERE</h2><ul class="link-list"><li><a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">Twitter / X</a></li><li><a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a></li><li><a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a></li><li><a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">Substack</a></li><li><a href="contact.html">Email me</a></li></ul></section>
    </aside>'''


def document(filename, title, description, content):
    current = NAV_PARENT.get(filename, filename)
    nav = ' '.join(f'<a href="{url}"' + (' aria-current="page"' if url == current else '') + f'>{label}</a>' for url, label in NAV)
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
  <link rel="stylesheet" href="assets/site.css?v=1998-2">
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
  <footer class="site-footer"><p><a href="index.html">Home</a> | <a href="links.html">Links</a> | <a href="contact.html">Email me</a> | <a href="#top">Back to top</a></p><p>Last updated {date_text(EDITORIAL['updated'])}. Thanks for visiting.<br>© 2026 Tate Brown</p></footer>
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
    updates = ''.join(f'''<article class="news-item"><h2><a href="{e(item['url'])}"><i class="news-date"><time datetime="{item['date']}">{date_text(item['date'], True)}:</time></i> {e(item['title'])}</a></h2><p>{e(item['text'])}</p></article>''' for item in EDITORIAL['updates'])
    content = f'''<table class="layout-table home-table" border="1" width="1080" role="presentation"><tbody><tr>
    <td class="portrait-column" width="320" bgcolor="#BCC3E3" valign="top">
      <h2 class="portrait-label">HELLO</h2>
      <a href="about.html"><img class="portrait-image" src="images/tate-profile.jpg" alt="Tate on a steam locomotive" width="1536" height="2048" fetchpriority="high"></a>
      <p class="bio-note">I'm Tate Brown.<br>Presenter and producer at Timcast.</p>
      <p class="bio-note">I like football and old websites.<br>I've also done a bit of <a href="kenya-to-south-africa.html">travelling</a>.</p>
      <p class="portrait-note"><a href="about.html">A bit about me</a> | <a href="contact.html">Get in touch</a></p>
      {shelf()}
    </td>
    <td class="news-column" width="460" bgcolor="#F9BD8C" valign="top">
      <p class="news-intro">All the latest . . .</p><h1 class="news-title">LATEST UPDATES</h1>
      {updates}
      <figure class="photo-teaser"><a href="travels.html#coast"><img src="images/africa-4.jpg" alt="A view from a camel on the beach" width="1536" height="2048" loading="lazy"></a><figcaption>A camel ride along the beach.<br><a href="travels.html">Open the photo album</a></figcaption></figure>
    </td>
    <td class="sidebar" width="300" valign="top">{sidebar()}</td>
    </tr></tbody></table>'''
    (ROOT / 'index.html').write_text(document('index.html', 'Home', 'Tate Brown. Writing, travel photographs, an Africa newsletter and full-show appearances.', content))


home()

page('films.html', 'Films', '', '''<div class="coming-soon"><p><b>Coming soon.</b></p></div><p>In the meantime, here are some <a href="appearances.html#start-here">Timcast IRL shows I've been on</a>.</p>''', 'Films by Tate Brown. Coming soon.')

article_list = ''.join(f'''<li><b><a href="{article['slug']}.html">{e(article['title'])}</a></b><br><time datetime="{article['date']}">{date_text(article['date'])}</time><br>{e(article['teaser'])}</li>''' for article in EDITORIAL['articles'])
page('writing.html', 'Writing', 'A few notes.', f'''<ul class="entry-list">{article_list}</ul><p><a href="newsletter.html">The Africa newsletter</a> is in the works.</p><p><a href="books.html" id="books">Books &amp; films</a> | <a href="books.html" id="notebook">Reading &amp; watching</a> | <a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">My Substack</a></p>''', 'Notes from Tate Brown on travel, websites and other interests.')

page('books.html', 'Books &amp; Films', '', '''
<section class="book-entry" id="shantaram"><img src="images/shantaram-cover.jpg" alt="Cover of Shantaram" width="313" height="475"><h2>Shantaram</h2><p><b>Gregory David Roberts</b></p><p>A novel about an Australian fugitive who finds his way into the underworld of 1980s Bombay. It draws on Roberts' own life.</p><p><a href="https://us.macmillan.com/books/9780312330538/shantaram/" target="_blank" rel="noopener noreferrer">Book details</a></p></section>
<section class="book-entry" id="nightcrawler"><img src="images/nightcrawler-poster.jpg" alt="Poster for Nightcrawler" width="1536" height="2048"><h2>Nightcrawler</h2><p><b>Directed by Dan Gilroy · 2014</b></p><p>Jake Gyllenhaal plays Lou Bloom, who starts filming crime scenes in Los Angeles and selling the footage to television news.</p><p><a href="https://www.universalpicturesathome.com/movies/nightcrawler" target="_blank" rel="noopener noreferrer">Film details &amp; trailer</a></p></section>
<p>My notes on these are still to come.</p>
''', 'Shantaram and Nightcrawler: books and films from Tate Brown\'s website.')

page('links.html', 'A few links', '', '''
<div class="entry-body"><h2><a href="https://www.braintreetownfc.org.uk/" target="_blank" rel="noopener noreferrer">Braintree Town FC</a></h2><p>The reason this website looks the way it does. I hope they never change it.</p>
<h2><a href="https://us.macmillan.com/books/9780312330538/shantaram/" target="_blank" rel="noopener noreferrer">Shantaram</a></h2><p>The publisher's page for Gregory David Roberts' novel.</p>
<h2><a href="https://www.universalpicturesathome.com/movies/nightcrawler" target="_blank" rel="noopener noreferrer">Nightcrawler</a></h2><p>Film details and the trailer.</p>
<h2>My other pages</h2><p><a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">Twitter / X</a><br><a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a><br><a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a><br><a href="https://realtatebrown.substack.com" target="_blank" rel="noopener noreferrer">Substack</a></p></div>
''', 'A few links from Tate Brown, including the website that inspired this one.')


def photograph(filename, caption, alt):
    return f'<figure><a href="images/{filename}" data-lightbox="{e(caption)}"><img src="images/{filename}" alt="{e(alt)}" width="1536" height="2048" loading="lazy"></a><figcaption>{e(caption)}</figcaption></figure>'


gallery = '<div class="gallery"><section id="kenya"><h2>Kenya</h2>' + photograph('africa-3.jpg', 'Shoe shopping in Kariobangi, Nairobi, Kenya.', 'Tate looking at shoes in Kariobangi, Nairobi') + '</section><section id="south-africa"><h2>South Africa</h2>' + photograph('africa-1.jpg', 'Monument Hill, Orania, South Africa. The Kleinreus figure in front of a semicircle of busts.', 'The Kleinreus figure and busts on Monument Hill in Orania') + '</section><section id="coast"><h2>By the sea</h2>' + photograph('africa-4.jpg', 'A camel ride along the beach.', 'A view from a camel walking along a beach') + photograph('africa-2.jpg', 'Lunch by the sea.', 'Lunch at a wooden table overlooking the sea') + '</section></div>'
page('travels.html', 'Travels', 'A few photos from Africa. Click to enlarge.', f'<p><a href="kenya-to-south-africa.html">Read about the trip</a></p><p class="album-index"><a href="#kenya">Kenya</a> | <a href="#south-africa">South Africa</a> | <a href="#coast">By the sea</a></p>{gallery}', 'Photographs from Tate Brown\'s travels, including Nairobi and Orania.')

page('newsletter.html', 'Africa Newsletter', '', '''
<div class="coming-soon"><p><b>Coming soon.</b></p></div>
<div class="entry-body"><p>I backpacked from Kenya to South Africa. Malawi was one of my favourite stops.</p><p>I'm working on a newsletter about Africa. I'd like to spend more time writing about culture, travel and what's going on elsewhere in the world.</p><p>I'll put the name and details here when it's ready.</p><p><a href="kenya-to-south-africa.html">A bit about the trip</a> | <a href="travels.html">The photo album</a></p></div>
<figure class="coming-photo"><a href="travels.html#kenya"><img src="images/africa-3.jpg" alt="Tate looking at shoes in Nairobi" width="1536" height="2048"></a><figcaption>Shoe shopping in Nairobi, Kenya.</figcaption></figure>
''', 'An Africa newsletter from Tate Brown. Coming soon.')

page('about.html', 'About me', '', f'''
<img class="about-portrait" src="images/tate-profile.jpg" alt="Tate Brown on a steam locomotive" width="1536" height="2048">
<div class="about-copy"><p>I'm Tate Brown. I'm a presenter and producer at Timcast.</p><p>I'm interested in culture, travel and what's going on elsewhere in the world. I'd like to do more of that here.</p><p>I like football and old websites. I've also <a href="kenya-to-south-africa.html">backpacked from Kenya to South Africa</a>.</p><p>I'm working on a <a href="newsletter.html">newsletter about Africa</a>. There are a few <a href="writing.html">notes</a> and <a href="travels.html">photographs</a> here already.</p><p>If you've seen me on Timcast IRL, you can find the <a href="appearances.html">full shows here</a>.</p><p>You can email me at <a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>
''', 'About Tate Brown, presenter and producer at Timcast.')

page('contact.html', 'Contact', '', f'''<p>If you'd like to get in touch, email me.</p><p><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a></p><button type="button" data-copy-email="{EMAIL}" hidden>Copy email address</button><p class="copy-status" id="copy-status" role="status" aria-live="polite"></p><p>I'm also on <a href="https://x.com/realTateBrown" target="_blank" rel="noopener noreferrer">Twitter / X</a>, <a href="https://www.instagram.com/realtatebrown" target="_blank" rel="noopener noreferrer">Instagram</a> and <a href="https://www.tiktok.com/@realtatebrown" target="_blank" rel="noopener noreferrer">TikTok</a>.</p>''', 'Contact Tate Brown.')

featured_rows = ''
for item in FEATURED:
    episode = EPISODES_BY_ID[item['id']]
    featured_rows += f'''<li><h3><a href="{e(episode['source_url'])}" target="_blank" rel="noopener noreferrer">{e(item['heading'])}</a></h3><p>{e(item['description'])}</p><p class="original-video-title">{date_text(episode['date'])} · {runtime(episode['duration'])} · Credited host · Full episode<br>Original title: {e(episode['title'])}</p></li>'''
featured_html = f'<section id="start-here"><h2>Three shows to start with</h2><p>A few conversations from the archive. Each link opens the full show.</p><ol class="start-here">{featured_rows}</ol></section>'
rows = ''
for episode in EPISODES:
    url = e(episode['source_url'])
    rows += f'''<tr data-appearance><td class="table-date"><time datetime="{e(episode['date'])}">{date_label(episode['date'])}</time></td><td><a class="episode-title" href="{url}" target="_blank" rel="noopener noreferrer">{e(episode['title'])}</a></td><td>{runtime(episode['duration'])}</td><td class="watch-cell"><a href="{url}" target="_blank" rel="noopener noreferrer" aria-label="Watch {e(episode['title'])}">Watch</a></td></tr>'''
years = Counter(episode['date'][:4] for episode in EPISODES)
stats_rows = ''.join(f'<tr><th scope="row">{year}</th><td>{count}</td></tr>' for year, count in sorted(years.items(), reverse=True))
stats = f'<table class="stats-table"><caption>Full shows in the archive</caption><thead><tr><th scope="col">Year</th><th scope="col">Episodes</th></tr></thead><tbody>{stats_rows}<tr><th scope="row">Total</th><td>{len(EPISODES)}</td></tr></tbody></table>'
archive = featured_html + f'''<section id="archive"><h2>The full archive</h2>{stats}<div class="archive-summary"><b id="appearance-count" role="status" aria-live="polite">{len(EPISODES)} full episodes</b><p>Newest first.</p></div><div class="archive-search"><label for="appearance-search">Find an episode: </label><input id="appearance-search" type="search" placeholder="Title or date" autocomplete="off"></div><table class="appearances-table" border="1"><thead><tr><th scope="col" class="date-col">Date</th><th scope="col">Episode</th><th scope="col" class="time-col">Length</th><th scope="col" class="watch-col">Watch</th></tr></thead><tbody>{rows}</tbody></table><p id="no-appearances" class="no-results" hidden>No matches. Try another title or date.</p><p class="archive-note">These are full shows from the official Timcast IRL channel. I'm credited in each episode's description. {e(DATA['scope'])}</p></section>'''
page('appearances.html', 'Appearances', "Here are some of the Timcast IRL shows I've been on.", archive, 'Selected Timcast IRL conversations and the full 110-episode Tate Brown archive.')

for article in EDITORIAL['articles']:
    body = '<div class="entry-body">' + ''.join(f'<p>{e(paragraph)}</p>' for paragraph in article['paragraphs'])
    if article.get('image'):
        body += f'''<figure class="entry-figure"><a href="images/{e(article['image'])}" data-lightbox="{e(article['image_caption'])}"><img src="images/{e(article['image'])}" alt="{e(article['image_alt'])}" width="1536" height="2048"></a><figcaption>{e(article['image_caption'])}</figcaption></figure>'''
    body += f'<p><a href="{e(article["related_url"])}">{e(article["related_label"])}</a></p>'
    if article.get('sources'):
        source_links = ' · '.join(f'<a href="{e(source["url"])}" target="_blank" rel="noopener noreferrer">{e(source["label"])}</a>' for source in article['sources'])
        body += f'<p class="source-note">{source_links}</p>'
    body += '</div><p class="entry-nav"><a href="writing.html">More writing</a> | <a href="index.html">Back to the homepage</a></p>'
    intro = f'<span class="entry-date">Posted <time datetime="{article["date"]}">{date_text(article["date"])}</time></span>'
    page(article['slug'] + '.html', article['title'], intro, body, article['teaser'])

page('404.html', 'Page not found', '', '<p>This page isn\'t here. <a href="/">Back to the homepage</a>.</p>', 'Page not found.')

sitemap_pages = [url for url, _ in NAV] + EXTRA_PAGES
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>https://tatebrown.com/{"" if url == "index.html" else url}</loc></url>\n' for url in sitemap_pages) + '</urlset>\n'
(ROOT / 'sitemap.xml').write_text(sitemap)
(ROOT / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://tatebrown.com/sitemap.xml\n')
print(f'Built {len(sitemap_pages) + 1} pages with {len(EPISODES)} verified appearances and {len(EDITORIAL["articles"])} notes.')
