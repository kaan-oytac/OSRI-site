#!/usr/bin/env python3
"""Builds the OSRI website.

Run it after changing anything in `content/` or `pages/`:

    python build.py

It reads the content files, fills in the shared header, navigation and footer,
and writes the finished .html pages into this folder. Those .html files are the
website — you never edit them by hand.

See PUBLISHING.md for the plain-English version.
"""
import datetime
import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent

# The live address. Used for link previews and the sitemap; both need the full
# URL, not a relative path. Change this if the domain ever changes.
SITE_URL = "https://osri.ca"

NAV = [
    ("index.html", "Home"),
    ("publications.html", "Publications"),
    ("questions.html", "Research Questions"),
    ("guidelines.html", "Guidelines"),
    ("submit.html", "Submit"),
    ("about.html", "About"),
]

TYPE_LABELS = {
    "review": "Literature review",
    "public-data": "Public dataset",
    "original-data": "Original data",
}

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


class ContentError(Exception):
    """A problem in a content file, reported with the file name."""


# --------------------------------------------------------------------------
# Reading content files
# --------------------------------------------------------------------------

def parse_block(text, source):
    """Split 'key: value' lines from the body text that follows '---'."""
    if "---" in text:
        head, _, body = text.partition("\n---\n")
    else:
        head, body = text, ""
    fields = {}
    for number, line in enumerate(head.strip().splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            raise ContentError(
                f"{source}, line {number}: expected 'something: value' but found:\n    {line}"
            )
        key, _, value = line.partition(":")
        fields[key.strip().lower()] = value.strip()
    body = body.strip()
    if body.startswith("<p>") and body.endswith("</p>") and body.count("<p>") == 1:
        body = body[3:-4].strip()
    fields["body"] = body
    return fields


def read_items(folder):
    items = []
    directory = ROOT / "content" / folder
    if not directory.is_dir():
        return items
    for path in sorted(directory.glob("*.txt")):
        if path.name.startswith("_"):
            continue
        item = parse_block(path.read_text(encoding="utf-8"), path.name)
        item["_file"] = path.name
        items.append(item)
    return items


def require(item, *keys):
    for key in keys:
        if not item.get(key):
            raise ContentError(f"{item['_file']}: missing '{key}:'")


def pretty_date(value, source):
    try:
        d = datetime.date.fromisoformat(value)
    except ValueError:
        raise ContentError(
            f"{source}: date '{value}' should be written as YYYY-MM-DD, e.g. 2026-09-12"
        )
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}", d


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def check_file(item, field):
    """A linked file that is not there produces a dead link nobody notices
    until a reader clicks it. Catch it at build time instead."""
    value = item.get(field)
    if not value:
        return
    if (ROOT / value).is_file():
        return
    name = pathlib.PurePosixPath(value).name
    matches = [str(c.relative_to(ROOT)).replace("\\", "/")
               for c in ROOT.rglob(name)
               if c.is_file() and "__pycache__" not in c.parts]
    hint = (f"\n    The file exists at:  {field}: {matches[0]}"
            f"\n    The path must include the folder, not just the file name."
            if matches else
            "\n    No file with that name exists anywhere in the site folder.")
    raise ContentError(
        f"{item['_file']}: {field} points to '{value}', which does not exist.{hint}")


