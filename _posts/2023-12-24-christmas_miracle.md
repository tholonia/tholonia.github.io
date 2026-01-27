---
layout: post
title: Christmas Miracle
author: duncan
date: 2023-12-24
categories: [BLOG]
tags: [about]
image: /assets/posts/2023-12-24-christmas_miracle/post_image.jpg
---
T'was the night before Christmas, and all through the house, not a creature was stirring, not even a mouse... except for the maniac banging away at the keyboard for the past 3 weeks until 4 AM every day :/  That would be me. 

The idea of moving all my content to Jekyll/GitPages seemed like such a great idea, and it was! I just had no idea what that would involve.

For starters, I needed to use a docker file for the Jekyll server as none of the versions of any of my libraries on my Arch Linux system seemed to be compatible with what Jekyll wanted. OK, so I learned docker stuff.  The first thing I learned was NOT use the Docker Desktop! Man, that screwed everything up for 2 days!  When you install Docker Desktop it create a new context which is useless (as in unusable) outside of the Desktop, but it changes that context for everything, breaking everything in the process until you spend hours finding the secret command to fix it (it's `docker context use default`).  Stick to the command line, and that includes not using the Visual Studio Docker extensions.  It just makes things more difficult when you have to debug it.  Here is the [video](https://www.youtube.com/watch?v=zijOXpZzdvs) a generally followed to get Docker/Jekyll running.

Then, I discovered I needed to write several temples using the Liquid Template language, which ain't pretty. So, I learned Liquid Script. And when I say is 'ain't pretty', what I really mean is it's a syntax nightmare.  While rational, sane code might look something like `x=a+100/y`, Liquid's brilliant adaptation is `{ % assign x = a | plus: 100 | divided_by: y % }`.  

OK, I used to write assembly code and COBOL back in the day, so, I'll survive this.

But there was some stuff that specifically needed Ruby code.  Tweaking Ruby was not an issue, but the whole gem architecture, Gemfile, .gemrc, bundler and it's 20+ arguments, ruby enviroinment, etc., etc., was annoying, but unlike Jekyll/Liquid, there's a lot of understandable docs out there.

Finally, I needed to write several Python scripts to make everything fit and help manage the content. Well, at least I know Python so that part was not so painful. These were script like [syncdate.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/syncdate.py), [syncdatefile.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/syncdatefile.py), which synchronized the date of the post and the date in the YAML date field in the FrontMatter, and [fm_key_mod.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/fm_key_mod.py) to delete and modify FromMatter arrays like 'tags:' and 'categories:' as I kept changing them daily.'

After many days of naming, renaming, editing, and re-editing my original content to fit into Jekyll architecture, I published to Git Pages (after setting up [gh](https://github.com/cli/cli) with a [token](https://cli.github.com/manual/gh_auth_login), CI/CD, LFS, and GitPages) ... and was presented with pages and pages of errors that made no sense to me, at least not until I figured out what they were... then they made a lot of sense.

I kept notes of what I was learning and needing to refer back to, which are viewable [here]({{site.url}}{% link JNOTES_dev_tholonia.md %}). For anyone who knows Jekyll or Docker, they will seem ridiculously simple, but like everything, it's only simple after you know it!

OK, All my content is up! Now, I had to categorize and tag each piece of content in a way that made sense. After two or three attempts, it was clear I had no idea how to do that... so I decided to let AI do it for me.

I wrote a program ([extract_kw.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/extract_kw.py)) that extracts keywords from a file, which looked something like:

```
$ ./extract_kw.py -f Alternative_Irrigation_Methods.pdf 

irrigation 0.6175
watering 0.5158
hydrogeology 0.4919
groundwater 0.4786
drought 0.4611

[irrigation,watering,hydrogeology,groundwater,drought]
```

With another script ([CATWORD.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/CATWORD.py)) I compared each of those keywords to an array of concepts, which itself was built by AI analyzing concepts of words. To do that, I created [arrays of concepts](https://github.com/tholonia/tholonia.github.io/blob/main/src/taxonomy2.toml) to create the categories. For example, for each category concept, such as ASTRONOMY, COMMUNICATION, ECONOMY, etc., I grouped 500 words associated with that concept, which I got from the very cool site [relatedwords.io](https://relatedwords.io/).

```
ASTRONOMY = [ "astrophysics", "astrology", "physic", ...]
COMMUNICATION = [ "interaction", "language", "message"...]
ECONOMY = [ "market", "economic", "gdp", "financial",...]
```
Then,  each keyword extracted from the document was conceptually compared to every one of those words using AI tools and an LLM (Large Language Model), and the similarities were added up and averaged for each category, resulting in some interesting categorizations.  This can be dramatically improved if I weight the results based on the relevance of the word the keyword is being compared to, but even without that, the results were impressive.

For example, the word "virus" was classified by relevance in the following order:

```
['virus', 'COMMUNICATION       ', 0.2639210671186447]
['virus', 'HEALTH              ', 0.2420676453755452]
['virus', 'BIOSCIENCE          ', 0.21397996693849564]
['virus', 'POLITICS            ', 0.21185217188163238]

```

I wasn't expecting to see COMMUNICATION at the top, but apparently, language IS a virus, at least conceptually, or that is what I am told by academics when I searched for "Language is a virus."  So the AI categorizer did its job well.

"Deception" was categorized as the following:  Check out the high relevance rating (where the max is 1.0).  Is the AI suggesting there is a lot of deception in the parapsychology world, even more than politics!? Hmmm, I'll have to ask my psychic if that's true!

```
['deception', 'PARAPSYCHOLOGY      ', 0.5500629571351138]
['deception', 'COMMUNICATION       ', 0.49766487181186675]
['deception', 'PSYCHOLOGY          ', 0.4660773128271103]
['deception', 'POLITICS            ', 0.4575957981022922]

```
And "sausage" was correctly identified as a health issue first and foremost.

```
['sausage', 'HEALTH              ', 0.13826854150885573]
['sausage', 'BIOSCIENCE          ', 0.13739087618887424]
['sausage', 'NATURE              ', 0.12656965479254723]
['sausage', 'ENERGY              ', 0.11748666873273368]

```

Combining [CATWORD.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/CATWORD.py) and [extract_kw.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/extract_kw.py) into one file ([CATFILE.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/CATFILE.py)) and adding a FrontMatter manager, I was able to read a PDF/TXT file, process it, and update the tags and categories in the relevant markdown file automatically. Yes, the code is a bit of a mess, but most of my code is. Whatever, it worked, which was an accomplishment considering I had never worked with `torch` and `tensors` before, and man, that stuff is dense!  

Large files, like a 3000 page book, took up to 11 minutes on an Nvidia GeForce 4070Ti.  To speed things up, rather than use the built-in Apache Tika server that comes with keyBERT (or maybe with SpaCy. I can't remember), I ran a [standalone tika server](https://docs.netgen.io/projects/lds/en/latest/ubuntu/tika.html), which was about about 10% faster.  And you *have* to use the LARGE LLM **"en_core_web_lg"**, as the small model is missing data required for this to work.  When you add the line
```
nlp = spacy.load("en_core_web_lg")
```
SpaCy will automatically download it if it can't find it.

OK, so now I have automated tags and categories. They weren't perfect, but at least they kept me in the ballpark, which made editing them much easier. 

And with that, and a ton of text editing, the site is (more or less) done!

### Notes:

Helpful note: The ONLY routines that worked properly were [keyBERT](https://maartengr.github.io/KeyBERT/guides/quickstart.html) libraries. The SpaCy and  NLTP AI text processors (see functions `get_keywords_nltk(fn)` and  `get_keywords_spacy(fn)` in [CATFILE.py](https://github.com/tholonia/tholonia.github.io/blob/main/src/CATFILE.py)) either failed or produced horrible results, at least for me and my terrible programming. Your mileage will certainly vary.

If you have CUDA/CuPy, this is an insanely useful link to have!

- https://spacy.io/usage 

