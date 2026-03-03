import streamlit as st
import datetime
import calendar
import random

# -----------------------------
# Configurări fixe (le poți schimba)
# -----------------------------
ROMANIAN_MONTHS = {
    1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie", 5: "Mai", 6: "Iunie",
    7: "Iulie", 8: "August", 9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
}

COMPANY_NAME = "S.C. CREATIVE WEBDEV S.R.L."
COMPANY_ADDRESS = "SOSEAUA GIURGIULUI NR. 113-115, BL. O, SC. 1, ET. 2, AP.10, SECTOR 4, BUCURESTI - Romania"
CLIENT_NAME = "SC Inkorporate SRL"
CLIENT_STREET = "Str. Esarfei 64-66"
CLIENT_CITY = "Bucuresti"

# -----------------------------
# Funcții pentru zile lucrătoare
# -----------------------------
def working_days_of_month(year: int, month: int) -> list[datetime.date]:
    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        dt = datetime.date(year, month, day)
        if dt.weekday() < 5:  # 0–4 = luni–vineri
            days.append(dt)
    return days

def random_working_days(days: list[datetime.date], max_count: int = 4) -> list[datetime.date]:
    if len(days) <= max_count:
        return sorted(days)
    return sorted(random.sample(days, max_count))

# -----------------------------
# Generare HTML raport (după modelul tău)
# -----------------------------
def generate_html_report():
    # Luna trecută din anul curent
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_month_date = first_day_this_month - datetime.timedelta(days=1)
    year = last_month_date.year
    month = last_month_date.month
    report_month_year = f"{ROMANIAN_MONTHS[month]} {year}"

    # Zile lucrătoare random (max 4) + ultima zi = data sosirii
    working_days = working_days_of_month(year, month)
    chosen_days = random_working_days(working_days, max_count=4)
    last_date_str = chosen_days[-1].strftime("%d/%m/%Y")

    defect_lines = ""
    for d in chosen_days:
        defect_lines += f"{d.day:02d}/{d.month:02d}/{d.year} - Verificare si intretinere retea de calculatoare.<br>"

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
        .center {{
            text-align: center;
            font-weight: bold;
        }}
        .left {{
            text-align: left;
        }}
        .normal {{
            font-weight: normal;
        }}
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
        <!-- Date firmă (sus, stânga) -->
        <div class="left">
            <strong>{COMPANY_NAME}</strong><br/>
            {COMPANY_ADDRESS}
        </div>
        <br/>

        <!-- Titlu -->
        <div class="center" style="font-size: 18pt; margin-bottom: 10px;">
            SESIZARE/RAPORT DE SERVICE
        </div>

        <!-- Tabel principal 2 coloane -->
        <table>
            <tr>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="30%" class="left"><strong>Produs</strong></td>
                            <td width="70%" class="normal">Revizie</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Beneficiar</strong></td>
                            <td class="normal">{CLIENT_NAME}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Serie</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Eticheta</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Adresa</strong></td>
                            <td class="normal">{CLIENT_STREET}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Localitate</strong></td>
                            <td class="normal">{CLIENT_CITY}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Telefon</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Fax</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Tip</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Nr Contr.</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Defecte Sesizate</strong></td>
                            <td class="normal"></td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="30%" class="left"><strong>Luna</strong></td>
                            <td width="70%" class="normal">{report_month_year}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Ora</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Lansare</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Trimitere</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Sosire</strong></td>
                            <td class="normal">{last_date_str}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Valoare Abonament</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Anunta</strong></td>
                            <td class="normal"></td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Defecte constatate -->
        <br/>
        <div class="center" style="margin-bottom: 5px;">
            Defecte Constatate
        </div>
        <table border="1" width="100%">
            <tr>
                <td width="30%" class="center"><strong>Defecte Constatate</strong></td>
                <td width="70%" class="normal">{defect_lines}</td>
            </tr>
        </table>

        <!-- Tip interventie / Rezultat / Cauza nerezolvarii (variantă simplificată) -->
        <br/>
        <div class="center" style="margin-bottom: 5px;">
            Tip Interventie / Rezultat / Cauza Nerezolvarii
        </div>
        <table border="1" width="100%">
            <tr>
                <th width="25%">Tip Interventie</th>
                <th width="15%">Selectat</th>
                <th width="25%">Rezultat</th>
                <th width="35%">Cauza Nerezolvarii</th>
            </tr>
            <tr><td class="left">Garantie</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Constatare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Revizie</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Instalare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Reinstalare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Mutare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Incasare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Rutina</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Programare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
            <tr><td class="left">Reprogramare</td><td class="center">☐</td><td class="center">Rezolvata</td><td></td></tr>
        </table>

        <!-- Inginer service / Confirmare client -->
        <br/>
        <table>
            <tr>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="40%" class="left"><strong>Inginer Service</strong></td>
                            <td width="60%" class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Marca</strong></td>
                            <td class="normal"></td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="50%" class="left"><strong>Confirmare Client Nume</strong></td>
                            <td width="50%" class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>L.S.</strong></td>
                            <td class="normal"></td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Buton de print (dispare la tipărire) -->
        <button class="print-btn" onclick="window.print()">Print Report</button>
    </body>
    </html>
    """
    return html

# -----------------------------
# Configurare pagină – ascunde meniuri, sidebar etc.
# -----------------------------
st.set_page_config(
    page_title="Raport de Service",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# -----------------------------
# Afișează DOAR raportul generat
# -----------------------------
report_html = generate_html_report()
st.components.v1.html(report_html, height=900, scrolling=True)
