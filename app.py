import datetime
import random
from fpdf import FPDF
import streamlit as st
from io import BytesIO

# -------------------------------------------------
# 1. Funcții pentru dată
# -------------------------------------------------
def get_prev_month_year():
    """Returnează (an, luna) pentru luna trecută din anul curent."""
    today = datetime.date.today()
    if today.month == 1:
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
    if month == 12:
        end = datetime.date(year, 12, 31)
    else:
        end = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

    weeks = {}
    current = start
    while current <= end:
        if current.weekday() < 5:  # luni–vineri
            idx = (current.day - 1) // 7
            weeks.setdefault(idx, []).append(current)
        current += datetime.timedelta(days=1)
    return weeks

def alege_zile_random(weeks_dict, max_zile=4):
    """
    Alege aleator câte o zi lucrătoare din fiecare săptămână, dar maxim max_zile în total.
    """
    selected = []
    for idx in sorted(weeks_dict.keys()):
        if len(selected) >= max_zile:
            break
        zile_sapt = weeks_dict[idx]
        if zile_sapt:
            selected.append(random.choice(zile_sapt))
    # dacă sunt mai puțin de 4 săptămâni lucrătoare în luna respectivă,
    # se poate întâmpla să ai sub 4 zile; asta respectă cerința „maxim 4”.
    return selected

