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
    "en": dict(home="Home", services="Services & Offerings", practitioners="Practitioners",
               resources="Resources", book="Book a Session", mentorship="Mentorship (coming soon)",
               back="← Back to Offerings"),
    "es": dict(home="Inicio", services="Servicios y Ofrendas", practitioners="Practicantes",
               resources="Recursos", book="Reservar una Sesión", mentorship="Mentoría (próximamente)",
               back="← Volver a Servicios"),
}

FOOTER_FINE = {
    "en": f"St. Thomas, US Virgin Islands &middot; &copy; {BRAND_NAME}. Fan-made clone for educational/demo purposes — not the official site.",
    "es": f"St. Thomas, Islas Vírgenes de EE. UU. &middot; &copy; {BRAND_NAME}. Clon no oficial creado con fines educativos/demostrativos — no es el sitio oficial.",
}

# ---------------------------------------------------------------------------
# Shared nav data
# ---------------------------------------------------------------------------
OFFERING_LINKS = [
    ("Akashic Record Readings", "akashic-record-readings"),
    ("Apothecary", "apothecary"),
    ("Astrology Readings", "astrology-readings"),
    ("Aura Photography", "aura-photography"),
    ("Breathwork", "breathwork"),
    ("Chakra Balancing", "chakra-balancing"),
    ("Dream Interpretation", "dream-interpretation"),
    ("Energetic Signature", "energetic-signature"),
    ("Magdalene Reiki", "magdalene-reiki"),
    ("Reiki Energy Healing", "reiki-energy-healing"),
    ("Sound Alchemy", "sound-alchemy"),
    ("Spirit Guide Conversations", "spirit-guide"),
    ("Tarot & Oracle Readings", "tarot-oracle-readings"),
]

PRACTITIONERS = [
    dict(name="Jet’aime Cherée", img="IMG_778146A87FB8-1.jpeg",
         bio="Jet’aime Cherée is a healer, facilitator, green witch, spiritual entrepreneur and Akashic oracle on the priestess path of remembering and reclaiming the sacred voice of the goddess within.",
         tags=["Akashic Record Readings", "Apothecary", "Sound Alchemy", "Reiki Energy Healing", "Guided Meditation", "Intuitive Guidance", "Magdalene Reiki", "Energetic Signature", "Tarot & Oracle Readings", "Dream Interpretation"]),
    dict(name="Gabrielle Querrard", img="IMG_9408.JPG",
         bio="I am a visionary, a dreamer, and an alchemist. I take ideas and turn them into action, I craft excellence from nothingness, and I weave into union the Divine energies of opportunity and time.",
         tags=["Aura Photography", "Tarot & Oracle Readings", "Reiki Energy Healing", "Dream Interpretation", "Apothecary"]),
    dict(name="Angelica Carby", img="IMG_9403.JPG",
         bio="I have always felt like our lives are like a great river; powerful, beautiful, majestic and who’s destiny it is to connect to an energy greater than itself - The source of all that is.",
         tags=["Reiki Energy Healing", "Intuitive Guidance", "Spirit Guide Conversations"]),
    dict(name="Sakile Braithwaite-Hall", img="IMG_9315.jpg",
         bio="Sakile Braithwaite-Hall is a soul seeker and connector embodying the illumination of light. She is on a journey of encouragement, support and providing visibility and opportunities of connection especially for people of color.",
         tags=["Reiki Energy Healing", "Guided Meditation", "Yoga"]),
    dict(name="Hadiya Sewer", img="IMG_1347.JPG",
         bio="I have a deep love for the Divine Oneness and the sacred journeys that our souls undergo as we traverse life, death, rebirth cycles.",
         tags=["Ouroboros Offerings"]),
    dict(name="Stephanie Smedile", img="IMG_9402.jpg",
         bio="Stephanie Smedile: the nurturing and empowering pattern disrupter. This devoted yogi is passionate about educating Spiritual Psychology and Sister Goddess Activation.",
         tags=["Intuitive Guidance"]),
    dict(name="Lexi O’toole", img="IMG_9318.JPG",
         bio="Coming soon.",
         tags=["Intuitive Guidance"]),
]

