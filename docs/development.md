---
layout: default
title: Development
tagline: It was not that hard
description: How I created this site and how you can help to improve both it and the course
---

## Contents
{:.no_toc}

* This text will be replaced by a table of contents (excluding the above header) as an unordered list
{:toc}

---

## Ways you can help improve this website

We need help! Here are a few ideas for how this website might be improved. If you would like to do one or more of these things, whether or not you are currently enrolled in AE353 at Illinois, [contact Prof. Bretl](mailto:tbretl@illinois.edu).

### Add a sidebar with the table of contents

It would be nice to have the table of contents in a sidebar that is always visible, instead of at the top of the page. [Leap Day](https://github.com/pages-themes/leap-day) is a theme for GitHub Pages that has this kind of sidebar (see [demo](https://pages-themes.github.io/leap-day/)). You could either change the theme of the site from [Cayman](https://github.com/pages-themes/cayman) to something like Leap Day, or add a custom sidebar to the Cayman theme.

### Improve site navigation

There is a row of buttons in the header that allow movement between pages on this site. There are a number of problems with this at the moment:

* The buttons are hard-coded. They should be generated programmatically, for example from a YAML configuration file.
* The buttons do not indicate what page you are on. They should.
* The buttons don't look very nice. They should look better. (Maybe in a single row along the top of the page?)

There are various third-party Jekyll themes that support this sort of thing, such as [Hyde](https://github.com/poole/hyde). I don't know how to use third-party Jekyll themes. You could figure that out.

## Tips and tricks for site creation

### Including a table of contents

This website was created using [Jekyll](https://jekyllrb.com) on [GitHub Pages](https://pages.github.com). If you look at the [code]({{ site.github.repository_url }}), you'll see that content is written in [Markdown](https://docs.github.com/en/github/writing-on-github/about-writing-and-formatting-on-github). By default, Jekyll uses [kramdown](https://kramdown.gettalong.org) to convert Markdown to HTML. Kramdown supports the [automatic generation of a table of contents](https://kramdown.gettalong.org/converter/html.html#toc). This table will include an entry for every header. To use this feature, you include the following lines at the top of your Markdown document:
```
## Contents
{:.no_toc}

* This text will be replaced by a table of contents (excluding the above header) as an unordered list
{:toc}
```
The `{:toc}` tag is what creates the table of contents. The `{:.no_toc}` tag ensures that the header "Contents" will not appear in this table. Note that you *must* put `{:toc}` on its own line immediately after a single list item. The text in this list item will be replaced.

You might think it is silly to include a line of text that will simply be replaced. In particular, it might seem reasonable to do this instead:
```
## Contents
{:.no_toc}

{:toc}
```
Don't! This will not work.




## How to preview this website on your own computer

It is helpful to preview changes I make to the website before they go live. To do so, I followed [these instructions](https://docs.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll) from the [GitHub pages documentation](https://docs.github.com/).

First, I [installed ruby, bundler, and jekyll](https://jekyllrb.com/docs/installation/macos/). I used Homebrew to install Ruby. I did not use rbenv.

Second, I created a [Gemfile](https://bundler.io/man/gemfile.5.html#NAME) and installed dependencies. If I had been starting from scratch with a new repository, I would have followed [these instructions from GitHub](https://docs.github.com/en/github/working-with-github-pages/creating-a-github-pages-site-with-jekyll). However, I had already [created a site](https://docs.github.com/en/github/working-with-github-pages/creating-a-github-pages-site), so instead I did the following things:
* Navigated to the `docs/` folder in my local copy of the repository, which is what I had previously chosen as my [publishing source](https://docs.github.com/en/github/working-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).
* Called `bundle init` (see [docs](https://bundler.io/v2.2/man/bundle-init.1.html)) to create a Gemfile.
* Added the line `gem "github-pages", group: :jekyll_plugins` to this Gemfile.
* Added the line `gem "webrick", "~> 1.7"` to this Gemfile, as suggested [here](https://github.com/github/pages-gem/issues/752#issuecomment-764647862). This is because I am using Ruby 3.0.x, which does not include the gem webrick, while GitHub Pages uses Ruby 2.7.x in production (as of January, 2021), which does include webrick. If I did not add this line, I would get the error `bundler: failed to load command: jekyll` when trying to test the site locally.
* Called `bundle install` (see [docs](https://bundler.io/man/bundle-install.1.html)) to install the dependencies needed to test the site locally.

Third, I tested the site by following [these instructions from GitHub](https://docs.github.com/en/github/working-with-github-pages/testing-your-github-pages-site-locally-with-jekyll). In particular, still inside the `docs/` folder, I called
```
bundle exec jekyll serve --baseurl '/ae353-sp21'
```
and then opened `http://localhost:4000/ae353-sp21/` in a browser. (See ["Clearing Up Confusion Around baseurl -- Again"](https://byparker.com/blog/2014/clearing-up-confusion-around-baseurl/) for why the `--baseurl '/ae353-sp21'` argument is necessary.)

The key benefit of this setup is that any local changes I make to files (e.g., this one: `howto.md`) show up immediately in my browser on `localhost`. In contrast, if I `git push` these changes, it can take several minutes for the site to rebuild and for these changes to show up in my browser on `tbretl.github.io/ae353-sp21`.

It took several hours to figure this all out. There were three causes of delay:

* I had to start over after I realized it was important to install Ruby with Homebrew. MacOS ships with Ruby, but this is installed globally, and you have the usual problem of needing to run with `sudo` when trying to subsequently install anything with bundler.
* Instructions for site creation assumed I was starting from scratch. Apparently, most people who recognize the need for local testing create the site with that in mind from the start. So, it took me a while to understand the `bundle init` / `bundle install` process.
* It took me forever to find the fix to `bundler: failed to load command: jekyll` (see above).
* I did not understand the `baseurl` concept (see above).

If I did this all again, it would take no more than ten minutes.
