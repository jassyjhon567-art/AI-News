# Manab AI — Bilingual Knowledge & News Platform

A fully serverless, automated, bilingual (English/Bengali) knowledge and news
platform. No database — content lives as flat-file JSON (`news.json`) plus
pre-rendered static HTML posts, hosted for free on GitHub Pages and kept
fresh by a GitHub Actions cron job.

## How it works

1. **`main.py`** runs on a schedule (every 6 hours) inside GitHub Actions.
   - Pulls the latest items from 100 RSS feeds across 10 niches (AI, Gadgets,
     Software Dev, How-To Guides, SEO/Marketing, Cyber Security, Business,
     Science, Health, Lifestyle).
   - Deduplicates stories using a word-overlap similarity check.
   - Expands each short RSS summary into a full 3-paragraph, 250–300 word
     article using Gemini (`gemini-1.5-flash`, JSON structured output), with
     an automatic fallback to a lightweight local expansion + MyMemory
     translation if Gemini is unavailable.
   - Produces a full, equally-detailed Bengali translation of every article.
   - Sources an image for each story (original RSS image → AI-generated via
     Pollinations → smart keyword-matched Unsplash photo). **If no image can
     be found or generated, the article is skipped entirely** (no image, no
     publish).
   - Writes static HTML files to `posts/en/` and `posts/bn/`, and updates
     `news.json` (capped at the latest 50 entries).
   - Optionally pings the Google Indexing API (with a 3-attempt retry queue)
     so new pages get crawled faster.
2. **`index.html`** is a single-file, dark-themed SPA that fetches
   `news.json` (cache-busted on every load) and renders a responsive card
   grid with a working EN/বাংলা language toggle and niche filter.
3. **`.github/workflows/main.yml`** wires it all together: checks out the
   repo, installs Python deps, runs `main.py`, and commits/pushes any new
   `news.json`, `posts/`, and `images/` files back to `main`.

## Repository structure

```
├── .github/workflows/main.yml
├── posts/
│   ├── en/
│   └── bn/
├── images/
├── index.html
├── news.json
├── main.py
└── README.md
```

## Setup

1. Create a new GitHub repository and push these files to the `main` branch.
2. In **Settings → Pages**, set the source to the `main` branch, root folder.
3. In **Settings → Secrets and variables → Actions**, add:
   - `GEMINI_API_KEY` — a Google AI Studio API key (optional; the pipeline
     falls back gracefully without it, using the free MyMemory translator).
   - `GCLOUD_KEY` — a Google Cloud service-account JSON key with Indexing
     API access (optional; indexing submission is skipped if absent).
   - `SITE_BASE_URL` — your published Pages URL, e.g.
     `https://your-username.github.io/manab-ai` (used to build canonical
     URLs for the indexing submissions and hreflang links).
4. Run the workflow once manually from the **Actions** tab
   (`workflow_dispatch`) to generate the first batch of content, or wait for
   the next scheduled run (every 6 hours).

## Notes & limitations

- `main.py` caps new articles to 12 per run to keep each Actions run fast and
  within free-tier limits; adjust `max_new_per_run` if needed.
- The MyMemory fallback translator has a small per-request character limit,
  so long articles are translated paragraph-by-paragraph with short delays
  between calls to stay within its free-tier rate limits.
- RSS feed availability and structure can change at any time — if a
  particular publisher blocks scraping or changes its feed format, that
  feed will simply yield fewer (or zero) entries on a given run rather than
  breaking the pipeline.
