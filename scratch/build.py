#!/usr/bin/env python3
"""Generates the static Spaciodual.us clone (HTML files) from content
scraped into scratch/content/. Run from anywhere; writes into the project
root (one level above this script's folder). Pure stdlib.

Usage: python3 scratch/build.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BRAND_NAME = "Spaciodual.us"

NAV_LABELS = {
    "en": dict(home="Home", services="Services & Offerings", practitioners="About",
               resources="Contact", book="Book a Session", mentorship="Mentorship (coming soon)",
               back="← Back to Offerings"),
    "es": dict(home="Inicio", services="Servicios y Ofrendas", practitioners="Nosotros",
               resources="Contacto", book="Reservar una Sesión", mentorship="Mentoría (próximamente)",
               back="← Volver a Servicios"),
}

HOME_DISCOVER_ES = [
    dict(eyebrow="Descubre", title="Spacio Dual", slug="spacio-dual", photo="earth-hands.png", icon="akashic.png",
         text=[
             "Spacio Dual es donde dos dimensiones convergen: la luz y la sombra, el cuerpo y el alma, lo consciente y lo inconsciente. Es un contenedor sagrado donde exploramos la dualidad inherente al ser humano — no para resolverla, sino para habitarla con consciencia y amor.",
             "Aquí no hay un camino prescrito. El proceso es orgánico, único para cada ser. Patria acompaña desde la escucha profunda y sin juicio, creando un espacio donde todo lo que eres tiene cabida: tus sombras, tus luces, tus contradicciones, tu grandeza.",
         ],
         link="book.html", link_text="Reserva tu Sesión"),
    dict(eyebrow="Descubre", title="Coaching de Vida", slug="coaching-de-vida", photo="buddha-monk.png", icon="5.png",
         text=[
             "Una conversación transformadora que te ayuda a ver con claridad lo que antes estaba nublado. No se trata de dar respuestas — se trata de hacer las preguntas correctas para que tú mismo descubras las tuyas.",
             "Te acompañamos a identificar patrones de comportamiento, diseñar metas con intención y construir el puente entre quién eres hoy y quién deseas ser. Sin guiones. Sin fórmulas. Solo presencia.",
         ],
         link="secciones/coaching-de-vida.html", link_text="Más Sobre Coaching"),
    dict(eyebrow="Descubre", title="Consejería Espiritual", slug="consejeria-espiritual", photo="F6DCE70D-CDC3-4C22-9138-2731A98D4A72.jpeg", icon="8.png",
         text="Conocerte, responsabilizarte y amarte, es identificarte con él todo y asumir tu conciencia de amor. Es estar dispuesto a trabajar aquellas partes de ti que no quieres reconocer. Allí donde hay resistencia y oscuridad es donde nace la luz que te hace ser.",
         link="secciones/consejeria-espiritual.html", link_text="Más Sobre Consejería"),
    dict(eyebrow="Descubre", title="Reiki y Energía", slug="reiki-energia", photo="reiki-energy-woman.png", icon="4.png",
         text="Tu cuerpo sabe cómo sanarse, solo tienes que ayudarlo a recordar, creando las condiciones necesarias para hacerlo realidad. Como práctica holística, el Reiki accede y activa los sistemas de energía sutil del cuerpo — chakras, cuerpo etérico — eliminando bloqueos y fomentando una alineación poderosa.",
         link="secciones/reiki-energia.html", link_text="Más sobre el Reiki"),
    dict(eyebrow="Descubre", title="Meditación", slug="meditacion", photo="beach-meditation.png", icon="15.png",
         text="La meditación es el silencio que te habita, que te conecta con tu esencia y te habla con amor. Es en esa quietud que logramos restaurar y transformar estructuras físicas de nuestro cerebro y activar mecanismos de sanación. En ese espacio aprendemos a ser selectivos con nuestra energía y atención. Dejamos de buscar respuestas en el exterior comprendiendo que todo está dentro de nosotros mismos.",
         link="secciones/meditacion.html", link_text="Más Sobre Meditación"),
    dict(eyebrow="Descubre", title="Hábitos", slug="habitos", photo="food-bowl.png", icon="4.png",
         img_style="object-position: left center;",
         text="Se dice que somos seres de hábitos, sin embargo, nunca nos detenemos a observar que hay detrás de esa rutina, de ese consumo desmedido, de esa conformidad y cansancio. Cuando sabes el por qué, cuando puedes identificar a qué respondes, comienzas a transformarte con un enfoque de amor propio y disciplina.",
         link="secciones/habitos.html", link_text="Más Sobre Hábitos"),
]

SECTION_PAGES = {
    "coaching-de-vida": dict(
        title="Coaching de Vida", hero="buddha-monk.png",
        tagline="Una conversación transformadora que te ayuda a ver con claridad lo que antes estaba nublado.",
        body=[
            "No se trata de dar respuestas — se trata de hacer las preguntas correctas para que tú mismo descubras las tuyas. Te acompañamos a identificar patrones de comportamiento, diseñar metas con intención y construir el puente entre quién eres hoy y quién deseas ser.",
            "Sin guiones. Sin fórmulas. Solo presencia. Cada sesión parte de tu realidad concreta — tus relaciones, tu trabajo, tus decisiones pendientes — y te ofrece un espacio estructurado para pensar con claridad y actuar con intención.",
        ],
        benefits=[
            "Mayor claridad sobre tus objetivos personales y profesionales.",
            "Herramientas prácticas para sostener el cambio en el tiempo.",
            "Un espacio de escucha sin juicio, a tu propio ritmo.",
            "Metas diseñadas con intención, no por inercia.",
        ],
    ),
    "consejeria-espiritual": dict(
        title="Consejería Espiritual", hero="F6DCE70D-CDC3-4C22-9138-2731A98D4A72.jpeg",
        tagline="Conocerte, responsabilizarte y amarte, es identificarte con él todo y asumir tu conciencia de amor.",
        body=[
            "Es estar dispuesto a trabajar aquellas partes de ti que no quieres reconocer. Allí donde hay resistencia y oscuridad es donde nace la luz que te hace ser.",
            "La consejería espiritual no busca imponer un camino ni una creencia — es un acompañamiento honesto que te ayuda a reconectar con tu propia brújula interior, especialmente en los momentos donde sientes que has perdido el rumbo.",
        ],
        benefits=[
            "Un espacio confidencial y libre de juicio para explorar lo que sientes.",
            "Herramientas para procesar la sombra sin evitarla.",
            "Mayor conexión con tu propósito y tu voz interior.",
            "Acompañamiento adaptado a tu proceso, no a un guion fijo.",
        ],
    ),
    "reiki-energia": dict(
        title="Reiki y Energía", hero="reiki-energy-woman.png",
        tagline="Tu cuerpo sabe cómo sanarse, solo tienes que ayudarlo a recordar.",
        body=[
            "Como práctica holística, el Reiki accede y activa los sistemas de energía sutil del cuerpo — chakras, cuerpo etérico — eliminando bloqueos y fomentando una alineación poderosa.",
            "Cada sesión crea las condiciones necesarias para que tu propio cuerpo recuerde su capacidad innata de sanar: un espacio de quietud, contacto consciente e intención enfocada en restaurar el flujo natural de tu energía.",
        ],
        benefits=[
            "Liberación de bloqueos energéticos acumulados.",
            "Mayor sensación de calma y equilibrio interior.",
            "Apoyo complementario a otros procesos de sanación.",
            "Reconexión con la capacidad natural del cuerpo de sanarse.",
        ],
    ),
    "meditacion": dict(
        title="Meditación", hero="beach-meditation.png",
        tagline="La meditación es el silencio que te habita, que te conecta con tu esencia y te habla con amor.",
        body=[
            "Es en esa quietud que logramos restaurar y transformar estructuras físicas de nuestro cerebro y activar mecanismos de sanación. En ese espacio aprendemos a ser selectivos con nuestra energía y atención.",
            "Dejamos de buscar respuestas en el exterior comprendiendo que todo está dentro de nosotros mismos. Practicar de forma guiada te ofrece un punto de apoyo real para sostener la práctica más allá de la sesión.",
        ],
        benefits=[
            "Reducción del estrés y la ansiedad en el día a día.",
            "Mayor claridad mental y capacidad de atención.",
            "Herramientas para regresar a la calma en cualquier momento.",
            "Una práctica sostenible que puedes llevar a tu vida diaria.",
        ],
    ),
    "habitos": dict(
        title="Hábitos", hero="food-bowl.png", hero_align="right",
        tagline="Se dice que somos seres de hábitos, sin embargo, nunca nos detenemos a observar qué hay detrás de esa rutina.",
        body=[
            "De ese consumo desmedido, de esa conformidad y cansancio. Cuando sabes el por qué, cuando puedes identificar a qué respondes, comienzas a transformarte con un enfoque de amor propio y disciplina.",
            "Trabajamos juntos para identificar los hábitos que ya no te sirven y diseñar, paso a paso, nuevas rutinas alineadas con quién quieres ser — sin exigencia ni perfeccionismo, con constancia y compasión.",
        ],
        benefits=[
            "Mayor conciencia sobre los patrones que te limitan.",
            "Estrategias prácticas para construir hábitos sostenibles.",
            "Un enfoque de disciplina desde el amor propio, no la exigencia.",
            "Acompañamiento personalizado a tu ritmo de cambio.",
        ],
    ),
}

SECTION_DIVIDER = (
    '<div class="section-divider" aria-hidden="true">'
    '<span class="divider-line"></span>'
    '<span class="divider-triangle"></span>'
    '<span class="divider-line"></span>'
    '</div>'
)

SVG_ICONS = {
    "facebook": '<svg viewBox="0 0 24 24"><path d="M13 22v-9h3l1-4h-4V6.5C13 5.4 13.6 5 14.7 5H17V1.2C16.6 1.1 15.3 1 13.9 1 11 1 9 2.8 9 6v3H6v4h3v9h4z"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="12" cy="12" r="4.5"/><circle cx="17.3" cy="6.7" r="1"/></svg>',
    "cart": '<svg viewBox="0 0 24 24"><circle cx="9" cy="21" r="1.3"/><circle cx="18" cy="21" r="1.3"/><path d="M2 3h3l2.4 12.2A2 2 0 0 0 9.4 17H18a2 2 0 0 0 2-1.6L21.5 8H6"/></svg>',
    "menu": '<svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"/></svg>',
}


def esc(s):
    return s


def rel(depth, path):
    return ("../" * depth) + path


def render_header(depth=0, solid=False, active="", lang="en"):
    prefix = rel(depth, "")
    nav = NAV_LABELS[lang]
    solid_class = " is-solid" if solid else ""
    always_solid = ' data-always-solid="true"' if solid else ""
    return f"""  <header class="site-header{solid_class}"{always_solid}>
    <div class="header-inner">
      <a href="{prefix}book.html" class="logo-text">{nav['book']}</a>
      <div class="header-icons">
        <a href="#" class="icon-link" aria-label="Facebook" target="_blank" rel="noopener">{SVG_ICONS['facebook']}</a>
        <a href="#" class="icon-link" aria-label="Instagram" target="_blank" rel="noopener">{SVG_ICONS['instagram']}</a>
        <a href="{prefix}book.html" class="icon-link" aria-label="Cart">{SVG_ICONS['cart']}</a>
      </div>
    </div>
  </header>"""


def render_footer(depth=0, lang="en"):
    prefix = rel(depth, "")
    nav = NAV_LABELS[lang]
    return f"""  <footer class="site-footer">
    <div class="container">
      <a href="{prefix}index.html" class="logo-text">{BRAND_NAME}</a>
      <nav class="footer-nav">
        <a href="{prefix}index.html">{nav['home']}</a>
        <a href="{prefix}index.html#spacio-dual">{nav['services']}</a>
        <a href="{prefix}nosotros.html">{nav['practitioners']}</a>
        <a href="{prefix}contacto.html">{nav['resources']}</a>
        <a href="{prefix}book.html">{nav['book']}</a>
      </nav>
      <div class="footer-social">
        <a href="#" aria-label="Facebook" target="_blank" rel="noopener">{SVG_ICONS['facebook']}</a>
        <a href="#" aria-label="Instagram" target="_blank" rel="noopener">{SVG_ICONS['instagram']}</a>
      </div>
    </div>
  </footer>"""


def page_shell(title, description, depth, body_html, extra_head="", solid_header=False, lang="en"):
    prefix = rel(depth, "")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="stylesheet" href="{prefix}css/style.css">
{extra_head}</head>
<body>
{render_header(depth, solid=solid_header, lang=lang)}
<main>
{body_html}
</main>
{render_footer(depth, lang=lang)}
<script src="{prefix}js/main.js"></script>
</body>
</html>
"""


