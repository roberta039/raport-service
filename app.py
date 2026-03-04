import streamlit as st
import datetime
import calendar
import random

# CONFIGURĂRI FIXE
ROMANIAN_MONTHS = {
    1: "Ianuarie", 2: "Februarie", 3: "Martie", 4: "Aprilie", 5: "Mai", 6: "Iunie",
    7: "Iulie", 8: "August", 9: "Septembrie", 10: "Octombrie", 11: "Noiembrie", 12: "Decembrie"
}

COMPANY_NAME = "S.C. CREATIVE WEBDEV S.R.L."
COMPANY_ADDRESS = (
    "SOSEAUA GIURGIULUI NR. 113-115<br>"
    "BL. O, SC. 1, ET. 2, AP.10<br>"
    "SECTOR 4, BUCURESTI - Romania"
)
CLIENT_NAME = "SC Inkorporate S.R.L."
CLIENT_STREET = "Str. Esarfei 64-66"
CLIENT_CITY = "Bucuresti"

# Opțiuni pentru blocurile cu bife
TIP_INTERVENTIE_OPTIONS = [
    "Garantie", "Constatare", "Revizie", "Instalare", "Reinstalare",
    "Mutare", "Incasare", "Rutina", "Programare", "Reprogramare"
]

RESULT_OPTIONS = [
    "Rezolvata", "Rezolvata Partial", "Nerezolvata",
    "Preluare Echipament", "Fara Accesorii",
    "Cu Accesorii", "Furnizat echipament back‑up"
]

CAUZA_NERECOL_OPTIONS = [
    "Lipsa Componente", "Insatisfactie Client", "Piese luate la reparat",
    "Lipsa acces Produs", "Terminat Programul",
    "Refuz Cumparare", "Linie Telefonica defecta"
]


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


