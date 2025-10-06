import re
import csv
import sys
from pathlib import Path

def sci_to_float(s):
    """Convert scientific notation like 0.2399731643E+00 to float"""
    try:
        return float(s.replace('E', 'e'))
    except Exception:
        return None

def parse_aim_file(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Split by CP blocks
    blocks = re.split(r'-{5,}\s*CP\s+', text)[1:]  # Skip header if present

    data = []
    for block in blocks:
        # CP number and type
        cp_match = re.search(r'(\d+),\s*Type\s*\((.*?)\)', block)
        if not cp_match:
            continue
        cp_number = cp_match.group(1)
        cp_type = f"({cp_match.group(2)})"

        # Initialize variable
        connection = ""

        # Case 1: Connected atoms line (for (3,-1) etc.)
        conn_match = re.search(r'Connected atoms:\s*(\d+)\((.*?)\)\s*--\s*(\d+)\((.*?)\)', block)
        if conn_match:
            connection = f"{conn_match.group(1)}{conn_match.group(2).strip()}-{conn_match.group(3)}{conn_match.group(4).strip()}"

        # Case 2: Corresponding nucleus line (for (3,-3))
        nuc_match = re.search(r'Corresponding nucleus:\s*(\d+)\((.*?)\)', block)
        if nuc_match:
            connection = f"{nuc_match.group(1)}{nuc_match.group(2).strip()}"

        # Extract values
        density_match = re.search(r'Density of all electrons:\s*([-\d\.E\+]+)', block)
        laplacian_match = re.search(r'Laplacian of electron density:\s*([-\d\.E\+]+)', block)
        g_match = re.search(r'Lagrangian kinetic energy G\(r\):\s*([-\d\.E\+]+)', block)
        v_match = re.search(r'Potential energy density V\(r\):\s*([-\d\.E\+]+)', block)

        row = {
            "CP Number": cp_number,
            "CP Type": cp_type,
            "Connected Atoms/Corresponding Nucleus": connection,
            "Density of all electrons": sci_to_float(density_match.group(1)) if density_match else None,
            "Laplacian of electron density": sci_to_float(laplacian_match.group(1)) if laplacian_match else None,
            "Lagrangian kinetic energy G(r)": sci_to_float(g_match.group(1)) if g_match else None,
            "Potential energy density V(r)": sci_to_float(v_match.group(1)) if v_match else None
        }
        data.append(row)

    return data

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_aim_data_v2.py <aim_output_file>")
        sys.exit(1)

    filename = sys.argv[1]
    data = parse_aim_file(filename)
    if not data:
        print("No critical point data found.")
        sys.exit(1)

    output_file = Path(filename).stem + "_AIM.csv"

    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "CP Number",
            "CP Type",
            "Connected Atoms/Corresponding Nucleus",
            "Density of all electrons",
            "Laplacian of electron density",
            "Lagrangian kinetic energy G(r)",
            "Potential energy density V(r)"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Extracted data written to: {output_file}")

if __name__ == "__main__":
    main()