def render_entry(item, show_abstract=True):
    require(item, "title", "date", "format", "type")
    check_file(item, "pdf")
    check_file(item, "image")
    shown, _ = pretty_date(item["date"], item["_file"])

    byline = " &middot; ".join(
        part for part in (
            item.get("author", "").strip(),
            item.get("school", "").strip(),
            f"Grade {item['grade']}" if item.get("grade") else "",
            shown,
        ) if part
    )

    kind = "Paper" if item["format"] == "paper" else "Mini-paper"
    tags = [f'<span class="tag paper">{kind}</span>' if kind == "Paper"
            else f'<span class="tag">{kind}</span>']
    label = TYPE_LABELS.get(item["type"])
    if not label:
        raise ContentError(
            f"{item['_file']}: type '{item['type']}' is not one of: "
            + ", ".join(TYPE_LABELS)
        )
    tags.append(f'<span class="tag">{label}</span>')
    if item.get("featured", "").lower() in ("yes", "true"):
        tags.append('<span class="tag">Editor\'s selection</span>')
    if item.get("pdf"):
        tags.append(f'<a href="{html.escape(item["pdf"], quote=True)}">PDF</a>')

    link = item.get("pdf") or "#"

    thumb, row_class = "", "entry"
    if item.get("image"):
        row_class = "entry has-figure"
        alt = html.escape(item.get("image-alt", ""), quote=True)
        thumb = (f'\n        <figure class="entry-thumb">'
                 f'<img src="{html.escape(item["image"], quote=True)}" alt="{alt}" loading="lazy">'
                 f'</figure>')
    abstract = ""
    if show_abstract and item["body"]:
        abstract = f'\n        <p class="abstract">{item["body"]}</p>'
    if show_abstract and item.get("note"):
        abstract += f'\n        <p class="entry-note">{item["note"]}</p>'

    return (
        f'      <li class="{row_class}" data-tags="{item["type"]}">{thumb}\n'
        f'        <div>\n'
        f'        <h3><a href="{html.escape(link, quote=True)}">{item["title"]}</a></h3>\n'
        f'        <p class="byline">{byline}</p>{abstract}\n'
        f'        <div class="meta">{"".join(tags)}</div>\n'
        f'        </div>\n'
        f'      </li>'
    )


def render_entry_list(items, show_abstract=True, empty=None):
    if not items:
        return ('    <div class="panel empty-state">\n'
                f'      {empty or "<p>Nothing here yet.</p>"}\n'
                '    </div>')
    rows = "\n".join(render_entry(i, show_abstract) for i in items)
    return f'    <ol class="entry-list">\n{rows}\n    </ol>'


def render_question(item):
    require(item, "group", "question", "dataset", "method", "tier")
    credit = ""
    if item.get("suggested-by"):
        credit = (f'<p class="muted" style="font-size:0.85rem;margin-bottom:0">'
                  f'Suggested by {item["suggested-by"]}</p>')
    note = f'<p>{item["body"]}</p>' if item["body"] else ""
    source_label = "Source" if item["tier"].lower().startswith("green (") else "Dataset"
    return f"""        <article class="rq">
          <div>
            <h3>{item['question']}</h3>
            {note}
            {credit}
          </div>
          <dl class="dataset">
            <dt>{source_label}</dt><dd>{item['dataset']}</dd>
            <dt>Method</dt><dd>{item['method']}</dd>
            <dt>Ethics tier</dt><dd>{item['tier']}</dd>
          </dl>
        </article>"""


def render_questions(items):
    if not items:
        return '    <p class="muted">No questions in the bank yet.</p>'
    groups = {}
    for item in items:
        require(item, "group")
        groups.setdefault(item["group"], []).append(item)

    out = []
    for name, members in groups.items():
        slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
        note = ""
        if members[0].get("group-note"):
            note = f'        <p class="muted">{members[0]["group-note"]}</p>\n'
        body = "\n".join(render_question(m) for m in members)
        out.append(
            f'      <div class="rq-group" id="{slug}">\n'
            f'        <h2>{name}</h2>\n{note}{body}\n'
            f'      </div>'
        )
    return "\n\n".join(out)


def render_news(path):
    if not path.exists():
        return ""
    rows = []
    for raw in path.read_text(encoding="utf-8").split("\n===\n"):
        if not raw.strip():
            continue
        item = parse_block(raw, path.name)
        item["_file"] = path.name
        require(item, "date", "title")
        shown, _ = pretty_date(item["date"], path.name)
        link = html.escape(item.get("link", "#"), quote=True)
        body = f'\n          <p>{item["body"]}</p>' if item["body"] else ""
        rows.append(
            f'        <li>\n'
            f'          <time datetime="{item["date"]}">{shown}</time>\n'
            f'          <a href="{link}">{item["title"]}</a>{body}\n'
            f'        </li>'
        )
    return f'      <ul class="news">\n' + "\n".join(rows) + "\n      </ul>"


# --------------------------------------------------------------------------
# Page shell
# --------------------------------------------------------------------------