def img(depth, name, alt="", cls="", style=""):
    prefix = rel(depth, "")
    cls_attr = f' class="{cls}"' if cls else ""
    style_attr = f' style="{style}"' if style else ""
    return f'<img src="{prefix}images/{name}" alt="{alt}"{cls_attr}{style_attr} loading="lazy">'


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
def build_home():
    depth = 0
    lang = "es"
    rows_data = HOME_DISCOVER_ES
    discover_rows = []
    for i, d in enumerate(rows_data):
        reverse = " reverse" if i % 2 == 1 else ""
        paragraphs = d['text'] if isinstance(d['text'], list) else [d['text']]
        text_html = "\n          ".join(f"<p>{p}</p>" for p in paragraphs)
        id_attr = f' id="{d["slug"]}"' if d.get("slug") else ""
        discover_rows.append(f"""      <div class="discover-row{reverse}"{id_attr}>
        <div class="discover-media">{img(depth, d['photo'], d['title'], style=d.get('img_style', ''))}</div>
        <div class="discover-text">
          <span class="eyebrow">{d['eyebrow']}</span>
          <h2>{d['title']}</h2>
          {text_html}
          <a href="{d['link']}" class="btn">{d['link_text']}</a>
        </div>
      </div>""")
    discover_html = "\n".join(discover_rows)

    body = f"""  <section class="hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <div class="hero-sub">para tu</div>
      <h1>Spacio Dual</h1>
    </div>
  </section>

  <section class="section-white intro-section">
    <div class="intro-bg" aria-hidden="true"></div>
    <div class="container intro-block">
      <h2 class="script-heading">&ldquo;No os conforméis a este siglo, sino transformaos por medio de la renovación de<br>vuestras mentes&rdquo;</h2>
      <p class="scripture-ref">— Romanos 12:2</p>
      <p class="intro-caption">Comienza tu viaje trascendental hacia una nueva conciencia de ser, estar y sentir. Dentro de un espacio seguro, íntegro y auténtico con diversas modalidades holísticas y energéticas que te ayudarán a restaurar el balance natural de tu esencia y presencia divina.</p>
      <a href="book.html" class="btn">Comienza tu Viaje</a>
    </div>
  </section>
  {SECTION_DIVIDER}

  <section class="section-white section-tight">
    <div class="container">
{discover_html}
    </div>
  </section>
  {SECTION_DIVIDER}

  <section class="section-dark text-center footer-lead">
    <div class="container">
      <h2>¿Todo listo para comenzar?</h2>
      <p>Reserva una sesión con nuestras practicantes y comienza el camino de regreso a ti mismo.</p>
      <a href="book.html" class="btn">Reservar una Sesión</a>
    </div>
  </section>"""
    title = BRAND_NAME
    description = f"Clon visual no oficial de {BRAND_NAME} — un santuario metafísico y esotérico de sanación en St. Thomas, Islas Vírgenes de EE. UU."

    html = page_shell(title, description, depth, body, solid_header=False, lang=lang)
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# HOME PAGE SECTION DETAIL PAGES (Coaching, Consejería, Reiki, Meditación, Hábitos)
# ---------------------------------------------------------------------------
def build_section_page(slug, data):
    depth = 1
    body_paras = "\n".join(f"      <p>{p}</p>" for p in data["body"])
    benefits_items = "\n".join(f"        <li>{b}</li>" for b in data["benefits"])
    hero_align_class = " hero-align-right" if data.get("hero_align") == "right" else ""

    body = f"""  <section class="hero page-hero{hero_align_class}" style="background-image:url('{rel(depth,'')}images/{data['hero']}')">
    <div class="hero-content">
      <a href="{rel(depth,'')}index.html#{slug}" class="back-link">&larr; Volver a Spaciodual.us</a>
      <h1>{data['title']}</h1>
      <p class="hero-sub" style="font-size:1.1rem">{data['tagline']}</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container" style="max-width:760px">
{body_paras}
      <h3 style="margin-top:40px">Beneficios</h3>
      <ul class="benefits-list">
{benefits_items}
      </ul>
      <div class="text-center mt-40">
        <a href="{rel(depth,'')}book.html" class="btn">Reserva tu Sesión</a>
      </div>
    </div>
  </section>"""

    html = page_shell(
        f"{data['title']} | {BRAND_NAME}",
        data["tagline"],
        depth, body, solid_header=True, lang="es",
    )
    out_dir = ROOT / "secciones"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# ABOUT PAGE (Nosotros)
