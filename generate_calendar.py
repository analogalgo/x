import datetime
import math
from app.engine import get_birth_card, get_spread_year, generate_yearly_spread_data, extract_chain, ROWS

def get_card_location(card, grid, crown):
    """Finds where a specific card is located in a given spread."""
    for ri, rn in enumerate(ROWS):
        if card in grid[rn]:
            return {"type": "grid", "row": rn, "col_idx": grid[rn].index(card)}
    
    if card in crown:
        return {"type": "crown", "idx": crown.index(card)}
        
    return {"type": "unknown"}

def generate_daily_calendar(first_name, birth_year, birth_month, birth_day, target_year=2026):
    """
    Generates a 364-day calendar starting from the user's birthday in the target_year.
    Combines:
    1. The Planetary Period (Mercury, Venus, etc.)
    2. The Fractal Walk Card (Card 1-52 of their spread cycle)
    3. The Global Daily Card Collision (Calendar date's birth card vs User's Spread)
    """
    # 1. Base Calcs
    user_birth_card, sv = get_birth_card(birth_month, birth_day)
    
    # Set the start date to their birthday in the target year
    start_date = datetime.date(target_year, birth_month, birth_day)
    age = target_year - birth_year
    spread_year = min(max(age + 1, 1), 90)
    
    # 2. Extract their specific yearly grid and a full 52-card chain
    yearly_grid, yearly_crown = generate_yearly_spread_data(spread_year)
    full_chain = extract_chain(yearly_grid, yearly_crown, user_birth_card, 52)
    
    calendar_data = []
    
    # 3. Walk through 364 days (7 periods x 52 days)
    for day_offset in range(364):
        current_date = start_date + datetime.timedelta(days=day_offset)
        
        # --- METHOD 1: The Fractal Walk ---
        period_idx = day_offset // 52
        planetary_period_name = ROWS[period_idx]
        
        # Day within the 52-day period (0-51)
        fractal_day_idx = day_offset % 52
        fractal_card = full_chain[fractal_day_idx]
        
        # --- METHOD 2: The Global Collision ---
        # What is the global card for this exact calendar date?
        global_card, _ = get_birth_card(current_date.month, current_date.day)
        
        # Where does this Global Card sit in the User's personal yearly spread?
        global_card_location = get_card_location(global_card, yearly_grid, yearly_crown)
        collision_planet = global_card_location.get('row', 'Crown / Unanchored')
        
        # Build the daily entry
        day_data = {
            "date": current_date.strftime("%Y-%m-%d"),
            "day_of_year": day_offset + 1,
            "period": planetary_period_name,
            "fractal_card": fractal_card,
            "global_card": global_card,
            "collision_planet": collision_planet
        }
        calendar_data.append(day_data)
        
    return calendar_data

if __name__ == "__main__":
    import json
    # Test generation for a specific user
    print("Generating 364-day Analog Calendar Matrix...")
    cal = generate_daily_calendar("Cassidy", 1991, 2, 17, target_year=2026)
    
    with open("cassidy_2026_calendar.txt", "w", encoding="utf-8") as f:
        f.write("--- SAMPLE: FIRST 7 DAYS (MERCURY PERIOD) ---\n")
        for day in cal[:7]:
            f.write(f"Date: {day['date']} (Day {day['day_of_year']})\n")
            f.write(f"  System Period: {day['period']}\n")
            f.write(f"  Fractal Card:  {day['fractal_card']}\n")
            f.write(f"  Global Card:   {day['global_card']} (Sits in your {day['collision_planet']} line)\n")
            f.write("-" * 40 + "\n")
            
        f.write("\n--- SAMPLE: SHIFT TO VENUS PERIOD (DAY 53) ---\n")
        day_53 = cal[52]
        f.write(f"Date: {day_53['date']} (Day {day_53['day_of_year']})\n")
        f.write(f"  System Period: {day_53['period']}\n")
        f.write(f"  Fractal Card:  {day_53['fractal_card']}\n")
        f.write(f"  Global Card:   {day_53['global_card']} (Sits in your {day_53['collision_planet']} line)\n")
        f.write("-" * 40 + "\n")
        
    print("Successfully wrote output to cassidy_2026_calendar.txt")
