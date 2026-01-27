These are the pages and utilities that make up the [THOLONIA Project](https://github.com/tholonia/tholonia.github.io/raw/main/_).

This site is in super-duper beta, which means the code is messy and may not work, the  pages are still being edited, cleaned, rewritten, etc., Lots of stuff is still in dev... so, many moving parts that have not settled down yet.

If you want to know about THOLONIA, go to the [gitpage](https://github.com/tholonia/tholonia.github.io/raw/main/_) or read the [book](https://github.com/tholonia/tholonia.github.io/raw/main/_the_book).

The only reason to be here is for the few utilities that have been written, listed below.


# Files
## python
- **`CATFILE.py`** - *update MD file with auto keyword generator*
- **`CATWORD.py`** - *tests categorization of a single word*
- **`TAX-REPORT.py`** - *prints out taxonomy with all unparsable words removes*
- **`syncdatefile.py`** - *synchronizes the filename date and the date tag*
- **`syncdate.py`** - *updates filename date*
- **`TAX_REPORT.py`** - *prints number of words in taxonomy category*
  - **`taxonomy2.toml`**
- **`extract_kw.py`** - *extracts keywords from a file (pdf,txt)*
- **`SPELLCHECK.py`** - spellchecker
  - **`skipwords.txt`** - words to ignore when spell checking
## bash
- **`ADDBIG`** - add large file to LFS 
- **`CLEAN_GITHUB`** - *uses `gh` to wipe caches, workflows, logs on github*
- **`FINDFILE`** - *find file in tree from current root.  Uses partial filename*
- **`FINDINFILE`**- *Finds any file that has matched content*
- **`MAKEGIF`** - *make an animated GIF with ffmpeg*
- **`MAKELINKS`** - *creates subdir .ZPROJECTS and fill with symlinks to collections*
- **`SERVE`** - *cleans caches and starts jekyll server (in docker)*
- **`TESTLINKS`** - *runs linkchecker (in docker only, uses Jekyll to test - doesn't work as expected)*
- **`STOPSERVER`** - *kill all jobs called 'server' (in docker)*

