import os
import csv
import glob
import re
import sys

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:
    tk = None


print('pdf_to_csv.py loaded')


def parse_line(line):
    # Find price (e.g. 49470.00 or 49.470,00)
    price_pattern = r"(\d+[\.,]\d{2})"
    price_match = re.search(price_pattern, line)
    if not price_match:
        return None

    price = price_match.group(1)
    before_price = line[:price_match.start()].strip()
    after_price = line[price_match.end():].strip()

    parts = before_price.split()
    if not parts:
        return None

    invent_num = parts[0]

    bud = ''
    mist = ''
    nazev_parts = []

    for i in range(len(parts) - 1, 0, -1):
        p = parts[i]
        if mist == '' and (p.isdigit() and len(p) > 1 or (any(c.isalpha() for c in p) and any(c.isdigit() for c in p))):
            mist = p
            continue
        if bud == '' and p.isdigit() and len(p) == 1:
            bud = p
            nazev_parts = parts[1:i]
            break

    if not nazev_parts:
        candidates = []
        for i, p in enumerate(parts[1:], 1):
            if p.isdigit() or (any(c.isalpha() for c in p) and any(c.isdigit() for c in p)):
                candidates.append((i, p))
        if len(candidates) >= 2:
            bud_idx, bud = candidates[-2]
            mist_idx, mist = candidates[-1]
            nazev_parts = parts[1:bud_idx]
        elif len(candidates) == 1:
            mist = candidates[-1][1]
            nazev_parts = parts[1:candidates[-1][0]]
        else:
            nazev_parts = parts[1:]

    nazev = ' '.join(nazev_parts).strip()

    odpov_prac = ''
    u_d_zby = ''
    poznamka = ''

    parts_after = after_price.split()
    if parts_after:
        name_parts = []
        idx = 0
        for i, part in enumerate(parts_after):
            if not any(c.isdigit() for c in part) and part and part[0].isupper():
                name_parts.append(part)
                idx = i + 1
                if len(name_parts) >= 2:
                    break
            elif name_parts:
                break
        if name_parts:
            odpov_prac = ' '.join(name_parts)

        rest = parts_after[idx:]
        if rest:
            u_parts = []
            p_parts = []
            for part in rest:
                if any(c.isdigit() for c in part):
                    u_parts.append(part)
                else:
                    p_parts.append(part)
            u_d_zby = ' '.join(u_parts).strip()
            poznamka = ' '.join(p_parts).strip()

    return {
        'Invent.číslo': invent_num,
        'Název': nazev,
        'Bud': bud,
        'Míst': mist,
        'Pořiz.cena': price,
        'Odpov.prac': odpov_prac,
        'Ú D.zby': u_d_zby,
        'Poznámka': poznamka
    }


def extract_table_rows_from_text(text):
    """Extract table rows and the 'Středisko' value from a page text."""
    rows = []
    if not text:
        return rows

    lines = text.split('\n')

    stredisko = ''
    for line in lines[:20]:
        if 'Středisko' in line and ':' in line:
            parts = line.split(':')
            if len(parts) > 1:
                stredisko = parts[1].strip()
            break

    header_idx = -1
    for i, line in enumerate(lines):
        if 'Invent.číslo' in line and 'Název' in line:
            header_idx = i
            break

    if header_idx == -1:
        return rows

    for line in lines[header_idx + 1:]:
        if not line.strip() or '---' in line or '===' in line or '+++' in line:
            continue
        if any(skip in line for skip in ['Součet', 'Množství', 'Celkem', 'Rozpočet',
                                        'Pozn', 'GINISEXPRESS', 'IČO', 'Lic',
                                        'Období', 'Čas', 'Datum', 'Strana',
                                        'Inventární', 'Začato', 'Skončeno', 'Místo vyhotovení',
                                        'Potvrzuji', 'Vedoucí', 'Odpovědný', 'Datum vyhotovení']):
            continue

        row = parse_line(line)
        if row:
            row['Středisko'] = stredisko
            rows.append(row)

    return rows


