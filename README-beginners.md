# Tibetan Translation Skills: a guide for translators new to Claude Code

This guide is for you if you translate Classical Tibetan and you have never used Claude Code, a
terminal, or any AI tool. Every step is spelled out. If you already know the command line, read
`README.md` instead.

## What this does, and what it does not

**It does:**

- Take a Tibetan passage (Wylie or Tibetan script) and write a draft English translation.
- Look up every word in a dictionary stored on your computer, and work out the grammar first.
- Try to find where a quotation comes from (the work and its Toh number).
- Check its own draft in a second, separate pass, and compare it with a machine translation from
  Dharmamitra (called MITRA).
- Fit the style to your readers: academic, new practitioner, seasoned practitioner, or a mix.

**It does not:**

- Replace reading the Tibetan. It is wrong sometimes, and it will say so when it is unsure.
- Produce a final text. The result is a careful draft for you to revise.
- Hide its doubts. Every place where the Tibetan could be read another way is listed in a line that
  starts with `Q:`. Those lines are your to-do list.

## How good is it?

In October 2026 the pipeline was tested on 33 pages of Tibetan that already have published English
translations (Drikung commentaries, a biography, sūtras, tantras and Indian commentaries). A separate
judge, reading the Tibetan, counted the mistakes in three versions of each page: the pipeline's,
Dharmamitra's machine translation (MITRA) on its own, and the published book.

- The pipeline on Opus at max effort: about one meaning-changing error every three pages, and two
  or three small ones (a nuance, a term) per page. Its English was rated 4.2 out of 5.
- MITRA on its own: about two or three meaning-changing errors per page and six small ones.
- The published translations: about four slips per page, mostly small.
- Opus asked to translate with no skill at all: not yet measured.

So it is a strong first draft that tells you where it was unsure, not a finished translation. The
full report is `docs/Test_Report_2026-10-03.md`.

## What you need

- A Mac or a Linux computer. (On a Mac, macOS 13 or later.)
- A Claude subscription. The free plan does not include Claude Code. Pro works. Max is more
  comfortable for long texts, because this translation method uses a lot of "tokens" (see "What it
  costs").
- About 1 GB of free disk space.
- An internet connection.

## Setup, step by step

### 1. Install Claude Code

Claude Code is the program that runs these skills. Choose one way.

**Way A: the desktop app (no typing needed for this step).** Go to https://claude.ai/download
(it forwards to claude.com/download), download the Mac app, open it, and sign in with your Claude
account. The app has a **Code** tab at the top. Use that tab, and choose **Local** (it runs on your
own computer). Do not use the Cowork tab or cloud sessions: they cannot see the skills installed on
your computer.

**Way B: the terminal.** Open Terminal (next step), paste this line, and press Enter:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

When it finishes it prints a message saying Claude Code was installed. Then type this and press Enter:

```bash
claude
```

A browser window opens so you can sign in. After you sign in, you are inside Claude Code. To leave
it, type `exit` and press Enter.

You still need Terminal for the setup in step 4, even if you use the app.

### 2. Open Terminal (on a Mac)

Press `Cmd + Space`, type `Terminal`, and press Enter. A window opens with a blinking cursor. This is
the **terminal**: a place where you type commands instead of clicking. To paste a command, press
`Cmd + V`. To run it, press Enter.

On Linux, press `Ctrl + Alt + T` on most systems, or search for "Terminal".

### 3. Get this folder

You need a copy of this project on your computer. Easiest, if you have `git`:

```bash
git clone https://github.com/gkoebler8-vjr/tibetan-translation-skills.git ~/Documents/Tibetan-Translation-Skills
```

If you do not have `git`, or the command offers to install developer tools, accept and wait; or
download the project as a zip file from https://github.com/gkoebler8-vjr/tibetan-translation-skills (the green "Code" button, then
"Download ZIP"), double-click it to unpack, and move the folder to your Documents folder.

Now tell the terminal to work inside that folder. Type `cd ` (with a space), drag the folder from
Finder into the Terminal window, and press Enter. Or type:

```bash
cd ~/Documents/Tibetan-Translation-Skills
```

(Use the real name of your folder if it is different.)

### 4. Run the installer

```bash
./install.sh
```

What it does, in order: copies the four skills to a hidden folder where Claude Code looks for them
(`~/.claude/skills`); sets up a small Python environment with two helper libraries; downloads the
Dharmamitra Tibetan Lexicon (about 274 MB); builds a searchable dictionary index on your computer.
It prints a numbered line for each step (1/4, 2/4 ...) and a download progress bar. Expect a few
minutes. It ends with a status listing and the word "done". Nothing is uploaded anywhere, and it is
safe to run again if interrupted.