def init_state():
    """Inițializează valorile implicite în sesiune, dacă nu există deja."""
    # câmpuri text generale
    for key, default in {
        "produs": "",
        "beneficiar": CLIENT_NAME,
        "serie": "",
        "eticheta": "",
        "telefon": "",
        "fax": "",
        "tip": "",
        "nr_contr": "",
        "data_ora_lansare": "",
        "data_ora_trimitere": "",
        "data_ora_sosire": "",
        "valoare_abonament": "",
        "anunta": ""
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # defecte sesizate/constatate (5 rânduri fiecare, editabile)
    if "defect_sesizate" not in st.session_state:
        st.session_state.defect_sesizate = [""] * 5
    if "defect_constatate" not in st.session_state:
        st.session_state.defect_constatate = [""] * 5

    # bife
    if "tip_interventie" not in st.session_state:
        st.session_state.tip_interventie = {opt: False for opt in TIP_INTERVENTIE_OPTIONS}
    if "rezultat" not in st.session_state:
        st.session_state.rezultat = {opt: False for opt in RESULT_OPTIONS}
    if "cauza_nerezolvarii" not in st.session_state:
        st.session_state.cauza_nerezolvarii = {opt: False for opt in CAUZA_NERECOL_OPTIONS}


def generate_html_report():
    """Generează HTML‑ul raportului, folosind valorile completate în UI."""

    # Luna trecută (pentru câmpul "Luna")
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_month_date = first_day_this_month - datetime.timedelta(days=1)
    year = last_month_date.year
    month = last_month_date.month
    report_month_year = f"{ROMANIAN_MONTHS[month]} {year}"

    # Zile lucrătoare + una pentru Data Ora Sosire (doar ca fallback)
    working_days = working_days_of_month(year, month)
    chosen_days = random_working_days(working_days, max_count=4)
    sosire_date_auto = chosen_days[-1].strftime("%d/%m/%Y") if chosen_days else ""

    # Dacă Data Ora Sosire nu e completată manual, folosim data automată
    data_ora_sosire_final = st.session_state.data_ora_sosire or sosire_date_auto

    # Construim listele de defecte
    defect_sesizate_html = "<br>".join(
        f"{i+1}. {txt}" for i, txt in enumerate(st.session_state.defect_sesizate) if txt.strip()
    )
    defect_constatate_html = "<br>".join(
        f"{i+1}. {txt}" for i, txt in enumerate(st.session_state.defect_constatate) if txt.strip()
    )

    # Construim rândurile pentru cele 3 blocuri cu bife (HTML <input type="checkbox">)
    tip_interventie_rows = ""
    for opt in TIP_INTERVENTIE_OPTIONS:
        checked = "checked" if st.session_state.tip_interventie[opt] else ""
        tip_interventie_rows += f'<tr><td><input type="checkbox" {checked}> {opt}</td></tr>'

    rezultat_rows = ""
    for opt in RESULT_OPTIONS:
        checked = "checked" if st.session_state.rezultat[opt] else ""
        rezultat_rows += f'<tr><td><input type="checkbox" {checked}> {opt}</td></tr>'

    cauza_rows = ""
    for opt in CAUZA_NERECOL_OPTIONS:
        checked = "checked" if st.session_state.cauza_nerezolvarii[opt] else ""
        cauza_rows += f'<tr><td><input type="checkbox" {checked}> {opt}</td></tr>'

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
        /* Spațiere mărită în chenarul dublu */
        .table-double th,
        .table-double td {{
            padding: 10px 4px;
            line-height: 1.6;
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
        /* Stil pentru printare A4 */
        @media print {{
            body {{
                margin: 0;
                padding: 0;
                font-size: 9pt;
            }}
            @page {{
                size: A4;
                margin: 0;
            }}
            .print-btn {{
                display: none;
            }}
            table {{
                max-width: 100%;
                page-break-inside: avoid;
            }}
        }}
    </style>
    </head>
    <body>
        <!-- Date firmă -->
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
                <!-- Stânga: date beneficiar / produs -->
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="30%" class="left"><strong>Produs</strong></td>
                            <td width="70%" class="normal">{st.session_state.produs}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Beneficiar</strong></td>
                            <td class="normal">{st.session_state.beneficiar}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Serie</strong></td>
                            <td class="normal">{st.session_state.serie}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Eticheta</strong></td>
                            <td class="normal">{st.session_state.eticheta}</td>
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
                            <td class="normal">{st.session_state.telefon}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Fax</strong></td>
                            <td class="normal">{st.session_state.fax}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Tip</strong></td>
                            <td class="normal">{st.session_state.tip}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Nr Contr.</strong></td>
                            <td class="normal">{st.session_state.nr_contr}</td>
                        </tr>
                    </table>
                </td>

                <!-- Dreapta: lună + date/ora -->
                <td width="50%" style="vertical-align: top;">
                    <table border="0" width="100%">
                        <tr>
                            <td width="30%" class="left"><strong>Luna</strong></td>
                            <td width="70%" class="normal">{report_month_year}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Lansare</strong></td>
                            <td class="normal">{st.session_state.data_ora_lansare}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Trimitere</strong></td>
                            <td class="normal">{st.session_state.data_ora_trimitere}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Data Ora Sosire</strong></td>
                            <td class="normal">{data_ora_sosire_final}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Valoare Abonament</strong></td>
                            <td class="normal">{st.session_state.valoare_abonament}</td>
                        </tr>
                        <tr>
                            <td class="left"><strong>Anunta</strong></td>
                            <td class="normal">{st.session_state.anunta}</td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- Bloc Defecte Sesizate (chenar dublu) -->
        <br>
        <div class="center" style="margin-bottom: 5px;">
            Defecte Sesizate
        </div>
        <table border="2" width="100%" style="border: double;" class="table-double">
            <tr>
                <td width="30%" class="center"><strong>Defecte Sesizate</strong></td>
                <td width="70%" class="normal">
                    {defect_sesizate_html}
                </td>
            </tr>
        </table>

        <!-- Bloc Defecte Constatate (chenar dublu) -->
        <br>
        <div class="center" style="margin-bottom: 5px;">
            Defecte Constatate
        </div>
        <table border="2" width="100%" style="border: double;" class="table-double">
            <tr>
                <td width="30%" class="center"><strong>Defecte Constatate</strong></td>
                <td width="70%" class="normal">
                    {defect_constatate_html}
                </td>
            </tr>
        </table>

        <!-- 3 corpuri: Tip Interventie, Rezultat, Cauza Nerezolvarii -->
        <br>
        <table border="1" style="border-collapse: collapse; width: 100%; border-width: 1px; border-color: #000; border-spacing: 0;">
            <tr>
                <!-- Stânga: Tip Interventie -->
                <td width="33%" style="vertical-align: top; padding: 4px;">
                    <table border="0" width="100%">
                        <tr><th class="center">Tip Interventie</th></tr>
                        {tip_interventie_rows}
                    </table>
                </td>

                <!-- Mijloc: Rezultat -->
                <td width="33%" style="vertical-align: top; padding: 4px;">
                    <table border="0" width="100%">
                        <tr><th class="center">Rezultat</th></tr>
                        {rezultat_rows}
                    </table>
                </td>

                <!-- Dreapta: Cauza Nerezolvarii -->
                <td width="33%" style="vertical-align: top; padding: 4px;">
                    <table border="0" width="100%">
                        <tr><th class="center">Cauza Nerezolvarii</th></tr>
                        {cauza_rows}
                    </table>
                </td>
            </tr>
        </table>

        <!-- Model/Obs și S/N -->
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

        <!-- Buton print -->
        <button class="print-btn" onclick="window.print()">Print Report</button>
    </body>
    </html>
    """
    return html


# CONFIGURARE PAGINĂ STREAMLIT
st.set_page_config(
    page_title="Raport de Service",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None,
)

# Inițializare state
init_state()

# UI DE EDITARE
st.header("Date generale")

col1, col2 = st.columns(2)
with col1:
    st.session_state.produs = st.text_input("Produs", value=st.session_state.produs)
    st.session_state.beneficiar = st.text_input("Beneficiar", value=st.session_state.beneficiar)
    st.session_state.serie = st.text_input("Serie", value=st.session_state.serie)
    st.session_state.eticheta = st.text_input("Eticheta", value=st.session_state.eticheta)
    st.session_state.telefon = st.text_input("Telefon", value=st.session_state.telefon)
    st.session_state.fax = st.text_input("Fax", value=st.session_state.fax)
    st.session_state.tip = st.text_input("Tip", value=st.session_state.tip)
    st.session_state.nr_contr = st.text_input("Nr Contr.", value=st.session_state.nr_contr)

with col2:
    st.session_state.data_ora_lansare = st.text_input("Data Ora Lansare", value=st.session_state.data_ora_lansare)
    st.session_state.data_ora_trimitere = st.text_input("Data Ora Trimitere", value=st.session_state.data_ora_trimitere)
    st.session_state.data_ora_sosire = st.text_input("Data Ora Sosire", value=st.session_state.data_ora_sosire)
    st.session_state.valoare_abonament = st.text_input("Valoare Abonament", value=st.session_state.valoare_abonament)
    st.session_state.anunta = st.text_input("Anunta", value=st.session_state.anunta)

# Defecte Sesizate
st.subheader("Defecte Sesizate")
for i in range(5):
    st.session_state.defect_sesizate[i] = st.text_input(
        f"Defect sesizat {i+1}",
        value=st.session_state.defect_sesizate[i]
    )

# Defecte Constatate
st.subheader("Defecte Constatate")
for i in range(5):
    st.session_state.defect_constatate[i] = st.text_input(
        f"Defect constatat {i+1}",
        value=st.session_state.defect_constatate[i]
    )

# Tip Interventie
st.subheader("Tip Interventie")
for opt in TIP_INTERVENTIE_OPTIONS:
    st.session_state.tip_interventie[opt] = st.checkbox(
        opt,
        value=st.session_state.tip_interventie[opt]
    )

# Rezultat
st.subheader("Rezultat")
for opt in RESULT_OPTIONS:
    st.session_state.rezultat[opt] = st.checkbox(
        opt,
        value=st.session_state.rezultat[opt]
    )

# Cauza Nerezolvarii
st.subheader("Cauza Nerezolvarii")
for opt in CAUZA_NERECOL_OPTIONS:
    st.session_state.cauza_nerezolvarii[opt] = st.checkbox(
        opt,
        value=st.session_state.cauza_nerezolvarii[opt]
    )

# Generare & afișare raport
if st.button("Generează raport"):
    report_html = generate_html_report()
    st.components.v1.html(report_html, height=1600, scrolling=True)
