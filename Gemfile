# frozen_string_literal: true

gem "jekyll", "~> 4.3"
gem "webrick", "~> 1.8"
gem "jekyll-sass-converter", "~> 2.2"
gem "sassc", "~> 2.4"


source "https://rubygems.org"

gem "jekyll-theme-chirpy", "~> 6.3", ">= 6.3.1"

group :test do
  gem "html-proofer", "~> 4.4"
end

# Windows and JRuby does not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions of the gem
# do not have a Java counterpart.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# needs to be include only oin lenovo, for some reason
gem 'jekyll-include-cache'

# gem "jekyll-inline-svg"
gem 'jekyll-openmoji'

gem 'jekyll-feed'

# gem 'jekyll-inline-svg'

group :jekyll_plugins do
  gem "jekyll-youtube"
end

# gem "markdown_helper"
