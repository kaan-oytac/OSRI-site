# Publishing a paper, and going live

Three parts. Do Part 1 and Part 2 once. Part 3 is the loop you repeat for
every paper from then on, and it takes about five minutes.

---

# PART 1 — Add your paper

Do this before going live, so the site opens with something in it.

## Step 1. Get the decision made

**Someone other than you must decide on your own paper.** You are the founding
editor; if you accept your own first paper, the venue has no credibility to
lend anyone else. A teacher, a reviewer, or your faculty advisor once you have
one.

Ask them for three or four sentences: accept, revise or decline, and why. Save
that email. It is your record that review happened.

## Step 2. Export the PDF

Export a **final PDF**, not a Google Doc link. Shared links break; your
Publications page promises work is "hosted here permanently".

Put this block at the top of page one. Every future paper will copy it, so it
is worth getting right now:

    [Title]
    [Author], Grade [__], [School]

    Published by the Okanagan Student Research Initiative
    osri.ca - [date]

    Licensed CC BY 4.0. The author retains copyright.

    [Only if the study involved people:]
    Reviewed under OSRI's [green/yellow] tier. OSRI ethics review is not
    IRB or REB approval and does not substitute for it.

Name the file plainly, with the year first:

    2026-wildfire-smoke-attendance.pdf

Save it into the **`files`** folder.

## Step 3. Write the entry

In **`content\publications\`**, make a copy of `_TEMPLATE.txt` and rename it to
the date plus a short name:

    2026-10-03-wildfire-smoke-attendance.txt

Open it in Notepad, delete the `#` comment lines at the top, and fill it in:

    title: Wildfire Smoke Days and Secondary School Attendance, 2017-2023
    author: Kaan Martin Oytac
    school: [Your School]
    grade: 12
    date: 2026-10-03
    format: paper
    type: public-data
    pdf: files/2026-wildfire-smoke-attendance.pdf
    note: Reviewed and accepted by [name]. The author is OSRI's Founding Editor and took no part in the decision on this paper.
    ---
    The abstract goes here, after the three dashes. One paragraph: the
    question you asked, the data you used, and what you found.

**The three fields that must be exactly right:**

| Field | Allowed values |
|---|---|
| `format:` | `paper` or `mini` |
| `type:` | `review`, `public-data`, or `original-data` |
| `date:` | `YYYY-MM-DD` — always this shape |
| `pdf:` | A **path**, so it must begin `files/` — `files/2026-my-paper.pdf` |

The `pdf:` line trips everyone once. It is the path from the site folder to the
PDF, not the file's name on its own. Writing `pdf: 2026-my-paper.pdf` points at
the site root, where there is no such file, and the link fails with "your file
could not be accessed". The build now catches this and tells you the correct
line, but it is worth knowing why.

Anything else stops the build, and the build will tell you which file and why.

The `note:` line is optional for other people's papers. For your own first
paper it is not — it is what makes publishing yourself read as rigour rather
than as a shortcut.

## Step 4. Build

Double-click **`build.bat`**. You should see:

    CHANGED    index.html
    CHANGED    publications.html
    ...
    1 papers, 0 mini-papers, 12 research questions
    BUILD OK - 2 file(s) updated

If it says **BUILD FAILED**, read the line above it. It names the file and the
problem. Nothing was changed, so fix it and run again.

## Step 5. Check it

Open `index.html`. Your paper should appear under "Latest papers" on the home
page and on the Publications page. Click the PDF link and confirm it opens.

---

# PART 2 — Go live, once

## Step 6. Install GitHub Desktop

Download it from **desktop.github.com**. Sign in, or create a free GitHub
account first.

This is the piece that makes everything afterwards easy. You will never type a
command.

## Step 7. Make the repository

In GitHub Desktop: **File → Add local repository →** choose your site folder.

It will say the folder is not a repository and offer to **create** one. Accept.

Then **Publish repository**:

- Name: `osri-site`
- **Untick "Keep this code private"** — Netlify's free plan needs to read it
- Click Publish repository

Everything in the folder is now on GitHub.

## Step 8. Connect Netlify

1. Sign up free at **netlify.com** (use "Sign up with GitHub" — simplest)
2. **Add new site → Import an existing project → GitHub**
3. Authorise Netlify, then pick `osri-site`
4. Leave every setting alone. `netlify.toml` already says what to do.
5. **Deploy**

A minute later you get an address like `wandering-lake-4821.netlify.app`.
**Open it and click through every page.** This is your site — the domain is
just a nicer name for it.

## Step 9. Point osri.ca at it

In Netlify: **Domain management → Add a domain →** type `osri.ca`.

Netlify shows you nameservers. Sign in wherever you bought the domain, find
DNS or nameserver settings, and replace what is there with Netlify's.

Usually live within the hour, occasionally up to a day. HTTPS switches itself
on once the domain resolves — you do not buy a certificate.

## Step 10. Turn on form notifications

**In Netlify: Forms → Form notifications → Add notification → Email
notification.** Enter your address. Do it for both forms.

Skip this and a student submits into silence.

Then test it yourself: go to osri.ca, submit the question suggestion form with
junk, and confirm the email arrives.

---

# PART 3 — The loop, every time after this

Once live, adding a paper is five minutes.

    1. PDF into the files folder
    2. A new .txt in content\publications\
    3. Double-click build.bat
    4. GitHub Desktop: type a summary, Commit, then Push origin

Netlify notices the push and updates osri.ca within a minute or two.

**In GitHub Desktop**, after building, you will see a list of changed files on
the left. In the bottom-left box type what you did — "Add lake temperature
paper" — then:

- Click **Commit to main**
- Click **Push origin** at the top

That is the whole thing. Nothing else to remember.

## If the site does not update

Check in this order:

1. **Did you run `build.bat`?** The `.html` files are the website. Editing a
   source file without building changes nothing that Netlify sees.
2. **Did you Push, not just Commit?** Commit saves locally. Push sends it.
3. **Is Netlify still deploying?** Netlify dashboard → **Deploys**. A green
   "Published" means done. Red means failed — click it to read why.
4. **Is it your browser?** Press **Ctrl+F5** on the live site.

If a rebuild seems to do nothing locally, double-click **`diagnose.bat`**. It
changes nothing and prints which folder it is working in and which files are
newer than which.

---

# Afterwards: the DOI

Your Guidelines promise, twice, that papers are "deposited in an archive that
issues a DOI". Keep that promise on paper one.

**zenodo.org** — run by CERN, free, no account cost. Upload the PDF, enter the
title and author, publish, and you get a permanent DOI like
`10.5281/zenodo.1234567`.

This matters more than it sounds: if osri.ca ever lapses, the paper still
exists at a citable address. That is the real line between publishing and
posting.

Do it **before** you announce the paper, so the DOI can be printed on the PDF
itself. For now, put the DOI at the end of the `note:` line; there is no
dedicated field for it yet.

---

# One-time checks before you tell anyone

- [ ] `editors@osri.ca` and `ethics@osri.ca` forward to an inbox you read
- [ ] No `example.org` anywhere: search the `pages` folder
- [ ] Privacy notice has a real date, not `[date]`
- [ ] Credits page has your name and year on the photograph
- [ ] Both forms tested on the live site, notification emails received
- [ ] Every nav link clicked, on a phone as well as a computer
- [ ] Domain auto-renew is ON — if osri.ca lapses, every published link breaks
