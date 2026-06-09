# Jenna Lynn Photography — Website

Static site for Jenna Lynn Photography (Wedding & Couples Photography), hosted
on GitHub Pages at **photographybyjennalynn.com**.

## Stack

- Plain HTML + CSS + vanilla JavaScript (no build step)
- Google Fonts (Cormorant Garamond, Montserrat)
- GitHub Pages for hosting, TLS, and CDN
- Google Forms for the contact form (no backend on the VPS)

## Local development

Just open `index.html` in a browser. There's no build step. The site is
intentionally simple.

## Production deployment

1. Push to `main` branch on GitHub.
2. GitHub Pages serves the site from `main` automatically.
3. The `CNAME` file in this repo tells GitHub Pages to use
   `photographybyjennalynn.com` as the custom domain.
4. DNS for `photographybyjennalynn.com` points to GitHub's IP set (managed
   in Namecheap).

## Updating photos

The `photos/` directory is for actual client photos. Currently empty (the
template ships with placeholder gradients in the gallery section). To add
real photos:

1. Drop optimized JPEGs/PNGs into `photos/` (keep file sizes reasonable —
   GitHub Pages has a 1GB repo size limit and 100GB/month bandwidth soft cap).
2. Update the `<img>` references in `index.html` (search for `src="photos/`).
3. Commit and push.

## Updating the contact form

The contact form in `index.html` is a UI mockup that doesn't actually send
email — it shows a "Yay!" success message but discards the data. The real
contact form is a Google Form embedded via iframe. To swap the Google Form:

1. Create the form in Google Forms.
2. Get the embed `<iframe>` snippet (Send → Embed).
3. Replace the `<form id="contactForm">...</form>` block in `index.html` with
   the iframe.
4. Style tweaks in `style.css` to match the site's look (the form should
   not have a stark white-on-white Google default).

## Privacy

- No analytics, no tracking pixels, no cookies.
- The site is static and public; visitors are anonymous to us.
- Form submissions go to Google (for the Google Form) and to our email
  (via Google Form's notification settings).

## Related

- The site is part of a pair — see `BenkoMatt/matthew-benko-portfolio` for
  the personal portfolio site.
