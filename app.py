import streamlit as st
import datetime
import calendar
import random

# Configurări fixe
ROMANIAN_MONTHS = {
    1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie", 5: "Mai", 6: "Iunie",
    7: "Iulie", 8: "August", 9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
}

# Adresa pe 3 rânduri separate (folosim <br> pentru trecerea pe rând nou)
COMPANY_NAME = "S.C. CREATIVE WEBDEV S.R.L."
COMPANY_ADDRESS = (
    "SOSEAUA GIURGIULUI NR. 113-115<br>"
    "BL. O, SC. 1, ET. 2, AP.10<br>"
    "SECTOR 4, BUCURESTI - Romania"
)
CLIENT_NAME = "SC Inkorporate S.R.L."
CLIENT_STREET = "Str. Esarfei 64-66"
CLIENT_CITY = "Bucuresti"


# Funcții ajutătoare
def working_days_of_month(year, month):
    """Returnează lista de zile lucrătoare (luni‑vineri) pentru o lună specifică."""
    days = []
    for day in range(1, calendar.monthrange(year, month)[1] + 1):
        dt = datetime.date(year, month, day)
        if dt.weekday() < 5:  # 0‑4 = luni‑vineri
            days.append(dt)
    return days


def random_working_days(days, max_count=4):
    """Selectează aleator până la max_count zile lucrătoare și le sortează."""
    if len(days) <= max_count:
        return sorted(days)
    return sorted(random.sample(days, max_count))


