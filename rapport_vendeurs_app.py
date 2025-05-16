
import streamlit as st
import pandas as pd

# Function to categorize the type of work
def categorize_work(description):
    temps_mecanique = ["ALG", "ALGL", "BAL", "DIVMEC", "MATME", "PP1", "PP2", "PP3", "SCAN", "01", "ALGL10", "ALGL12"]
    temps_routier = ["BAL195", "BAL225", "CRV", "CRVC", "DIVRO", "MDI", "MDILB", "NET", "NETX", "SER", "02", "03", "04", "05", "06", "07", "08", "09", "BAL-SUR", "CRVL", "CRVLXL", "MDIX", "MDIE", "MDIL", "MDIX", "VL", "VL02", "VL03", "MATVUL", "ROT"]
    
    if description in temps_mecanique:
        return "Temps mécanique"
    elif description in temps_routier:
        return "Temps routier"
    else:
        return "Pièces"

# Function to generate the report
def generate_report(file):
    df = pd.read_excel(file, engine='openpyxl')
    
    # Initialize variables
    report = {}
    current_vendor = None
    
    # Iterate through each row in the dataframe
    for index, row in df.iterrows():
        if pd.notna(row['Unnamed: 7']):
            current_vendor = row['Unnamed: 7']
            if current_vendor not in report:
                report[current_vendor] = {"Temps mécanique": 0, "Temps routier": 0, "Pièces": 0, "Total": 0}
        elif current_vendor:
            category = categorize_work(row['Article'])
            amount = row['Montant vente']
            if pd.notna(amount) and isinstance(amount, (int, float)):
                report[current_vendor][category] += amount
                report[current_vendor]["Total"] += amount
    
    # Convert the report dictionary to a dataframe
    report_df = pd.DataFrame.from_dict(report, orient='index')
    
    return report_df

# Streamlit app
st.title("Générateur de rapport par vendeur")
uploaded_file = st.file_uploader("Téléverser un fichier Excel", type=["xlsx"])

if uploaded_file:
    report_df = generate_report(uploaded_file)
    st.write("Rapport généré :")
    st.dataframe(report_df)
    
    # Provide download link for the report
    report_csv = report_df.to_csv().encode('utf-8')
    st.download_button("Télécharger le rapport", report_csv, "rapport_vendeurs.csv", "text/csv")