RESOURCES = [
    dict(cat="Herbalism", name="Bay Leaf", img="unnamed-9.jpg", blurb="Bay is used for divination and prophecy. It makes the mind receptive and enables the practitioner to understand and interpret as the oracle."),
    dict(cat="Herbalism", name="Elder Berry", img="unnamed-8.jpg", blurb="Wine made of Elderberries is an appropriate ritual cup for ceremonies that honor those who have gone before us and to attune to the transformational powers of the Great Goddess, who presides over life and death."),
    dict(cat="Herbalism", name="Calendula (Marigold)", img="unnamed-7.jpg", blurb="Marigold is known as an herb of immortal life force, which symbolises the undying spirit. This immortal quality is also invoked in many a love charm intended to make love last forever so it shall never wilt."),
    dict(cat="Herbalism", name="Hibiscus", img="unnamed-6.jpg", blurb="Hibiscus flowers are often used in charms for love and lust, but the dried buds have another use: they can be used as a cleansing and strengthening aid, refreshing exhausted minds and tired spirits."),
    dict(cat="Herbalism", name="Peppermint", img="unnamed-5.jpg", blurb="Peppermint can support lucid and vivid dreaming, and some report a prophetic quality to dreams when peppermint is utilized."),
    dict(cat="Herbalism", name="Raspberry Leaf", img="unnamed-4.jpg", blurb="Raspberry is commonly used in love spells and blends. The leaves are carried by pregnant women to relieve pains of pregnancy and childbirth."),
    dict(cat="Herbalism", name="Rosemary", img="unnamed-3.jpg", blurb="When burned, Rosemary emits powerful cleansing and purifying vibrations, it is smoldered to remove negativity - particularly prior to magick practices."),
    dict(cat="Herbalism", name="Chamomile", img="unnamed-2.jpg", blurb="It is an excellent herb for chakra balancing and to help one find one's inner centre. Chamomile may inspire confidence and open the heart to expressing love and compassion."),
    dict(cat="Herbalism", name="Mugwort", img="unnamed-1.jpg", blurb="Mugwort is revered for lucid and prophetic dreams and is one of the most popular herbs for scrying and enhancing psychic skills."),
    dict(cat="Herbalism", name="Rose", img="unnamed.jpg", blurb="Roses used in magick and ceremony are very powerful, even placing a single rose or sprinkling petals upon the altar when casting spells adds an incredible frequency to your rituals."),
    dict(cat="Crystals", name="Pyrite", img="unnamed-4.jpg", blurb="Pyrite comes from the Greek word pyre or pyros which means fire. It resonates with fire energy, symbolizing the warmth and lasting presence of the sun."),
    dict(cat="Crystals", name="Smokey Quartz", img="unnamed-2.jpg", blurb="In the metaphysical world, Smoky Quartz is one of the most efficient crystals for grounding and cleansing and is an extraordinary amulet of protection."),
    dict(cat="Crystals", name="Amethyst", img="unnamed.jpg", blurb="Amethyst is most notably known for its master healing spiritual properties: it heals a soul in discord, awakens spirituality, activates intuition, and provides energetic protection."),
    dict(cat="Crystals", name="Clear Quartz", img="unnamed-1.jpg", blurb="Clear Quartz, also called Ice Crystal, from the Greek word “krystallos” meaning “ice” — ancients believed it to be sacred water frozen so hard it could never thaw."),
    dict(cat="Crystals", name="Selenite", img="unnamed-3.jpg", blurb="Selenite is named after Selene, the Greek Moon Goddess. It is said to hold the feminine powers of the moon and all that the divine feminine can catalyze."),
]

