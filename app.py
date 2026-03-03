import datetime
import random
from fpdf import FPDF
import streamlit as st
from io import BytesIO

# -------------------------------------------------
# 1. Funcții de dată și logică a zilelor
# -------------------------------------------------
def get_prev_month_year():
    """Returnează (an, luna) pentru luna trecută din anul curent."""
    today = datetime.date.today()
    if today.month == 1:
        # ianuarie -> luna trecută este decembrie anul anterior
        return today.year - 1, 12
    return today.year, today.month - 1

def nume_luna_ro(month: int) -> str:
    """Returnează denumirea lunii în limba română."""
    luni = {
        1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie",
        5: "Mai", 6: "Iunie", 7: "Iulie", 8: "August",
        9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
    }
    return luni[month]

def zile_lucratoare_grupate_pe_saptamani(year: int, month: int):
    """
    Returnează un dicționar:
        { index_saptamana (0-based) : [lista de date (date) care sunt luni‑vineri] }
    """
    start = datetime.date(year, month, 1)
    if month == 12:
        end = datetime.date(year, 12, 31)
    else:
        end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    weeks = {}
    current = start
    while current <= end:
        if current.weekday() < 5:  # doar zile de luni‑vineri
            idx = (current.day - 1) // 7
            weeks.setdefault(idx, []).append(current)
        current += datetime.timedelta(days=1)
    return weeks

def alege_zile_random(weeks_dict, max_zile=4):
    """
    Alege aleator câte o zi lucrătoare din fiecare săptămână (cheie din weeks_dict),
    dar maxim max_zile în total.
    """
    selected = []
    for idx in sorted(weeks_dict.keys()):
        if len(selected) >= max_zile:
            break
        zile_sapt = weeks_dict[idx]
        if zile_sapt:
            selected.append(random.choice(zile_sapt))
    return selected

