import streamlit as st
import datetime
import calendar
import random
from typing import List
from fpdf import FPDF

# -------------------------
# Funcții de dată
# -------------------------
def working_days_of_month(year: int, month: int) -> List[datetime.date]:
    days = []
    num_days = calendar.monthrange(year, month)[1]
    for d in range(1, num_days + 1):
        date_obj = datetime.date(year, month, d)
        if date_obj.weekday() < 5:  # luni–vineri
            days.append(date_obj)
    return days

def random_working_days(days: List[datetime.date], max_count: int = 4) -> List[datetime.date]:
    if len(days) <= max_count:
        return sorted(days)
    return sorted(random.sample(days, max_count))

# -------------------------
# HTML pentru raport
# -------------------------
def generate_html(
    client_name: str,
    client_city: str,
    client_street: str,
    company_name: str,
    company_address: str,
    report_month_year: str,
    report_dates: List[datetime.date],
    selected_interventions: List[str],
):
    # Liniile pentru „Defecte constatate”
    defect_lines = "<br>".join(
        f"{d.day:02d}/{d.month:02d}/{d.year} - Verificare si intretinere retea de calculatoare."
        for d in report_dates
    )

    # tipuri de intervenție – adaptate după model
    interventions = [
        "Garantie", "Constatare", "Revizie", "Instalare", "Reinstalare",
        "Mutare", "Incasare", "Rutina", "Programare", "Reprogramare"
    ]

    intervention_rows = ""
    for it in interventions:
        checkbox = "☑" if it in selected_interventions else "□"
        result = "Rezolvata"  # poți ulterior să faci acest câmp dinamic
        intervention_rows += f"""
        <tr>
            <td width="40%">{it}</td>
            <td width="20%" align="center">{checkbox}</td>
            <td width="40%" align="center">{result}</td>
        </tr>
        """

    last_date = report_dates[-1]

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .left {{ text-align: left; }}
        .center {{ text-align: center; font-weight: bold; font-size: 18pt; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #000; padding: 4px; font-size: 10pt; }}
        h3 {{ margin-top: 16px; margin-bottom: 8px; }}
    </style>
    </head>
    <body>
        <div class="left">
            <strong>{company_name}</strong><br/>
            {company_address}
        </div>
        <br/>
        <div class="center">SESIZARE/RAPORT DE SERVICE</div>
        <br/>

        <!-- 2 corpuri sub titlu -->
        <table>
            <tr>
                <td width="50%">
                    <strong>Produs</strong><br/>
                    Revizie<br/><br/>

                    <strong>Beneficiar</strong><br/>
                    {client_name}<br/><br/>

                    <strong>Adresa</strong><br/>
                    {client_street}<br/><br/>

                    <strong>Localitate</strong><br/>
                    {client_city}<br/><br/>

                    <strong>Telefon</strong><br/>
                    ______________________<br/><br/>

                    <strong>NrContr.</strong><br/>
                    ______________________<br/><br/>

                    <strong>Defecte sesizate</strong><br/>
                    ____________________________________________<br/>
                    ____________________________________________<br/>
                </td>
                <td width="50%">
                    <strong>Luna</strong><br/>
                    {report_month_year}<br/><br/>

                    <strong>Data</strong><br/>
                    {last_date.day:02d}/{last_date.month:02d}/{last_date.year}<br/><br/>

                    <strong>Ora</strong><br/>
                    __________<br/><br/>

                    <strong>Lansare</strong><br/>
                    __________<br/><br/>

                    <strong>Trimitere</strong><br/>
                    __________<br/><br/>

                    <strong>Sosire</strong><br/>
                    {last_date.day:02d}/{last_date.month:02d}/{last_date.year}<br/><br/>

                    <strong>Valoare Abonament</strong><br/>
                    __________<br/><br/>

                    <strong>Anunta</strong><br/>
                    __________<br/><br/>
                </td>
            </tr>
        </table>

        <!-- Defecte constatate -->
        <h3 style="text-align:center;">Defecte constatate</h3>
        <table>
            <tr>
                <td width="30%"><strong>Defecte Constatate</strong></td>
                <td width="70%">{defect_lines}</td>
            </tr>
        </table>

        <!-- Tip interventie / Rezultat / Cauza nerezolvarii (simplificat) -->
        <h3 style="text-align:center;">Tip interventie / Rezultat / Cauza nerezolvarii</h3>
        <table>
            <tr>
                <th width="40%">Tip interventie</th>
                <th width="20%">Selectat</th>
                <th width="40%">Rezultat</th>
            </tr>
            {intervention_rows}
        </table>

        <!-- Inginer service / Confirmare client -->
        <br/>
        <table>
            <tr>
                <td width="50%">
                    <strong>Inginer service</strong><br/>
                    ___________________________<br/><br/>
                    <strong>Marca</strong><br/>
                    ___________________________
                </td>
                <td width="50%">
                    <strong>Confirmare client nume</strong><br/>
                    ___________________________<br/><br/>
                    <strong>L.S.</strong><br/>
                    ___________________________
                </td>
            </tr>
        </table>

    </body>
    </html>
    """
    return html

# -------------------------
# HTML -> PDF
# -------------------------
def html_to_pdf(html_content: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.write_html(html_content)
    # returnează bytes ai fișierului PDF
    return pdf.output(dest="S").encode("latin1")

# -------------------------
# Interfața Streamlit
# -------------------------
st.title("Generator Raport de Service")

st.write("Aplicație gratuită (GitHub + Streamlit) pentru generarea Raportului de Service.")

with st.form("report_form"):
    # Date firmă
    company_name = st.text_input(
        "Denumire firmă (apar sus, stânga)",
        value="S.C. CREATIVE WEBDEV S.R.L."
    )
    company_address = st.text_input(
        "Adresă firmă (linia de sub denumire)",
        value="SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10, SECTOR 4, BUCURESTI - Romania"
    )

    # Date client
    client_name = st.text_input("Beneficiar", value="SC Inkorporate SRL")
    client_street = st.text_input("Adresă beneficiar", value="Str. Esarfei 64-66")
    client_city = st.text_input("Localitate beneficiar", value="Bucuresti")

    # Intervenții posibile (bife)
    interventions_options = [
        "Garantie", "Constatare", "Revizie", "Instalare", "Reinstalare",
        "Mutare", "Incasare", "Rutina", "Programare", "Reprogramare"
    ]
    selected_interventions = st.multiselect(
        "Selectează tipurile de intervenție efectuate:",
        options=interventions_options,
        default=["Revizie"]
    )

    submitted = st.form_submit_button("Generează raport")

if submitted:
    # luna trecută
    today = datetime.date.today()
    last_month_date = today.replace(day=1) - datetime.timedelta(days=1)
    year, month = last_month_date.year, last_month_date.month

    work_days = working_days_of_month(year, month)
    chosen_days = random_working_days(work_days, max_count=4)

    # „Februarie 2026” etc.
    # .capitalize() pentru prima literă mare la denumirea lunii (în engleză implicit, dar poți forța manual în română)
    report_month_year = last_month_date.strftime("%B %Y")

    st.write("Zilele alese pentru raport (zile lucrătoare, max 4):")
    st.write(", ".join(d.strftime("%d/%m/%Y") for d in chosen_days))

    html = generate_html(
        client_name=client_name,
        client_city=client_city,
        client_street=client_street,
        company_name=company_name,
        company_address=company_address,
        report_month_year=report_month_year,
        report_dates=chosen_days,
        selected_interventions=selected_interventions,
    )

    pdf_bytes = html_to_pdf(html)
    last_date_str = chosen_days[-1].strftime("%Y%m%d")

    st.download_button(
        label="Descarcă raport PDF",
        data=pdf_bytes,
        file_name=f"Raport_Service_{last_date_str}.pdf",
        mime="application/pdf"
    )