OFFERINGS = {
    "akashic-record-readings": dict(
        title="Akashic Record Readings", hero="AdobeStock_296303487.jpeg",
        tagline="Akasha is Universal life force and the creative mind that is unlimited space unbound by any element in nature.",
        body=[
            "The Akashic Records, or The Soul’s Records, are an etheric library of information that contains knowledge and intelligence about every sentient being in the universe. It contains all the soul’s lifetimes, origins, emotions and past. Your Akashic Record is the divine knowing of the entire experience of your soul.",
            "The Akashic Records are a compendium of consciousness that the mind uses to illustrate the understanding that every thought, word, emotion, experience and intent ever to have occurred exists in the collective consciousness accessible to us all on some level. A reading is a deep remembrance of who you are at soul level and an activation for your path ahead.",
            "Your soul—the essence of who you are—has often traveled through many lifetimes to make you who you are today. By finding out more about your soul’s journey, you can better understand, heal, and thrive in this current life.",
        ],
        faq=[
            ("Is this a Past Life Reading?", "An Akashic Reading can source information from and for pretty much any topic including past lives, cosmic experiences and genetic memories."),
            ("What kind of questions should I ask?", "Set aside some quiet time for self-inquiry and craft 3 specific, focused questions born from a burning desire to know."),
            ("How long is the session?", "Sessions usually run about 2 hours."),
            ("Can I record the session?", "In-person sessions can be recorded by you or your practitioner. Virtual sessions are recorded via Zoom and sent within 24 hours."),
        ],
        cta="Book an Akashic Record Reading",
    ),
    "apothecary": dict(
        title="Apothecary", hero="6E0C505F-CF4F-46CF-94C3-84D1A42CB10E.jpeg",
        tagline="Preserving the wisdom of ancient botany.",
        body=[
            "Traditional and ancient wisdom of our Herbal Apothecary includes advice and recommendations for plant-based formulations to heal your body through the innate intelligence of Mother Earth.",
            "Herbal knowledge that was once common in every household is now a rare commodity. However, we are beginning to remember our ancient practices. Anyone interested in alternative medicine and botanical curatives can utilize plant-based medicines that offer healing possibilities for the body, mind, and spirit.",
            "Plant-based remedies work in a comprehensive way to treat entire bodily systems rather than a single symptom, nourishing and restoring balance so that organs in disharmony can return to optimal function.",
            "Trust the power of nature. Many plants that grow in our particular climate are specific to treating the illnesses of our territory. Our medicine is in our own backyard.",
        ],
        is_store=True,
        cta="Contact our Apothecary Practitioners",
    ),
    "astrology-readings": dict(
        title="Astrology Readings", hero="unsplash-image-yOIT88xWkbg.jpg",
        tagline="An Astrology Reading is a detailed breakdown of who you are according to the cosmos.",
        body=[
            "Your birth chart is a personal roadmap based on the positioning of the sun, moon, stars and planetary alignments. The specific degree the celestial bodies were aligned when you were born — and where they have transited to during your lifetime — gives a detailed account of your purpose, desires, passions, idiosyncrasies, talents and ambitions.",
            "At the exact time of your birth, the planetary alignment tells a story about who you are and who you are destined to become. Your astro chart tells the story of your life – past, present and future – including the significant moments that will help guide you.",
            "Whether you’re at a crossroads in your life and need direction, or are simply curious, your reading will be an enlightening and healing experience.",
        ],
        cta="Book an Astrology Reading",
    ),
    "aura-photography": dict(
        title="Aura Photography", hero="53F3B10C-3766-4FCC-B291-7F6D39F7ECF8.jpeg",
        tagline="An Aura Photography session captures a snapshot of your energetic signature, your human aura in real time.",
        body=[
            "Auras are the energy maps of our souls. The auric field is the vibration or energetic space that surrounds a person or object and can be viewed by the eye as luminous colourful shades.",
            "The human aura is both a colorful energy field and a reflection of the subtle life energies within the body. Auras are an energetic atmosphere that resides around every living thing including human beings, plants, animals, and inanimate objects.",
            "Aura Photography captures the colorful essence of our subtle spirit in real-time by utilizing biofeedback technology via a hand/body sensor measuring device, encompassing a comprehensive session detailing what energies are present in your auric field.",
            "We invite you to explore the magic of your personal auric signature! Visit us at Spaciodual.us to book an Aura Photography session with Gabrielle, our aura photography facilitator!",
        ],
        cta="Book an Aura Photography Session",
    ),
    "breathwork": dict(
        title="Breathwork", hero="unsplash-image-0tTA6cewPr8.jpg",
        tagline="Learn to utilize your breath as a meditative tool to explore your inner divine.",
        body=[
            "Breathwork is a form of meditation that uses accelerated breathing to achieve alternative and elevated states of consciousness. This altered state allows the practitioner to explore their inner realm of consciousness and achieve healing.",
            "We breathe all day, every day, yet most of us don’t pay much attention to our breathing. The goal of breathwork meditation is to disrupt egoic patterning by breathing in a specific way, saturating the cells with oxygen and creating heightened physical, mental and energetic responses.",
            "Breathwork sessions are led by a qualified guide who walks participants through the experience, learning to breathe with the diaphragm and abdominal muscles instead of shallow breathing patterns.",
            "Breathwork is appropriate for anyone and can be done individually or in a group. Experience your breath like never before with a breathwork event at Spaciodual.us!",
        ],
        cta="Book a Breathwork Session",
    ),
    "chakra-balancing": dict(
        title="Chakra Balancing", hero="IMG_9388.JPG",
        tagline="Chakra is the Sanskrit word for wheel. Chakra balancing is based on the ancient Eastern belief in seven energy centers in the physical body.",
        body=[
            "The 7 chakras are the 7 wheels of energy in our body, located at specific points ranging from the feet to the top of the head.",
            "The physical, emotional and spiritual health of your body is dependent on free flowing energy within the body. No chakra works independently of the others — each only works fully when the rest are also fully engaged. As above, so below, as within, so without.",
            "Chakra Balancing healing sessions are an excellent way to heal your energy flow and find ease and grace within your body, mind and spirit through the reinstatement of harmony and balance within your field.",
        ],
        benefits=[
            "Greater and faster ability to heal your mental, physical, spiritual and emotional issues.",
            "Increased openness, memory, concentration and awareness.",
            "Positive outlook in terms of understanding, perception of behaviors and thought process.",
            "Heightened creativity and better resourcefulness because of better perception.",
            "Sense of self-worth, self-esteem and self-confidence.",
            "Improved and deeper sleep, better control over your emotions and improved patience.",
        ],
        cta="Book a Chakra Balancing Session",
    ),
    "dream-interpretation": dict(
        title="Dream Interpretation", hero="IMG_7785.JPG",
        tagline="The dream is the small hidden door in the deepest and most intimate sanctum of the soul.",
        body=[
            "Dream interpretation is the process of assigning meaning to the symbolism of dreams. Symbolism is a universal archetypical language that bridges invisible worlds, and dream interpretation is the conduit between words and worlds.",
            "In many ancient societies, such as those of Egypt and Greece, dreaming was considered a supernatural communication or a means of divine intervention, whose message could be interpreted by those with oracular powers.",
            "The focus of dream interpretation is not to understand the dream but to understand the dreamer.",
        ],
        cta="Book a Dream Interpretation Session",
    ),
    "energetic-signature": dict(
        title="Energetic Signature", hero="89B1E647-C628-4C09-930A-61BA5DD0AAF5.jpeg",
        tagline="Energetic Signatures are the vibrations that make up our essence.",
        body=[
            "Whether you are consciously aware of it or not, each of us has an Energy Signature. As we grow, learn, mature and evolve, our personality emerges through life experience and we begin to create signature patterns of our souls in the form of repetitive vibrational offerings that manifest as our reality.",
            "These vibrations can show up as patterns of emotions and feelings. Over time, we can feel how this signature impacts our emotions, our response to situations and ideas, and the availability of inspiration and empowerment we gift ourselves.",
            "By becoming aware of the patterns of your soul and the vibration that you are offering, you start to make sense of your life experience thus far, and then can begin to intentionally shift the patterns and stories that are hindering your manifesting progress.",
        ],
        cta="Book an Energetic Signature Session",
    ),
    "magdalene-reiki": dict(
        title="Magdalene Reiki", hero="8DC7A4C1-7BEF-432A-AF64-D4005F5D2119.jpeg",
        tagline="Magdalene Reiki: a lost knowledge of feminine folkloric healing.",
        body=[
            "Magdalene Reiki channels the consciousness of ancient spiritual traditions that originated in the sacred temples of the Goddess. This healing modality is a resurrection of the divine feminine principles of energy by means of touch, visualization, meditation, intention and attention.",
            "You become a vessel and conduit of energies that activate the natural healing and revealing processes of the body to restore physical, emotional and spiritual vibrancy.",
            "Magdalene energetic healing evokes mystical and spiritual phenomena in our everyday experience through the divine feminine — seeking a deeper understanding of internal alchemy as a means to transform consciousness.",
        ],
        cta="Book a Magdalene Reiki Session",
    ),
    "reiki-energy-healing": dict(
        title="Reiki Energy Healing", hero="IMG_8728.JPG",
        tagline="Reiki is an energetic practice that draws from the infinite wellspring of healing available in the liminal realm.",
        body=[
            "Energy therapy, energy healing, vibrational medicine, psychic healing, spiritual medicine or spiritual healing are branches of alternative medicine based on the belief that healers can channel life force healing energy into a client and effect positive results.",
            "Energy can stagnate in the body where there has been physical injury or emotional distress. In time, these energy blocks can reveal themselves as illness, anxiety, depression, fatigue or disease. Reiki healing accesses and activates the body's subtle energy systems (aura, chakras, etheric body) to remove blocks and encourage powerful alignment and flow.",
            "Through the use of ancient symbols and universal life force, reiki purifies through time and space, deepening our connection to our own spiritual nature and gifts.",
        ],
        cta="Book a Reiki Energy Healing Session",
    ),
    "sound-alchemy": dict(
        title="Sound Alchemy", hero="F6DCE70D-CDC3-4C22-9138-2731A98D4A72.jpeg",
        tagline="Sound Journeys are an ancient form of deep meditation that includes various ambient sounds played live.",
        body=[
            "A sound bath uses a variety of different traditional crystal bowls, gemstone bowls, cymbals, chimes and other instruments to guide you into an immersive experience in sound frequency that helps to cleanse the soul.",
            "A Sound Bath is a deeply-immersive, full-body listening meditative experience that intentionally uses sound to invite gentle yet powerful therapeutic and restorative processes to nurture the mind and body, guiding you into a deep meditative state.",
            "Sound baths are a holistic practice that dates back to ancient times — Tibetans have been using these instruments, considered sonic frequency technologies, for more than 2,000 years.",
        ],
        benefits_title="Benefits of Sound Alchemy",
        benefits_named=[
            ("Reduce stress and anxiety", "The sounds created by the particular instruments used during a sound bath are meant to activate the alpha and theta brain waves associated with deep meditative and peaceful states."),
            ("Open up and reconnect with one’s self", "Sound baths allow one to completely reset their body and reconnect with their own intentions, restoring the body and stimulating the mind toward healing."),
            ("Feel more relaxed, balanced, and focused", "Lying in savasana, a comfortable restorative pose, allows your body to become more relaxed and balanced, realigning mind, body and heart space."),
        ],
        cta="Book a Sound Alchemy Session",
    ),
    "spirit-guide": dict(
        title="Spirit Guide Conversations", hero="AdobeStock_129541963.jpeg",
        tagline="Spirit Guide Conversations opens a portal to peer through the looking glass of time and space.",
        body=[
            "This session offers a return back to origin, the beginning, the remembrance of where your path was rooted and connected.",
            "Spirit Guide Conversations offers a closer look at the unfinished stories that may anchor you in patterns of limiting beliefs, and instead offers a fresh perspective illuminated by both compassion and empowerment.",
            "During this session, spirit guides and guardians tactfully weave threads of revelation between pivotal moments in your life in order to unveil the higher emanations of your destiny. This 2.5–3 hour session is a deep dive into the original odyssey of your life, steeped in the waters of rebirth, renewal, and revolutionary self love.",
        ],
        cta="Book a Spirit Guide Conversations Session",
    ),
    "tarot-oracle-readings": dict(
        title="Tarot Readings", hero="A7EE8061-C537-451D-8A5F-516D34B1D947.PNG",
        tagline="The Tarot has been used for centuries to reveal hidden truths.",
        body=[
            "Tarot cards are a method of sacred symbolism used for receiving guidance and wisdom from the Universe by accessing the storybook of our life, the mirror of our soul and the key to our inner wisdom.",
            "When you connect with your higher self via tarot and oracle cards, intuition and subtle energy, you gain a very intimate perspective of how you operate in the world and what your true potential is.",
            "In a Tarot card reading, or the practice of cartomancy, we utilize the cards to gain insight into the past, present or future by formulating a question, then drawing and interpreting the symbolism, color theory, numerology, astrology and hidden meanings of the cards.",
            "The Tarot is a tool, an ally and a mentor for those who are open and ready to hear the symbolic language of the Soul.",
        ],
        cta="Book a Tarot Reading",
    ),
}