def process_pdfs_to_csv(input_dir, output_file='output.csv'):
    """Process all PDFs in `input_dir` and write structured CSV to `output_file`."""
    if pdfplumber is None:
        print('Chyba: modul pdfplumber není nainstalovaný. Nainstaluj závislosti: pip install -r requirements.txt')
        return

    if not os.path.exists(input_dir):
        print(f"Složka '{input_dir}' neexistuje!")
        return

    pdf_files = sorted(glob.glob(os.path.join(input_dir, '*.pdf')))
    if not pdf_files:
        print(f"Žádné PDF soubory nenalezeny ve složce '{input_dir}'!")
        return

    print(f"Nalezeno {len(pdf_files)} PDF souborů ve '{input_dir}'\n")

    all_data = []
    for pdf_file in pdf_files:
        print(f"Čtu: {pdf_file}")
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text() or ''
                    rows = extract_table_rows_from_text(text)
                    all_data.extend(rows)
                    if rows:
                        print(f"  Strana {page_num + 1}: +{len(rows)} záznamů")
        except Exception as e:
            print(f"  Chyba při čtení {pdf_file}: {e}")

    if all_data:
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Invent.číslo', 'Středisko', 'Název', 'Bud', 'Míst', 'Pořiz.cena', 'Odpov.prac', 'Ú D.zby', 'Poznámka']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                for r in all_data:
                    row_out = {k: r.get(k, '') for k in fieldnames}
                    writer.writerow(row_out)

            print(f"\n✓ Data úspěšně uložena do {output_file}")
            print(f"Celkem záznamů: {len(all_data)}")
        except Exception as e:
            print(f"Chyba při zápisu do CSV: {e}")
    else:
        print('\nŽádná data k uložení!')


def choose_input_dir_via_gui_or_console():
    """Select a directory using available GUI tool or console fallback.

    Order tried:
      1) tkinter
      2) zenity (Linux)
      3) kdialog (KDE)
      4) yad
      5) PyGObject (Gtk.FileChooser)
      6) console input / default 'sbirky'
    """
    import shutil
    selected = None

    # 1) tkinter
    if tk is not None:
        try:
            root = tk.Tk()
            root.withdraw()
            selected = filedialog.askdirectory(title='Vyber složku se sbirkami', initialdir=os.getcwd())
            root.destroy()
            if selected:
                return selected
        except Exception:
            selected = None

    # 2) zenity
    if shutil.which('zenity'):
        try:
            import subprocess
            p = subprocess.run(['zenity', '--file-selection', '--directory', '--title', 'Vyber složku se sbirkami', '--filename', os.getcwd() + '/'], capture_output=True, text=True)
            if p.returncode == 0:
                sel = p.stdout.strip()
                if sel:
                    return sel
        except Exception:
            pass

    # 3) kdialog (KDE)
    if shutil.which('kdialog'):
        try:
            import subprocess
            p = subprocess.run(['kdialog', '--getexistingdirectory', os.getcwd(), '--title', 'Vyber složku se sbirkami'], capture_output=True, text=True)
            if p.returncode == 0:
                sel = p.stdout.strip()
                if sel:
                    return sel
        except Exception:
            pass

    # 4) yad
    if shutil.which('yad'):
        try:
            import subprocess
            p = subprocess.run(['yad', '--file', '--directory', '--title', 'Vyber složku se sbirkami', '--filename', os.getcwd() + '/'], capture_output=True, text=True)
            if p.returncode == 0:
                sel = p.stdout.strip()
                if sel:
                    return sel
        except Exception:
            pass

    # 5) PyGObject gtk file chooser
    try:
        from gi.repository import Gtk
        dialog = Gtk.FileChooserDialog(title='Vyber složku se sbirkami', action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        dialog.set_current_folder(os.getcwd())
        resp = dialog.run()
        if resp == Gtk.ResponseType.OK:
            sel = dialog.get_filename()
            dialog.destroy()
            if sel:
                return sel
        dialog.destroy()
    except Exception:
        pass

    # 6) console fallback
    try:
        prompt = f"Zadej cestu ke slozce (stiskni Enter pro '{os.path.join(os.getcwd(), 'sbirky')}'): "
        user_in = input(prompt).strip()
    except Exception:
        user_in = ''

    if user_in:
        return user_in

    return os.path.join(os.getcwd(), 'sbirky')


if __name__ == '__main__':
    input_dir = None
    output_file = 'output.csv'
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = choose_input_dir_via_gui_or_console()

    # Optional second arg: output file
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    process_pdfs_to_csv(input_dir=input_dir, output_file=output_file)
