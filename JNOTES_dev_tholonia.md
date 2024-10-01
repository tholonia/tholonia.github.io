###### Overview of Contents:  Instructions and notes for tholonia.com jekyll docker.  Meant to be official README.md 

# Step-by-Step Process for Updating the tholonia.com Site

## Preparation

Open two terminals.

## Terminal 1

1. **Navigate to the project directory:**
   ```sh
   cd /home/jw/sites/tholonia/chirpy2
   ```

2. **Check if the Chirpy image is running:**
   ```sh
   docker ps # shows running containers
   docker ps -a # shows all containteres, including non running
   # if not running...
   docker start -i e830ca5561f3
   
   ```
   
3. **If the Chirpy image is not running, start it:**
   ```sh
   run -it -d -p 4001:4001 -p 35729:35729 --mount src=$(pwd),target=$(pwd),type=bind --name chirpyRun chirpy2:updated
   ```

4. **If the Chirpy image is running, access it:**
   ```sh
   docker exec --workdir $(pwd) -it <CID> bash
   ```

5. **Inside the Docker container, start the server:**
   ```sh
   ./SERVE
   ```

6. **If necessary, install dependencies:**
   ```sh
   bundle install
   ```

## Terminal 2

## Posts	
***
1. **Create a new post:**

   ```sh
   ./add_post.py -t title
   ```
2. **Update the post image:**
   
   - Replace the image at `assets/posts/postname/post_image.png`.
   
3. **Edit the markdown file for the post:**
   
   - Modify the file located at `_posts/postname.md`.
   
4. **Create supporting content such as videos.**

