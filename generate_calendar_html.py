import datetime
from app.engine import get_birth_card, get_spread_year, generate_yearly_spread_data, extract_chain, ROWS

def get_card_location(card, grid, crown):
    """Finds where a specific card is located in a given spread."""
    for ri, rn in enumerate(ROWS):
        if card in grid[rn]:
            return {"type": "grid", "row": rn, "col_idx": grid[rn].index(card)}
    
    if card in crown:
        return {"type": "crown", "idx": crown.index(card)}
        
    return {"type": "unknown"}


# Procedural Language Dictionaries
PERIOD_PREFIXES = {
    'Mercury': 'Speed and communication govern this cycle. Information moves without resistance.',
    'Venus': 'Connection and attraction govern this cycle. Relationships solidify or dissolve under applied pressure.',
    'Mars': 'Friction and aggressive action govern this cycle. Conflict is structurally required.',
    'Jupiter': 'Expansion and luck govern this cycle. Risk is mathematically favorable if properly leveraged.',
    'Saturn': 'Discipline and restriction govern this cycle. The structure is unbending. Do not negotiate.',
    'Uranus': 'Disruption and sudden shifts govern this cycle. Stability is an illusion; pivot immediately.',
    'Neptune': 'Illusion and intuition govern this cycle. What you see is obscured. Trust silent calculations over loud promises.'
}

# Fully mapped 52-card interpretations (Strict, Analog, Mathematical)
CARD_MEANINGS = {
    # HEARTS (Emotional Output / Relationship Parameters)
    'A♥': 'Initiate new emotional variables. A baseline reset in connection.',
    '2♥': 'Emotional partnership requires equal data exchange. Synchronize inputs.',
    '3♥': 'Creative emotional expression. Output data without filtering.',
    '4♥': 'Build emotional structure. Reject unstable or volatile inputs today.',
    '5♥': 'Emotional disruption. Do not resist the sudden shift in your relational baseline.',
    '6♥': 'Emotional responsibility. You must maintain the equilibrium of your environment.',
    '7♥': 'Emotional calculation. Seek the absolute truth; discard all sentimentality.',
    '8♥': 'Emotional power. Direct the matrix of your connections with absolute force.',
    '9♥': 'Emotional completion. A relational variable has expired. Delete it.',
    '10♥': 'Emotional mastery. Total public or relational synchronization is highly probable.',
    'J♥': 'A messenger of emotional data. Process the incoming variables; do not react.',
    'Q♥': 'Emotional sovereignty. Receive external inputs but carefully guard your core structure.',
    'K♥': 'Emotional authority. You dictate the relational parameters of the environment today.',

    # CLUBS (Behavioral Output / Intellectual Data)
    'A♣': 'Initiate a new behavioral algorithm. New knowledge has been acquired.',
    '2♣': 'Behavioral protocol requires partnership. Communicate and synchronize your data.',
    '3♣': 'Behavioral expression. Output your strategies and algorithms clearly.',
    '4♣': 'Structural knowledge. Rigidly solidify your mental frameworks.',
    '5♣': 'Behavioral disruption. Pivot your routine and physical location immediately.',
    '6♣': 'Intellectual responsibility. Stabilize the turbulent data flow in your network.',
    '7♣': 'Behavioral calculation. Isolate the obstacle. Process the data and remove the variable.',
    '8♣': 'Intellectual command. Apply extreme mental pressure and focus to the system.',
    '9♣': 'Intellectual completion. An outdated mindset or pattern must be deleted permanently.',
    '10♣': 'Intellectual mastery. Total comprehension and execution of the active system.',
    'J♣': 'A messenger of new data. Rapidly adapt to the incoming stream of information.',
    'Q♣': 'Intellectual sovereignty. Process the complex data without yielding control.',
    'K♣': 'Intellectual authority. Dictate the behavioral parameters and rules of your environment.',

    # DIAMONDS (Material Output / Resource Parameters)
    'A♦': 'Initiate material calculation. A newly integrated financial variable enters the grid.',
    '2♦': 'Financial partnership requires structural alignment. Do not merge structural assets blindly.',
    '3♦': 'Material expression. Create tangible, physical outputs from the raw data.',
    '4♦': 'Material structure. Anchor your resources. Minimize all uncalculated risk.',
    '5♦': 'Material disruption. Anticipate a sudden, volatile shift in your financial grid.',
    '6♦': 'Material responsibility. Maintain the baseline of your physical and financial assets.',
    '7♦': 'Financial calculation. Apply severe logical pressure to your current resources.',
    '8♦': 'Material command. Direct your financial energy with absolute and unyielding authority.',
    '9♦': 'Material completion. A structural asset or financial cycle concludes its lifecycle.',
    '10♦': 'Material mastery. Maximum optimization of the physical and financial grid.',
    'J♦': 'A messenger of material shifts. Calculate the new financial vectors immediately.',
    'Q♦': 'Material sovereignty. Control the resources without unnecessary expenditure.',
    'K♦': 'Material authority. You are the final variable in all financial and asset calculations.',

    # SPADES (Structural Output / Physical Labor)
    'A♠': 'Initiate absolute structural change. A stark new foundation is required.',
    '2♠': 'Labor protocol requires partnership. Collaborate only if your algorithms align perfectly.',
    '3♠': 'Structural expression. Construct the physical architecture of your current goal.',
    '4♠': 'Absolute structure. The system is entirely rigid. Do not attempt modification.',
    '5♠': 'Structural disruption. The physical baseline is shifting; pivot rapidly or face failure.',
    '6♠': 'Structural responsibility. The burden of the entire physical grid is yours today.',
    '7♠': 'Structural calculation. Identify and ruthlessly extract the flaw in your physical architecture.',
    '8♠': 'Exercise structural power and command. Strategy and labor outrank emotion today.',
    '9♠': 'Structural completion. A physical phase expires. Purge the remnant data from the system.',
    '10♠': 'Structural mastery. Flawless physical execution of the chosen algorithm.',
    'J♠': 'A messenger of physical action. Execute the requested protocol immediately and without hesitation.',
    'Q♠': 'Structural sovereignty. You actively govern the physical and labor outputs of the system.',
    'K♠': 'Absolute authority. You are the final structural variable in any physical conflict today.',

    # Fallback
    'default': 'Rely on core algorithms. Maintain your structural integrity.'
}

