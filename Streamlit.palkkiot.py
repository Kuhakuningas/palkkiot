def puhdista_tiedot(df):
    st.write("Excel-sarakkeet ennen käsittelyä:", df.columns.tolist())  # Tulostetaan sarakenimet

    # Etsitään ensimmäinen rivi, jossa on varsinainen data
    df.columns = df.iloc[0]  # Käytetään ensimmäistä riviä sarakeotsikoina
    df = df[1:].reset_index(drop=True)  # Poistetaan otsikkorivi datasta
    
    # Poistetaan mahdolliset tyhjät sarakkeet
    df = df.dropna(axis=1, how="all")

    # Tulostetaan sarakenimet uudelleen varmistaaksemme, että ne on asetettu oikein
    st.write("Excel-sarakkeet käsittelyn jälkeen:", df.columns.tolist())

    # Normalisoidaan sarakenimet (varmistetaan, että ne ovat odotetussa muodossa)
    sarakenimi_map = {
        "JUTTU": "Juttu",
        "AVUSTAJA": "Avustaja",
        "TEKSTI": "Teksti",
        "KUVAT": "Kuvat",
        "YHT.": "Yhteensä",
        "LASKUTETTU": "Laskutettu"
    }
    df.rename(columns=sarakenimi_map, inplace=True)

    # Tarkistetaan, että oleelliset sarakkeet ovat mukana
    tarvittavat_sarakkeet = list(sarakenimi_map.values())
    df = df[[col for col in tarvittavat_sarakkeet if col in df.columns]]

    # Muutetaan numeeriset sarakkeet oikeaan muotoon
    for sarake in ["Teksti", "Kuvat", "Yhteensä"]:
        if sarake in df.columns:
            df[sarake] = pd.to_numeric(df[sarake], errors="coerce").fillna(0)

    return df
