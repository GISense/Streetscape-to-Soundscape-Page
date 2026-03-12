# Streetscape-to-Soundscape — User Study

A browser-based perceptual evaluation tool where participants listen to audio clips and select the one that best matches a displayed street scene photograph. Built to evaluate the **Sound2IMG** model's soundscape generation quality.

---

## Table of Contents

- [Project Overview](#project-overview)
- [File Structure](#file-structure)
- [How It Works](#how-it-works)
- [Configuration File — `s2s_study_src.js`](#configuration-file--s2s_study_srcjs)
  - [Changing Images](#changing-images)
  - [Changing Audio Files](#changing-audio-files)
  - [Changing the Correct Answer](#changing-the-correct-answer)
  - [Adding or Removing Trials](#adding-or-removing-trials)
- [Styling — `s2s.css`](#styling--s2scss)
  - [Changing Colors](#changing-colors)
- [HTML — `user_study_s2s.html`](#html--user_study_s2shtml)
  - [Changing the Page Title or Description](#changing-the-page-title-or-description)
  - [Changing the Number of Trials](#changing-the-number-of-trials)
  - [Changing the API Endpoint](#changing-the-api-endpoint)
- [Asset Requirements](#asset-requirements)
- [Deployment / Serving](#deployment--serving)
- [Scoring & Data Collection](#scoring--data-collection)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

Each trial in the study presents:

1. A **street scene photograph** (ground truth image)
2. **Three audio clips** labeled A, B, and C
3. One of the three clips is the correct matching soundscape; the other two are distractors from different scenes

Participants select the audio they feel best represents the street scene. A progress bar tracks completion and answers are submitted to a backend API endpoint when finished.

---

## File Structure

```
project-root/
│
├── user_study_s2s.html                        # Main HTML page (the study UI)
│
├── config/
│   └── s2s_study_src.js                       # Trial data: images, audio paths, correct answers
│
├── static/
│   ├── css/
│   │   ├── bulma.min.css                      # Bulma CSS framework
│   │   ├── fontawesome.all.min.css            # FontAwesome icons
│   │   └── user_study/
│   │       └── s2s.css                        # Custom styles for the study UI
│   │
│   ├── images/
│   │   └── GISenseLabLogoPNG.png              # Favicon / lab logo
│   │
│   └── user_study/
│       └── Q2/
│           ├── ground_truth/                  # Street scene images (.jpg)
│           │   ├── 157.jpg
│           │   ├── 158639.jpg
│           │   └── ...
│           └── audio/                         # Audio soundscape files (.wav)
│               ├── 157.wav
│               ├── 158639.wav
│               └── ...
```

---

## How It Works

1. When the page loads, `s2s_study_src.js` is read — it defines the `S2S_CONFIG` object containing all trial data.
2. The HTML script loops through `S2S_CONFIG` and dynamically builds one trial card per entry.
3. Each card shows the image and three audio players (A, B, C).
4. Clicking an audio row (not the player controls themselves) selects that option and highlights it green.
5. The progress bar fills as more trials are answered.
6. On submit, all answers are sent as JSON to `/api/s2s` via a POST request, and a thank-you screen is shown.

---

## Configuration File — `s2s_study_src.js`

> **This is the only file you need to edit for most customizations.**

Located at: `config/s2s_study_src.js`

Each trial is defined as a key in the `S2S_CONFIG` object, named `sub_1` through `sub_10`. Here is a single trial entry explained in full:

```javascript
sub_1: {
  image:  "static/user_study/Q2/ground_truth/157.jpg",  // Path to the street scene image
  audios: {
    A: "static/user_study/Q2/audio/157.wav",            // Audio for option A
    B: "static/user_study/Q2/audio/268504.wav",         // Audio for option B
    C: "static/user_study/Q2/audio/62750.wav"           // Audio for option C
  },
  answer: "A"                                           // The correct option letter
},
```

All file paths are **relative to the HTML file** (the project root).

---

### Changing Images

To swap out the street scene image for a trial, update the `image` field:

```javascript
// Before
image: "static/user_study/Q2/ground_truth/157.jpg",

// After — using a new image
image: "static/user_study/Q2/ground_truth/my_new_scene.jpg",
```

- Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`
- Recommended dimensions: at least **580 × 280px** (the display crops to this aspect ratio)
- Place the new image file in `static/user_study/Q2/ground_truth/` (or adjust the path to match wherever you put it)

---

### Changing Audio Files

Each trial has three audio slots: `A`, `B`, and `C`. To replace any of them, update the path in the `audios` object:

```javascript
audios: {
  A: "static/user_study/Q2/audio/my_correct_audio.wav",    // new correct audio
  B: "static/user_study/Q2/audio/distractor_one.wav",      // new distractor
  C: "static/user_study/Q2/audio/distractor_two.wav"       // new distractor
},
```

- Supported formats: `.wav`, `.mp3` (if you use `.mp3`, update the `type="audio/mpeg"` attribute in the HTML — `.wav` files work with `audio/wav`)
- Place audio files in `static/user_study/Q2/audio/` (or any folder, as long as the path in the config matches)
- Distractors should be audio from **different scenes** to keep the task meaningful

> **Tip:** To use a different folder structure (e.g., for a new study round `Q3`), simply update the paths in `s2s_study_src.js` to point to your new folder — no other files need changing.

---

### Changing the Correct Answer

The `answer` field records which option letter (`"A"`, `"B"`, or `"C"`) is the ground-truth match. This is used for backend scoring.

```javascript
// The correct audio is in slot B, so set answer to "B"
audios: {
  A: "static/user_study/Q2/audio/distractor1.wav",
  B: "static/user_study/Q2/audio/correct_audio.wav",   // ← correct
  C: "static/user_study/Q2/audio/distractor2.wav"
},
answer: "B"    // ← must match the slot containing the correct audio
```

> **Important:** The `answer` field does **not** affect what the participant sees or hears — it is purely a metadata label sent to the server for scoring purposes. Make sure it always matches the actual slot containing the correct audio.

---

### Adding or Removing Trials

**To add a new trial**, append a new entry to `S2S_CONFIG` in `s2s_study_src.js`:

```javascript
// Add after sub_10:
sub_11: {
  image:  "static/user_study/Q2/ground_truth/my_new_scene.jpg",
  audios: {
    A: "static/user_study/Q2/audio/new_correct.wav",
    B: "static/user_study/Q2/audio/new_distractor1.wav",
    C: "static/user_study/Q2/audio/new_distractor2.wav"
  },
  answer: "A"
},
```

Then open `user_study_s2s.html` and update the `TOTAL` constant:

```javascript
// Before
const TOTAL = 10;

// After
const TOTAL = 11;
```

Also update the instructions text in the HTML if it references a specific trial count:

```html
<!-- Find and update this line -->
For each of the 10 trials below ...
<!-- Change to -->
For each of the 11 trials below ...
```

**To remove a trial**, delete its `sub_N` block from `s2s_study_src.js` and decrement `TOTAL` in the HTML. Make sure the remaining keys are still numbered sequentially from `sub_1` upward with no gaps.

---

## Styling — `s2s.css`

Located at: `static/css/user_study/s2s.css`

### Changing Colors

All main colors are defined as CSS variables at the top of the file for easy global changes:

```css
:root {
  --s2s-bg: #e8edf2;          /* Page background color */
  --s2s-card-bg: #ffffff;     /* Trial card background */
  --s2s-accent: #4a7fb5;      /* Primary blue accent (borders, labels) */
  --s2s-accent-dark: #2d5a8a; /* Darker blue (hover states, submit button) */
  --s2s-selected: #27ae60;    /* Green color shown when an option is selected */
  --s2s-label-bg: rgba(0,0,0,0.6); /* "Trial N / 10" badge background */
}
```

For example, to change the selected-option highlight from green to purple:

```css
--s2s-selected: #8e44ad;
```

### Other Style Customizations

| What to change | Where in the CSS |
|---|---|
| Header gradient colors | `.s2s-hero { background: linear-gradient(...) }` |
| Image display size | `.s2s-streetscape { height: 280px; max-width: 580px; }` |
| Card spacing / padding | `.s2s-trial-card { padding: ... margin-bottom: ... }` |
| Submit button size | `.s2s-submit-btn { padding: ... font-size: ... }` |
| Max page width | `.s2s-container { max-width: 860px; }` |

---

## HTML — `user_study_s2s.html`

### Changing the Page Title or Description

The browser tab title:
```html
<title>User Study — Streetscape-to-Soundscape</title>
```

The large heading shown in the header banner:
```html
<div class="s2s-hero-title">Streetscape-to-Soundscape &nbsp;·&nbsp; User Study</div>
```

The subtitle beneath it:
```html
<div class="s2s-hero-subtitle">
  Help evaluate our Sound2IMG model by listening to audio clips and
  deciding which one best matches the street scene shown.
</div>
```

The instructions box shown above the trials:
```html
<div class="s2s-instructions">
  <strong>Instructions</strong>
  For each of the 10 trials below, look carefully at the street photograph ...
</div>
```

### Changing the Number of Trials

Find this line near the top of the `<script>` block and change the value:

```javascript
const TOTAL = 10;   // Change this to match the number of sub_N entries in s2s_study_src.js
```

### Changing the API Endpoint

Responses are submitted via a `fetch` POST call. To change the backend endpoint:

```javascript
// Find this block in the <script> section:
fetch("/api/s2s", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(submissionData)
})

// Change "/api/s2s" to your endpoint, e.g.:
fetch("https://your-server.com/api/study-responses", { ... })
```

The payload sent is a JSON array structured like this:

```json
[
  { "trial": 1, "scene_id": "157", "selected_option": "A" },
  { "trial": 2, "scene_id": "158639", "selected_option": "C" },
  ...
]
```

`scene_id` is derived automatically from the image filename (without extension).

---

## Asset Requirements

| Asset type | Format | Notes |
|---|---|---|
| Street scene images | `.jpg`, `.png`, `.webp` | Recommended min 580×280px |
| Audio clips | `.wav` | `.mp3` also works; update MIME type in HTML if switching |
| Favicon | `.png` | Referenced in `<link rel="icon">` in the `<head>` |

---

## Deployment / Serving

Because the page loads audio and images from relative paths, it **must be served by a web server** — opening the HTML file directly via `file://` in a browser will block audio/image loading due to browser security policies.

**Quick local server options:**

```bash
# Python 3
python3 -m http.server 8080

# Node.js (npx)
npx serve .

# VS Code
# Use the "Live Server" extension
```

Then visit `http://localhost:8080/user_study_s2s.html` in your browser.

For production, deploy the entire project folder to any static file host (GitHub Pages, Netlify, Vercel, Nginx, Apache, etc.) and ensure the backend API endpoint at `/api/s2s` is reachable.

---

## Scoring & Data Collection

The `answer` field in each `sub_N` block in `s2s_study_src.js` is the ground truth. Your backend at `/api/s2s` receives each participant's selections and can compare them against the ground truth to compute accuracy.

Example scoring logic (Python pseudocode):

```python
ground_truth = {
    "157":    "A",
    "158639": "B",
    "172440": "C",
    # ... etc
}

score = sum(
    1 for r in responses
    if r["selected_option"] == ground_truth[r["scene_id"]]
)
accuracy = score / len(responses)
```

If you do not have a backend, you can temporarily remove the `fetch(...)` call and log results to the console instead for local testing:

```javascript
console.log("Submitted:", JSON.stringify(submissionData, null, 2));
```

---

## Troubleshooting

**Audio clips don't play**
- Make sure the server is running (don't open the HTML via `file://`)
- Verify the `.wav` paths in `s2s_study_src.js` exactly match the actual filenames and folder structure (paths are case-sensitive on Linux servers)

**Images don't load**
- Same as above — check file paths and case sensitivity
- Confirm the images exist at `static/user_study/Q2/ground_truth/`

**Trials don't appear on the page**
- Open your browser's developer console (F12) and look for JavaScript errors
- The most common cause is a syntax error in `s2s_study_src.js` after editing — check for missing commas or brackets

**"Trial N" is missing from the study**
- Ensure `s2s_study_src.js` contains a `sub_N` entry for every number from 1 up to `TOTAL`
- Ensure there are no gaps (e.g., `sub_1`, `sub_2`, `sub_4` with no `sub_3` will skip Trial 3)

**Responses aren't reaching the server**
- Check the browser console for network errors after clicking Submit
- Confirm your API endpoint is correct and running
- CORS headers may need to be enabled on the server if the frontend and backend are on different domains