HOME_DISCOVER = [
    dict(eyebrow="Discover", title="The Akashic Records", photo="earth-hands.png", icon="akashic.png",
         text="The Akashic Records or The Soul’s Records are an etheric Library of Information that contains knowledge and intelligence about every sentient being in the universe. It contains all the soul’s lifetimes, origins, emotions and past. Your Akashic Record is the divine knowing of the entire experience of your soul.",
         link="offerings/akashic-record-readings.html", link_text="Learn more about The Akashic Records"),
    dict(eyebrow="Discover", title="Energetics & Chakras", photo="89B1E647-C628-4C09-930A-61BA5DD0AAF5.jpeg", icon="5.png",
         text="The physical, emotional and spiritual health of your body is dependent on free flowing energy within the body. The chakras are the passageway for that energy to flow within your avatar. The 7 chakras are the 7 wheels of energy in our body.",
         link="offerings/chakra-balancing.html", link_text="Learn more about Energy & Chakras"),
    dict(eyebrow="Discover", title="Magdalene Reiki", photo="8DC7A4C1-7BEF-432A-AF64-D4005F5D2119.jpeg", icon="15.png",
         text="Magdalene Reiki encompasses a lost knowledge of folkloric feminine healing and channels the consciousness of spiritual traditions that originated in the sacred temples of the Goddess.",
         link="offerings/magdalene-reiki.html", link_text="Learn more about Magdalene Reiki"),
    dict(eyebrow="Discover", title="Herbal Healing", photo="67355A69-A421-4324-B0E8-346A4E21E172.jpeg", icon="4.png",
         text="Herbal Knowledge that was once common in every household is now a rare commodity. By crafting herbal teas, tinctures, compresses, salves, and more we can take control of our health in a holistic and organic way.",
         link="resources.html", link_text="Learn more about Herbal Healing"),
    dict(eyebrow="Discover", title="Sound Healing", photo="F6DCE70D-CDC3-4C22-9138-2731A98D4A72.jpeg", icon="8.png",
         text="Sound Baths are an ancient form of deep meditation that includes various ambient sounds played live, using crystal bowls, gemstone bowls, cymbals, chimes and other instruments to cleanse the soul.",
         link="offerings/sound-alchemy.html", link_text="Learn more about Sound Healing"),
    dict(eyebrow="Discover", title="The Tarot", photo="A7EE8061-C537-451D-8A5F-516D34B1D947.PNG", icon="thetarot.png",
         text="A Tarot Deck is a classic set of 78 cards divided into major and minor arcana. Tarot and Oracle readings can help you gain clarity and connection to an answer you’re seeking.",
         link="offerings/tarot-oracle-readings.html", link_text="Learn more about The Tarot"),
    dict(eyebrow="Discover", title="Astrology", photo="unsplash-image-U-Kty6HxcQc.jpg", icon="astrology.png",
         text="Your Astrological Birth Chart is a personal roadmap which illuminates your calling, so you can unlock your full potential and understand the significant moments that guide you.",
         link="offerings/astrology-readings.html", link_text="Learn more about Astrology"),
]

