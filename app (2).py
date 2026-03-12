"""
══════════════════════════════════════════
MONEY TREE GANG BANGERS — app.py
Flask server — run: python app.py
Visit: http://localhost:5000
══════════════════════════════════════════
"""

from flask import Flask, render_template, request, jsonify
import json, re, os

app = Flask(__name__, template_folder='.', static_folder='.')

# ── GROUP DATA ──────────────────────────────────────────────────────────────
GROUP = {
    "name":    "Money Tree Gang Bangers",
    "short":   "MTGB",
    "tagline": "From the streets to the summit",
    "founded": "2018",
    "city":    "Johannesburg, South Africa",
    "bio_short": "Six voices. One vision. Money Tree Gang Bangers rose from the concrete to become Southern Africa's most electrifying hip-hop collective.",
    "socials": {
        "instagram": {"handle": "@mtgb_official",  "url": "#", "icon": "📸"},
        "twitter":   {"handle": "@MoneyTreeGB",    "url": "#", "icon": "🐦"},
        "youtube":   {"handle": "MoneyTreeGangTV", "url": "#", "icon": "▶️"},
        "spotify":   {"handle": "Money Tree Gang", "url": "#", "icon": "🎵"},
        "tiktok":    {"handle": "@mtgbofficial",   "url": "#", "icon": "🎬"},
        "soundcloud":{"handle": "mtgb",            "url": "#", "icon": "☁️"},
    }
}

# ── MEMBERS ─────────────────────────────────────────────────────────────────
MEMBERS = [
    {
        "name":  "Khumalo Vibe",
        "alias": "K-Vibe",
        "role":  "MC · Hype Man",
        "emoji": "🎤",
        "bio":   "K-Vibe is the engine of the group — relentless energy, rapid-fire delivery, and bars that cut deep. Born in Soweto, he's been spitting since age 12.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Concrete Dreams","year":"2022","dur":"3:24"},
            {"title":"Soweto Sunrise","year":"2023","dur":"2:58"},
            {"title":"No Ceilings JHB","year":"2024","dur":"3:41"},
        ]
    },
    {
        "name":  "Lethabo Flex",
        "alias": "L-Flex",
        "role":  "MC · Songwriter",
        "emoji": "✍️",
        "bio":   "The pen behind the group's deepest cuts. L-Flex weaves storytelling and melody in a way that transcends genre. His hooks are unforgettable.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Letter To My Father","year":"2021","dur":"4:12"},
            {"title":"Rands & Sense","year":"2023","dur":"3:55"},
            {"title":"Trees Don't Lie","year":"2024","dur":"3:18"},
        ]
    },
    {
        "name":  "Sipho Drip",
        "alias": "S-Drip",
        "role":  "MC · Style Icon",
        "emoji": "💎",
        "bio":   "S-Drip brings the swag and the substance. His fashion-forward persona is matched only by his lyrical precision. Raised in Alex township.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Fresh Kicks","year":"2022","dur":"2:47"},
            {"title":"Drip Season","year":"2023","dur":"3:03"},
            {"title":"Flex On Em","year":"2024","dur":"3:36"},
        ]
    },
    {
        "name":  "DJ Roots",
        "alias": "Rootz",
        "role":  "DJ · Producer",
        "emoji": "🎧",
        "bio":   "The architect of the MTGB sound. DJ Roots blends gqom, drill, and classic boom-bap into a signature sonic landscape no one else can replicate.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Township Bounce","year":"2021","dur":"4:44"},
            {"title":"Bass Cathedral","year":"2023","dur":"5:02"},
            {"title":"Roots Mix Vol.3","year":"2024","dur":"6:15"},
        ]
    },
    {
        "name":  "Nomsa Blade",
        "alias": "N-Blade",
        "role":  "MC · Vocalist",
        "emoji": "🔥",
        "bio":   "MTGB's wildcard and most versatile performer. N-Blade can spit bars, melt into melodic hooks, or switch to spoken word in the same 16 bars.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Wildfire","year":"2022","dur":"3:11"},
            {"title":"She The Realest","year":"2023","dur":"3:29"},
            {"title":"Cold Blade","year":"2024","dur":"2:54"},
        ]
    },
    {
        "name":  "Thabo Gold",
        "alias": "T-Gold",
        "role":  "MC · Visionary",
        "emoji": "🌳",
        "bio":   "The philosophical heart of MTGB. T-Gold's verses are meditative, political, and poetic. He writes the group's anthems and manifesto tracks.",
        "socials": {"ig":"#","tw":"#","sc":"#","sp":"#"},
        "tracks": [
            {"title":"Roots Of Gold","year":"2021","dur":"4:33"},
            {"title":"The Manifesto","year":"2023","dur":"5:10"},
            {"title":"Grow Or Die","year":"2024","dur":"3:47"},
        ]
    },
]

# ── DISCOGRAPHY ─────────────────────────────────────────────────────────────
DISCOGRAPHY = [
    {"title":"Planting Seeds",       "year":"2018","type":"ep",    "emoji":"🌱","tracks":5,  "desc":"The debut EP that introduced the world to MTGB's raw vision."},
    {"title":"Root System",          "year":"2019","type":"album", "emoji":"🌿","tracks":12, "desc":"First full-length — gritty, honest, and undeniably fresh."},
    {"title":"Green Season",         "year":"2020","type":"album", "emoji":"🍃","tracks":14, "desc":"Their pandemic-era masterpiece. Recorded in lockdown. Dropped hard."},
    {"title":"Paper Chase",          "year":"2021","type":"single","emoji":"💵","tracks":1,  "desc":"The track that broke them to a mainstream audience overnight."},
    {"title":"Money Talks",          "year":"2022","type":"album", "emoji":"💰","tracks":16, "desc":"Career-defining. Nominated for 3 SAMAs. Toured the continent."},
    {"title":"Gang Chronicles Vol.1","year":"2023","type":"ep",    "emoji":"📖","tracks":8,  "desc":"A deep-cut EP for the day-ones. No features. Pure collective energy."},
    {"title":"Canopy",               "year":"2024","type":"album", "emoji":"🌳","tracks":18, "desc":"Their most ambitious record yet. Features, orchestras, and pure heat."},
    {"title":"Money Tree Anthem",    "year":"2025","type":"single","emoji":"🏆","tracks":1,  "desc":"The 2025 comeback single. Streaming numbers are violent."},
]

