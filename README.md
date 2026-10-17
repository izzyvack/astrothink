# AstroThink website

This folder contains the complete static website, ready for GitHub Pages. It uses HTML, CSS, and JavaScript, with local images and Merriweather fonts. No installation or build step is required.

## Put it on GitHub Pages

1. Create your repository on GitHub. A public repository works with GitHub Free.
2. Extract the ZIP on your computer.
3. In the repository, choose **Add file → Upload files**. Upload the extracted files and folders, including `assets/`. `index.html` should be at the repository's top level. Upload the contents, rather than the ZIP itself or an extra outer folder.
4. Commit the upload to `main`.
5. Open **Settings → Pages**. Under **Source**, choose **Deploy from a branch**. Choose **main** and **/(root)**, then save.
6. GitHub will show the website address on that page when deployment completes.

The relative links work at a project address such as `https://YOUR-USERNAME.github.io/YOUR-REPOSITORY/`, as well as at a custom domain.

GitHub's official setup instructions: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## Edit the website

- `index.html`: homepage.
- `about.html`, `programs.html`, `team.html`, `contact.html`: organization pages.
- `space-ai.html`, `python-neural-networks.html`, `beyond-the-stethoscope.html`, `career-pathways.html`: program pages.
- `explore.html`: parachute lab and online learning links.
- `styles.css`: colors, fonts, spacing, and responsive layouts.
- `app.js`: navigation, filters, email copying, and the parachute experiment.
- `assets/`: pictures, logos, font files, and the font license.

You can edit the HTML files directly. Alternatively, shared page templates live in `tools/build.py`, with team and program information in `content/site.json`. To regenerate the HTML after changing those files, run:

```sh
python tools/build.py
```

Regeneration overwrites the HTML pages, so make further content changes in the templates or JSON if using that approach. To add canonical links and a sitemap after you know the final website URL, fill in `site_url` in `content/site.json` and regenerate.

The program dates describe completed Summer 2026 sessions. Update them when future dates are confirmed. Learning portal links open the existing AstroThink service, where account and course features are hosted. Contact links open the visitor's email application.

## Assets

AstroThink's logo, team photographs, and partner logos come from its existing website and Instagram. The rover illustration comes from the user's supplied artwork. Merriweather is included under the SIL Open Font License in `assets/fonts/OFL.txt`.