# Example collision interpretations (Where the global card lands in your spread)
COLLISION_SUFFIXES = {
    'Mercury': 'However, external forces will attempt fast, disorganized communication. Filter the noise.',
    'Venus': 'An external variable will attempt emotional connection. Verify their structural integrity before engaging.',
    'Mars': 'Expect an external entity to introduce sudden friction or conflict. Meet force with calculation.',
    'Jupiter': 'The environment provides unexpected expansion. Capitalize on this external variable immediately.',
    'Saturn': 'The external environment will heavily restrict you today. Surrender ambition and focus on survival mechanics.',
    'Uranus': 'An external disruption to your schedule is highly probable. Do not resist the pivot.',
    'Neptune': 'The environment is highly deceptive today. Do not sign contracts or trust unverified data.',
    'Crown / Unanchored': 'The world operates outside your direct grid today. Anchor yourself and observe the chaos.'
}

def generate_sentence(period, fractal_card, collision_planet):
    """Procedurally generates a harsh, mathematical interpretation paragraph."""
    p1 = PERIOD_PREFIXES.get(period, 'Maintain structural integrity.')
    p2 = CARD_MEANINGS.get(fractal_card, CARD_MEANINGS['default'])
    p3 = COLLISION_SUFFIXES.get(collision_planet, COLLISION_SUFFIXES['Crown / Unanchored'])
    
    return f"{p1} For your specific coordinates, {p2.lower()} {p3}"


