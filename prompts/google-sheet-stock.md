# Prompt: let a client update products, prices and stock from a Google Sheet

Copy everything inside the box below into Claude Code when you're ready. Fill in the [brackets] first.

```
I build websites for small businesses in Trinidad & Tobago (Portside Digital). I want the client to update
their products, prices and stock themselves from a Google Sheet, without touching code and without a backend.

Site: [path to the site file, e.g. event-rentals-demo/index.html]
Client: [business name] — [what they sell or rent]
Published Google Sheet CSV link: [paste the "Publish to web → CSV" link, or say "not yet" and use a sample]

Please:
1. Design the sheet layout for this business. Give me the exact column headers for row 1
   (at least: name, category, price, unit, in_stock, show, image_url, description) and 5 sample rows
   I can paste in. Explain which columns the client edits day to day.
2. Change the site so the product list is built from the sheet:
   - fetch the published CSV on page load
   - use a proper CSV parser that handles commas and quotes inside cells (no extra libraries if possible)
   - only show rows where show = yes
   - show "Sold out" and disable adding when in_stock is 0; show "Only X left" when it's low
   - keep prices formatted as TT$ with commas
   - keep a built-in backup list so the site still works if Google is slow or down, and skip bad rows
     instead of breaking
   - keep everything that already depends on the product list working (filters, cart / quote builder,
     totals, WhatsApp message)
3. Add a short loading state and make sure the page still looks right before the sheet loads.
4. Write me a one-page client guide (plain English, no tech words): how to edit the sheet on their phone,
   what each column means, how long changes take to show (a few minutes), and what NOT to put in the
   sheet because it's public (costs, suppliers, customer details).
5. Test it with the sample data, check it on a phone-sized screen, then commit and push.

Notes:
- Host on Cloudflare Pages (free, business use allowed), not GitHub Pages.
- The published sheet is public read-only; the client only shares edit access with staff and me.
- Stock does NOT go down automatically after a sale with this setup. If I later want that, tell me
  what it would take (WiPay payment webhook → Cloudflare Worker → update stock) as a separate step.
- For rentals, "stock" really means availability per date; if this client needs date-based availability,
  point that out and suggest the simplest option rather than building it now.
```

## How to publish the sheet (do this before running the prompt)

1. Make the Google Sheet with the headers in row 1.
2. File → Share → Publish to web.
3. Choose the sheet tab, then "Comma-separated values (.csv)", then Publish.
4. Copy the link. It looks like
   `https://docs.google.com/spreadsheets/d/e/2PACX-.../pub?gid=0&single=true&output=csv`

## What to charge

Suggested add-on: **+TT$500** one-time for "update your own products and prices" on any site.