HEAD = """<!DOCTYPE html>
<html lang="en-CA">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{site}/{page}">

  <!-- How the page looks when the link is shared in a message, an email
       preview, or on social media. Without these it shows as a bare URL. -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Okanagan Student Research Initiative">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{site}/{page}">
  <meta property="og:image" content="{site}/assets/social.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Okanagan Student Research Initiative">
  <meta property="og:locale" content="en_CA">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{site}/assets/social.jpg">

  <link rel="icon" href="assets/seal.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&display=swap">
  <link rel="stylesheet" href="css/styles.css">
</head>
<body>
"""


def header(active):
    rows = []
    for href, label in NAV:
        current = ' aria-current="page"' if href == active else ""
        rows.append(f'        <li><a href="{href}"{current}>{label}</a></li>')
    items = "\n".join(rows)
    return f"""<div class="utility">
  <div class="wrap">
    <span>Okanagan Valley, British Columbia</span>
    <nav aria-label="Utility">
      <a href="about.html#contact">Contact</a>
      <a href="about.html#join">Join OSRI</a>
      <a href="submit.html">Submit work</a>
    </nav>
  </div>
</div>

<header class="masthead">
  <div class="wrap">
    <img class="seal" src="assets/seal.png" alt="" width="84" height="89">
    <a class="wordmark" href="index.html">
      <span class="name">Okanagan Student Research Initiative</span>
      <span class="place">Student-led research, reviewed and published</span>
    </a>
  </div>
</header>

<nav class="primary-nav" aria-label="Primary">
  <div class="wrap">
    <ul>
{items}
    </ul>
  </div>
</nav>

<div class="guilloche-rule" role="presentation"></div>

<main id="main">
"""


