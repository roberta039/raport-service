import datetime
import random
from fpdf import FPDF
import streamlit as st

# -----------------------
# 1. Funcții de dată
# -----------------------

def get_prev_month_year():
    """Returnează (an, luna) pentru luna trecută din anul curent."""
    today = datetime.date.today()
    if today.month == 1:
        # ianuarie -> luna trecută este decembrie anul anterior
        return today.year - 1, 12
    return today.year, today.month - 1

def nume_luna_ro(month: int) -> str:
    luni = {
        1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie",
        5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August",
        9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
    }
    return luni[month]

def zile_lucratoare_grupate_pe_saptamani(year: int, month: int):
    """
    Returnează un dict:
      { index_saptamana (0-based) : [lista de date (date) care sunt luni-vineri] }
    """
    start = datetime.date(year, month, 1)
    # calculăm ultima zi a lunii:
    if month == 12:
        end = datetime.date(year, 12, 31)
    else:
        end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    weeks = {}
    current = start
    while current <= end:
        # doar zile lucrătoare: 0 = luni, ..., 4 = vineri
        if current.weekday() < 5:
            idx = (current.day - 1) // 7  # 0,1,2,3,... pentru fiecare "săptămână" din lună
            weeks.setdefault(idx, []).append(current)
        current += datetime.timedelta(days=1)
    return weeks

def alege_zile_random(weeks_dict, max_zile=4):
    """
    Alege aleator câte o zi lucrătoare din fiecare săptămână (cheie din weeks_dict),
    dar maxim max_zile în total.
    """
    selected = []
    # iterăm săptămânile în ordine
    for idx in sorted(weeks_dict.keys()):
        if len(selected) >= max_zile:
            break
        zile_sapt = weeks_dict[idx]
        if zile_sapt:
            selected.append(random.choice(zile_sapt))
    return selected

# -----------------------
# 2. Generare PDF
# -----------------------

def genereaza_pdf(an: int, luna: int, zile_selectate):
    """
    Creează PDF-ul raportului într-un format apropiat de model:
    - antet firmă
    - titlu SESIZARE/RAPORT DE SERVICE
    - Luna: <NumeLuna><An>
    - tabel cu "Defecte constatate" + Data
    - câmp "Sosire" = ultima zi din lista selectată
    Returnează bytes (pentru download).
    """
    luna_str = f"{nume_luna_ro(luna)}{an}"

    pdf = FPDF()
    pdf.add_page()

    # Antet firmă
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 7, "S.C. CREATIVE WEBDEV S.R.L.", ln=1, align="C")
    pdf.cell(0, 7, "SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10,", ln=1, align="C")
    pdf.cell(0, 7, "SECTOR 4, BUCURESTI - Romania", ln=1, align="C")
    pdf.ln(5)

    # Titlu
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "***SESIZARE/RAPORT DE SERVICE***", ln=1, align="C")
    pdf.ln(3)

    # Luna
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 7, f"Luna: {luna_str}", ln=1, align="L")
    pdf.ln(3)

    # Tabel simplificat "Defecte constatate"
    pdf.set_font("Arial", size=10)
    col1_w = pdf.w * 0.6
    col2_w = pdf.w * 0.3
    th = 8  # înălțime rând

    # header tabel
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col1_w, th, "Defecte constatate", border=1, align="C")
    pdf.cell(col2_w, th, "Data", border=1, ln=1, align="C")

    pdf.set_font("Arial", size=10)
    if not zile_selectate:
        pdf.cell(col1_w, th, "-", border=1, align="L")
        pdf.cell(col2_w, th, "-", border=1, ln=1, align="C")
    else:
        for d in zile_selectate:
            # descriere generică, după modelul tău:
            descriere = "Verificare si intretinere retea de calculatoare."
            pdf.cell(col1_w, th, descriere, border=1, align="L")
            pdf.cell(col2_w, th, d.strftime("%d/%m/%Y"), border=1, ln=1, align="C")

    pdf.ln(5)

    # Câmp "Sosire" = ultima zi din listă (dacă există)
    if zile_selectate:
        ultima = max(zile_selectate)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, f"Sosire: {ultima.strftime('%d/%m/%Y')}", ln=1, align="R")

    # Returnează PDF ca bytes (compatibil cu fpdf2)
    return pdf.output(dest="S")

# -----------------------
# 3. Aplicația Streamlit
# -----------------------

def main():
    st.title("Generator Raport de Service (PDF)")

    st.write(
        "Aplicație care generează automat un raport de service în PDF "
        "pentru **luna trecută** din anul curent, alegând aleator "
        "câte o zi lucrătoare din fiecare săptămână (maxim 4 zile)."
    )

    if st.button("Generează raport pentru luna trecută"):
        # 1. determinăm luna trecută
        an, luna = get_prev_month_year()

        # 2. toate zilele lucrătoare grupate pe săptămâni
        weeks = zile_lucratoare_grupate_pe_saptamani(an, luna)

        # 3. selectăm random câte o zi/săptămână, max 4
        zile_selectate = alege_zile_random(weeks, max_zile=4)

        # 4. generăm PDF-ul
        pdf_bytes = genereaza_pdf(an, luna, zile_selectate)

        # Info pe ecran
        st.success(
            f"Raport generat pentru **{nume_luna_ro(luna)} {an}** "
            f"cu {len(zile_selectate)} zile de intervenție."
        )
        st.write("Zilele alese:")
        for d in sorted(zile_selectate):
            st.write("-", d.strftime("%d/%m/%Y"))

        # 5. Buton de download
        file_name = f"Raport_Service_{nume_luna_ro(luna)}{an}.pdf"
        st.download_button(
            label="Descarcă raportul PDF",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()