HOME_DISCOVER_ES = [
    dict(eyebrow="Descubre", title="Descubre Spaciodual.us", photo="earth-hands.png", icon="akashic.png",
         text=[
             "Spaciodual.us es el espacio donde dos dimensiones convergen: la luz y la sombra, el cuerpo y el alma, lo consciente y lo inconsciente. Es un contenedor sagrado donde exploramos la dualidad inherente al ser humano — no para resolverla, sino para habitarla con consciencia y amor.",
             "Aquí no hay un camino prescrito. El proceso es orgánico, único para cada ser. Patria acompaña desde la escucha profunda y sin juicio, creando un espacio donde todo lo que eres tiene cabida: tus sombras, tus luces, tus contradicciones, tu grandeza.",
         ],
         link="book.html", link_text="Reserva tu Sesión"),
    dict(eyebrow="Descubre", title="El Coaching de Vida", photo="buddha-monk.png", icon="5.png",
         text=[
             "El coaching de vida y negocios es una conversación transformadora que te ayuda a ver con claridad lo que antes estaba nublado. No se trata de dar respuestas — se trata de hacer las preguntas correctas para que tú mismo descubras las tuyas.",
             "Desde la sociología y el coaching certificado, te acompañamos a identificar patrones de comportamiento, diseñar metas con intención y construir el puente entre quién eres hoy y quién deseas ser. Sin guiones. Sin fórmulas. Solo presencia.",
         ],
         link="book.html", link_text="Más Sobre Coaching"),
    dict(eyebrow="Descubre", title="La Consciencia Corporal", photo="mary-jesus-procession.jpeg", icon="15.png",
         text=[
             "La salud física, emocional y espiritual del cuerpo depende del libre flujo de energía en su interior. Los chakras son los portales a través de los cuales esa energía circula en nuestro avatar. Los 7 chakras son las 7 ruedas de energía de nuestro cuerpo, centros ubicados desde los pies hasta la coronilla del cráneo.",
             "A través del acompañamiento consciente, exploramos cómo los bloqueos energéticos se manifiestan en el cuerpo — como fatiga, ansiedad, dolor o enfermedad — y trabajamos juntos para restaurar el flujo natural de la vida. El cuerpo siempre sabe. Solo necesita que lo escuchen.",
         ],
         link="offerings/chakra-balancing.html", link_text="Más sobre los Chakras"),
    dict(eyebrow="Descubre", title="El Reiki y La Energía", photo="reiki-energy-woman.png", icon="4.png",
         text=[
             "El Reiki es una práctica energética que canaliza la fuente inagotable de sanación disponible en el reino liminal. La energía puede estancarse en el cuerpo donde ha habido lesión física o angustia emocional. Con el tiempo, estos bloqueos energéticos pueden manifestarse como enfermedad, ansiedad, depresión, fatiga o dolencia.",
             "Como práctica holística, el Reiki accede y activa los sistemas de energía sutil del cuerpo — aura, chakras, cuerpo etérico — para eliminar bloqueos y fomentar una alineación poderosa. El cuerpo posee una capacidad inherente de sanarse a sí mismo. El Reiki la despierta.",
         ],
         link="offerings/reiki-energy-healing.html", link_text="Más sobre el Reiki"),
    dict(eyebrow="Descubre", title="Sanación con Sonido", photo="F6DCE70D-CDC3-4C22-9138-2731A98D4A72.jpeg", icon="8.png",
         text="Los Baños de Sonido son una forma ancestral de meditación profunda que incluye distintos sonidos ambientales tocados en vivo, con cuencos de cristal, cuencos de gemas, platillos, campanas y otros instrumentos para purificar el alma.",
         link="offerings/sound-alchemy.html", link_text="Conoce más sobre la Sanación con Sonido"),
    dict(eyebrow="Descubre", title="El Tarot", photo="A7EE8061-C537-451D-8A5F-516D34B1D947.PNG", icon="thetarot.png",
         text="Una baraja de Tarot es un conjunto clásico de 78 cartas divididas en arcanos mayores y menores. Las lecturas de Tarot y Oráculo pueden ayudarte a ganar claridad y conexión con la respuesta que estás buscando.",
         link="offerings/tarot-oracle-readings.html", link_text="Conoce más sobre el Tarot"),
    dict(eyebrow="Descubre", title="Astrología", photo="unsplash-image-U-Kty6HxcQc.jpg", icon="astrology.png",
         text="Tu Carta Astral es un mapa personal que ilumina tu vocación, para que puedas desbloquear todo tu potencial y comprender los momentos significativos que te guían.",
         link="offerings/astrology-readings.html", link_text="Conoce más sobre la Astrología"),
]

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
    dropdown_items = "\n".join(
        f'          <a href="{prefix}offerings/{slug}.html">{title}</a>'
        for title, slug in OFFERING_LINKS
    )
    solid_class = " is-solid" if solid else ""
    always_solid = ' data-always-solid="true"' if solid else ""
    return f"""  <header class="site-header{solid_class}"{always_solid}>
    <div class="header-inner">
      <a href="{prefix}book.html" class="logo-text">{nav['book']}</a>
      <nav class="main-nav">
        <a href="{prefix}index.html" class="nav-link">{nav['home']}</a>
        <div class="nav-item-dropdown">
          <a href="#" class="nav-link">{nav['services']}</a>
          <div class="dropdown-panel">
{dropdown_items}
            <a href="#" class="is-disabled" style="opacity:.5">{nav['mentorship']}</a>
          </div>
        </div>
        <a href="{prefix}practitioners.html" class="nav-link">{nav['practitioners']}</a>
        <a href="{prefix}resources.html" class="nav-link">{nav['resources']}</a>
        <a href="{prefix}book.html" class="nav-link">{nav['book']}</a>
      </nav>
      <div class="header-icons">
        <a href="#" class="icon-link" aria-label="Facebook" target="_blank" rel="noopener">{SVG_ICONS['facebook']}</a>
        <a href="#" class="icon-link" aria-label="Instagram" target="_blank" rel="noopener">{SVG_ICONS['instagram']}</a>
        <a href="{prefix}book.html" class="icon-link" aria-label="Cart">{SVG_ICONS['cart']}</a>
      </div>
      <button class="nav-toggle" aria-label="Menu"><span></span><span></span><span></span></button>
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
        <a href="{prefix}practitioners.html">{nav['practitioners']}</a>
        <a href="{prefix}resources.html">{nav['resources']}</a>
        <a href="{prefix}book.html">{nav['book']}</a>
      </nav>
      <div class="footer-social">
        <a href="#" aria-label="Facebook" target="_blank" rel="noopener">{SVG_ICONS['facebook']}</a>
        <a href="#" aria-label="Instagram" target="_blank" rel="noopener">{SVG_ICONS['instagram']}</a>
      </div>
      <p class="footer-fine">{FOOTER_FINE[lang]}</p>
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


def img(depth, name, alt="", cls=""):
    prefix = rel(depth, "")
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<img src="{prefix}images/{name}" alt="{alt}"{cls_attr} loading="lazy">'


# ---------------------------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------------------------
def build_home(lang="en"):
    depth = 0
    rows_data = HOME_DISCOVER_ES if lang == "es" else HOME_DISCOVER
    discover_rows = []
    for i, d in enumerate(rows_data):
        reverse = " reverse" if i % 2 == 1 else ""
        paragraphs = d['text'] if isinstance(d['text'], list) else [d['text']]
        text_html = "\n          ".join(f"<p>{p}</p>" for p in paragraphs)
        discover_rows.append(f"""      <div class="discover-row{reverse}">
        <div class="discover-media">{img(depth, d['photo'], d['title'])}</div>
        <div class="discover-text">
          <span class="eyebrow">{d['eyebrow']}</span>
          <h2>{d['title']}</h2>
          {text_html}
          <a href="{d['link']}" class="btn">{d['link_text']}</a>
        </div>
      </div>""")
    discover_html = "\n".join(discover_rows)

    if lang == "es":
        body = f"""  <section class="hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <div class="hero-sub">para tu</div>
      <h1>Spacio Dual</h1>
    </div>
  </section>

  <section class="section-white intro-section">
    <div class="intro-bg" aria-hidden="true"></div>
    <div class="container intro-block">
      <h2 class="script-heading">El alquimista interior que abre puerta hacia el infinito</h2>
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

  <section class="section-dark text-center">
    <div class="container">
      <h2>¿Todo listo para comenzar?</h2>
      <p>Reserva una sesión con nuestras practicantes y comienza el camino de regreso a ti mismo.</p>
      <a href="book.html" class="btn">Reservar una Sesión</a>
    </div>
  </section>
  {SECTION_DIVIDER}"""
        title = BRAND_NAME
        description = f"Clon visual no oficial de {BRAND_NAME} — un santuario metafísico y esotérico de sanación en St. Thomas, Islas Vírgenes de EE. UU."
    else:
        body = f"""  <section class="hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <div class="hero-sub">for the</div>
      <h1>Spacio Dual</h1>
    </div>
  </section>

  <section class="section-white intro-section">
    <div class="intro-bg" aria-hidden="true"></div>
    <div class="container intro-block">
      <h2 class="script-heading">The Inner Alchemist Who Opens the Door to the Infinite</h2>
      <p class="intro-caption">Begin your transcendental journey toward a new consciousness of being, presence and feeling. Within a safe, honest and authentic space, discover a variety of holistic and energetic modalities that will help you restore the natural balance of your essence and divine presence.</p>
      <a href="book.html" class="btn">Begin Your Journey</a>
    </div>
  </section>
  {SECTION_DIVIDER}

  <section class="section-white section-tight">
    <div class="container">
{discover_html}
    </div>
  </section>
  {SECTION_DIVIDER}

  <section class="section-dark text-center">
    <div class="container">
      <h2>Ready to Begin?</h2>
      <p>Book a session with one of our practitioners and start your journey home to yourself.</p>
      <a href="book.html" class="btn">Book a Session</a>
    </div>
  </section>
  {SECTION_DIVIDER}"""
        title = BRAND_NAME
        description = f"Unofficial visual clone of {BRAND_NAME} — a metaphysical and esoteric healing sanctuary in St. Thomas, USVI."

    html = page_shell(title, description, depth, body, solid_header=False, lang=lang)
    (ROOT / "index.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# OFFERING PAGES
# ---------------------------------------------------------------------------
def matching_practitioners(title):
    matches = [p for p in PRACTITIONERS if any(title.lower() in t.lower() or t.lower() in title.lower() for t in p["tags"])]
    return matches[:4] or PRACTITIONERS[:2]


def build_offering(slug, data):
    depth = 1
    body_paras = "\n".join(f"      <p>{p}</p>" for p in data["body"])

    extra = ""
    if data.get("benefits"):
        items = "\n".join(f'        <li><strong>{n.upper()}.</strong> {b}</li>' for n, b in zip(
            ["one", "two", "three", "four", "five", "six", "seven", "eight"], data["benefits"]))
        extra += f"""    <div class="container">
      <ol style="list-style:none; padding:0; max-width:760px; margin:40px auto 0;">
{items}
      </ol>
    </div>