# -------------------------------------------------
# 2. Generare PDF – structură conform modelului
# -------------------------------------------------
def genereaza_pdf(an: int, luna: int, zile_selectate):
    """
    Creează PDF‑ul cu layout cât mai apropiat de tabelul original
    (generat de la zero, fără conversie DOCX → PDF).
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Margini
    left_margin = 10
    right_margin = 10
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    total_width = pdf.w - left_margin - right_margin

    # -------------------------------------------------
    # Antet firmă – aliniat la stânga
    # -------------------------------------------------
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 7, "S.C. CREATIVE WEBDEV S.R.L.", ln=1, align="L")
    pdf.cell(0, 7, "SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10,", ln=1, align="L")
    pdf.cell(0, 7, "SECTOR 4, BUCURESTI - Romania", ln=1, align="L")
    pdf.ln(3)

    # -------------------------------------------------
    # Titlu central
    # -------------------------------------------------
    pdf.set_font("Arial", "B", size=14)
    pdf.cell(0, 10, "***SESIZARE/RAPORT DE SERVICE***", ln=1, align="C")
    pdf.ln(3)

    # -------------------------------------------------
    # Două corpuri sub titlu:
    #  - stânga: câmpuri beneficiar
    #  - dreapta: lună / date / ore / abonament etc.
    # -------------------------------------------------
    left_width = 80          # coloană stânga
    right_width = total_width - left_width

    def write_left_right(label_left, value_right):
        pdf.set_font("Arial", "B", size=10)
        pdf.cell(left_width, 6, label_left, border=1, align="L")
        pdf.set_font("Arial", size=10)
        pdf.cell(right_width, 6, value_right, border=1, align="L", ln=1)

    # Bloc stânga: Beneficiar & date contract (etichetă, serie etc.)
    write_left_right("Produs", "Revizie")
    write_left_right("Beneficiar", "SC Inkorporate SRL")
    write_left_right("Adresa", "Str. Esarfei 64-66")
    write_left_right("Localitate", "Bucuresti")
    write_left_right("Telefon", "")
    write_left_right("Serie", "")
    write_left_right("Nr Contr.", "")
    write_left_right("Valoare Abonament", "")
    write_left_right("Anunta", "")

    # Bloc dreapta: lună / timp (în această implementare folosim același „schelet”
    # dar valorile relevante sunt luna și sosirea)
    luna_str = f"{nume_luna_ro(luna)}{an}"
    data_sosire = max(zile_selectate).strftime("%d/%m/%Y") if zile_selectate else ""

    write_left_right("Luna", luna_str)
    write_left_right("Lansare (Data/Ora)", "")
    write_left_right("Trimitere (Data/Ora)", "")
    write_left_right("Sosire (Data/Ora)", data_sosire)

    pdf.ln(4)

    # -------------------------------------------------
    # Corp „Defecte sesizate” – pe mijloc
    # -------------------------------------------------
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(0, 6, "Defecte sesizate", ln=1, align="C")
    pdf.ln(2)

    # -------------------------------------------------
    # Corp „Defecte constatate”
    #  - în stânga textul „Defecte constatate”
    #  - în dreapta datele la care s-au făcut verificările/întreținerea
    # -------------------------------------------------
    label_width = 45
    text_width = total_width - label_width

    pdf.set_font("Arial", "B", size=10)
    pdf.cell(label_width, 6, "Defecte constatate", border=1, align="L")
    pdf.cell(text_width, 6, "", border=1, ln=1)

    pdf.set_font("Arial", size=10)
    descriere = "Verificare si intretinere retea de calculatoare."
    zile_sortate = sorted(zile_selectate)

    # max 4 rânduri, conform cerinței
    for i in range(4):
        stanga = "" if i > 0 else ""  # prima linie deja are labelul sus, rândurile 2–4 doar conținut
        if i < len(zile_sortate):
            text = f"{zile_sortate[i].strftime('%d/%m/%Y')} - {descriere}"
        else:
            text = ""
        pdf.cell(label_width, 6, stanga, border=1, align="L")
        pdf.cell(text_width, 6, text, border=1, ln=1, align="L")

    pdf.ln(5)

    # -------------------------------------------------
    # Trei corpuri:
    #  - stânga: Tip interventie
    #  - mijloc: Rezultat
    #  - dreapta: Cauza nerezolvarii
    # -------------------------------------------------
    pdf.set_font("Arial", "B", size=10)
    col_tip = 60
    col_rezultat = 60
    col_cauza = total_width - col_tip - col_rezultat

    # Header
    pdf.cell(col_tip, 7, "Tip interventie", border=1, align="C")
    pdf.cell(col_rezultat, 7, "Rezultat", border=1, align="C")
    pdf.cell(col_cauza, 7, "Cauza nerezolvarii", border=1, align="C", ln=1)

    pdf.set_font("Arial", size=10)

    # Rânduri (simplificate, dar corespondente modelului)
    randuri = [
        ("Garantie", "Rezolvata", "Lipsa Componente"),
        ("Constatare", "", "Insatisfactie Client"),
        ("Revizie", "", ""),
        ("Instalare", "Preluare Echipament", ""),
        ("Reinstalare", "Fara Accesorii", ""),
        ("Mutare", "Cu Accesorii", ""),
        ("Incasare", "", "Linie Telefonica defecta"),
        ("Rutina", "Furnizat echipament back-up", ""),
        ("Programare", "Model/obs.: ____________________", ""),
        ("Reprogramare", "S/N: ____________________", ""),
    ]

    for tip, rezultat, cauza in randuri:
        pdf.cell(col_tip, 6, tip, border=1, align="L")
        pdf.cell(col_rezultat, 6, rezultat, border=1, align="L")
        pdf.cell(col_cauza, 6, cauza, border=1, align="L", ln=1)

    pdf.ln(5)

    # -------------------------------------------------
    # Sub cele 3 corpuri:
    #  - stânga: Inginer service + Marca
    #  - dreapta: Confirmare client nume + LS
    # -------------------------------------------------
    left_part_width = total_width / 2
    right_part_width = total_width / 2

    pdf.set_font("Arial", size=10)
    pdf.cell(left_part_width, 7, "Inginer service: __________________   Marca: __________________", border=1, align="L")
    pdf.cell(right_part_width, 7, "Confirmare client nume: __________________   LS: ____________", border=1, align="L", ln=1)

    # Returnăm PDF ca bytes pentru Streamlit
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# -------------------------------------------------
# 3. Aplicația Streamlit
# -------------------------------------------------
def main():
    st.title("Generator Raport de Service (PDF)")

    st.write(
        "Aplicație care generează automat un raport de service în PDF "
        "pentru **luna trecută** din anul curent, alegând aleator "
        "câte o zi lucrătoare din fiecare săptămână (maxim 4 zile), "
        "într-un format apropiat de modelul tău."
    )

    if st.button("Generează raport pentru luna trecută"):
        # determinăm luna trecută
        an, luna = get_prev_month_year()

        # zile lucrătoare grupate pe săptămâni
        weeks = zile_lucratoare_grupate_pe_saptamani(an, luna)

        # selectăm random câte o zi/săptămână, max 4
        zile_selectate = alege_zile_random(weeks, max_zile=4)

        # generăm PDF‑ul
        pdf_bytes = genereaza_pdf(an, luna, zile_selectate)

        # Mesaj în UI
        st.success(
            f"Raport generat pentru **{nume_luna_ro(luna)} {an}** "
            f"cu {len(zile_selectate)} zile de intervenție."
        )
        st.write("Zilele alese:")
        for d in sorted(zile_selectate):
            st.write("-", d.strftime("%d/%m/%Y"))

        # Buton de download
        file_name = f"Sesiz_Raport_de_Service_{nume_luna_ro(luna)}{an}.pdf"
        st.download_button(
            label="Descarcă raportul PDF",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()
