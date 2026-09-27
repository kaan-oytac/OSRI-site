# Running the OSRI site

> **Publishing your first paper, or going live for the first time?**
> Read **LAUNCH.md** instead. It is a numbered walkthrough from finished
> manuscript to live website. This file is the day-to-day reference you come
> back to afterwards.


Everything you change day to day lives in two folders:

    content\    the things that change often (publications, questions, announcements)
    pages\      the wording of each page

One more file matters:

    build.bat     double-click this to rebuild the site
    diagnose.bat  double-click this if a rebuild seems to do nothing

You never edit the `.html` files in the main folder. Those are generated.
After any change, rebuild them.

### The easy way: double-click `build.bat`

`build.bat` sits in the site folder. Double-click it. A black window opens,
builds the site, and waits for a keypress so you can read what it said.
That is the whole process — no typing, no terminal.

### The typed way: `python build.py`

If you prefer PowerShell, you must be **inside the site folder** first, or
Python will not find the file:

    PS C:\Users\you> python build.py
    can't open file 'C:\Users\you\build.py': [Errno 2] No such file or directory

That error means you are in the wrong folder, not that anything is broken.
The quickest fix: open the site folder in File Explorer, click the address
bar, type `powershell`, and press Enter. PowerShell opens already inside that
folder. Then `python build.py` works.

Either way, open `index.html` afterwards to check it, then publish (see
"Putting changes live" below).

---

## Adding a publication

