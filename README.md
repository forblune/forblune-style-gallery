# Forblune Style Gallery

[Live gallery](https://gallery.forblune.com) · [Forblune portfolio](https://portfolio.forblune.com)

A working collection of 24 small websites made to compare eight different visual languages. Each example has its own subject, type scale, spacing rhythm, interaction pattern, and responsive behavior; the gallery is used to choose a direction before a client build starts.

The examples are fictional design studies. Names, products, prices, schedules, records, and business data do not represent real customers.

## Browse by direction

| Direction | Examples | Best suited to |
|---|---|---|
| [Editorial](https://gallery.forblune.com/#editorial) | niche perfume, private stay, select shop | image-led retail and hospitality |
| [Kinetic](https://gallery.forblune.com/#kinetic) | sneaker drop, music festival, esports team | launches and event campaigns |
| [Cinematic](https://gallery.forblune.com/#cinematic) | architecture studio, restaurant, photographer | story-led portfolios |
| [Corporate](https://gallery.forblune.com/#corporate) | clinic, law firm, manufacturer | services that depend on trust and clear information |
| [Product](https://gallery.forblune.com/#product) | invoicing tool, sleep app, developer API | software and product explanation |
| [Commerce](https://gallery.forblune.com/#commerce) | grocery store, class booking, furniture shop | browsing, comparison, and purchase flows |
| [Experimental](https://gallery.forblune.com/#experimental) | water campaign, media-art show, smart-ring teaser | a single strong campaign idea |
| [Utility](https://gallery.forblune.com/#utility) | store dashboard, inventory ERP, help desk | dense operational interfaces |

Open any card in the live gallery to use the full page. Filters in the header narrow the list without reloading it.

## What is implemented

- 24 standalone HTML pages with their own CSS and JavaScript
- keyboard focus states and reduced-motion handling
- desktop, tablet, and mobile layouts
- working filters, drawers, dialogs, tables, forms, or charts where the example calls for them
- no customer data, testimonials, conversion claims, or fabricated client results

Product and utility examples draw their visual evidence from the interface itself. Image-led examples use external editorial photography and may need an internet connection to load every photograph.

## Repository layout

```text
index.html              gallery index and category filters
sites/<slug>/index.html individual examples
sites/<slug>/meta.json  project notes used during review
_reference/             design-language and review notes
```

The deployed build includes the gallery index and the example pages. Project notes and review material remain source-only.

## Run locally

```sh
python -m http.server 8080
```

Visit `http://localhost:8080` for the gallery or open an example directly, such as `http://localhost:8080/sites/kinetic-sneaker/`.

## Deploy

```sh
bash deploy.sh
```

`deploy.sh` assembles a static `dist/` directory and deploys it through Cloudflare Workers Static Assets. The public address is `https://gallery.forblune.com`.
