# Adding images to the site

The site ships with original artwork only (see `assets\ornaments\`), so nothing
on it carries a copyright risk. If you want photographs, paintings, historical
plates or coins, use the sources below and record each one in
`pages\credits.html`.

---

## Where the images go

| Slot | How to fill it |
|---|---|
| **Home page background** | Replace `assets\hero.jpg` and `assets\hero-small.jpg` — see below |
| **Beside a publication** | Add `image: assets/my-plate.jpg` and `image-alt: what it shows` to the publication's file in `content\publications\` |
| **Anywhere in a page** | Paste a `<figure class="plate">` block — see the example at the bottom of this file |

After any change, run `build.bat`.

---

## Changing the home page photograph

The opening section of the home page sits on a photograph, with a cream wash
laid over it: heaviest on the left where the words are, lightest on the right
so the picture shows through.

Two files drive it, both in `assets\`:

| File | Size | Used by |
|---|---|---|
| `hero.jpg` | 1500 px wide | Laptops and desktops |
| `hero-small.jpg` | 800 px wide | Phones (keeps the page light on mobile data) |

To change the picture, replace both files, keeping the names. Export the large
one at **1500 px wide** and the small one at **800 px wide**, JPEG quality
around 60, and keep them under roughly 450 KB and 150 KB. squoosh.app does this
in a browser for free and shows the file size as you adjust.

### Tuning how much shows through

In `css\styles.css`, find `.statement::before`. The numbers are how opaque the
cream wash is at each point across the section:

    rgba(249, 249, 246, 0.97) 0%      <- fully cream behind the heading
    rgba(249, 249, 246, 0.96) 46%
    rgba(249, 249, 246, 0.80) 62%
    rgba(249, 249, 246, 0.46) 82%
    rgba(249, 249, 246, 0.34) 100%    <- photograph most visible here

Lower numbers show more photograph. **Do not lower the first two** — those sit
behind the heading and the paragraph, and text over a busy photograph becomes
unreadable, especially outdoors on a phone. If a new photograph is darker or
busier than the current one, raise them instead.

There is a second copy of these numbers further down, inside
`@media (max-width: 720px)`, which runs top-to-bottom for phones. Change both.

### Choosing a photograph that works here

- **Landscape or square.** A tall portrait photo gets cropped hard.
- **Busy on one side, calm on the other** works best — the calm part goes under
  the text.
- **Avoid a bright sky filling the frame.** Pale photographs disappear under a
  cream wash; mid-toned ones keep their character.
- **Photographs students took themselves** are ideal: no licensing question at
  all, and another name to credit.

---

## Vetted sources

All of these are genuinely free to use. Stick to them and you will not have a
problem.

### Best for historical plates, paintings, artefacts and coins

**The Met (Metropolitan Museum of Art) — Open Access**
metmuseum.org/art/collection · Filter by "Open Access". Over 400,000 images
released under **CC0**, which means no permission and no attribution required.
Excellent for Greek and Roman sculpture, coins, arms and armour, and drawings.

**Smithsonian Open Access**
si.edu/openaccess · About 4.5 million items under **CC0**, spanning natural
history specimens, scientific instruments, and archival photographs. The
strongest source for anything scientific.

**Rijksmuseum — Rijksstudio**
rijksmuseum.nl/en/rijksstudio · Roughly 800,000 high-resolution images, mostly
public domain. Superb Dutch Golden Age painting and botanical drawing.

**Cleveland Museum of Art — Open Access**
clevelandart.org/art/collection · CC0 on public-domain works.

**Library of Congress — Free to Use**
loc.gov/free-to-use · Curated sets already cleared for reuse.

### Best for natural history and scientific illustration

**Biodiversity Heritage Library**
biodiversitylibrary.org · Over 150,000 public-domain illustrations from
historical natural history literature. This is where to find 19th-century
botanical plates of species that actually grow in the Okanagan — ponderosa
pine, sagebrush, bitterroot, saskatoon, antelope-brush.

**BHL on Flickr**
flickr.com/photos/biodivlibrary · The same material, easier to browse.

**Public Domain Review**
publicdomainreview.org · Curated and beautifully chosen. Good when you want one
striking image rather than a search.

### Photographs

**Wikimedia Commons** — commons.wikimedia.org · Enormous, but licences vary per
file. Always open the file page and read the licence box before using it.
Many files require attribution (CC BY / CC BY-SA); some are public domain.

**Unsplash** and **Pexels** — free for commercial use, no attribution required,
but the look is modern stock photography and will fight the tone of the site.

---

## Checking a licence properly

Before you use any image, confirm one of these three things:

1. **CC0 / Public domain / "No known copyright restrictions"** — use freely.
2. **CC BY** — use with credit. Record it in `pages\credits.html`.
3. **You made it.** — use freely.

If it is **CC BY-NC**, **CC BY-ND**, "editorial use only", or the licence is not
stated anywhere, **do not use it**. An unstated licence is not permission.

Two traps worth knowing:

- **A photograph of a public-domain painting may carry its own copyright** in
  some countries, even though the painting itself is out of copyright. Using
  the museum's own Open Access file avoids this entirely.
- **A Google Images result is not a source.** Follow it back to the
  institution that holds the work, and use their file and their licence
  statement.

---

## A note on what suits this site

Roman busts and antique coins read as "academia" in a generic way, and on a page
about Okanagan wildfire smoke data they will look borrowed.

Two directions fit OSRI better:

1. **Historical scientific illustration** — botanical plates, ornithological
   drawings, geological cross-sections. These *are* what published research
   looked like before photography, so they carry real meaning here rather than
   decoration. BHL has thousands, free.
2. **The valley itself** — the lake, the ridges, the orchards, the smoke
   seasons. Nothing says "this is local research" faster, and student authors
   can photograph it themselves, which sidesteps licensing altogether and gives
   them another credit.

A middle path: use a species plate for each research-question group — a
ponderosa pine for climate, a kokanee salmon for the lake, and so on. Distinctive,
free, and connected to the questions being asked.

---

## Pasting a figure into a page

```html
<figure class="plate">
  <img src="assets/pinus-ponderosa.jpg"
       alt="Botanical plate showing ponderosa pine needles, cone and bark"
       loading="lazy">
  <figcaption>
    <em>Pinus ponderosa</em>, plate 512.
    <span class="credit">C. S. Sargent, <em>The Silva of North America</em> (1897),
    via the Biodiversity Heritage Library. Public domain.</span>
  </figcaption>
</figure>
```

Always write a real `alt` description — it is what a blind reader gets, and
search engines read it too. Describe what the image shows, not what it is
called.

## Keeping the site fast

Photographs come off a camera at several megabytes, which is far too big.
Before adding one:

- Resize to **1600 pixels wide at most** (the site never displays wider).
- Save as JPEG at about 80% quality, or WebP.
- Aim for under 300 KB per image.

On Windows, Paint can resize (Image → Resize), or use squoosh.app in a browser
— it is free, runs locally, and shows you the file size as you adjust quality.