# -------------------------------------------------
# 2. Generare PDF – layout după modelul DOCX
# -------------------------------------------------
def genereaza_pdf(an: int, luna: int, zile_selectate):
    """
    Creează PDF-ul raportului cu layout apropiat 1:1 de modelul
    „Sesiz-Raport de Service_INK 2026.docx”.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    left_margin = 10
    right_margin = 10
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)

    # --------------------
    # Antet firmă (sus)
    # --------------------
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 7, "S.C. CREATIVE WEBDEV S.R.L.", ln=1, align="C")
    pdf.cell(0, 7, "SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10,", ln=1, align="C")
    pdf.cell(0, 7, "SECTOR 4, BUCURESTI - Romania", ln=1, align="C")
    pdf.ln(3)

    # --------------------
    # Titlu SESIZARE/RAPORT DE SERVICE
    # --------------------
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "***SESIZARE/RAPORT DE SERVICE***", ln=1, align="C")
    pdf.ln(3)

    # --------------------
    # Bloc date generale (în spiritul tabelului din model)
    # --------------------
    pdf.set_font("Arial", size=10)

    # vom face linii tip: Label (bold) | Valoare | spațiu liber (pentru seamăn cu tabelul cu multe coloane)
    col_label = 40
    col_value = 70
    col_extra = pdf.w - left_margin - right_margin - col_label - col_value

    def row3(label_bold, value="", extra=""):
        pdf.set_font("Arial", "B", 10)
        pdf.cell(col_label, 6, label_bold, border=1)
        pdf.set_font("Arial", 10)
        pdf.cell(col_value, 6, value, border=1)
        pdf.cell(col_extra, 6, extra, border=1, ln=1)

    # câmpuri, conform modelului tău, cu valorile tale de exemplu
    row3("Produs", "Revizie", "")
    row3("Beneficiar", "SC Inkorporate SRL", "")
    row3("Adresa", "Str. Esarfei 64-66", "")
    row3("Localitate", "Bucuresti", "")
    row3("Telefon", "", "Fax")
    row3("Serie", "", "Eticheta")
    row3("Nr Contr.", "", "Contr.")
    row3("Valoare Abonament", "", "")
    row3("Anunta", "", "")

    # câmpuri temporale
    luna_str = f"{nume_luna_ro(luna)}{an}"
    data_lansare = ""  # poți completa dacă vrei să generezi automat
    ora_lansare = ""
    data_trimitere = ""
    ora_trimitere = ""
    data_sosire = max(zile_selectate).strftime("%d/%m/%Y") if zile_selectate else ""
    ora_sosire = ""

    # linie specială pentru „Luna / Data / Ora”
    # facem un rând cu trei sub-câmpuri
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_label, 6, "Luna", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(40, 6, luna_str, border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 6, "Data", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(25, 6, "", border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(15, 6, "Ora", border=1)
    pdf.set_font("Arial", 10)
    rest_width = pdf.w - left_margin - right_margin - col_label - 40 - 20 - 25 - 15
    pdf.cell(rest_width, 6, "", border=1, ln=1)

    # Linia „Lansare Data/Ora”
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_label, 6, "Lansare", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(40, 6, data_lansare, border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 6, "Ora", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(25, 6, ora_lansare, border=1)
    pdf.cell(15, 6, "", border=1)
    pdf.cell(rest_width, 6, "", border=1, ln=1)

    # Linia „Trimitere Data/Ora”
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_label, 6, "Trimitere", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(40, 6, data_trimitere, border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 6, "Ora", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(25, 6, ora_trimitere, border=1)
    pdf.cell(15, 6, "", border=1)
    pdf.cell(rest_width, 6, "", border=1, ln=1)

    # Linia „Sosire Data/Ora”
    pdf.set_font("Arial", "B", 10)
    pdf.cell(col_label, 6, "Sosire", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(40, 6, data_sosire, border=1)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(20, 6, "Ora", border=1)
    pdf.set_font("Arial", 10)
    pdf.cell(25, 6, ora_sosire, border=1)
    pdf.cell(15, 6, "", border=1)
    pdf.cell(rest_width, 6, "", border=1, ln=1)

    pdf.ln(4)

    # --------------------
    # Tabel „Defecte Constatate”
    # (exact ca în model: 1 col „Defecte Constatate”, 4 rânduri cu date+descriere)
    # --------------------
    table_width = pdf.w - left_margin - right_margin
    pdf.set_font("Arial", "B", 10)
    pdf.cell(50, 7, "Defecte Constatate", border=1)
    pdf.cell(table_width - 50, 7, "", border=1, ln=1)

    pdf.set_font("Arial", 10)
    descriere = "Verificare si intretinere retea de calculatoare."

    # în model sunt 4 rânduri; dacă avem mai puțin de 4 zile, completăm doar câte avem
    zile_sortate = sorted(zile_selectate)
    for i in range(4):
        pdf.cell(50, 6, "" if i > 0 else "", border=1)  # prima linie are header-ul în model, dar aici îl lăsăm gol ca în rândurile 2-4
        if i < len(zile_sortate):
            text = f"{zile_sortate[i].strftime('%d/%m/%Y')} - {descriere}"
        else:
            text = ""
        pdf.cell(table_width - 50, 6, text, border=1, ln=1)

    pdf.ln(5)

    # --------------------
    # Tabel „Tip Interventie / Rezultat / ...”
    # după structura din model (tip, X-uri, cauze etc.)
    # --------------------
    pdf.set_font("Arial", "B", 10)

    # Lățimi de coloană aproximate după model (ajustate la lățimea paginii)
    col_t_interv = 35
    col_x1 = 10
    col_x2 = 10
    col_text_lung = 45
    col_x3 = 10
    col_rezultat = 45
    col_cauza = 30
    col_nerez = 30
    total_w = col_t_interv + col_x1 + col_x2 + col_text_lung + col_x3 + col_rezultat + col_cauza + col_nerez
    max_w = pdf.w - left_margin - right_margin
    if total_w > max_w:
        factor = max_w / total_w
        col_t_interv = int(col_t_interv * factor)
        col_x1 = int(col_x1 * factor)
        col_x2 = int(col_x2 * factor)
        col_text_lung = int(col_text_lung * factor)
        col_x3 = int(col_x3 * factor)
        col_rezultat = int(col_rezultat * factor)
        col_cauza = int(col_cauza * factor)
        col_nerez = int(col_nerez * factor)

    # Header principal: Tip Interventie / Rezultat / Cauza / Nerezolvarii
    pdf.cell(col_t_interv, 7, "***Tip Interventie***", border=1)
    pdf.cell(col_x1, 7, "", border=1)
    pdf.cell(col_x2, 7, "", border=1)
    pdf.cell(col_text_lung, 7, "", border=1)
    pdf.cell(col_x3, 7, "", border=1)
    pdf.cell(col_rezultat, 7, "***Rezultat***", border=1)
    pdf.cell(col_cauza, 7, "***Cauza***", border=1)
    pdf.cell(col_nerez, 7, "***Nerezolvarii***", border=1, ln=1)

    pdf.set_font("Arial", 10)

    # Rânduri, după modelul textului tău (fără să încercăm să desenăm exact toate X-urile, dar păstrând structura):
    randuri = [
        ("Garantie", "", "", "", "", "Rezolvata", "", "Lipsa Componente"),
        ("Constatare", "", "", "", "", "", "", "Insatisfactie Client"),
        ("Revizie", "", "X", "", "", "", "", ""),
        ("Instalare", "", "", "", "", "Preluare Echipament", "", ""),
        ("Reinstalare", "", "", "", "", "Fara Accesorii", "", ""),
        ("Mutare", "", "", "", "", "Cu Accesorii", "", ""),
        ("Incasare", "", "", "", "", "", "Linie Telefonica defecta", ""),
        ("Rutina", "", "", "Furnizat echipament back-up", "", "", "", ""),
        ("Programare", "", "", "Model/obs.: ____________________", "", "", "", ""),
        ("Reprogramare", "", "", "S/N: ____________________", "", "", "", ""),
        ("Inginer", "", "", "", "", "", "Confirmare Client Nume", ""),
    ]

    for tip, x1, x2, text_lung, x3, rez, cauza, nerez in randuri:
        pdf.cell(col_t_interv, 6, tip, border=1)
        pdf.cell(col_x1, 6, x1, border=1)
        pdf.cell(col_x2, 6, x2, border=1)
        pdf.cell(col_text_lung, 6, text_lung, border=1)
        pdf.cell(col_x3, 6, x3, border=1)
        pdf.cell(col_rezultat, 6, rez, border=1)
        pdf.cell(col_cauza, 6, cauza, border=1)
        pdf.cell(col_nerez, 6, nerez, border=1, ln=1)

    pdf.ln(8)
    pdf.cell(0, 6, "Service: __________________    Marca: __________________    L.S.: __________________", ln=1, align="C")

    # Returnează bytes pentru Streamlit
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
        "cu format identic modelului încărcat."
    )

    if st.button("Generează raport pentru luna trecută"):
        an, luna = get_prev_month_year()
        weeks = zile_lucratoare_grupate_pe_saptamani(an, luna)
        zile_selectate = alege_zile_random(weeks, max_zile=4)

        pdf_bytes = genereaza_pdf(an, luna, zile_selectate)

        st.success(
            f"Raport generat pentru **{nume_luna_ro(luna)} {an}** "
            f"cu {len(zile_selectate)} zile de intervenție."
        )
        st.write("Zilele alese:")
        for d in sorted(zile_selectate):
            st.write("-", d.strftime("%d/%m/%Y"))

        file_name = f"Sesiz_Raport_de_Service_{nume_luna_ro(luna)}{an}.pdf"
        st.download_button(
            label="Descarcă raportul PDF",
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()