"""
    if data.get("benefits_named"):
        cards = "\n".join(f"""        <div class="card"><div class="card-body">
          <h3>{name}</h3>
          <p>{desc}</p>
        </div></div>""" for name, desc in data["benefits_named"])
        extra += f"""    <div class="container">
      <h2 class="text-center">{data.get('benefits_title', 'Benefits')}</h2>
      <div class="grid" style="grid-template-columns:repeat(3,1fr); margin-top:40px;">
{cards}
      </div>
    </div>
"""

    faq_html = ""
    if data.get("faq"):
        items = "\n".join(f"""      <div class="faq-item">
        <h4>{q}</h4>
        <p>{a}</p>
      </div>""" for q, a in data["faq"])
        faq_html = f"""  <section class="section-white section-tight">
    <div class="container" style="max-width:760px">
      <h2 class="text-center">Frequently Asked Questions</h2>
{items}
    </div>
  </section>
"""

    prac = matching_practitioners(data["title"])
    prac_cards = "\n".join(f"""        <div class="card">
          {img(depth, p['img'], p['name'])}
          <div class="card-body">
            <h3>{p['name']}</h3>
            <p>{p['bio']}</p>
          </div>
        </div>""" for p in prac)

    store_note = ""
    if data.get("is_store"):
        store_note = """    <div class="container text-center">
      <div class="notice-badge">This is a static demo of the Apothecary shop — products shown for illustration only, no real checkout.</div>
      <div class="grid" style="grid-template-columns:repeat(3,1fr); margin-bottom:40px;">
        <div class="card"><div class="card-body">
          <h3>Herbal Tea Blend</h3>
          <p>A calming loose-leaf tea blend crafted for grounding and clarity.</p>
          <div class="product-price">$18.00</div>
          <button class="btn mock-add-to-cart mt-40">Add to Cart</button>
        </div></div>
        <div class="card"><div class="card-body">
          <h3>Cleansing Salve</h3>
          <p>A botanical salve blended with calendula and rosemary.</p>
          <div class="product-price">$22.00</div>
          <button class="btn mock-add-to-cart mt-40">Add to Cart</button>
        </div></div>
        <div class="card"><div class="card-body">
          <h3>Ritual Tincture</h3>
          <p>A small-batch herbal tincture for daily intention setting.</p>
          <div class="product-price">$28.00</div>
          <button class="btn mock-add-to-cart mt-40">Add to Cart</button>
        </div></div>
      </div>
    </div>