# ── CONCERTS ─────────────────────────────────────────────────────────────────
CONCERTS = [
    {"month":"APR","day":"12","year":"2026","show":"CANOPY WORLD TOUR","venue":"FNB Stadium","city":"Johannesburg, South Africa","price":"R350","sold":False},
    {"month":"APR","day":"25","year":"2026","show":"CANOPY WORLD TOUR","venue":"Cape Town Stadium","city":"Cape Town, South Africa","price":"R350","sold":False},
    {"month":"MAY","day":"03","year":"2026","show":"CANOPY WORLD TOUR","venue":"Moses Mabhida Stadium","city":"Durban, South Africa","price":"R300","sold":False},
    {"month":"MAY","day":"17","year":"2026","show":"CANOPY WORLD TOUR","venue":"Lusaka Arena","city":"Lusaka, Zambia","price":"K850","sold":False},
    {"month":"JUN","day":"07","year":"2026","show":"CANOPY WORLD TOUR","venue":"Accra Sports Stadium","city":"Accra, Ghana","price":"GHS 120","sold":False},
    {"month":"JUN","day":"21","year":"2026","show":"CANOPY WORLD TOUR","venue":"O2 Academy Brixton","city":"London, UK","price":"£45","sold":True},
    {"month":"JUL","day":"04","year":"2026","show":"CANOPY WORLD TOUR","venue":"Brooklyn Mirage","city":"New York, USA","price":"$65","sold":True},
    {"month":"AUG","day":"15","year":"2026","show":"HOME SEASON","venue":"The Venue JHB","city":"Johannesburg, South Africa","price":"R250","sold":False},
]

# ── HISTORY & AMBITIONS ──────────────────────────────────────────────────────
HISTORY = {
    "paras": [
        "It started in <strong>2018</strong> in a rented garage in Tembisa, Johannesburg — six childhood friends who had nothing but a laptop, a cheap microphone, and an unshakeable belief that their voices mattered. <strong>Money Tree Gang Bangers</strong> was born not from ambition, but from necessity.",
        "Their debut EP <em>Planting Seeds</em> circulated on WhatsApp before it ever hit streaming platforms. By 2019 they were headlining local shows; by 2020 their lockdown album <em>Green Season</em> had broken through continental boundaries, racking up millions of plays from Nigeria to Sweden.",
        "The 2022 album <em>Money Talks</em> was a turning point — three SAMA nominations, a sold-out Johannesburg arena, and collaborations with artists from across Africa and the diaspora. MTGB was no longer just a group. They were a movement.",
    ],
    "timeline": [
        {"year":"2018","text":"Formed in Tembisa. Released debut EP 'Planting Seeds' digitally."},
        {"year":"2019","text":"First paid headline show. Signed to independent label. Toured SA."},
        {"year":"2020","text":"Released 'Green Season' during lockdown — went viral across Africa."},
        {"year":"2021","text":"'Paper Chase' single peaks at #1 on SA Hip-Hop charts."},
        {"year":"2022","text":"'Money Talks' album. 3× SAMA nominations. Arena tour across SA."},
        {"year":"2023","text":"Continental tour. 40+ cities. 'Gang Chronicles Vol.1' drops."},
        {"year":"2024","text":"'Canopy' album. International features. UK + US debut shows."},
        {"year":"2025","text":"'Money Tree Anthem' released. World Tour announced."},
    ]
}

AMBITIONS = [
    {"icon":"🌍","title":"Global Domination","text":"MTGB is building toward becoming the first SA hip-hop collective to headline a major US/UK festival on their own terms."},
    {"icon":"🎬","title":"Film & Visual Media","text":"A full-length MTGB documentary and music video series are in production, chronicling the group's journey from garage to global."},
    {"icon":"🏫","title":"Youth Academy","text":"The MTGB Foundation plans to open a free music production academy in Tembisa by 2027, giving back to the community that built them."},
    {"icon":"💿","title":"Label Independence","text":"Launching their own imprint — Money Tree Records — to sign and mentor emerging African artists on their own terms."},
    {"icon":"🤝","title":"Pan-African Collabs","text":"Deepening ties with artists from Nigeria, Ghana, Kenya and beyond to create music that unifies the continent under one sound."},
]

# ── ROUTES ───────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template(
        'index.html',
        group=GROUP,
        members=MEMBERS,
        discography=DISCOGRAPHY,
        concerts=CONCERTS,
        history=HISTORY,
        ambitions=AMBITIONS,
    )

@app.route('/api/newsletter', methods=['POST'])
def newsletter():
    data  = request.get_json()
    email = data.get('email','').strip()
    if not email or '@' not in email:
        return jsonify({"success": False, "message": "Invalid email address."}), 400
    # In production: save to DB / send to Mailchimp / etc.
    print(f"[NEWSLETTER] New subscriber: {email}")
    return jsonify({"success": True, "message": f"Welcome to the Money Tree, {email}!"})

if __name__ == '__main__':
    print("\n🌳  Money Tree Gang Bangers — Server Starting")
    print("🚀  Visit: http://localhost:5000\n")
    app.run(debug=True, port=5000)