The `content\publications\` folder starts with only `_TEMPLATE.txt` in it.
Files whose names start with an underscore are ignored by the build, so the
template sits there as a reference without appearing on the site.

1. Go into `content\publications\`
2. Copy any existing file and rename it. Use the date and a short name, like
   `2026-10-03-lake-temperature.txt`. The filename is only for your own
   ordering; the site uses the `date:` line inside.
3. Open it in Notepad and fill it in:

       title: How August Surface Temperature in Okanagan Lake Has Changed Since 1990
       author: Priya Sharma
       school: Kelowna Secondary School
       grade: 11
       date: 2026-10-03
       format: paper
       type: public-data
       pdf: files/2026-lake-temperature.pdf
       ---
       The abstract goes here, after the three dashes. One paragraph is plenty.

4. Put the PDF itself in the `files\` folder, and make the `pdf:` line match
   its name. Leave the `pdf:` line out entirely if there is no file yet.
5. Run `python build.py`

**The lines that matter:**

| Line | What to put |
|---|---|
| `format:` | `paper` or `mini` — decides which section it appears in |
| `type:` | `review`, `public-data` or `original-data` — sets the tag and the filter |
| `date:` | Always `YYYY-MM-DD`. Newest appears first. |
| `featured:` | `yes` adds an "Editor's selection" tag. Leave it out otherwise. |
| `pdf:` | Path to the file, e.g. `files/name.pdf`. Optional. |

The newest three papers and three mini-papers appear on the home page
automatically. You do not maintain that list separately.

---

## Adding a research question

1. Go into `content\questions\`
2. Copy an existing file. **The number at the start of the filename controls
   the order and the grouping**, so pick one that sits where you want it:

   - `10`–`19` Wildfire, air & climate
   - `20`–`29` Water, lake & land
   - `30`–`39` Housing, community & economy
   - `40`–`49` School, behaviour & daily life

   To start a new group, use a new number range and write the new group name
   on the `group:` line. Groups appear in filename order.

3. Fill it in:

       group: Water, lake & land
       question: How has August surface temperature in Okanagan Lake changed since 1990?
       dataset: Water Survey of Canada; Okanagan Basin Water Board monitoring reports
       method: Annual August mean by year; linear trend
       tier: Green
       suggested-by: Priya Sharma, Kelowna Secondary School
       ---
       A short note on why this question is worth answering.

   `suggested-by:` is optional — use it to credit a student who sent the
   question in through the form.

4. Run `python build.py`

---

## Adding an announcement

Open `content\news.txt`. Each announcement is separated by a line of three
equals signs. Newest goes at the top:

    date: 2026-10-03
    title: Reviewer pool reaches twenty
    link: about.html#join
    ---
    A one-line description.
    ===
    date: 2026-09-15
    ...

---

## Changing wording on a page

Open the matching file in `pages\` — `pages\about.html`, `pages\guidelines.html`,
and so on. These are the editable versions. Edit the text between the tags,
leave the tags alone, and run `python build.py`.

Anything in double curly braces, like `{{questions}}`, is where the build
inserts content from the `content` folder. Don't delete those.

---

## When a rebuild does not seem to take effect

Double-click **`diagnose.bat`**. It changes nothing and prints:

- the exact folder it is running in
- whether the folder is properly extracted
- whether Python is found
- the modification time of every file in `pages\` and every output `.html`
- the build output

The three things that cause this, in order of how often they happen:

1. **The build failed and the message scrolled past.** A mistake in *any one*
   page or content file stops the whole build, so an error in `about.html` will
   stop your edit to `index.html` from appearing. The build prints which file.
2. **Two copies of the folder.** You edited one and built the other. `build.bat`
   now prints the folder it is working in at the top — check it matches where
   you edited.
3. **Editing inside the zip.** Windows lets you open and appear to save files
   inside a zip without extracting it. Right-click the zip, choose
   **Extract All**, and work only in the folder it creates.

If the build says **"BUILD OK - but nothing changed"**, your edit is not in the
folder being built. That message names the folder.

## When something goes wrong

If you make a mistake in a content file, `build.py` refuses to rebuild and
tells you which file and what is wrong:

    The site was NOT rebuilt. There is a problem in a content file:

      2026-10-03-lake-temperature.txt: date 'Oct 3 2026' should be written as YYYY-MM-DD

Your live site is untouched until a build succeeds. Fix the file, run it again.

---

## Putting changes live

### First-time setup (about 30 minutes, once)

1. Make a free account at **github.com** and a free account at **netlify.com**.
2. On GitHub, create a new repository called `osri-site`. Choose **Public**.
3. Upload this whole folder to it (GitHub's "uploading an existing file" link
   lets you drag the folder in).
4. On Netlify: **Add new site → Import an existing project → GitHub →**
   pick `osri-site`. Netlify reads `netlify.toml` and fills in the settings
   itself. Click Deploy.
5. Netlify gives you a temporary address like `wandering-lake-4821.netlify.app`.
   Check the site works there.
6. **Domain settings → Add a domain → `osri.ca`.** Netlify shows you the two
   nameservers to enter at whoever you bought the domain from. Do that, then
   wait — it usually takes under an hour, occasionally a day.
7. HTTPS turns itself on once the domain resolves. Nothing to buy.

### Every time after that

Edit the file on **github.com** directly (click the file, then the pencil
icon, then "Commit changes"), or edit locally and upload. Netlify sees the
change, runs `python build.py` itself, and the site updates in under a minute.

You do not have to run `build.py` yourself before uploading — but it is worth
doing anyway, so you catch a mistake on your own computer instead of on the
live site.

---

## The two forms

`Submit a manuscript` and `Suggest a research question` are handled by
**Netlify Forms**. There is nothing to install; Netlify detects them on deploy.

- Read submissions at: Netlify dashboard → your site → **Forms**
- To get an email each time: **Forms → Form notifications → Add notification
  → Email notification**. Do this on day one, or you will not notice
  submissions.
- The free plan covers 100 submissions a month, which is well beyond what
  OSRI will see in its first year.
- Both forms have a hidden anti-spam field. Ignore it; it is not visible to
  students.

**Suggested questions do not appear on the site automatically.** They arrive
in your inbox, you decide, and you add the good ones to
`content\questions\` with a `suggested-by:` credit. That is deliberate — an
academic venue should not have an unmoderated posting feature.

---

## Before you launch

- [ ] Add at least one real publication to `content\publications\`. The folder
      currently holds only `_TEMPLATE.txt`, which the build ignores, so both
      sections read "Nothing published here yet."
- [ ] Put your real email addresses in `pages\about.html` and
      `pages\privacy.html` (search both for `example.org`).
- [ ] Put your real name in the People section of `pages\about.html`.
- [ ] Put today's date at the top of `pages\privacy.html` (search for `[date]`).
- [ ] Buy the domain. Hosting is free; the domain is not. See below.
- [ ] Turn on Netlify form notifications.

## Buying the domain

Netlify hosting is free, and it gives you a free address like
`osri-site.netlify.app`. The domain `osri.ca` is a separate thing that you
rent from a registrar, and it always costs money — nothing makes that part
free.

- A `.ca` domain runs roughly **$15–25 CAD a year**. Registrars that sell them
  include Namecheap, Cloudflare, Porkbun and Canadian Domain Name Services.
- `.ca` domains have a Canadian presence requirement, set by CIRA. As a
  Canadian resident you qualify; you enter your own details when you buy it.
- Watch the renewal price, not just the first-year price. Some registrars
  advertise a cheap first year and charge more afterwards. Turn on
  auto-renew — a lapsed domain can be bought by someone else, and links to
  your published papers would break permanently.
- You do **not** need to buy hosting, an SSL certificate, or a website
  builder plan. Netlify's free tier covers the site and HTTPS.

Once bought: in Netlify, **Domain settings → Add a domain → osri.ca**.
Netlify shows you nameservers; enter those at your registrar. It usually
works within the hour.


## The optional `note:` line

A publication can carry a short italic note under its abstract, for anything a
reader deserves to know:

    note: Reviewed and accepted by [name]; the author is OSRI's founding editor and took no part in the decision on this paper.

Use it for a conflict-of-interest disclosure, a correction, or a withdrawal
notice. Leave the line out entirely when there is nothing to say.

## Consent templates and privacy notice

Two pages exist that are not in the main navigation, because they are
reference material rather than places people browse:

- `pages\consent.html` — five ready-to-use consent templates (anonymous
  survey, parental permission, assent, adult interview, debrief). Linked from
  the ethics section of the Guidelines page and from the footer.
- `pages\privacy.html` — the privacy notice, linked from under both forms and
  from the footer. **Fill in the date and your real email address before
  launch.** It describes what the site actually does, so if you change how
  submissions are handled, change this page too.


## Images and ornaments

The site's decorative artwork lives in `assets\ornaments\` and is generated by
`make_ornaments.py` — drawn from scratch by mathematics, so none of it carries
a copyright or needs attribution. You only need to re-run that script if you
want to change the artwork itself.

The home page opens on a photograph (`assets\hero.jpg`). To swap it, or to
change how much of it shows through the cream wash, see **IMAGES.md**.

To add other photographs or historical plates, read **IMAGES.md** too. It lists vetted
public-domain sources, how to check a licence, where the image slots are, and
how to keep file sizes down.

Every image on the site is listed on `pages\credits.html`. Add a row there
whenever you add an image — a venue that asks authors to cite their sources
should cite its own.

### Giving a publication a thumbnail

Add two lines to its file in `content\publications\`:

    image: assets/lake-temperature-chart.png
    image-alt: Line chart of August lake surface temperature, 1990 to 2025

The entry then shows a small plate beside the title. A chart from the paper
itself works better than a stock photograph.
