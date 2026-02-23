from app import engine, pdf_generator
import datetime
import os

def test_full_cycle():
    print("Testing Full Cycle: Calculation -> PDF")
    
    # 1. Calculation
    print("Step 1: Calculating Letter Data...")
    first_name = "Cassidy"
    b_year, b_month, b_day = 1991, 2, 17
    target_date = "2026-03-15"
    
    data = engine.calculate_letter_data(first_name, b_year, b_month, b_day, target_date)
    
    if "error" in data:
        print("ERROR:", data['error'])
        return
        
    print(f"Data Generated: Period={data['period']['card']}, LongRange={data['year_long']['long_range']}")
    
    # 2. Content Generation (Mock)
    content = f"""
This is a test letter for {first_name}.

The Pattern: {data['period']['card']} in {data['period']['planet']}.
The Year's Pressure: {data['year_long']['long_range']}.
The Excavation: {data['year_long']['pluto']}.
The Trajectory: {data['year_long']['result']}.

Displacement: {data['year_long']['displacement']}.
Environment: {data['year_long']['environment']}.

This PDF proves the engine is integrated correctly.
    """
    
    # 3. PDF Generation
    print("Step 2: Generating PDF...")
    filename = f"test_full_{first_name}.pdf"
    pdf_path = os.path.join(os.getcwd(), filename)
    
    try:
        pdf_generator.build_pdf(pdf_path, "MARCH 2026", first_name, content)
        print(f"SUCCESS: PDF created at {pdf_path}")
    except Exception as e:
        print(f"FAILURE: PDF generation failed: {e}")

if __name__ == "__main__":
    test_full_cycle()
