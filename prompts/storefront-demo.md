# Storefront demo: Claude Code prompt (social media shop + Google Sheet stock)

A demo to show the client before he pays: his own shop page that customers open from his social media bio,
with products, sizes, stock and a cart that sends the order to WhatsApp. He can edit a Google Sheet on his
phone and watch the shop change.

## Before you start (5 minutes, on your phone or PC)

1. Get from the client (or his page): **business name, logo, what he sells, 6–12 product photos with
   prices**, his WhatsApp number and Instagram/TikTok handle. If you don't have photos yet, say "use
   placeholders".
2. Make a **Google Sheet** (in your account for the demo; move it to his later). Leave it empty; Claude
   Code will give you the headers and sample rows to paste.
3. Open Claude Code (phone app or PC) in this repo and paste the prompt below. Fill in the `[brackets]`.
4. When Claude Code gives you the sheet headers, paste them in, then **File → Share → Publish to web →
   CSV → Publish**, copy the link and send it back to Claude Code.

---

```
Build a DEMO storefront for a potential client of my web business (Portside Digital, Trinidad & Tobago).
It's a mobile-first online shop that his customers open from the link in his social media bio. He updates
products, prices and stock from a Google Sheet on his phone. Orders go to his WhatsApp. No backend.
Goal: impress him enough to buy, so it must look like a real, polished brand shop, not a template.

CLIENT
- Business name: [BUSINESS NAME]
- Sells: [WHAT HE SELLS, e.g. men's streetwear / sneakers / perfumes]
- Brand colours / vibe: [colours, or "take them from the logo in ./storefront-demo/assets"]
- Logo + product photos: ./storefront-demo/assets (if empty, use tasteful placeholders and tell me)
- WhatsApp: [868XXXXXXX]   Instagram: [@handle]   TikTok: [@handle or none]
- Delivery: [e.g. Delivery TT$40 Trinidad, TT$80 Tobago, pickup in (area)]
- Published Google Sheet CSV link: [paste it, or "not yet"]

STEP 1 — THE SHEET (do this first and show me)
- Design the sheet for this kind of product. Row 1 headers, at least:
  id, name, category, price, sale_price, sizes, colours, stock, show, badge, image_url, description
  - sizes / colours: comma separated (e.g. "S,M,L,XL")
  - stock: one number, OR per size like "S:2,M:0,L:5" (support both)
  - show: yes/no   badge: New / Hot / Sale / blank
- Give me the headers and 10 realistic sample rows for this business, ready to paste.
- Tell me exactly how to publish it as CSV. Then wait for the link (use the sample rows until then).

STEP 2 — THE SHOP (single folder ./storefront-demo, plain HTML/CSS/JS, no build step, no frameworks)
- Header: logo, business name, search, cart icon with count. Sticky on scroll.
- Hero: big brand banner with a short tagline and "Shop now". Social links.
- Category chips + filters (size, price, in stock only) + sort (new, price low/high).
- Product grid: photo, name, price (sale price with old price crossed out), badge, "Only 2 left",
  "Sold out" (greyed, can't add).
- Product view (sheet/modal on mobile): photos, description, size and colour pickers that disable
  sold-out sizes, quantity, "Add to cart", "Ask about this on WhatsApp".
- Cart drawer: items, change qty, remove, delivery/pickup choice, total in TT$ ("TT$1,250.00").
  Saved in localStorage.
- Checkout = "Send order on WhatsApp": opens wa.me/[number] with a neat pre-filled message:
  order list (name, size, colour, qty, price), delivery choice, total, and fields for the customer's
  name and area. Optional note.
- "Share this product" button (copies link / uses the phone share sheet) with deep links like
  #product=ID so he can post one product's link in a story.
- Footer: contact, WhatsApp, socials, "Powered by Portside Digital".
- Data: fetch the published CSV on load with a real CSV parser (quotes/commas inside cells), only rows
  with show = yes, skip bad rows instead of breaking, keep a built-in backup copy of the sample data
  so the shop never shows empty, and a nice loading skeleton. Add a tiny cache-buster so his edits show
  within a minute or two.
- Fast and polished: lazy-loaded images, smooth small animations, big tap targets, looks great at
  390px wide first, then tablet and desktop. Accessible (labels, contrast, keyboard).
- SEO/social: page title, description, and an Open Graph image so the link looks good when shared on
  WhatsApp/Instagram.

STEP 3 — "WHAT YOU'D GET" EXTRAS FOR THE DEMO
- A small dismissible banner at the top: "Demo for [BUSINESS NAME] by Portside Digital".
- A page /storefront-demo/admin-preview.html that shows what the paid Admin Dashboard upgrade looks
  like (login screen → products list, stock per size, orders list, low-stock alert, discount code).
  It is a clickable MOCKUP with fake data only, clearly labelled "Preview — Admin Dashboard package".
  No real login, no real data.
- A one-page client guide (plain English, phone screenshots described step by step): how to add a
  product, change a price, mark sold out, hide a product, and what NOT to put in the sheet because
  it's public (costs, suppliers, customer details).

STEP 4 — CHECK & PUBLISH
- Test with the sample data and (if given) the live sheet: change a stock number in the sheet and
  confirm the shop updates; test sold-out sizes, the cart, and the WhatsApp message text.
- Take screenshots at phone and desktop width, look at them, and fix anything that looks off.
- Commit and push. Tell me how to publish it on Cloudflare Pages (free) so I can send him a link, and
  give me a short WhatsApp message to send him with the link.

RULES
- Use only the client's real name/logo/photos or neutral placeholders. Never copy another brand's
  images or name.
- Don't put anything private in the code or the sheet.
- Keep it one folder so I can reuse it as a template for the next client.
```

---

## After the demo

- **Show him on his phone:** open the shop, then change a price in the sheet together and refresh. That
  is the moment that sells it.
- **Prices to quote:** Storefront + Google Sheet **TT$2,500** · Storefront + Admin Dashboard **TT$5,500** ·
  online card payments **+TT$2,000** · domain about TT$75/year · hosting TT$0 on Cloudflare.
- If he buys, move the Google Sheet to his Google account (or share it with him as owner) and connect his
  domain.
