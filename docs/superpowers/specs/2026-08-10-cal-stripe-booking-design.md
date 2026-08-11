# Booking + Payment Integration (Cal.com + Stripe)

## Context

Spaciodual.us is a static site hosted on GitHub Pages (no server-side code —
`serve.py` is a local dev file server only). The 5 service pages (all under
`secciones/`: Coaching de Vida, Consejería Espiritual, Reiki y Energía,
Meditación, Hábitos) each end with a "Reserva tu Sesión" button. Today that
button links to `book.html`, a fully static mock: a 2-step form that
collects fake payment details (name, card number, expiry, CVV) and then a
fake date/time picker. Nothing is actually processed or booked.

(The `offerings/` directory and its 12 pages, plus the `apothecary.html`
product-shop page mentioned below, were removed in a later cleanup pass —
the "excluded from scope" note about it is kept for historical context in
case product checkout is reintroduced later.)

The goal is to replace this mock with a real, working booking + payment
flow, without adding any custom backend, since the site stays on GitHub
Pages.

## Decisions

- **No custom backend.** Use hosted third-party tools directly from the
  static site: Cal.com for scheduling, Stripe (via Cal.com's built-in
  Stripe app) for payment.
- **Scheduler: Cal.com.** Free tier, embeddable, connects to a real
  calendar, has a native Stripe payment app.
- **Combined flow.** Payment is collected as part of confirming a booking
  slot in Cal.com (via its Stripe app), not as a separate step. This
  replaces both the fake card form and the fake date/time picker in one
  motion.
- **Scope: sessions only.** There is no product-shop page currently on the
  site (the earlier `offerings/apothecary.html` was removed in cleanup).
  If a product shop is reintroduced later, it should get its own checkout
  flow, not the calendar-booking flow described here.
- **One shared Cal.com Event Type** for all 5 services: 60 minutes, $90.
  Services don't have individually different pricing/duration at this
  time.
- **Which service was requested is captured via a required custom
  question** on the Cal.com event type ("Servicio solicitado"), since all
  5 services share one event type. Service-specific entry points
  pre-fill this field; the generic entry point (`book.html`) leaves it for
  the customer to choose from a dropdown inside Cal.com's own form.
- **Widget presentation:**
  - The 5 service pages: clicking "Reserva tu Sesión" opens Cal.com's
    scheduler as a **popup modal** (via Cal.com's official embed script),
    staying on the page, with "Servicio solicitado" pre-filled to that
    page's service name.
  - `book.html`: keeps its own page, header "Reservar una Sesión" link and
    the cart icon still route here. The fake 2-step form is replaced with
    an **inline embedded Cal.com widget** for the same shared event type.
    No card fields are collected on our own page — Stripe payment happens
    inside the Cal.com/Stripe flow, never touching our code. This also
    avoids ever handling raw card data ourselves.

## Manual setup (user-performed, not code)

Before any of this can go live, the user will, outside of this codebase:

1. Create a free Cal.com account, connect a real calendar (Google/Outlook/
   iCloud).
2. Install Cal.com's Stripe app and connect their existing Stripe account.
3. Create one Event Type (e.g. "Sesión de 60 min", 60 min, $90, payment
   required via the Stripe app).
4. Add a required custom booking question "Servicio solicitado" (dropdown
   or short text) listing the 5 service names.
5. Provide the Cal.com username and event type slug (e.g.
   `spaciodual/sesion-60-min`) for the config values below.

## Code changes

**`js/main.js`** — add a small config block at the top:
```js
var CAL_USERNAME = null;   // e.g. "spaciodual"
var CAL_EVENT_SLUG = null; // e.g. "sesion-60-min"
```
Add logic to:
- Load Cal.com's official embed script and initialize it only when both
  config values are set.
- Wire up `data-cal-link`/popup trigger behavior on service-page booking
  buttons, passing the service name as a pre-filled value for "Servicio
  solicitado".
- Render the inline embed on `book.html` when configured.
- When `CAL_USERNAME`/`CAL_EVENT_SLUG` are `null`, every booking
  entry point shows a "coming soon" message using the site's existing
  `notice-badge` styling instead of attempting to load a broken embed.

**5 service pages** (`secciones/*.html`) — the `Reserva tu Sesión` button's
`href="../book.html"` is replaced with a popup trigger (button + data
attributes consumed by the `main.js` logic above), carrying that page's
service name.

**`book.html`** — the mock 2-step form (`.checkout-form`, both
`.checkout-panel` steps, the card-detail fields) is removed and replaced
with a container for the inline Cal.com embed. The existing
`notice-badge` "static demo" copy is replaced with the "coming soon"
placeholder copy (pre-configuration) or removed once real values are set.

**Unaffected:** header/cart icon links (still point to `book.html`), all
other pages' content.

## Rollout & testing

1. Implement with config values `null`; verify locally (`serve.py`) that
   all 5 service pages and `book.html` show the placeholder state
   cleanly — no broken embeds, no dead ends.
2. User completes the manual Cal.com/Stripe setup and provides the
   username + event slug.
3. Config values are filled in; verify locally that the popup opens and
   pre-fills correctly from a few different service pages, and that the
   inline widget + dropdown work on `book.html`.
4. Attempt an end-to-end dry-run booking using Stripe test mode (if
   supported by Cal.com's Stripe app) before relying on this for real
   bookings. If test mode isn't available through that app, this gets
   flagged explicitly rather than assumed to work.
5. Commit and push to `sajesanctuary-clone` as with prior changes — live
   on GitHub Pages within a minute or two of pushing.

## Out of scope

- Apothecary / product checkout.
- Per-service pricing or duration (all 5 share one event type for now).
- Any custom backend, serverless functions, or webhook handling.
