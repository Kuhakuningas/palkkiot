import streamlit as st
import pandas as pd

def puhdista_tiedot(df):
    st.write("Excel-sarakkeet ennen käsittelyä:", df.columns.tolist())  # Tulostetaan sarakenimet tarkistusta varten
    df = df.iloc[4:, :].reset_index(drop=True)  # Poistetaan ylimääräiset rivit ja nollataan indeksit
    df.columns = df.iloc[0]  # Käytetään ensimmäistä riviä sarakeotsikoina
    df = df[1:].reset_index(drop=True)  # Poistetaan otsikkorivi taulukosta

    # Tulostetaan sarakenimet uudelleen varmistaaksemme, että ne on asetettu oikein
    st.write("Excel-sarakkeet käsittelyn jälkeen:", df.columns.tolist())

    # Valitaan vain tarvittavat sarakkeet riippumatta niiden sijainnista
    tarvittavat_sarakkeet = ["Juttu", "Avustaja", "Teksti", "Kuvat", "Yhteensä", "Laskutettu"]
    df = df[[col for col in tarvittavat_sarakkeet if col in df.columns]]

    # Muunnetaan numerotyyppiset sarakkeet oikeaan muotoon
    for sarake in ["Teksti", "Kuvat", "Yhteensä"]:
        if sarake in df.columns:
            df[sarake] = pd.to_numeric(df[sarake], errors="coerce").fillna(0)

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
