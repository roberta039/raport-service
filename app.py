import streamlit as st
import datetime
import calendar
import random

# ------------------------------------------------------------
# 1. Funcții helper – date & zile lucrătoare random
# ------------------------------------------------------------
ROMANIAN_MONTHS = {
    1: "Ianuarie",
    2: "Februarie",
    3: "Martie",
    4: "Aprilie",
    5: "Mai",
    6: "Iunie",
    7: "Iulie",
    8: "August",
    9: "Septembrie",
    10: "Octombrie",
    11: "Noiembrie",
    12: "Decembrie"
}

def working_days_of_month(year: int, month: int) -> list[datetime.date]:
    """Returnează lista de zile lucrătoare (luni–vineri) pentru o lună/an."""
    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        dt = datetime.date(year, month, day)
        if dt.weekday() < 5:  # 0–4 = luni–vineri
            days.append(dt)
    return days

def random_working_days(days: list[datetime.date], max_count: int = 4) -> list[datetime.date]:
    """Alege până la max_count zile lucrătoare random și le sortează."""
    if len(days) <= max_count:
        return sorted(days)
    return sorted(random.sample(days, max_count))

# ------------------------------------------------------------
# 2. Generare HTML raport
# ------------------------------------------------------------
def generate_html_report(
    company_name: str,
    company_address: str,
    client_name: str,
    client_street: str,
    client_city: str,
    selected_interventions: list[str],
    report_month_year: str,
    report_dates: list[datetime.date],
    last_date_str: str
):
    # Linii „Defecte constatate” – câte un rând pentru fiecare zi aleasă
    defect_lines = "<br>".join(
        f"{d.day:02d}/{d.month:02d}/{d.year} - Verificare si intretinere retea de calculatoare."
        for d in report_dates
    )

    # Tabel simplificat „Tip intervenție / Rezultat / Cauza”
    interventions = [
        "Garantie", "Constatare", "Revizie", "Instalare", "Reinstalare",
        "Mutare", "Incasare", "Rutina", "Programare", "Reprogramare"
    ]
    rows = ""
    for it in interventions:
        checked = "☑" if it in selected_interventions else "□"
        result = "Rezolvata" if it in selected_interventions else ""
        cause = "Lipsa componente" if it not in selected_interventions else ""
        rows += f"""
        <tr>
            <td width="40%">{it}</td>
            <td width="20%" align="center">{checked}</td>
            <td width="40%" align="center">{result or cause}</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            font-size: 10pt;
        }}
        .center {{ text-align: center; }}
        .left   {{ text-align: left; }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid black;
            padding: 4px;
        }}
        .print-btn {{
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }}
        @media print {{
            .print-btn {{ display: none; }}
            body {{
                margin: 0;
                padding: 0;
            }}
        }}
    </style>
    </head>
    <body>

    <!-- Date firmă – aliniate la stânga -->
    <div class="left">
        <strong>{company_name}</strong><br/>
        {company_address}
    </div>

    <h1 class="center">SESIZARE/RAPORT DE SERVICE</h1>

    <!-- 2 corpuri sub titlu -->
    <table>
        <tr>
            <td width="50%">
                <strong>Produs</strong><br/>
                Revizie<br/><br/>

                <strong>Beneficiar</strong><br/>
                {client_name}<br/><br/>

                <strong>Eticheta / Serie</strong><br/>
                {client_name}<br/><br/>

                <strong>Adresa</strong><br/>
                {client_street}<br/><br/>

                <strong>Localitate</strong><br/>
                {client_city}<br/><br/>

                <strong>Telefon</strong><br/>
                ________________<br/><br/>

                <strong>NrContr.</strong><br/>
                ________________<br/><br/>

                <strong>Defecte sesizate</strong><br/>
                ___________________________<br/>
                ___________________________<br/>
            </td>
            <td width="50%">
                <strong>Luna</strong><br/>
                {report_month_year}<br/><br/>

                <strong>Data</strong><br/>
                {last_date_str}<br/><br/>

                <strong>Ora</strong><br/>
                ________________<br/><br/>

                <strong>Lansare</strong><br/>
                ________________<br/><br/>

                <strong>Trimitere</strong><br/>
                ________________<br/><br/>

                <strong>Sosire</strong><br/>
                {last_date_str}<br/><br/>

                <strong>Valoare Abonament</strong><br/>
                ________________<br/><br/>

                <strong>Anunta</strong><br/>
                ________________<br/>
            </td>
        </tr>
    </table>

    <!-- Defecte constatate -->
    <h2 class="center">Defecte constatate</h2>
    <table>
        <tr>
            <td width="100%">
                {defect_lines}
            </td>
        </tr>
    </table>

    <!-- Tip interventie / Rezultat / Cauza nerezolvarii -->
    <h2 class="center">Tip interventie / Rezultat / Cauza nerezolvarii</h2>
    <table>
        <tr>
            <th width="40%">Tip interventie</th>
            <th width="20%">Selectat</th>
            <th width="40%">Rezultat / Cauza</th>
        </tr>
        {rows}
    </table>

    <!-- Inginer service / Confirmare client -->
    <table>
        <tr>
            <td width="50%">
                <strong>Inginer service</strong><br/>
                ________________<br/><br/>

                <strong>Marca</strong><br/>
                ________________
            </td>
            <td width="50%">
                <strong>Confirmare client nume</strong><br/>
                ________________<br/><br/>

                <strong>L.S.</strong><br/>
                ________________
            </td>
        </tr>
    </table>

    <!-- Buton de print în HTML (va dispărea la tipărire) -->
    <button class="print-btn" onclick="window.print()">Print Report</button>

    </body>
    </html>
    """
    return html

