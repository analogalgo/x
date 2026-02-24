import os
import subprocess
from generate_calendar_html import generate_html_planner

def export_to_print(first_name, birth_year, birth_month, birth_day, target_year=2026):
    print(f"1. Calculating 364-day Analog Matrix for {first_name}...")
    generate_html_planner(first_name, birth_year, birth_month, birth_day, target_year)
    
    html_file = "planner_prototype.html"
    pdf_file = f"Analog_Planner_{first_name}_{target_year}.pdf"
    
    print("2. Firing formatting engine and printing to physical PDF layout...")
    # Use playwright CLI because it handles async loops cleanly on Windows
    cmd = f'playwright pdf {html_file} {pdf_file}'
    subprocess.run(cmd, shell=True, check=True)
    
    print(f"3. SUCCESS! Your master print file is ready at: {pdf_file}")

if __name__ == "__main__":
    export_to_print("Cassidy", 1991, 2, 17, 2026)
