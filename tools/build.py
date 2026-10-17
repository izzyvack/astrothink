#!/usr/bin/env python3
"""Build the static AstroThink pages from content/site.json. No dependencies."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT
DATA = json.loads((ROOT / 'content/site.json').read_text())
ORIGIN = DATA.get('site_url', '').rstrip('/')
EMAIL = DATA['email']

def e(value):
    return escape(str(value), quote=True)

def arrow(diagonal=False, small=False):
    path = 'M5 17 17 5M5 5h12v12' if diagonal else 'M4 12h15m-6-6 6 6-6 6'
    return f'<svg class="arrow{" arrow-small" if small else ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="{path}"/></svg>'

def star():
    return '<svg class="star" viewBox="0 0 48 48" aria-hidden="true"><polygon points="24,3 30.2,16.2 44.7,18 34,28 36.8,42.5 24,35.5 11.2,42.5 14,28 3.3,18 17.8,16.2"/></svg>'

def symbol(kind):
    paths = {
      'space-ai':'<path d="M60 10C42 29 39 48 42 76h36c3-28 0-47-18-66Z"/><circle cx="60" cy="43" r="9"/><path d="M42 57 29 78v16l16-9m33-28 13 21v16l-16-9M50 83v12m10-12v24m10-24v12M42 67h36"/>',
      'python-neural-networks':'<path d="M27 31 54 47m-27-16 27 42m-27 16 27-42m-27 42 27-16m12-26 27-16M66 47l27 42M66 73l27-42m-27 42 27 16"/><circle cx="21" cy="28" r="7"/><circle cx="21" cy="92" r="7"/><circle cx="60" cy="44" r="7"/><circle cx="60" cy="76" r="7"/><circle cx="99" cy="28" r="7"/><circle cx="99" cy="92" r="7"/>',
      'beyond-the-stethoscope':'<path d="M44 17v29c0 21 32 21 32 0V17M37 17h14m18 0h14M60 63v19c0 25 37 25 37 0V64"/><circle cx="97" cy="56" r="9"/><path d="M14 76h12l6-11 9 24 8-13h11"/>',
      'career-pathways':'<path d="M19 48h82v56H19zM44 48V34h32v14M19 67h82M54 63h12v12H54zM25 18h29m-29 8h18M84 12h19v20H84l-9 8V12h9Z"/>'
    }
    return f'<svg class="subject-symbol" viewBox="0 0 120 120" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round" aria-hidden="true">{paths[kind]}</svg>'

def button(text, href, cls='', external=False):
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    sr = '<span class="sr-only"> (opens in a new tab)</span>' if external else ''
    return f'<a class="button {cls}" href="{e(href)}"{attrs}>{text}{sr}{arrow(external)}</a>'

def link(text, href, external=False):
    attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
    sr = '<span class="sr-only"> (opens in a new tab)</span>' if external else ''
    return f'<a class="text-link" href="{e(href)}"{attrs}>{text}{sr}{arrow(external,True)}</a>'

def mail(subject):
    from urllib.parse import quote
    return 'mailto:'+EMAIL+'?subject='+quote(subject)

def header(active):
    links = [('about','About','about.html'),('programs','Programs','programs.html'),('team','Team','team.html'),('explore','Explore','explore.html'),('contact','Contact','contact.html')]
    nav = ''.join(f'<a href="{url}"'+(' aria-current="page"' if key==active else '')+f'>{title}</a>' for key,title,url in links)
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="container nav-shell">
<a class="brand" href="index.html" aria-label="AstroThink home"><img src="assets/astrothink-logo.jpg" alt="" width="52" height="52"><span>AstroThink</span></a>
<button class="menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false"><span>Menu</span><span class="menu-lines" aria-hidden="true"></span></button>
<nav class="main-nav" id="main-nav" aria-label="Main navigation">{nav}<a class="nav-cta" href="https://astrothink.flyingminds.org/login" target="_blank" rel="noopener noreferrer">Learning portal<span class="sr-only"> (opens in a new tab)</span>{arrow(True,True)}</a></nav>
</div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="container"><div class="footer-top">
<div class="footer-identity"><a class="footer-name" href="index.html">Astro<span>Think</span></a><p>AstroThink is a <a href="https://flyingminds.org/" target="_blank" rel="noopener noreferrer">FlyingMinds</a> program based in Naperville, Illinois.</p></div>
<div><p class="footer-kicker">Website</p><nav class="footer-links" aria-label="Footer navigation"><a href="about.html">About AstroThink</a><a href="programs.html">Our programs</a><a href="team.html">Our team</a><a href="explore.html">Interactive activities</a><a href="contact.html">Contact</a></nav></div>
<div class="footer-contact"><p class="footer-kicker">Contact</p><a href="mailto:{EMAIL}">{EMAIL}</a><div class="footer-socials"><a href="{DATA['instagram']}" target="_blank" rel="noopener noreferrer">Instagram<span class="sr-only"> (opens in a new tab)</span></a><a href="https://www.linkedin.com/company/astrothink/" target="_blank" rel="noopener noreferrer">LinkedIn<span class="sr-only"> (opens in a new tab)</span></a></div></div>
</div><div class="footer-bottom"><span>© 2026 AstroThink</span><a href="#top">Back to top ↑</a></div></div></footer>'''

def contact_band():
    return f'''<section class="contact-band"><div class="container contact-band-inner"><div><h2>Contact AstroThink</h2><p>Email us about student programs, school visits, or community partnerships.</p></div>{button('Contact the team','contact.html')}</div></section>'''

def page(filename, title, description, body, active='', preload=False):
    preload_tag = '<link rel="preload" href="assets/fonts/merriweather-variable.woff2" as="font" type="font/woff2" crossorigin>'
    url_metadata = ''
    if ORIGIN:
        url_metadata = f'<link rel="canonical" href="{e(ORIGIN)}/{filename}"><meta property="og:url" content="{e(ORIGIN)}/{filename}"><meta property="og:image" content="{e(ORIGIN)}/assets/astrothink-logo.jpg">'
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | AstroThink</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#101113">
<link rel="icon" type="image/jpeg" href="assets/astrothink-logo.jpg">{url_metadata}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)} | AstroThink"><meta property="og:description" content="{e(description)}">
{preload_tag}<link rel="stylesheet" href="styles.css"><script src="app.js" defer></script>
</head><body id="top" data-page="{active or 'home'}">{header(active)}<main id="main">{body}</main>{footer()}</body></html>'''
    (DIST/filename).write_text(html)

def team_card(person, number, full=False):
    tag = 'h2' if full else 'h3'
    extra = f'<p class="team-school">{e(person["school"])}</p><p class="team-bio">{e(person["bio"])}</p>' if full else ''
    return f'''<article class="team-card"><div class="portrait"><img src="assets/{person['photo']}" alt="{e(person['name'])}" loading="lazy" decoding="async" width="600" height="675"></div><{tag}>{e(person['name'])}</{tag}><p class="team-role">{e(person['role'])}</p>{extra}</article>'''

def parachute_diagram():
    return '''<svg viewBox="0 0 400 310" role="img" aria-labelledby="parachute-title"><title id="parachute-title">A parachute with upward air resistance and downward gravity.</title><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"><path d="M110 110a90 90 0 0 1 180 0c-15-18-30-18-45 0-15-18-30-18-45 0-15-18-30-18-45 0-15-18-30-18-45 0Z" fill="#f5d5e3" stroke="#b93370"/><path d="M155 110c0-52 18-90 45-90s45 38 45 90M200 20v90" stroke="#b93370"/><path d="m110 110 82 133m-37-133 37 133m8-133v133m45-133-37 133m82-133-82 133" stroke="#40667c"/><rect x="185" y="243" width="30" height="30" stroke="#40667c" fill="#c3dce9"/><path d="M328 154V76m-6 9 6-9 6 9M80 182v78m-6-9 6 9 6-9" stroke="#40667c"/></g><g fill="#35556a" font-family="Merriweather, Georgia, serif" font-size="11" font-weight="300"><text x="311" y="174">Drag</text><text x="51" y="284">Gravity</text></g></svg>'''

def partner_bar():
    return '''<section class="community-bar" aria-label="Community partners"><div class="container community-inner"><p class="kicker">Our partners</p><div class="partner-wordmark"><img src="assets/alive-center.png" alt="Alive Center" width="150" height="62" loading="lazy"></div><div class="partner-wordmark"><img src="assets/npl.png" alt="Naperville Public Library" width="150" height="62" loading="lazy"></div><div class="partner-wordmark"><img src="assets/district-204.png" alt="Indian Prairie School District 204" width="150" height="62" loading="lazy"></div></div></section>'''

def home():
    rows = ''
    for p in DATA['programs']:
        rows += f'''<a class="program-row" href="{p['slug']}.html"><div><h3 class="program-row-title">{e(p['title'])}</h3><p class="program-row-description">{e(p['short'])}</p></div><p class="program-row-meta">{e(p['audience'])}<br>{e(p['format'])}, {e(p['length'])}</p>{arrow()}</a>'''
    people = [DATA['team'][i] for i in [0,1,2,5]]
    cards = ''.join(team_card(p,i+1) for i,p in enumerate(people))
    return f'''<section class="hero"><div class="container hero-grid"><div class="hero-copy"><p class="hero-location">Naperville, Illinois</p><h1>AstroThink</h1><p class="hero-description">We are a student-led FlyingMinds program that teaches space science and artificial intelligence through hands-on activities. We run programs at schools, libraries, and community spaces in the Naperville area, along with online programs for older students.</p><div class="button-row">{button('Our programs','programs.html','button-blue')}{link('Our team','team.html')}</div></div>
<figure class="hero-art"><img class="rover-image" src="assets/mars-rover.webp" alt="White wireframe illustration showing the wheels, body, and mast of a Mars rover" width="1367" height="1151" fetchpriority="high" decoding="async"><figcaption>Our space curriculum includes rockets, parachutes, and Mars rovers.</figcaption></figure></div></section>
{partner_bar()}
<section class="section container mission" id="about"><div><h2 class="section-title">Our mission</h2></div><div class="mission-copy"><p class="mission-lead">We introduce students to space science and AI through activities they can build, test, and discuss. Our goal is to make these subjects approachable to students who have never tried them before.</p><p>Our team develops the curriculum and teaches the programs. Activities have included paper rockets, parachutes, and beginner AI lessons, with additional programs in coding, healthcare, and career exploration.</p>{link('About AstroThink','about.html')}</div></section>
<section class="section program-preview" aria-labelledby="programs-title"><div class="container"><div class="heading-row"><h2 class="section-title" id="programs-title">Our programs</h2><p>We offer programs for different ages, from elementary students trying engineering activities to high school students learning Python.</p></div><div class="program-list">{rows}</div><div class="program-bottom"><p>Summer 2026 sessions have concluded. See individual programs for details and contact us about future sessions.</p>{link('View all programs','programs.html')}</div></div></section>
<section class="section learn-feature"><div class="container learn-feature-grid"><div class="learn-feature-copy"><h2 class="section-title">Interactive activities</h2><p>Our parachute lab shows how canopy size and payload mass affect a fall. Students can change one variable at a time and compare the results.</p>{button('Open the parachute lab','explore.html','button-outline')}</div><figure class="diagram-preview">{parachute_diagram()}<figcaption>Gravity and air resistance act in opposite directions as the parachute falls.</figcaption></figure></div></section>
<section class="section container" aria-labelledby="team-title"><div class="heading-row"><h2 class="section-title" id="team-title">Our team</h2>{link('View the full team','team.html')}</div><div class="team-preview-grid">{cards}</div></section>
<section class="quote-strip"><div class="container quote-inner"><blockquote><p>“My favorite activity was the rocket”</p><cite>Kaidyn, age 8</cite></blockquote><blockquote><p>“I want to make my own robot”</p><cite>Zack, age 8</cite></blockquote></div></section>{contact_band()}'''

def programs():
    rows = ''
    for p in DATA['programs']:
        rows += f'''<article class="program-item" data-program data-filters="{' '.join(p['filter'])}"><div class="program-item-copy"><h2>{e(p['title'])}</h2><p>{e(p['description'])}</p>{link('Program details',p['slug']+'.html')}</div><div class="program-item-meta"><p><span class="meta-label">Who it's for</span>{e(p['audience'])}</p><p><span class="meta-label">Format</span>{e(p['format'])}, {e(p['length'])}</p><p><span class="meta-label">Cost</span>{e(p['cost'])}</p><p class="status-note">{e(p['status'])}</p></div></article>'''
    return f'''<section class="page-heading"><div class="container"><div class="page-heading-row"><h1>Our programs</h1><aside class="page-note"><p>Summer 2026 programs have concluded. Contact the team for future dates.</p></aside></div><p>AstroThink offers programs in space science, artificial intelligence, coding, healthcare, and career exploration. Age groups and session details are listed below.</p></div></section><section class="container program-index" aria-label="Program directory"><div class="filters" role="group" aria-label="Filter programs"><button class="filter-button" type="button" data-filter="all" aria-pressed="true">All programs</button><button class="filter-button" type="button" data-filter="younger" aria-pressed="false">Elementary & middle</button><button class="filter-button" type="button" data-filter="high-school" aria-pressed="false">High school</button><button class="filter-button" type="button" data-filter="online" aria-pressed="false">Online</button><span class="filter-count" role="status" aria-live="polite">4 programs</span></div><div>{rows}</div></section>{online_tools()}{contact_band()}'''

def online_tools():
    return f'''<section class="section online-tools"><div class="container"><h2 class="section-title">Online learning</h2><div class="tools-grid"><article class="tool-item"><h3>App Incubator</h3><p>Describe an app idea, choose who it's for, and use AI to build a live preview in the AstroThink learning portal.</p>{link('Open App Incubator','https://astrothink.flyingminds.org/design-course',True)}</article><article class="tool-item"><h3>Physics demos</h3><p>Explore paper airplanes, Mars rovers, parachutes, and circuits through the existing interactive demos.</p>{link('Visit the demo library','https://astrothink.flyingminds.org/astrothink/demos',True)}</article><article class="tool-item"><h3>Structured courses</h3><p>Explore space, physics, and AI through lessons, quizzes, and progress tracking in the learning portal.</p>{link('Browse courses','https://astrothink.flyingminds.org/courses',True)}</article></div><p class="portal-note">These tools open in AstroThink's existing learning portal. Some activities require a portal account.</p></div></section>'''

def program_detail(p):
    topics = ''.join(f'<li><div><h3>{e(t["name"])}</h3><p>{e(t["text"])}</p></div></li>' for i,t in enumerate(p['topics']))
    dates = f'<p><strong>Previous session:</strong> {e(p["dates"])}<br>{e(p["schedule"])}</p>' if p.get('dates') else ''
    facts = [('Who it’s for',p['audience']),('Format',p['location']),('Length',p['length']),('Cost',p['cost'])]
    facts_html = ''.join(f'<div><p class="fact-label">{e(k)}</p><p class="fact-value">{e(v)}</p></div>' for k,v in facts)
    return f'''<section class="detail-hero"><div class="container"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><a href="programs.html">Programs</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['title'])}</span></nav><div class="detail-grid"><div class="detail-copy"><p class="kicker">{e(p['audience'])} / {e(p['format'])}</p><h1>{e(p['title'])}</h1><p>{e(p['description'])}</p><p class="status-note">{e(p['status'])}</p></div></div></div></section><div class="container detail-facts">{facts_html}</div><section class="section container detail-body"><div><h2>Program topics</h2><p class="section-intro">{e(p['short'])}</p></div><div><ol class="topic-list">{topics}</ol><aside class="session-note"><p class="kicker">Session information</p>{dates}<p>{e(p['note'])}</p>{button('Ask about this program',mail('Question about '+p['title']))}</aside></div></section>{contact_band()}'''

def team():
    cards=''.join(team_card(p,i+1,True) for i,p in enumerate(DATA['team']))
    return f'''<section class="page-heading"><div class="container"><h1>Our team</h1><p>Our team develops curriculum, teaches programs, and coordinates STEM outreach.</p></div></section><section class="section container" aria-label="AstroThink team"><div class="team-full-grid">{cards}</div></section>{contact_band()}'''

def about():
    founders=''.join(team_card(p,i+1) for i,p in enumerate(DATA['team'][:2]))
    return f'''<section class="page-heading"><div class="container"><p class="kicker">A FlyingMinds program</p><h1>About AstroThink</h1><p>We're a student-led team based in the Naperville area, bringing space science and AI into places where students can explore them together.</p></div></section><section class="section container about-full"><div><h2>Our work</h2><p>AstroThink teaches students about space science and artificial intelligence through workshops, projects, and online activities. Students learn about topics such as rocket flight, parachutes, and how computers learn from data.</p><p>We develop lessons and activities for schools, libraries, and community programs, alongside resources students can explore online. Our programs now also include Python, healthcare, and career exploration for older students.</p>{link('See our programs','programs.html')}</div><div><div class="team-preview-grid" style="grid-template-columns:repeat(2,minmax(0,1fr))">{founders}</div><p class="muted" style="font-size:11px;margin-top:22px">Founded by Maya Sharma and Anwita Vemana.</p></div></section><section class="partner-list"><div class="container"><h2 class="partner-heading">Our partners</h2><div class="partner-grid"><article class="partner-tile"><img src="assets/alive-center.png" alt="Alive Center" width="210" height="80" loading="lazy"><h3>Alive Center</h3><p>A community partner and host for AstroThink's student-led space and AI program.</p></article><article class="partner-tile"><img src="assets/npl.png" alt="Naperville Public Library" width="210" height="80" loading="lazy"><h3>Naperville Public Library</h3><p>Our Career Pathways series has brought students and guest speakers together at the 95th Street Library.</p></article><article class="partner-tile"><img src="assets/district-204.png" alt="Indian Prairie School District 204" width="210" height="80" loading="lazy"><h3>District 204</h3><p>AstroThink's school programs have included hands-on space and AI sessions at Welch Elementary.</p></article></div></div></section><section class="section container about-full"><div><h2>Programs and guest speakers</h2></div><div><p>Our programs connect classroom ideas to people and projects. Students have explored healthcare with Aurora Public Library, asked career questions in a library speaker series, and taken their first steps with Python and neural networks online.</p><p>Space science guests have included astrobiologist Will Wallentine, whose work explores life in extreme environments and what it can tell us about other worlds.</p>{link('Meet everyone on the team','team.html')}</div></section>{contact_band()}'''

def contact():
    return f'''<section class="page-heading"><div class="container"><h1>Contact</h1><p>Ask about a program, bring an activity to your community, or say hello.</p></div></section><section class="container contact-layout"><div class="contact-main"><p class="kicker">Email the team</p><a class="contact-email" href="mailto:{EMAIL}">{EMAIL}</a><p>Tell us a little about what you're looking for. For program questions, include the student's grade and the topic they're interested in.</p><button class="copy-email" type="button" data-copy-email="{EMAIL}">Copy email address {arrow(False,True)}</button><p class="copy-status" role="status" aria-live="polite"></p><div class="social-row"><span>Follow along</span><a href="{DATA['instagram']}" target="_blank" rel="noopener noreferrer">@astrothinkfm ↗<span class="sr-only"> (opens in a new tab)</span></a></div></div><div class="contact-options"><a class="contact-option" href="{e(mail('AstroThink program inquiry'))}"><h2>Find a program{arrow(True)}</h2><p>Ask about dates, age groups, and future sessions.</p></a><a class="contact-option" href="{e(mail('AstroThink community partnership'))}"><h2>Work with us{arrow(True)}</h2><p>Schools, libraries, and community groups interested in a collaboration.</p></a><a class="contact-option" href="{e(mail('Getting involved with AstroThink'))}"><h2>Get involved{arrow(True)}</h2><p>Tell us about your interests in teaching, curriculum, or STEM outreach.</p></a></div></section><section class="section faq"><div class="container faq-grid"><h2 class="section-title">Frequently asked questions</h2><div><details><summary>What ages are the programs for?</summary><p>Our core space and AI activities are for younger students. Other programs serve middle and high school students. The programs page lists the age group for each offering.</p></details><details><summary>Does every program cost the same?</summary><p>No. Python & Neural Networks, Beyond the Stethoscope, and Career Pathways were offered free in Summer 2026. Ask us about pricing and availability for future sessions and school programs.</p></details><details><summary>How do I register for the next session?</summary><p>Our published Summer 2026 sessions have concluded. Email us or check Instagram for information about future sessions.</p></details><details><summary>Do I need an account to explore?</summary><p>You can use the parachute lab on this site without an account. Some tools in the existing AstroThink learning portal require a separate portal account.</p></details></div></div></section>'''

def explore():
    return f'''<div class="explore-hero"><section class="page-heading"><div class="container"><h1>Interactive activities</h1><p>Use the parachute lab to explore gravity and air resistance, or visit the learning portal for more activities.</p></div></section></div><section class="container lab-section" aria-labelledby="lab-title"><div class="lab-top"><h2 id="lab-title">Parachute lab</h2><p class="kicker">Flight and air resistance</p></div><div class="lab" data-parachute-lab><div class="lab-stage" role="img" aria-label="Animation of a parachute falling from 20 metres to the ground"><p class="lab-stage-label">Drop height / 20 m</p><p class="lab-altitude"><span data-height>20.0</span> m to ground</p><div class="lab-guide" aria-hidden="true"></div><div class="parachute-drop" aria-hidden="true"><svg viewBox="0 0 100 112" fill="none" stroke-width="1.1" stroke-linejoin="round"><g data-canopy><path d="M5 42a45 37 0 0 1 90 0c-8-8-15-8-22.5 0-7.5-8-15-8-22.5 0-7.5-8-15-8-22.5 0C20 34 12 34 5 42Z" fill="#eeb2cf" stroke="#b93370"/><path d="M27.5 42C27.5 20 36 5 50 5s22.5 15 22.5 37M50 5v37" stroke="#b93370"/></g><path d="m5 42 42 53M27.5 42 47 95M50 42v53m22.5-53-19.5 53M95 42 53 95" stroke="#416b83"/><rect x="43" y="95" width="14" height="14" fill="#76b8da" stroke="#416b83"/></svg></div><p class="lab-stage-caption">Compare the fall time<br>for different canopy sizes.</p><div class="lab-ground" aria-hidden="true"></div><p class="lab-ground-label">GROUND LEVEL</p></div><div class="lab-controls"><div class="control"><label class="control-label" for="canopy">Canopy diameter <output id="canopy-value" for="canopy">0.80 m</output></label><input id="canopy" type="range" min="0.3" max="1.3" step="0.05" value="0.8" aria-describedby="canopy-hint"><div class="range-labels" id="canopy-hint"><span>0.30 m</span><span>1.30 m</span></div></div><div class="control"><label class="control-label" for="payload">Payload mass <output id="payload-value" for="payload">0.30 kg</output></label><input id="payload" type="range" min="0.1" max="1" step="0.05" value="0.3" aria-describedby="payload-hint"><div class="range-labels" id="payload-hint"><span>0.10 kg</span><span>1.00 kg</span></div></div><div class="lab-readout"><div><span class="readout-label">Terminal speed</span><span class="readout-value" data-terminal>2.52 <span class="readout-unit">m/s</span></span></div><div><span class="readout-label">Predicted fall time</span><span class="readout-value" data-time>8.1 <span class="readout-unit">s</span></span></div></div><div class="lab-actions"><button class="button button-blue" type="button" data-drop>Drop parachute {arrow()}</button><button class="button button-outline reset-button" type="button" data-reset aria-label="Reset experiment">↺</button></div><p class="lab-status" role="status" aria-live="polite">Change a setting, then drop the parachute.</p></div></div><div class="lab-caption"><p>A simplified model with constant air density, a fully open canopy, and quadratic drag. The animation runs at real time.</p><p>Earth gravity: 9.81 m/s² / Air density: 1.225 kg/m³ / Drag coefficient: 1.5</p></div><div class="lab-explanation"><div><h3>How the model works</h3><p>Gravity pulls the payload down. Air resistance pushes against the motion. A larger canopy catches more air, increasing drag. A heavier payload needs a greater drag force to balance its weight.</p><p>When those forces balance, the parachute reaches its terminal speed. Try keeping the mass fixed while changing the canopy diameter.</p></div><aside class="experiment-prompt"><p class="kicker">Suggested experiment</p><p>Double the canopy diameter while keeping the mass the same. The canopy area becomes four times larger. In this model, that halves the terminal speed.</p></aside></div></section>{online_tools()}{contact_band()}'''

def main():
    DIST.mkdir(exist_ok=True)
    page('index.html','Home','Student-led space science, AI, and hands-on STEM programs in Naperville and online. Explore AstroThink programs and meet the team.',home(),preload=True)
    page('about.html','About','Meet AstroThink, a student-led FlyingMinds program for space science, artificial intelligence, and hands-on STEM education.',about(),'about')
    page('programs.html','Programs','Explore AstroThink space and AI, Python and neural networks, healthcare, and career exploration programs.',programs(),'programs')
    page('team.html','Our team','Meet the students behind AstroThink: curriculum developers, teachers, and STEM outreach leaders.',team(),'team')
    page('explore.html','The parachute lab','Change the canopy size and payload in a real-time parachute experiment. Explore gravity, air resistance, and terminal speed.',explore(),'explore')
    page('contact.html','Contact','Contact AstroThink about programs, school and library partnerships, and getting involved with student-led STEM education.',contact(),'contact')
    for p in DATA['programs']:
        page(p['slug']+'.html',p['title'],p['short'],program_detail(p),'programs')
    # A useful, styled destination for mistyped links on static hosting.
    page('404.html','Page not found','The page you requested could not be found.',f'<section class="section container"><p class="kicker">404</p><h1 class="section-title" style="margin:20px 0">Page not found</h1><p class="section-intro" style="margin-bottom:25px">Find your way back to AstroThink.</p>{button("Go to the homepage","index.html")}</section>')
    urls=['index.html','about.html','programs.html','team.html','explore.html','contact.html']+[p['slug']+'.html' for p in DATA['programs']]
    if ORIGIN:
        (DIST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}/{url}</loc></url>' for url in urls)+'</urlset>')
    (DIST/'robots.txt').write_text('User-agent: *\nAllow: /\n')
    (DIST/'.nojekyll').touch()
    print(f'Built {len(urls)} pages + 404.')

if __name__ == '__main__':
    main()