"""

    body = f"""  <section class="hero page-hero" style="background-image:url('{rel(depth,'')}images/{data['hero']}')">
    <div class="hero-content">
      <a href="{rel(depth,'')}index.html" class="back-link">&larr; Back to Offerings</a>
      <h1>{data['title']}</h1>
      <p class="hero-sub" style="font-size:1.1rem">{data['tagline']}</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container" style="max-width:760px">
{body_paras}
      <div class="text-center mt-40">
        <a href="{rel(depth,'')}book.html" class="btn">{data['cta']}</a>
      </div>
    </div>
  </section>
{extra}{faq_html}
  <section class="section-white section-tight">
    <div class="container">
      <h2 class="text-center">View our {data['title']} Practitioners</h2>
      <div class="grid mt-40">
{prac_cards}
      </div>
    </div>
  </section>
{store_note}"""

    html = page_shell(
        BRAND_NAME,
        data["tagline"],
        depth, body, solid_header=True,
    )
    out_dir = ROOT / "offerings"
    out_dir.mkdir(exist_ok=True)
    (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# PRACTITIONERS PAGE
# ---------------------------------------------------------------------------
def build_practitioners():
    depth = 0
    cards = "\n".join(f"""        <div class="card">
          {img(depth, p['img'], p['name'])}
          <div class="card-body">
            <div class="card-tags">{', '.join(p['tags'][:4])}</div>
            <h3>{p['name']}</h3>
            <p>{p['bio']}</p>
          </div>
        </div>""" for p in PRACTITIONERS)

    body = f"""  <section class="hero page-hero" style="background-image:url('images/unsplash-image-h1x7EEaYINQ.jpg')">
    <div class="hero-content">
      <h1>Our Practitioners</h1>
      <p class="hero-sub" style="font-size:1.1rem">The {BRAND_NAME} Team</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container">
      <div class="grid">
{cards}
      </div>
    </div>
  </section>"""

    html = page_shell(
        BRAND_NAME,
        f"Meet the healers, facilitators and guides of {BRAND_NAME}.",
        depth, body, solid_header=True,
    )
    (ROOT / "practitioners.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# RESOURCES PAGE
# ---------------------------------------------------------------------------
def build_resources():
    depth = 0
    categories = {}
    for r in RESOURCES:
        categories.setdefault(r["cat"], []).append(r)

    sections = []
    for cat, items in categories.items():
        cards = "\n".join(f"""        <div class="card">
          {img(depth, r['img'], r['name'])}
          <div class="card-body">
            <div class="card-tags">{cat}</div>
            <h3>{r['name']}</h3>
            <p>{r['blurb']}</p>
          </div>
        </div>""" for r in items)
        sections.append(f"""  <section class="section-white section-tight">
    <div class="container">
      <h2>{cat}</h2>
      <div class="grid mt-40">
{cards}
      </div>
    </div>
  </section>""")
    sections_html = "\n".join(sections)

    body = f"""  <section class="hero page-hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <h1>Resources</h1>
      <p class="hero-sub" style="font-size:1.1rem">Herbalism &amp; Crystal Wisdom</p>
    </div>
  </section>
{sections_html}
  <section class="section-dark text-center">
    <div class="container">
      <h2>Coming Soon</h2>
      <p>Symbolism, Ritual &amp; Ceremony, Energy and Mythology.</p>
    </div>
  </section>"""

    html = page_shell(
        BRAND_NAME,
        f"Herbalism and crystal resources from {BRAND_NAME}.",
        depth, body, solid_header=True,
    )
    (ROOT / "resources.html").write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# BOOK / STATIC MOCKUP PAGE
# ---------------------------------------------------------------------------
def build_book():
    depth = 0
    offering_options = "\n".join(f'          <option>{title}</option>' for title, _ in OFFERING_LINKS)

    body = f"""  <section class="hero page-hero" style="background-image:url('images/hero-sanctuary.jpg')">
    <div class="hero-content">
      <h1>Book a Session</h1>
      <p class="hero-sub" style="font-size:1.1rem">Please fill out the form below to request a session</p>
    </div>
  </section>

  <section class="section-white">
    <div class="container text-center">
      <div class="notice-badge">This is a static demo booking form. No real scheduling or payment happens here — it does not submit anywhere.</div>
      <form class="form-mock">
        <div class="form-row">
          <label for="name">Full Name</label>
          <input id="name" type="text" placeholder="Jane Doe">
        </div>
        <div class="form-row">
          <label for="email">Email</label>
          <input id="email" type="email" placeholder="jane@example.com">
        </div>
        <div class="form-row">
          <label for="offering">Session Type</label>
          <select id="offering">
{offering_options}
          </select>
        </div>
        <div class="form-row">
          <label for="date">Preferred Date</label>
          <input id="date" type="date">
        </div>
        <div class="form-row">
          <label for="notes">Notes</label>
          <textarea id="notes" placeholder="Tell us a little about what you're seeking..."></textarea>
        </div>
        <button type="submit" class="btn">Request Session</button>
        <p class="form-mock-note small-note" style="display:none; margin-top:16px;"></p>
      </form>
    </div>
  </section>"""

    html = page_shell(
        BRAND_NAME,
        "Static demo booking page — no real scheduling.",
        depth, body, solid_header=True,
    )
    (ROOT / "book.html").write_text(html, encoding="utf-8")


def main():
    build_home(lang="es")
    for slug, data in OFFERINGS.items():
        data["title"] = data.get("title", slug)
        build_offering(slug, data)
    build_practitioners()
    build_resources()
    build_book()
    print("Build complete.")


if __name__ == "__main__":
    main()
