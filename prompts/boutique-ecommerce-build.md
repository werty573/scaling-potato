# Boutique e-commerce + admin + POS: Claude Code build prompt

## Before you start (one time)

1. Install **Node.js (LTS)**, **Git** and **Claude Code** on your PC.
2. Create free accounts in **your client's name/email** (she owns them, you get access):
   **Supabase** (database), **Vercel** (hosting), **Resend** (emails), **GitHub** (code).
3. Ask **WiPay** for their developer/API docs and test (sandbox) account details.
4. Make a folder, e.g. `C:\dev\boutique`, and copy the **demo store files** into `C:\dev\boutique\demo`.
5. Put her **logo**, a few **product photos** and her **product list** (if she has one) in `C:\dev\boutique\assets`.
6. Open Claude Code in `C:\dev\boutique` and paste the prompt below. Fill in the `[brackets]` first.

Work one phase at a time. Test each phase yourself before saying "continue".

---

```
You are building a production e-commerce system for a clothing boutique in Trinidad & Tobago:
an online store, an admin dashboard and an in-store point of sale (POS), all sharing ONE inventory.
This is a real business that will take real money. Correctness of stock and payments matters more
than speed. Work in phases, stop at each CHECKPOINT, and wait for me to say "continue".

BUSINESS DETAILS
- Store name: [STORE NAME]
- Domain: [yourstore.com]
- Brand colours / fonts / look: copy them from the demo in ./demo (read every file in ./demo first and
  keep the same style). Logo and photos are in ./assets.
- Currency: TTD, shown as "TT$1,250.00". Timezone: America/Port_of_Spain.
- Delivery options: [e.g. delivery Trinidad TT$40, Tobago TT$80, free over TT$500] and store pickup at
  [store address].
- Owner email for alerts: [owner email]. WhatsApp: [number].

STACK (use these unless something is impossible; tell me before changing anything)
- Next.js (App Router) + TypeScript (strict) + Tailwind CSS.
- Supabase: Postgres, Auth (email + password for staff), Storage (product images),
  Row Level Security on EVERY table.
- Vercel hosting + Vercel Cron for scheduled jobs.
- Resend for emails. Zod to validate every input. Vitest for unit tests, Playwright for end-to-end.
- WiPay for online card payments (details below).
- Keep monthly running cost at or near zero on free tiers.

DATA MODEL (Postgres; money stored as integer cents; all times stored in UTC)
- products: id, name, slug, description, category_id, base_price, status (draft/active/archived),
  created_at, updated_at.
- categories, collections (e.g. "New In", "Sale"), product_collections.
- product_images: product_id, optional colour, url, sort order, alt text.
- variants: id, product_id, size, colour, sku (unique), barcode (optional), price (nullable = use
  base price), sale_price + sale_start + sale_end (optional), stock_on_hand, low_stock_threshold
  (default 3), active.
- inventory_movements (ledger, never edited or deleted): variant_id, change (+/-), reason
  (online_sale, pos_sale, restock, adjustment, return, cancellation, reservation_release),
  reference (order id), staff_id, note, created_at. stock_on_hand must always equal the sum of
  movements; add a check/report that proves it.
- customers: name, email, phone, addresses (no passwords needed for customers in v1; guest checkout).
- orders: id, order_number (human friendly, e.g. B-1001), channel (online/pos), status, customer info,
  delivery method + address, subtotal, discount_total, delivery_fee, total, payment_method
  (wipay/cash/card_terminal/bank_transfer), payment_status, payment_reference, notes, staff_id (POS),
  created_at.
- order_items: order_id, variant_id, product name/size/colour/sku SNAPSHOT, unit_price, quantity,
  line_total.
- order_status_history: order_id, from, to, staff_id, note, created_at.
- discount_codes: code (case-insensitive, unique), type (percent/fixed/free_delivery), value,
  min_spend, start/end dates, total usage limit, per-customer limit, applies_to (all / categories /
  products), active, times_used.
- staff_profiles: user_id, name, role (owner / staff).
- pos_shifts: staff_id, opened_at, opening_cash, closed_at, counted_cash, expected_cash, difference.
- audit_log: who did what to which record and when (price changes, stock adjustments, refunds,
  discount changes, role changes).
- settings: store info, delivery fees, low-stock defaults, alert email.

NON-NEGOTIABLE RULES
1. Stock can never go below zero and two people can never buy the last item. Do every stock change
   inside ONE Postgres function (called via RPC) that locks the variant rows (SELECT ... FOR UPDATE),
   checks stock, writes the movement and updates stock_on_hand in a single transaction.
2. Never trust prices, discounts or totals from the browser. The server recalculates everything from
   the database at checkout and at payment confirmation.
3. Online checkout reserves stock for 20 minutes while the customer pays. If payment does not
   complete, release it automatically (cron + on next read). Paid orders convert the reservation
   into a sale. Cancelled/refunded orders return stock through the ledger.
4. An order becomes "paid" ONLY after the server verifies the payment with WiPay (signed callback or
   server-to-server status check, per WiPay's docs). Payment callbacks must be idempotent (the same
   callback twice must not double anything). Log every callback.
5. The Supabase service-role key and WiPay secrets live only in server environment variables. Never
   in client code, never committed. Add .env.example with placeholder names only.
6. RLS: the public can read active products/variants/images only. Customers never read other orders.
   Staff can use POS and view/update orders but cannot change prices, discounts, settings or staff.
   Owner can do everything. Test these rules.
7. Rate-limit checkout, discount-code checks and login. Validate all inputs with Zod.
8. Mobile first. Admin and POS must work well on a tablet and a phone.
9. Don't guess APIs. Read the current docs for Next.js, Supabase, Resend and WiPay before using them.
   If WiPay's docs are missing or unclear, STOP and tell me what you need instead of inventing it.

PHASE 1: SETUP (CHECKPOINT after)
- Scaffold the project, Tailwind theme from the demo's colours/fonts, Supabase migrations for the
  whole data model, RLS policies, seed data (2 categories, 6 products with sizes and colours,
  realistic stock, 1 owner + 1 staff test user).
- Write the stock RPC functions first (reserve, release, sell, restock, adjust, return) with unit
  tests, including a concurrency test: 10 parallel purchases of a variant with stock 1 → exactly 1
  succeeds.
- README with how to run locally.

PHASE 2: ONLINE STORE (CHECKPOINT after)
- Pages: home (from the demo design), shop with filters (category, size, colour, price, in stock,
  on sale) and sort, product page (image gallery per colour, size/colour picker that shows only
  available combinations, "Only 2 left", "Sold out", size guide), cart (drawer + page), checkout,
  order confirmation, order lookup (order number + email), contact, about, policies (returns,
  delivery, privacy, terms — draft text for the owner to approve).
- Sale prices show the old price crossed out. Discount code box in the cart/checkout.
- Checkout: contact details, delivery or pickup, delivery fee, discount, total, then WiPay.
- Emails: order confirmation, status updates (packed, out for delivery, ready for pickup, completed,
  cancelled), with the store branding.
- SEO basics (titles, descriptions, Open Graph images, sitemap, robots), fast images, accessible
  forms. WhatsApp chat button.

PHASE 3: WIPAY PAYMENTS (CHECKPOINT after)
- Read WiPay's current developer docs. Implement their hosted checkout / payment request flow for TTD
  in SANDBOX mode first.
- Return page + callback/webhook handler that verifies the payment (signature/hash or status API as
  their docs require), marks the order paid exactly once, converts the reservation, sends the email.
- Failed / cancelled / abandoned payments release stock. Show the customer a clear message and a
  "try again" button.
- Admin can mark an order as paid by bank transfer manually (owner only, audit logged).
- Give me a test plan with WiPay sandbox cards and run it.

PHASE 4: ADMIN DASHBOARD (CHECKPOINT after)
- /admin, staff login, role-based menu.
- Dashboard home: today's / this week's / this month's sales (online vs in-store), orders waiting to
  be packed, low-stock list, best sellers.
- Products: list with search and filters; create/edit with images (upload, reorder, assign to
  colour), variant matrix (pick sizes × colours → generates variants with auto SKUs like
  CAT-PRODUCT-COLOUR-SIZE, editable), per-variant price/sale price/stock/threshold/barcode,
  duplicate product, archive. Bulk edit stock and prices.
- CSV import/export of products and variants (with a downloadable template and a dry-run preview
  that shows errors before importing).
- Inventory: stock per variant, restock (receive new stock), adjustments with a required reason,
  full movement history per variant, stock value report.
- Low-stock alerts: badge in the dashboard, instant email when a variant drops to or below its
  threshold (once, not on every sale), and a daily 8am digest (Vercel Cron).
- Orders: list with filters (status, channel, date, payment), order detail, change status (with
  history), cancel (returns stock), refund (full or per item, returns stock unless marked damaged),
  print packing slip, customer contact buttons (WhatsApp/email).
- Discounts: create/edit codes with all the rules in the data model, see usage; sale prices by
  product, category or collection with start/end dates.
- Reports (date range picker, compare to previous period, CSV export): sales by day/week/month,
  online vs in-store, best and worst sellers, sales by category, sales by size/colour, discount
  usage, average order value, stock value, dead stock (no sales in 60 days).
- Settings (owner only): store info, delivery fees, alert email, staff accounts and roles.

PHASE 5: IN-STORE POS (CHECKPOINT after)
- /pos, installable as a PWA on a tablet or phone, big touch-friendly buttons.
- Open shift (opening cash) → sell → close shift (count cash, show expected vs counted).
- Add items by search, tapping a product grid, or barcode scan (camera, and USB/Bluetooth scanners
  that type like a keyboard). Choose size/colour, quantity, see live stock.
- Apply a discount code or a manual discount (staff manual discounts capped at [10]% unless the
  owner approves with a PIN).
- Payment: cash (with change calculator), card (recorded; the customer pays on the bank card
  machine), bank transfer, or split payment.
- Every sale uses the same stock RPC, so the website updates instantly.
- Receipt: printable (58/80 mm thermal printer friendly) and send by WhatsApp link or email.
- Returns/exchanges from a past receipt.
- If the internet drops, show a clear "Offline — sales paused" banner. Do not take offline sales in
  v1 (prevents overselling).
- End-of-day summary: sales by payment method, items sold, cash expected.

PHASE 6: TESTING, SECURITY & LAUNCH (CHECKPOINT after)
- Playwright tests for: browse → add to cart → discount → checkout → sandbox payment → paid → stock
  reduced; POS sale reduces online stock; last-item race; cancel/refund returns stock; staff cannot
  reach owner pages; RLS blocks reading other customers' orders.
- Run a security review: secrets, RLS, input validation, rate limits, admin route protection,
  webhook verification, dependency audit. Fix what you find.
- Lighthouse on home, shop and product pages on mobile; aim for 90+ performance and accessibility.
- Backups: confirm Supabase backups for the plan we're on and add a weekly CSV export of products,
  stock and orders emailed to the owner.
- Deploy to Vercel, connect the domain, switch WiPay to live only when I say so.
- Write OWNER_GUIDE.md in plain English (how to add a product, restock, handle an order, create a
  discount, use the POS, close a shift, read reports) and HANDOVER.md for me (env vars, accounts,
  how to deploy, how to restore a backup).

HOW TO WORK
- Before Phase 1, show me a short plan and any questions. Then go.
- Commit after every working step with clear messages. Never commit secrets.
- At each CHECKPOINT: run lint, type check and tests; start the app; take screenshots of the new
  pages on mobile and desktop; give me a short summary and what I should click to test it.
- If something needs a decision or an account I haven't set up, stop and ask.
```

---

## Tips while building

- **Effort:** on the Pro plan, use **high** for Phases 1, 3 and 6 (stock, payments, security) and
  **medium** for the rest.
- If it gets stuck or the chat gets long, start a new session and say: *"Read the README and git log,
  we're on Phase X, continue."*
- After each phase, show the client screenshots. It keeps them confident about paying the next
  milestone.
- **Don't switch WiPay to live** until you've placed real test orders, refunded them, and checked the
  stock went back.