FOOTER = """</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="brand">
        <span class="name">Okanagan Student Research Initiative</span>
        <p>A student-run venue for secondary school research in the Okanagan Valley. OSRI suggests research questions matched to real datasets, reviews manuscripts against a published ethics standard, and hosts the finished work online at no cost to authors.</p>
        <p><strong>OSRI ethics review is not IRB or REB approval</strong> and does not substitute for it.</p>
      </div>
      <div>
        <h3>Initiative</h3>
        <ul>
          <li><a href="about.html">About OSRI</a></li>
          <li><a href="about.html#panel">Ethics Review Panel</a></li>
          <li><a href="about.html#join">Join OSRI</a></li>
          <li><a href="about.html#contact">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3>Publish</h3>
        <ul>
          <li><a href="guidelines.html">Submission guidelines</a></li>
          <li><a href="guidelines.html#ethics">Ethics standard</a></li>
          <li><a href="guidelines.html#ai">AI disclosure policy</a></li>
          <li><a href="consent.html">Consent templates</a></li>
          <li><a href="submit.html">Submit a manuscript</a></li>
        </ul>
      </div>
      <div>
        <h3>Browse</h3>
        <ul>
          <li><a href="publications.html#papers">Papers</a></li>
          <li><a href="publications.html#mini-papers">Mini-papers</a></li>
          <li><a href="questions.html">Research questions</a></li>
          <li><a href="questions.html#suggest">Suggest a question</a></li>
          <li><a href="credits.html">Image credits</a></li>
        </ul>
      </div>
    </div>
    <img class="fleuron" src="assets/ornaments/laurel-divider.svg" alt="" width="340" height="42">
    <div class="footer-legal">
      <p>&copy; {year} Okanagan Student Research Initiative. Published work is licensed CC BY 4.0 unless otherwise stated. <a href="privacy.html">Privacy</a></p>
      <p>OSRI operates on the unceded territory of the Syilx Okanagan people.</p>
    </div>
  </div>
</footer>
</body>
</html>
"""


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build():
    publications = read_items("publications")
    for item in publications:
        require(item, "date", "format")
        _, item["_date"] = pretty_date(item["date"], item["_file"])
        if item["format"] not in ("paper", "mini"):
            raise ContentError(
                f"{item['_file']}: format must be 'paper' or 'mini', not '{item['format']}'"
            )
    publications.sort(key=lambda i: i["_date"], reverse=True)

    papers = [i for i in publications if i["format"] == "paper"]
    minis = [i for i in publications if i["format"] == "mini"]
    questions = read_items("questions")

    empty_papers = (
        "<p><strong>No papers have been published yet.</strong> OSRI opened for "
        "submissions in its founding year; the first accepted paper will appear here.</p>"
        '<p><a href="submit.html">Submit a manuscript</a> &middot; '
        '<a href="guidelines.html">Read the guidelines first</a></p>')
    empty_minis = (
        "<p><strong>No mini-papers yet.</strong> A mini-paper is one to three "
        "paragraphs: a single claim, the evidence for it, and one limitation. It is "
        "the quickest way to have real work published and reviewed.</p>"
        '<p><a href="submit.html">Submit a mini-paper</a> &middot; '
        '<a href="questions.html">Find a question to answer</a></p>')

    tokens = {
        "papers": render_entry_list(papers, empty=empty_papers),
        "mini-papers": render_entry_list(minis, empty=empty_minis),
        "latest-papers": render_entry_list(papers[:3], empty=empty_papers),
        "latest-minis": render_entry_list(minis[:3], show_abstract=False, empty=empty_minis),
        "questions": render_questions(questions),
        "news": render_news(ROOT / "content" / "news.txt"),
        "year": str(datetime.date.today().year),
    }

    built = []
    for src in sorted((ROOT / "pages").glob("*.html")):
        meta = {}
        lines = src.read_text(encoding="utf-8").split("\n")
        start = 0
        for index, line in enumerate(lines):
            if line.startswith("<!-- ") and ":" in line and line.endswith(" -->"):
                key, _, value = line[5:-4].partition(":")
                meta[key.strip()] = value.strip()
                start = index + 1
            else:
                break
        if "title" not in meta or "description" not in meta:
            raise ContentError(f"pages/{src.name}: needs a title and description comment at the top")

        body = "\n".join(lines[start:]).strip("\n") + "\n"
        page = HEAD.format(title=meta["title"], description=meta["description"],
                           site=SITE_URL, page=src.name)
        page += header(src.name) + body + FOOTER.format(year=tokens["year"])

        for name, value in tokens.items():
            page = page.replace("{{" + name + "}}", value)

        leftover = re.search(r"\{\{([a-z-]+)\}\}", page)
        if leftover:
            raise ContentError(
                f"pages/{src.name}: unknown placeholder {{{{{leftover.group(1)}}}}}. "
                f"Known ones: " + ", ".join(sorted(tokens))
            )

        target = ROOT / src.name
        previous = target.read_text(encoding="utf-8") if target.exists() else None
        target.write_text(page, encoding="utf-8")
        built.append((src.name, previous != page))

    today = datetime.date.today().isoformat()
    urls = "\n".join(
        f"  <url><loc>{SITE_URL}/{name}</loc><lastmod>{today}</lastmod></url>"
        for name, _ in sorted(built) if name != "404.html")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n",
        encoding="utf-8")

    changed = [name for name, diff in built if diff]

    print(f"Writing into: {ROOT.resolve()}")
    print()
    for name, diff in built:
        print(f"  {'CHANGED  ' if diff else 'unchanged'}  {name}")
    print()
    print(f"{len(papers)} papers, {len(minis)} mini-papers, "
          f"{len(questions)} research questions")
    print()
    if changed:
        print(f"BUILD OK - {len(changed)} file(s) updated: {', '.join(changed)}")
    else:
        print("BUILD OK - but nothing changed.")
        print()
        print("Every page already matched its source. If you were expecting a")
        print("change, the edit was probably saved somewhere else - a second")
        print("copy of this folder, or inside the zip rather than the extracted")
        print("folder. The folder written to is printed above; check that your")
        print("edit is in ITS pages\\ folder.")
    print()
    print("Also wrote sitemap.xml and robots.txt.")
    print("Open index.html in your browser. Press Ctrl+F5 if it looks stale.")


if __name__ == "__main__":
    try:
        build()
    except ContentError as problem:
        print("\nThe site was NOT rebuilt. There is a problem in a content file:\n")
        print(f"  {problem}\n")
        print("Fix that file and run this again. Nothing else was changed.")
        sys.exit(1)