def generate_html_planner(first_name, birth_year, birth_month, birth_day, target_year=2026):
    # Get base data
    user_birth_card, sv = get_birth_card(birth_month, birth_day)
    start_date = datetime.date(target_year, birth_month, birth_day)
    age = target_year - birth_year
    spread_year = min(max(age + 1, 1), 90)
    
    yearly_grid, yearly_crown = generate_yearly_spread_data(spread_year)
    full_chain = extract_chain(yearly_grid, yearly_crown, user_birth_card, 52)
    
    # HTML Setup
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Analog Algorithm | {first_name}'s {target_year} Planner</title>
    <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=Inter:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --paper: #F3F1ED; /* High-end beige paper */
            --ink: #111111;
            --accent: #B83B3B; /* Stark red for emphasis */
            --page-width: 600px;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #E2DFD8; /* Slightly darker background outside the book */
            color: var(--ink);
            margin: 0;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .book-page {{
            background: var(--paper);
            width: var(--page-width);
            min-height: 800px;
            padding: 50px 60px;
            box-shadow: -15px 15px 30px rgba(0,0,0,0.1), inset 3px 0px 5px rgba(0,0,0,0.05); /* Page depth */
            border-radius: 2px 5px 5px 2px;
            border-left: 1px solid #d4d1cc; /* Book spine seam */
            margin-bottom: 60px;
            position: relative;
        }}
        
        /* Typography */
        h1.header {{
            font-family: 'Crimson Pro', serif;
            font-size: 2.2rem;
            text-transform: uppercase;
            font-weight: 700;
            margin: 0;
            letter-spacing: -1px;
            border-bottom: 2px solid var(--ink);
            padding-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: baseline;
        }}
        h1.header span.date {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1rem;
            font-weight: 400;
            color: #555;
            letter-spacing: 0;
        }}
        
        .metadata-bar {{
            display: flex;
            justify-content: space-between;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.75rem;
            text-transform: uppercase;
            margin-top: 15px;
            color: #555;
            border-bottom: 1px dashed #ccc;
            padding-bottom: 15px;
            margin-bottom: 40px;
        }}
        
        .metadata-bar div strong {{
            color: var(--ink);
        }}

        .data-header {{
            font-family: 'Crimson Pro', serif;
            font-size: 1.2rem;
            text-transform: uppercase;
            font-weight: 700;
            margin-top: 30px;
            color: var(--ink);
        }}

        .reading-paragraph {{
            font-size: 1.05rem;
            line-height: 1.7;
            text-align: justify;
            margin-top: 10px;
            color: #222;
        }}

        .collision-box {{
            margin-top: 40px;
            padding: 20px;
            border: 1px solid var(--ink);
            background-color: #ECE9E4;
            position: relative;
        }}
        
        .collision-box::before {{
            content: "EXTERNAL COLLISION WARNING";
            position: absolute;
            top: -10px;
            left: 15px;
            background-color: #ECE9E4;
            padding: 0 10px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--accent);
        }}

        .collision-text {{
            font-size: 0.95rem;
            line-height: 1.6;
            margin: 0;
            font-style: italic;
        }}

        .footer-metrics {{
            position: absolute;
            bottom: 40px;
            left: 60px;
            right: 60px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            text-transform: uppercase;
            color: #888;
            display: flex;
            justify-content: space-between;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }}
        
        .card-glyph {{
            font-size: 1.8rem;
            font-family: serif;
            color: var(--accent);
        }}
        .card-glyph.black {{ color: var(--ink); }}
    </style>
</head>
<body>
"""

    # Generate only a 3-day sample to see the prototype
    for day_offset in range(3):
        current_date = start_date + datetime.timedelta(days=day_offset)
        period_idx = day_offset // 52
        planetary_period_name = ROWS[period_idx]
        
        fractal_day_idx = day_offset % 52
        fractal_card = full_chain[fractal_day_idx]
        
        global_card, _ = get_birth_card(current_date.month, current_date.day)
        global_card_location = get_card_location(global_card, yearly_grid, yearly_crown)
        collision_planet = global_card_location.get('row', 'Crown / Unanchored')
        
        # Determine Color for cards
        f_color = "black" if "♠" in fractal_card or "♣" in fractal_card else ""
        g_color = "black" if "♠" in global_card or "♣" in global_card else ""
        
        paragraph = generate_sentence(planetary_period_name, fractal_card, collision_planet)

        # Build Page
        html_content += f"""
    <!-- PAGE: DAY {day_offset + 1} -->
    <div class="book-page">
        <h1 class="header">
            {current_date.strftime("%a, %b %d")}
            <span class="date">Day {day_offset + 1:03d} / 364</span>
        </h1>
        
        <div class="metadata-bar">
            <div>Owner: <strong>{first_name.upper()}</strong></div>
            <div>Age Matrix: <strong>{spread_year}</strong></div>
            <div>Birth Anchor: <strong>{user_birth_card}</strong></div>
        </div>

        <div class="data-header">
            System Period: {planetary_period_name.upper()}
        </div>
        
        <div style="display: flex; align-items: center; margin-top: 10px;">
            <div style="font-size: 0.85rem; font-family: 'JetBrains Mono', monospace; margin-right: 15px;">FRACTAL VARIABLE:</div>
            <div class="card-glyph {f_color}">{fractal_card}</div>
        </div>

        <p class="reading-paragraph">
            {paragraph}
        </p>

        <div class="collision-box">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; margin-right: 15px; color: #555;">GLOBAL OVERRIDE:</div>
                <div class="card-glyph {g_color}" style="font-size: 1.4rem;">{global_card}</div>
            </div>
            <p class="collision-text">
                The global environment operates exactly at the {global_card} coordinate today. Because this variable lands mathematically inside your {collision_planet.upper()} line, {COLLISION_SUFFIXES.get(collision_planet, COLLISION_SUFFIXES['Crown / Unanchored']).lower()}
            </p>
        </div>

        <div class="footer-metrics">
            <div>Algorithm: Analog</div>
            <div>Print Authorization Valid</div>
            <div>ID: TAA-{target_year}-{first_name[:3].upper()}-{day_offset:04d}</div>
        </div>
    </div>
"""

    html_content += """
</body>
</html>
"""
    
    # Write to file
    with open("planner_prototype.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("Successfully generated beautifully formatted physical planner prototype.")


if __name__ == "__main__":
    generate_html_planner("Cassidy", 1991, 2, 17, target_year=2026)