It needs Python 3 and `curl`. Macs normally have `curl`. If Python is missing, the Mac may offer to
install developer tools: accept, wait, then run `./install.sh` again.

**Optional: more dictionaries.** This adds about 38 MB of free Tibetan-English dictionaries from
Christian Steinert's open project (Hopkins, Rangjung Yeshe, Berzin and others). They are downloaded
to your computer, not shared. Their copyright stays with their authors.

```bash
./install.sh --public
```

If you already have a folder of your own dictionaries (GoldenDict or StarDict format), see
`docs/own-dictionaries.md`.

### 5. Check that it worked

Run these two commands, one at a time. The first looks up a Tibetan phrase in your local dictionary:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/tibdict.py annotate "བླ་མའི་བྱིན་རླབས་ཁོ་ན་ལས།"
```

You should see a list of words with dictionary entries. The second asks Dharmamitra where a quotation
comes from, so it needs the internet:

```bash
python3 ~/.claude/skills/tibetan-translate/tools/dm.py identify "rnam rtog ma rig chen po ste / 'khor ba'i rgya mtshor ltung byed yin"
```

You should see a line starting `VERBATIM MATCH` and a list of works. If both print something, you are
ready. If not, see "Common problems".

## Your first translation

1. Make a folder for your project, for example `Documents/My-Translation`, in Finder.
2. Open Claude Code in that folder. In the desktop app: **Code** tab, **Local**, **Select folder**, and
   choose it. In the terminal:

   ```bash
   cd ~/Documents/My-Translation
   ```

   ```bash
   claude
   ```

3. Choose the model and effort first (see "Choosing the model and effort").
4. Type a request and paste the Tibetan under it. Wylie or Tibetan script both work. For example:

   ```text
   Please translate this Tibetan passage: ...
   ```

   You can also start with `/tibetan-translate`. Typing `/` shows the skills you can call.
5. **It asks one question.** Before translating it needs to know who the translation is for. The four
   audiences:
   - **Academic**: for scholars. Keeps Sanskrit terms with full diacritics, adds notes with sources and
     variant readings, stays close to the Tibetan.
   - **New practitioner**: for an educated reader who is new to Buddhism. Plain English, Sanskrit
     translated where possible, no notes in the text.
   - **Seasoned practitioner**: for readers who already know the vocabulary (dharmakaya, mahamudra).
     Keeps the standard terms, warm and direct, few notes.
   - **Hybrid**: a practitioner text with a thin scholarly layer behind it (notes at the end).

   It also asks your purpose (publication, study aid, practice/recitation, or a working crib for
   yourself) and your house style: terms to keep, diacritics or none, verse metred or free.
   **If you are unsure,** answer "you choose". It will pick seasoned practitioner and study aid, and
   tell you so.
6. **Wait.** A page can take many minutes. Press `Esc` to stop it if you must.
7. **Read the result.** A header line, one translation, and short notes.
8. **Ask for changes in ordinary words**, for example: "Make this less formal", "Use 'primordial
   awareness' for ye shes everywhere", "Why did you read the second line as a condition?"

### What the notes mean

- `Q:` a doubt. The Tibetan could be read another way; it gives the other reading. Decide yourself.
- `Alt:` another possible rendering of a hard word or line.
- `Issue:` a choice it made, such as swapping a term, unpacking a compressed phrase, or letting an
  image go.
- `Source:` where a quotation comes from, or that it could not find the source.
- `Check:` what the second, independent check found and fixed.
- `MITRA:` where Dharmamitra's machine translation disagrees on something that matters.

## Working on a longer text

- **One folder per text.** Open Claude Code in that folder each time you work on the text.
- **The files it keeps.** Next to your text it writes `<name>.construal.md` (its working notes on the
  grammar of each passage) and `<name>.glossary.tsv` (every term it decided: Wylie, English, note).
  You can open the glossary in Excel or any text editor. Edit it, and the next passages follow your
  changes: your glossary overrides its dictionary.
- **Put your brief in a file called `CLAUDE.md`** in the folder, so it never asks again. For
  example:

  ```text
  Audience: seasoned practitioner. Purpose: publication.
  House style: no diacritics; keep dharmakaya and mahamudra; metred verse for liturgy.
  ```

- **Feed it a page at a time**, 5 to 12 sentences or stanzas: the independent check runs once per
  page, so this is cheaper than one at a time.
- **Ask for a check any time**: "Please check the passage above against the Tibetan."
- **`Check:`** means a second pass looked for errors (wrong negation, wrong agent, a dropped
  connective, an invented word) and fixed those it confirmed. It is a safety net, not a guarantee.
- **`MITRA:`** means Dharmamitra's model translated the same passage, and the two differ on a
  meaning. It is a flag to look again at the Tibetan. It is not a vote: the machine translation is
  often wrong and has no sense of your style.

## Choosing the model and effort

Claude comes in different "models" (like different translators with different skill). "Effort" is how
hard the model thinks before answering. These skills are tuned for the strongest setting: **Opus**
(or **Fable**) at **max** effort. On a weaker setting, the skill stops and asks you to switch. You can
tell it to go ahead, but expect more mistakes: in the tests, Opus at max made about one meaning error in three
pages, Opus at high effort about one in every page or two, and Sonnet two to three a page.

In the desktop app, use the model picker next to the send button. In the terminal, type:

```text
/model opus
```

and then:

```text
/effort max
```

Typing `/model` or `/effort` alone opens a picker. Per Anthropic's documentation, `max` applies to the
current session only, so set it again each time you start Claude Code. The first line of each
reply states the model and effort, so you can check.

## What it costs

Claude counts text in **tokens**: small pieces of words. Your plan gives you an allowance of tokens
per time window, and heavy use uses it up faster.

A page of 10 to 12 sentences or stanzas uses roughly **a quarter to four hundred thousand tokens** on
Opus at max effort (measured on thirty test pages in October 2026). That is a lot: the thorough
method costs more than a quick translation. In the same tests, Opus at `xhigh` effort used about a
third less and made about as many meaning errors (one in three pages) as max did; Sonnet was not cheaper
and made two to three meaning errors a page.

- On **Max (5x)**, one five-hour window held about ten to twelve pages at max effort in the tests.
- On **Pro**, which is about a fifth of that, expect two or three pages per window; use it for the
  passages you most want checked, not for a whole book in an afternoon.

These are rough estimates, not promises. Plans and limits change; check your plan's usage on
claude.ai. If you run out, wait for the allowance to renew, or continue the next day.

## Common problems

**"command not found: claude"** The installer put Claude Code somewhere your terminal does not look
yet. Close Terminal and open a new window. If it persists, run these two lines (Mac):

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

```bash
source ~/.zshrc
```

**"python3: command not found"** Python is missing. On a Mac, running `python3` once usually offers to
install Apple's developer tools; accept, wait, retry. Or install Python from https://www.python.org.

**The dictionary download failed or stopped.** Check your internet connection and run `./install.sh`
again. It continues where it can. For `--public`, a message says some files could not be fetched;
run `./install.sh --public` again later.

**"The skill is calibrated for Opus or Fable" (or a similar message).** You are on another model or
a lower effort. Set `/model opus` and `/effort max`, as above, or tell it to proceed anyway.

**Dharmamitra is slow, or the second command above fails.** The service is outside our control. The
translation still works: source identification and the MITRA comparison are skipped, and it will say
so. Try again later.

**The skill does not appear when you type `/`.** In the desktop app, make sure you are in the **Code**
tab with **Local** selected, not Cowork or a cloud session. Then type `/reload-skills`, or restart
Claude Code. If still missing, run `./install.sh --skills-only` again.

## Where to ask for help

- Installing or signing in to Claude Code: https://code.claude.com/docs/en/setup and the beginner
  guide https://code.claude.com/docs/en/terminal-guide
- Problems with these skills, or questions about translation choices: contact the author, Gabriel
  Kobler, or open an issue at https://github.com/gkoebler8-vjr/tibetan-translation-skills/issues.
- Disagreements about a reading of the Tibetan: ask the translators you already trust. The `Q:`
  lines are what to bring.

## Glossary

- **Skill**: a set of instructions Claude Code loads on request. Here there are four; you mainly use
  `tibetan-translate`.
- **Model**: the AI that does the thinking (Opus, Fable, Sonnet ...).
- **Effort**: how long the model thinks before answering. `max` is the most.
- **Token**: a small piece of text. Usage and plan limits are counted in tokens.
- **Terminal**: the window where you type commands.
- **Wylie**: the standard way to write Tibetan in Roman letters (for example `bla ma`).
- **Construal**: the grammar worked out before translating: who does what, which particle links which
  clause, where a negation applies. The draft is written from it.
- **Toh**: the Tohoku catalogue number of a work in the Derge Kangyur or Tengyur.
- **MITRA**: Dharmamitra's machine translation model, used as a second opinion.

## Licence and credits

Code is MIT, text is CC BY 4.0. Dictionary data is downloaded, not bundled, and stays with its
authors. Thanks to Dharmamitra (lexicon, search, MITRA), 84000, Christian Steinert (open dictionary
files) and the Edition Garchen Stiftung translators, whose work served as references in testing. See
`LICENSE` and `LICENSE-NOTES.md`.