# ---------------------------------------------------------------------------
def build_about():
    depth = 0

    body = f"""  <section class="hero page-hero" style="background-image:url('images/earth-hands.png')">
    <div class="hero-content">
      <h1>Nosotros</h1>
      <p class="hero-sub" style="font-size:1.1rem">La historia detrás de {BRAND_NAME}</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container" style="max-width:760px">
      <p>{BRAND_NAME} es donde dos dimensiones convergen: la luz y la sombra, el cuerpo y el alma, lo consciente y lo inconsciente. Es un contenedor sagrado donde exploramos la dualidad inherente al ser humano — no para resolverla, sino para habitarla con consciencia y amor.</p>
      <p>Aquí no hay un camino prescrito. El proceso es orgánico, único para cada ser. Patria acompaña desde la escucha profunda y sin juicio, creando un espacio donde todo lo que eres tiene cabida: tus sombras, tus luces, tus contradicciones, tu grandeza.</p>
      <p>Comienza tu viaje trascendental hacia una nueva conciencia de ser, estar y sentir. Dentro de un espacio seguro, íntegro y auténtico, ofrecemos diversas modalidades holísticas y energéticas que te ayudarán a restaurar el balance natural de tu esencia y presencia divina.</p>
      <div class="text-center mt-40">
        <a href="book.html" class="btn">Reserva tu Sesión</a>
      </div>
    </div>
  </section>"""

    html = page_shell(
        BRAND_NAME,
        f"Conoce la historia y la filosofía detrás de {BRAND_NAME}.",
        depth, body, solid_header=True, lang="es",
    )
    (ROOT / "nosotros.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# CONTACT PAGE (Contacto)
# ---------------------------------------------------------------------------
def build_contact():
    depth = 0

    body = f"""  <section class="hero page-hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <h1>Contacto</h1>
      <p class="hero-sub" style="font-size:1.1rem">Escríbenos, con gusto te respondemos</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container text-center">
      <div class="notice-badge">Este es un formulario de demostración. No se envía a ningún lado — conecta aquí tu correo, teléfono o dirección reales.</div>
      <form class="form-mock">
        <div class="form-row">
          <label for="name">Nombre completo</label>
          <input id="name" type="text" placeholder="Tu nombre">
        </div>
        <div class="form-row">
          <label for="email">Correo electrónico</label>
          <input id="email" type="email" placeholder="tucorreo@ejemplo.com">
        </div>
        <div class="form-row">
          <label for="phone">Teléfono (opcional)</label>
          <input id="phone" type="tel" placeholder="Tu número de teléfono">
        </div>
        <div class="form-row">
          <label for="message">Mensaje</label>
          <textarea id="message" placeholder="Cuéntanos en qué podemos ayudarte..."></textarea>
        </div>
        <button type="submit" class="btn">Enviar Mensaje</button>
        <p class="form-mock-note small-note" style="display:none; margin-top:16px;"></p>
      </form>
    </div>
  </section>"""

    html = page_shell(
        BRAND_NAME,
        f"Ponte en contacto con {BRAND_NAME}.",
        depth, body, solid_header=True, lang="es",
    )
    (ROOT / "contacto.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# BOOK / STATIC MOCKUP PAGE
# ---------------------------------------------------------------------------
def build_book():
    depth = 0
    all_sections = list(SECTION_PAGES.values())
    offering_options = "\n".join(f'          <option>{d["title"]}</option>' for d in all_sections)
    time_slots = ["9:00 AM", "10:30 AM", "12:00 PM", "2:00 PM", "3:30 PM", "5:00 PM"]
    time_slot_buttons = "\n".join(
        f'          <button type="button" class="time-slot">{t}</button>' for t in time_slots
    )

    body = f"""  <section class="hero page-hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <h1>Reserva tu Sesión</h1>
      <p class="hero-sub" style="font-size:1.1rem">Dos pasos: pago y luego selección de fecha y hora</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container text-center">
      <div class="notice-badge">Esta es una demostración estática. No se procesa ningún pago ni se agenda ninguna sesión real todavía — el pago y el calendario se conectarán más adelante.</div>

      <div class="checkout-steps" aria-hidden="true">
        <div class="checkout-step-indicator is-active" data-step-indicator="1"><span>1</span>Pago</div>
        <div class="checkout-step-line"></div>
        <div class="checkout-step-indicator" data-step-indicator="2"><span>2</span>Fecha y Hora</div>
      </div>

      <form class="form-mock checkout-form">
        <div class="checkout-panel is-active" data-step="1">
          <div class="form-row">
            <label for="offering">Tipo de Sesión</label>
            <select id="offering">
{offering_options}
            </select>
          </div>
          <div class="form-row">
            <label for="name">Nombre en la Tarjeta</label>
            <input id="name" type="text" placeholder="Tu nombre completo">
          </div>
          <div class="form-row">
            <label for="email">Correo Electrónico</label>
            <input id="email" type="email" placeholder="tucorreo@ejemplo.com">
          </div>
          <div class="form-row">
            <label for="card">Número de Tarjeta</label>
            <input id="card" type="text" inputmode="numeric" placeholder="0000 0000 0000 0000">
          </div>
          <div class="form-row-split">
            <div class="form-row">
              <label for="expiry">Vencimiento</label>
              <input id="expiry" type="text" placeholder="MM/AA">
            </div>
            <div class="form-row">
              <label for="cvv">CVV</label>
              <input id="cvv" type="text" inputmode="numeric" placeholder="123">
            </div>
          </div>
          <button type="button" class="btn checkout-next">Continuar a Fecha y Hora</button>
        </div>

        <div class="checkout-panel" data-step="2">
          <div class="form-row">
            <label for="date">Selecciona una Fecha</label>
            <input id="date" type="date">
          </div>
          <div class="form-row">
            <label>Selecciona una Hora</label>
            <div class="time-slot-grid">
{time_slot_buttons}
            </div>
          </div>
          <button type="button" class="btn checkout-back btn-outline-dark">&larr; Volver a Pago</button>
          <button type="submit" class="btn">Confirmar Reserva</button>
        </div>

        <p class="form-mock-note small-note" style="display:none; margin-top:16px;"></p>
      </form>
    </div>
  </section>"""

    html = page_shell(
        f"Reserva tu Sesión | {BRAND_NAME}",
        "Reserva tu sesión: pago y selección de fecha y hora.",
        depth, body, solid_header=True, lang="es",
    )
    (ROOT / "book.html").write_text(html, encoding="utf-8")


def main():
    build_home()
    for slug, data in SECTION_PAGES.items():
        build_section_page(slug, data)
    build_about()
    build_contact()
    build_book()
    print("Build complete.")


if __name__ == "__main__":
    main()