5. **For large documents (e.g., PDFs) that are too large for GitHub:**
   - Upload the document to [Internxt Drive](https://drive.internxt.com/).
   - Copy the download link.
***
## Material

To add new material... 

Add material to  [Internxt Drive](https://drive.internxt.com/) if necessary.

Run
```sh
./add_material.py \
	--title "THIS is a TEST" \
	--src1 https:/... \
	--src1title "View/Download 'THIS is a TEST' (15 pages)" \

# --image defaults fo a black 225x225 square
```
***
6. **Commit changes:**

   ```sh
   git status
```
   - Add any untracked files.

7. **Publish the changes:**
   ```sh
   ./PUSH
```

8. **Check the publish status on GitHub:**
   - Visit [GitHub Repository](https://github.com/tholonia/tholonia.github.io).

9. **Save any system changes made to the Docker image:**
   ```sh
   # docker commit <CID> chirpy2v<vernum>:<tag>
   docker commit 11dcf5450616 chirpy2v1:updated Ron
   ```
   To check all external  links in the document,  run 
```
./check_ext_links.sh <path_to_MD_file>
```
***

***

***



# Root Dir

- /home/jw/sites/tholonia/chirpy2



# Adding a post


```sh
cp EX_post_template.md  _posts/YYYY-MM-DD-TITLE.md
cp EX_post_image.jpg 
```

Edit post

```sh
mkdir assets/YYYY-MM-DD-TITLE
cp EX_post_image.jpg assets/YYYY-MM-DD-TITLE/post_image.jpg
```

Update image

# Adding material

run **ADD_MAT**
```
./add_material.py \
	--title "THIS is a TEST" \
	--src1 https:/... \
	--src1title "View/Download 'THIS is a TEST' (15 pages)" \

# --image defaults fo a black 225x225 square


```

# Site Pages

List all categories and pages in 

- http://0.0.0.0:4001/list_cats
- 

# Docker Commands

### Start the container form an image

Save changes to image

```
docker commit 11dcf5450616 chirpy2:updated
```



```sh
# made sure `pwd` is correct
cd /home/jw/sites/tholonia/chirpy2

# tunneling ports 4000, 35729
docker run -it -d \
-p 4001:4001 \
-p 35729:35729 \
--mount src=$(pwd),target=$(pwd),type=bind \
--name chirpyRun chirpy2:updated
```

### Start and container
```sh
docker start <CID>
```

### Enter the running container

```sh
docker exec --workdir $(pwd) -it <container_ID> bash
```

### Prepare server (if new container)

```sh
bundle install
```

Once the site it published, run 

```
https://www.drlinkcheck.com/
```




# RUNNING

## Run server

```sh
./SERVE
# server live at http://0.0.0.0:4001/
```

### To update Ruby Gems

```bash
gem update --system
```

### Publishing (from HOST only)

```bash
# first check with
git status
# then
./PUSH
```
If 'dubious owner' error message appears after running ./START, from inside the docker image run
```bash
git config --global --add safe.directory /home/jw/sites/tholonia/chirpy2
```



# OLD NOTES

To start Chirpy/Jeckyll up up clean...

```bash
cd ~/sites/tholonia/chirpy2 
#make sure server is running
sudo systemctl start docker
#delete any running containers
ps -a #to get cointainer_ID
docker stop <container_ID>
docker rm <container_ID>
#run the container
docker run -p 4000:4000 -p 35729:35729 -it --mount src=$(pwd),target=$(pwd),type=bind -d --name chirpyRun chirpy:latest

docker ps -a # get container_ID
docker exec --workdir $(pwd) -it <container_ID> bash
#Inside the container
bundle build (???)
./SERVE

#Site now live at  http://0.0.0.0:4000/
# make edits

./SPELLCHECK.py # "update 'src/skipwords.txt'

# add new content
git add .
./PUSH

#goto site: https://github.com/tholonia/tholonia.github.io
# (editor ast: https://github.dev/tholonia/tholonia.github.io)

# if problems, seach text files like this
clear && find -type f -exec grep JNOTES_dev_tholonia.md /dev/null {} \;|grep -v Cache|grep -v _site




```



## Porting to new domain

Change domain name in all MD files

```
find -name "*.md" -exec perl -pi -e 's/https:\/\/tholonia.github.io\//https:\/\/github.com\/tholonia\/tholonia.github.io\/raw\/main\/_/gmi' {} \;
```
to replace all existing repo-named links to raw/main links because `tholonia.github.io` automatically reverst to `tholonia.com`
```
https://tholonia.github.io/
```
to 
```
https://github.com/tholonia/tholonia.github.io/raw/main/_
```



Useful and used Docker commands:

These are related to getting as Jekyll server running in a container for the purposes of locally testing a Jekyll/Git-Pages website
```bash
docker container ls
docker image ls
```

### To wipe all 

```bash
sudo systemctl stop docker
docker system prune -a
docker rmi $(docker images -a -q)
sudo systemctl start docker
```

### Build (and capture the IMAGE_ID of the build)

```bash
$ cd /some/directory
$ docker build -t tsite . > /tmp/d_build.log
$ IMAGE_ID=`grep "Successfully built" /tmp/d_build.log|awk '{print $3}'`
$ CMD=`"docker run -p 4000:4000 -p 35729:35729 -it --mount src=$(pwd),target=$(pwd),type=bind -d --name jekyll tsite"`
$ CONT_ID=${CMD}
$ docker exec --workdir $(pwd) -it jekyll bash
```
### build

```bash
docker build -t tsite . > /tmp/d_build.log
```

###  mount
this uses the \`PWD\`as the mounted dir
```bash
docker run -p 4000:4000 -p 35729:35729 -it --mount src=$(pwd),target=$(pwd),type=bind -d --name chirpy2 tsite
```
If running, it needs to be stopped and deleted

```bash
docker stop ${CONT_ID}
docker rm ${CONT_ID}
```
or
```bash
docproc -k ${CONT_ID}
```

To list all processes...

```bash
docproc --showall ${CONT_ID}
```

###  enter

```bash
docker exec --workdir $(pwd) -it chirpy2 bash
```


### inside container

```bash
$ sh run-once-after-dockerfile.sh  #(if needed)
$ bundle exec jekyll serve --host 0.0.0.0 --livereload --watch --trace
```
### To save the changes
```bash
$ docker commit ${CONT_ID} tsite:latest
```
### To delete, 
```bash
$ docker stop $CONT_ID  # the container must first me stopped (if active)
$ docker rm $CONT_ID
$ docker system prune --all --force
```


### No idea what this does !
```bash
$ docker attach $CONT_ID  # No idea what this does !
```

### Cloning and running  container
```bash
$ docker commit -m="Cloned MM for Chirpy" b990b4fece5a chirpy:latest
$ docker run -p 4000:4000 -p 35729:35729 -it --mount src=$(pwd),target=$(pwd),type=bind -d --name chirpyRun chirpy:latest
```

# SITES

## Linkchecker

- https://www.drlinkcheck.com/

## Wordnets

- https://relatedwords.io/

## CUDA/CuPy SpaCy widget

- https://spacy.io/usage  #widget
- https://tika.apache.org/1.24/api/org/apache/tika/parser/pdf/PDFParserConfig.OCR_STRATEGY.html  #OCRStrategy

## Docker Image for Minimal Mistakes Jekyll Theme

- https://github.com/techrail/mmistakes-docker

## Minimal Mistakes Theme

- https://github.com/mmistakes/minimal-mistakes

## Setting up jekyll with minimal-mistakes theme

- https://brasier.me/jekyll/theme/2019/01/19/installing-minimal-mistakes-jekyll/#\

## Theme Setup - installation

- https://blog.christianposta.com/theme-setup/

## Existing minimal-mistakes repos

- https://github.com/topics/minimal-mistakes

## Bootstrap Icons

- https://www.tutorialrepublic.com/bootstrap-icons-classes.php

## Ruby Plugin: directory

- https://github.com/sillylogger/jekyll-directory

## OpenMoji

- https://frankindev.com/2022/05/23/github-flavored-joypixels-cheat-sheet/

## IFTTT

- https://ictsolved.github.io/auto-post-articles-from-jekyll-blog-to-social-sites/

# Problems

## perlmalink or actual links for PDF files

### Solution

All files that are in LFS require PERMALINK URL's and all files in the main repo require REAL URLs.
There are the files in the LFS:

```
_the_book/assets/latest/THOLONIA_THE_BOOK.md.zip filter=lfs diff=lfs merge=lfs -text
_the_book/assets/latest/THOLONIA_THE_BOOK.html.zip filter=lfs diff=lfs merge=lfs -text
_the_book/assets/latest/THOLONIA_THE_BOOK.pdf filter=lfs diff=lfs merge=lfs -text
_the_book/assets/latest/THOLONIA_THE_BOOK.epub filter=lfs diff=lfs merge=lfs -text
_material/assets/book_red_NOTFREE.zip filter=lfs diff=lfs merge=lfs -text
_material/assets/book_ICHING_THE_BOOK.zip filter=lfs diff=lfs merge=lfs -text
_material/assets/book_THOLONIA_COLORING_BOOK.zip filter=lfs diff=lfs merge=lfs -text
_material/assets/book*.zip filter=lfs diff=lfs merge=lfs -text
**/*.m4a filter=lfs diff=lfs merge=lfs -text

```
**this is not correct!**
Current state...

- NOT in LFS
  - All `/_material/material*` uses `/material/material...` ( tholonia.github.io)
  - All book chapters use `/_the_book/...` (in  tholonia.github.io)

- IN LFS
  - All `/_material/book` uses `/material/book*...` (in  tholonia.github.io)
  - The entire book uses `/_the_book/...` (but in tholonia.github.io/raw/main/)










## Invalid US-ASCII character "\xE2" on line 3

```
Conversion error: Jekyll::Converters::Scss encountered an error while converting 'assets/css/styles.scss': Invalid US-ASCII character "\xE2" on line 3
```

### Solution:

see https://askubuntu.com/questions/683406/how-to-automate-dpkg-reconfigure-locales-with-one-command for more

```bash


# Install program to configure locales
apt-get install -y locales
dpkg-reconfigure locales  # choose '160' for 'en_US.UTF-8 UTF-8'
locale-gen C.UTF-8        # choose option 3
/usr/sbin/update-locale LANG=C.UTF-8

# Install needed default locale for Makefly
echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && locale-gen

# Set default locale for the environment (added to /etc/profile)

export LC_ALL="C.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"

```

## Docs in docker saved as root causes problems with username in host

### Solution

Log into docker as root

```bash
$ adduser jw
$ apt-get install sudo joe
```

edit /etc/sudoers. 

change 
```
root ALL=(ALL:ALL) ALL
```
to 

```
root ALL=(ALL:ALL) ALL
jw ALL=(ALL:ALL) ALL
```

- Log out of docker

- commit changes to image

- stop and kill container

- relogin with `--user jw` argument

```bash
docker run -p 4000:4000 -p 35729:35729 -it --mount src=$(pwd),target=$(pwd),type=bind -d --name chirpyRun chirpy:latest" 
```

Run `sudo bundler install`

## Need to rebuild from scratch
### Solution
Create or delete a repo as needed
```bash
gh auth login --with-token <  ~/.ssh/gh_token
gh repo delete  tholonia.github.io --yes
gh repo create  tholonia.github.io --public
```
Default `.gitignore` file
```bash
# Bundler cache
.bundle
vendor
Gemfile.lock
# Jekyll cache
.jekyll-cache
_site/
# RubyGems
*.gem
# NPM dependencies
node_modules
package-lock.json
# IDE configurations
.idea
.vscode
.directory
# Misc
assets/js/dist
PUSH
SERVE
*.ORG
x
xx
*.zip
SAVE 
```

```bash
gh auth login --with-token <  ~/.ssh/gh_token
gh repo delete  tholonia.github.io --yes
gh repo create  tholonia.github.io --public 

rm -rf .git
rm .gitattributes
rm -rf _site/*

GIT_TRACE=1
git init
git branch -M main
git remote add origin git@github.com:tholonia/tholonia.github.io.git

git lfs install
# auto track
find -type f -name "THOLONIA_THE_BOOK*"|grep -v "_site"|awk '{print "git lfs track "$1}' |sh -x
find -type f -name "THOLONIA_THE_BOOK*"|grep -v "_site"|awk '{print "git add -f  "$1}' |sh -x
git commit -m "Move large file to Git LFS"

# is need to remove from git repo but keep in file system
find -type f -name "THOLONIA_THE_BOOK*"|grep -v "_site"|awk '{print "git rm --cached "$1}' |sh -x 
find -type f -name "THOLONIA_THE_BOOK*"|grep -v "_site"|awk '{print "git add -f  "$1}' |sh -x 
git commit -m "Move large file to Git LFS"


# all books are LFS
git lfs track "_material/assets/book*.zip"
git add -f _material/assets/book*.zip
#git lfs track "_material/assets/book*.pdf"
#git add "_material/assets/book*.pdf"
git add .gitattributes
git lfs status ; git lfs ls-files # check that they are committed
git commit -m "Tracking and adding LFS artifacts"
git push --set-upstream origin main

# check for any files over github limit
# find -size +100M

# now add the rest of the content
git add .
git commit -m "first commit after LFS"
git push origin main

```
## No `_layouts` folder exists, and most of the data is not in the `_data` folder

### Solution

It seems that GitHub wants people to use GEM layouts, which embed `_layouts`, `_includes`, `_sass`, `_assets`, so you can't see them anymore. I am sure there is a super good reason for this, otherwise, why would they make it ridiculously more obtuse than it already is :/

Run

```bash
$ bundle show jekyll-theme-chirpy
```
This will show the folder where the GEM theme files are.  For example
```bash
/usr/local/src/rbenv/versions/3.1.2/lib/ruby/gems/3.1.0/gems/jekyll-theme-chirpy-6.3.1
```
Run the following to copy these folder to you local ${WEB_ROOT}.  Some of these folders may not exist.
```bash
$ DIR='/usr/local/src/rbenv/versions/3.1.2/lib/ruby/gems/3.1.0/gems/jekyll-theme-chirpy-6.3.1"

$ rsync -avr ${DIR"/_layouts ${WEB-ROOT}
$ rsync -avr ${DIR"/_data ${WEB-ROOT}
$ rsync -avr ${DIR"/_sass ${WEB-ROOT}
$ rsync -avr ${DIR"/_assets ${WEB-ROOT}
```

## Git committing large files

### Solution

Add LFS to git
```bash
# add to tracker
git lfs track "projects/material/assets/book*.pdf*"
git add "projects/material/assets/book*.pdf*"
git add .gitattributes
# check
git lfs status ; git lfs ls-files # check that they are committed
# apply
git commit -m "Tracking and adding LFS artifacts"
git push origin main

# check for any files over github limit
find -size +100M

```
To untrack LFS files
```bash
git lfs untrack '<file-type>'
git rm --cached '<file-type>'
git add '<file-type>'
git commit -m "restore '<file-type>' to git from lfs"
```
To add a new path for LFS
```bash
git lfs track "assets/books/*.pdf"
git add assets/books/*.pdf
git lfs status ; git lfs ls-files # check that they are committed
git commit -m "Tracking and adding LFS artifacts"

```

To force a rebuild

```bash
git commit --allow-empty -m "Trigger rebuild"
git push
```
##  

## SVG file complains `Uncaught SyntaxError: Unexpected end of input (at (index):1:13421)`files

### Solution (this did not work.  awaiting reply from devs)
```bash
$ sudo apt-get install ruby-dev
$ sudo gem install jekyll-inline-sv
```

Then follow the instructions at https://github.com/sdumetz/jekyll-inline-svg

## Old files still exist in `./_site`

### Solution

rebuild site from scratch

```bash
$ rm -rf _site
$ jekyll build
```



# UTILS

to change FM `date:` field in MD files to match the filename date using the `-o` flag.  `-i` flag to change filename to FM date.  Filename dates MUST be YYYY-MM-DD_"
```
ls *.md |awk '{print "~/sites/tholonia/chirpy2/syncdatefile.py -f "$1" -o"}'|sh
```
To automatically redate all files from from some date in 2020. (CHECK CODE).  
```
~/sites/tholonia/chirpy2/syncdate.py
```
Hardcoded to 
```
/home/jw/store/sites/tholonia/chirpy2/projects/videos
```

# KEYWORDS

To clean a TOML word list, such as `taxonomy.toml'
```
./CHECK_TAXONOMY > taxonomy_cleaned.toml
```
To update categories and tags in a MD file:
```
./CATFILE.py -f _material/assets/ballism_and_yaism_updated.pdf  -l 10 -s 2 -v
```

To update keyword for all MD files in a folder
```
find _material/ -type f -name "*pdf" |awk '{print "./CATFILE.py -f "$1"  -l 1000 -s 2 -v "}'
```

# Files
## python
- **`CATFILE.py`** - *update MD file with auto keyword generator*
- **`CATWORD.py`** - *tests categorization of a single word*
- **`TAX-REPORT.y`** - *prints out taxonomy with all unparsable words removes*
- **`syncdatefile.py`** - *synchronizes the filename date and the date tag*
- **`syncdate.py`** - *updates filename date*
- **`TAX_REPORT.py`** - *prints number of words in taxonomy category*
- **`extract_kw.py`** - *extracts keywords from a file (pdf,txt)*
## bash
- **`ADDBIG`** - add large file to LFS 
- **`CLEAN_GITHUB`** - *uses `gh` to wipe caches, workflows logs on github*
- **`FINDFILE`** - *find file in tree from current root.  Uses partial filename*
- **`FINDINFILE`**- *Finds any file that has matched content*
- **`MAKEGIF`** - *make an animated GIF with ffmpeg*
- **`MAKELINKS`** - *creates subdir .ZPROJECTS and fills with symlinks to collections*
- **`SERVE`** - *cleans caches and starts jekyll server (in docker)*
- **`TESTLINKS`** - *runs linkchecker (in docker only, uses Jekyll to test)*
- **`STOPSERVER`** - *kill all jobs called 'server' (in docker)*

## Versions



$ sudo apt list --installed|grep -i gem

ruby-rubygems 3.3.5-2 
rubygems-integration 1.18 

ruby 3.1.2p20

# Giscus

https://andrewlock.net/replacing-disqus-with-github-discussions-using-giscus/

repo_id ("octolytics-dimension-repository_id")

## Discussion links

https://github.com/orgs/community/discussions/83085

https://github.com/giscus/giscus/issues/1272

https://www.reddit.com/r/github/comments/18ucot3/giscus_rejects_allany_repos_i_select_despite/



## Conda ENVs and Scripts

```
conda env list                               
```

**Rife**

-  interpolation scripts

**fooocus**

- env for SD/ComfyUI

**llama** 

- `/bin/ollama serve`
- `~/src/ollama-webui/backend/start.sh`
- ``${TROOT}/src/ollama/docsum*`

**spacy**  (keyBERT, NLTP)

- `${TROOT}/SPELLCHECK.py`
- `CATWORD.py`, `CATFILE.py`

#### dead/unused
- dev  
- open-musiclm 
- AI  possibly dead.  Not used anymore?

# Required software to get book publishing running

### Debian 12


```sh
# sudo apt-get remove libuv1
sudo apt-get install libuv1
sudo apt-get install libuv1-dev
sudo apt-get install npm

sudo npm install -g less

# required...
sudo rm lessc
cd /usr/bin
rm lessc
sudo ln -fs /usr/local/lib/node_modules/less/bin/lessc ./lessc

sudo apt-get install pandoc

# Install "prince" and "prince-books" manually
# download generic PrinceXML from https://www.princexml.com/download/11/
# download generic Prince-books fromhttps://www.princexml.com/books/

sudo apt-get install pdftk



```



### To clean large files from git repo

- install "git-filter-repo"

- make clean clone

 ```
git-filter-repo \
--invert-paths \
--path _the_book/assets/latest/THOLONIA_THE_BOOK.html.zip
 ```
- rebuilt (copy)  .gitattributes
- rebuilt (copy) .git/config
```sh
git branch --unset-upstream
git-filter-repo --invert-paths --path
add -f _the_book/assets/latest/THOLONIA_THE_BOOK.pdf
```