# Generare raport HTML
def generate_html_report():
    """Generează raportul HTML conform modelului dorit."""

    # Luna trecută
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_month_date = first_day_this_month - datetime.timedelta(days=1)
    year = last_month_date.year
    month = last_month_date.month
    report_month_year = f"{ROMANIAN_MONTHS[month]} {year}"

    # Zile lucrătoare alese aleator (max 4)
    working_days = working_days_of_month(year, month)
    chosen_days = random_working_days(working_days, max_count=4)

    # Data Ora Sosire = ultima zi aleasă (ora se completează manual)
    sosire_date = chosen_days[-1].strftime("%d/%m/%Y")

    # Blocul "Defecte Constatate" – rând pentru fiecare zi
    defect_lines = ""
    for d in chosen_days:
        defect_lines += (
            f"{d.day:02d}/{d.month:02d}/{d.year} - "
            f"Verificare si intretinere retea de calculatoare.<br>"
        )

    # Spațiu suplimentar pentru completare manuală la "Defecte Constatate"
    defect_lines += "<br>" * 15

    # Spațiu pentru blocul "Defecte Sesizate" (fără date pre‑completate)
    defect_sesizate_space = "<br>" * 8

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
            <strong>{COMPANY_NAME}</strong><br>
            {COMPANY_ADDRESS}
        </div>
        <br>

        <!-- Titlu -->
        <div class="center" style="font-size: 18pt; margin-bottom: 10px;">
            SESIZARE/RAPORT DE SERVICE
        </div>

        <!-- Tabel principal 2 coloane -->
        <table>
            <tr>
                <!-- Coloana stânga: date beneficiar / produs -->
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
                            <td class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Fax</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Tip</strong></td>
                            <td class="normal"></td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Nr Contr.</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                    </table>
                </td>

                <!-- Coloana dreapta: luna, date/ora, abonament -->
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="30%" class="left"><strong>Luna</strong></td>
                            <td width="70%" class="normal">{report_month_year}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Lansare</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Trimitere</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Sosire</strong></td>
                            <td class="normal">{sosire_date}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Valoare Abonament</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Anunta</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Bloc Defecte Sesizate (același layout ca Defecte Constatate, dar gol) -->
        <br>
        <div class="center" style="margin-bottom: 5px;">
            Defecte Sesizate
        </div>
        <table border="1" width="100%">
            <tr>
                <td width="30%" class="center"><strong>Defecte Sesizate</strong></td>
                <td width="70%" class="normal">
                    {defect_sesizate_space}
                </td>
            </tr>
        </table>

        <!-- Bloc Defecte Constatate cu date + spațiu liber -->
        <br>
        <div class="center" style="margin-bottom: 5px;">
            Defecte Constatate
        </div>
        <table border="1" width="100%">
            <tr>
                <td width="30%" class="center"><strong>Defecte Constatate</strong></td>
                <td width="70%" class="normal">
                    {defect_lines}
                </td>
            </tr>
        </table>

        <!-- Tabel cu 3 coloane: Tip Interventie, Rezultat, Cauza Nerezolvarii -->
        <br>
        <table border="1" width="100%">
            <tr>
                <!-- Col 1: Tip Interventie -->
                <td width="33%" style="vertical-align: top; padding: 0; margin: 0;">
                    <div class="center" style="margin-bottom: 5px;">Tip Interventie</div>
                    <table border="1" width="100%">
                        <tr>
                            <th colspan="10">Tip Interventie</th>
                        </tr>
                        <tr>
                            <td width="10%">Garantie</td>
                            <td width="10%">Constatare</td>
                            <td width="10%">Revizie</td>
                            <td width="10%">Instalare</td>
                            <td width="10%">Reinstalare</td>
                            <td width="10%">Mutare</td>
                            <td width="10%">Incasare</td>
                            <td width="10%">Rutina</td>
                            <td width="10%">Programare</td>
                            <td width="10%">Reprogramare</td>
                        </tr>
                        <tr>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                        </tr>
                    </table>
                </td>

                <!-- Col 2: Rezultat -->
                <td width="33%" style="vertical-align: top; padding: 0; margin: 0;">
                    <div class="center" style="margin-bottom: 5px;">Rezultat</div>
                    <table border="1" width="100%">
                        <tr>
                            <th colspan="7">Rezultat</th>
                        </tr>
                        <tr>
                            <td width="14%">Rezolvata</td>
                            <td width="14%">Rezolvata Partial</td>
                            <td width="14%">Nerezolvata</td>
                            <td width="14%">Preluare Echipament</td>
                            <td width="14%">Fara Accesorii</td>
                            <td width="14%">Cu Accesorii</td>
                            <td width="14%">Furnizat echipament back-up</td>
                        </tr>
                        <tr>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                        </tr>
                    </table>
                </td>

                <!-- Col 3: Cauza Nerezolvarii -->
                <td width="33%" style="vertical-align: top; padding: 0; margin: 0;">
                    <div class="center" style="margin-bottom: 5px;">Cauza Nerezolvarii</div>
                    <table border="1" width="100%">
                        <tr>
                            <th colspan="7">Cauza Nerezolvarii</th>
                        </tr>
                        <tr>
                            <td width="14%">Lipsa Componente</td>
                            <td width="14%">Insatisfactie Client</td>
                            <td width="14%">Piese luate la reparat</td>
                            <td width="14%">Lipsa acces Produs</td>
                            <td width="14%">Terminat Programul</td>
                            <td width="14%">Refuz Cumparare</td>
                            <td width="14%">Linie Telefonica defecta</td>
                        </tr>
                        <tr>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                            <td class="center">☐</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Corp mic pentru Model/Obs. și S/N -->
        <br>
        <div style="text-align: left;">
            Model/Obs.: ___________<br>
            S/N: ___________
        </div>

        <!-- Inginer service / Confirmare client -->
        <br>
        <table>
            <tr>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="40%" class="left"><strong>Inginer Service</strong></td>
                            <td width="60%" class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Marca</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                    </table>
                </td>
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="50%" class="left"><strong>Confirmare Client Nume</strong></td>
                            <td width="50%" class="normal">________________</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>L.S.</strong></td>
                            <td class="normal">________________</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Buton de print -->
        <button class="print-btn" onclick="window.print()">Print Report</button>
    </body>
    </html>
    """
    return html


# Configurare pagină Streamlit
st.set_page_config(
    page_title="Raport de Service",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

# Afișare raport direct, fără alt text/butoane Streamlit
report_html = generate_html_report()
st.components.v1.html(report_html, height=900, scrolling=True)