# ------------------------------------------------------------
# 3. UI Streamlit
# ------------------------------------------------------------
st.title("Raport de Service – Pagina web (fără PDF)")

st.write(
    "Aplicația generează raportul direct în pagină ca HTML. "
    "Poți tipări din browser sau cu butonul de print."
)

with st.form("report_form"):
    # Date firmă
    company_name = st.text_input(
        "Denumire firmă (sus stânga)",
        value="S.C. CREATIVE WEBDEV S.R.L."
    )
    company_address = st.text_input(
        "Adresă firmă",
        value="SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10, SECTOR 4, BUCURESTI - Romania"
    )

    # Beneficiar
    client_name = st.text_input("Beneficiar", value="SC Inkorporate SRL")
    client_street = st.text_input("Adresă beneficiar", value="Str. Esarfei 64-66")
    client_city = st.text_input("Localitate", value="Bucuresti")

    # Tipuri de intervenție
    interventions_options = [
        "Garantie", "Constatare", "Revizie", "Instalare", "Reinstalare",
        "Mutare", "Incasare", "Rutina", "Programare", "Reprogramare"
    ]
    selected_interventions = st.multiselect(
        "Selectează tipurile de intervenţie efectuate",
        options=interventions_options,
        default=["Revizie"]
    )

    submitted = st.form_submit_button("Generează raportul")

if submitted:
    # Luna trecută
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_month_date = first_day_this_month - datetime.timedelta(days=1)
    year = last_month_date.year
    month = last_month_date.month
    report_month_year = f"{ROMANIAN_MONTHS[month]} {year}"

    # Zile lucrătoare & selecție random (max 4)
    working_days = working_days_of_month(year, month)
    chosen_days = random_working_days(working_days, max_count=4)

    last_date_str = chosen_days[-1].strftime("%d/%m/%Y")

    # Generează HTML raport
    html_report = generate_html_report(
        company_name=company_name,
        company_address=company_address,
        client_name=client_name,
        client_street=client_street,
        client_city=client_city,
        selected_interventions=selected_interventions,
        report_month_year=report_month_year,
        report_dates=chosen_days,
        last_date_str=last_date_str
    )

    # Afișează raportul ca pagină HTML în Streamlit
    st.components.v1.html(html_report, height=900, scrolling=True)

    st.info(
        "Raportul este generat ca pagină web. "
        "Poți folosi butonul 'Print Report' din raport sau comanda Ctrl+P din browser pentru tipărire."
    )
