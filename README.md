import streamlit as st
import pandas as pd

def puhdista_tiedot(df):
    df = df.iloc[4:, 4:10]  # Poistetaan ylimääräiset rivit ja sarakkeet
    df.columns = ["Juttu", "Avustaja", "Teksti", "Kuvat", "Yhteensä", "Laskutettu"]
    df = df.dropna(subset=["Juttu", "Avustaja"], how="all")
    df = df.iloc[1:].reset_index(drop=True)  # Poistetaan ylimääräinen otsikkorivi
    df["Teksti"] = pd.to_numeric(df["Teksti"], errors="coerce").fillna(0)
    df["Kuvat"] = pd.to_numeric(df["Kuvat"], errors="coerce").fillna(0)
    df["Yhteensä"] = pd.to_numeric(df["Yhteensä"], errors="coerce").fillna(0)
    return df

def muodosta_viestit(df):
    avustajat = df.groupby("Avustaja")
    sahkopostit = {}
    for avustaja, data in avustajat:
        if pd.isna(avustaja):
            continue
        juttulista = "\n".join([f"{row['Juttu']}: Teksti {row['Teksti']} €, Kuvat {row['Kuvat']} €, Yhteensä {row['Yhteensä']} €" for _, row in data.iterrows()])
        viesti = f"""Hei {avustaja},

Kiitos paljon jutustasi! Laita se laskutukseen seuraavin tiedoin:

{juttulista}

Ystävällisin terveisin,
Sari
"""
        sahkopostit[avustaja] = viesti
    return sahkopostit

def main():
    st.title("Chatbot avustajien palkkioille")
    st.write("Lataa Excel-tiedosto, niin muodostamme sähköpostiviestit.")
    uploaded_file = st.file_uploader("Lataa Excel-tiedosto", type=["xlsx"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        df = puhdista_tiedot(df)
        sahkopostit = muodosta_viestit(df)
        
        st.write("### Muodostetut sähköpostiviestit:")
        for avustaja, viesti in sahkopostit.items():
            with st.expander(avustaja):
                st.text(viesti)
        
        # Tallennetaan viestit tekstitiedostoksi
        output_text = "\n".join([f"{viesti}\n{'='*50}" for viesti in sahkopostit.values()])
        st.download_button("Lataa viestit tekstitiedostona", output_text, "sahkopostit.txt")

if __name__ == "__main__":
    main()
