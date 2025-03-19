import streamlit as st
import pandas as pd

def puhdista_tiedot(df):
    st.write("Excel-sarakkeet ennen käsittelyä:", df.columns.tolist())  # Tulostetaan sarakenimet tarkistusta varten
    df = df.iloc[4:, :].reset_index(drop=True)  # Poistetaan ylimääräiset rivit ja nollataan indeksit
    df.columns = df.iloc[0].astype(str).str.upper()  # Käytetään ensimmäistä riviä sarakeotsikoina ja muutetaan isoksi
    df = df[1:].reset_index(drop=True)  # Poistetaan otsikkorivi taulukosta

    # Tulostetaan sarakenimet uudelleen varmistaaksemme, että ne on asetettu oikein
    st.write("Excel-sarakkeet käsittelyn jälkeen:", df.columns.tolist())

    # Muutetaan sarakenimet vastaamaan odotettuja
    sarakenimet = {"JUTTU": "JUTTU", "AVUSTAJA": "AVUSTAJA", "TEKSTI": "TEKSTI", "KUVAT": "KUVAT", "YHT.": "YHTEENSÄ", "YHTEENSÄ": "YHTEENSÄ", "LASKUTETTU": "LASKUTETTU"}
    df = df.rename(columns=sarakenimet)

    # Valitaan vain tarvittavat sarakkeet
    tarvittavat_sarakkeet = ["JUTTU", "AVUSTAJA", "TEKSTI", "KUVAT", "YHTEENSÄ", "LASKUTETTU"]
    df = df[[col for col in tarvittavat_sarakkeet if col in df.columns]]

    # Muunnetaan numerotyyppiset sarakkeet oikeaan muotoon
    for sarake in ["TEKSTI", "KUVAT", "YHTEENSÄ"]:
        if sarake in df.columns:
            df[sarake] = pd.to_numeric(df[sarake], errors="coerce").fillna(0)

    return df

def muodosta_viestit(df):
    if "AVUSTAJA" not in df.columns:
        st.error("Virhe: 'AVUSTAJA'-sarake puuttuu käsitellystä datasta!")
        st.stop()
    
    avustajat = df.groupby("AVUSTAJA")
    sahkopostit = {}
    for avustaja, data in avustajat:
        if pd.isna(avustaja):
            continue
        juttulista = "\n".join([f"{row['JUTTU']}: Teksti {row['TEKSTI']} €, Kuvat {row['KUVAT']} €, Yhteensä {row['YHTEENSÄ']} €" for _, row in data.iterrows()])
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
        st.write("### Ensimmäiset rivit ennen käsittelyä:")
        st.write(df.head())
        df = puhdista_tiedot(df)
        st.write("### Ensimmäiset rivit käsittelyn jälkeen:")
        st.write(df.head())
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

    main()



