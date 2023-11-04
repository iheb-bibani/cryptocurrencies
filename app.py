import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px

# Liste des cryptomonnaies disponibles
cryptos_disponibles = {
    'Bitcoin (BTC-USD)': 'BTC-USD',
    'Ethereum (ETH-USD)': 'ETH-USD',
    'Cardano (ADA-USD)': 'ADA-USD',
    'Binance Coin (BNB-USD)': 'BNB-USD',
    'Solana (SOL-USD)': 'SOL-USD',
    'XRP (XRP-USD)': 'XRP-USD',
    'Polkadot (DOT-USD)': 'DOT-USD',
    'Dogecoin (DOGE-USD)': 'DOGE-USD',
    'Avalanche (AVAX-USD)': 'AVAX-USD',
    'Chainlink (LINK-USD)': 'LINK-USD'
}

# Sélectionnez la cryptomonnaie
selected_crypto = st.selectbox("Sélectionnez une cryptomonnaie :", list(cryptos_disponibles.keys()))

# Téléchargez les données de la cryptomonnaie sélectionnée
crypto_ticker = cryptos_disponibles[selected_crypto]
crypto_df = yf.download(crypto_ticker, start="2014-01-01", end="2023-12-31")

# Calculer les rendements quotidiens en pourcentage
crypto_df['Rendement Quotidien'] = crypto_df['Adj Close'].pct_change() * 100

# Convertissez l'index en un objet de type 'DatetimeIndex'
crypto_df.index = pd.to_datetime(crypto_df.index)

# Créez une colonne pour l'année correspondante à chaque date
crypto_df['Annee'] = crypto_df.index.year

# Créez une colonne pour le mois correspondant à chaque date
crypto_df['Mois'] = crypto_df.index.month

# Initialiser une liste pour les rendements mensuels par année
rendements_mensuels_par_annee = []

# Parcourir les années
annees_uniques = crypto_df['Annee'].unique()
for annee in annees_uniques:
    annee_df = crypto_df[crypto_df['Annee'] == annee]
    rendements_mensuels = annee_df.groupby(annee_df['Mois'])['Rendement Quotidien'].sum()
    rendements_mensuels_par_annee.append(rendements_mensuels)

# Créez un DataFrame pour les rendements mensuels par année
df_rendements_mensuels = pd.DataFrame(rendements_mensuels_par_annee, index=annees_uniques)

# Triez les colonnes dans l'ordre des mois
mois_labels = {
    1: 'Janvier',
    2: 'Février',
    3: 'Mars',
    4: 'Avril',
    5: 'Mai',
    6: 'Juin',
    7: 'Juillet',
    8: 'Août',
    9: 'Septembre',
    10: 'Octobre',
    11: 'Novembre',
    12: 'Décembre'
}

df_rendements_mensuels = df_rendements_mensuels.rename(columns=mois_labels)

# Définissez une fonction de couleur personnalisée
def color_negative_red(val):
    color = 'red' if val < 0 else 'green'
    return f'color: {color}'

# Appliquez la fonction de couleur personnalisée au DataFrame
styled_df = df_rendements_mensuels.style.applymap(color_negative_red)

# Utilisation de Streamlit pour afficher le tableau sans avoir besoin de spécifier sa taille
st.write(f"Tableau des Rendements Mensuels par Année pour {selected_crypto}")
st.table(styled_df)

# Parcourir les mois et calculer les rendements mensuels
rendements_mensuels = []

for mois in range(1, 13):
    mois_df = crypto_df[crypto_df['Mois'] == mois]
    if len(mois_df) > 0:
        rendement_mensuel = mois_df['Rendement Quotidien'].sum()
        rendements_mensuels.append(rendement_mensuel)

# Créez un DataFrame pour les rendements mensuels
mois_labels = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
rendements_mensuels_df = pd.DataFrame({'Mois': mois_labels, 'Rendement Mensuel': rendements_mensuels})

# Utilisation de Streamlit pour afficher le graphique Plotly
st.title('Rendements Mensuels pour chaque Mois')
fig = px.bar(
    rendements_mensuels_df,
    x='Mois',
    y='Rendement Mensuel',
    labels={'Rendement Mensuel': 'Rendement Mensuel (%)'},
    color='Rendement Mensuel',  # Utilisation de la colonne des rendements comme couleur
    color_continuous_scale='RdYlGn',  # Dégradé de couleurs (vous pouvez en choisir un parmi les palettes disponibles)
)

st.plotly_chart(fig)

mois_labels = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']

# Créez un DataFrame pour les rendements mensuels par mois (tous les mois de toutes les années)
rendements_mensuels_par_mois = []
for mois in range(1, 13):
    rendements_mensuels_mois = []
    for annee in annees_uniques:
        mois_df = crypto_df[(crypto_df['Annee'] == annee) & (crypto_df['Mois'] == mois)]
        rendement_mensuel = mois_df['Rendement Quotidien'].sum()
        rendements_mensuels_mois.append(rendement_mensuel)
    rendements_mensuels_par_mois.append(rendements_mensuels_mois)

# Créez un DataFrame pour les rendements mensuels par mois
df_rendements_mensuels_mois = pd.DataFrame(rendements_mensuels_par_mois, columns=annees_uniques, index=mois_labels)

# Transposez le DataFrame pour avoir les mois en colonnes
df_rendements_mensuels_mois = df_rendements_mensuels_mois.T

# Utilisation de Streamlit pour afficher le graphique Plotly
st.title('Rendements Mensuels par Mois pour Chaque Année')
mois = st.multiselect("Choisir le(s) mois : ",df_rendements_mensuels_mois.columns)
fig = px.line(df_rendements_mensuels_mois,x = df_rendements_mensuels.index,y=mois, title='Rendements Mensuels par Mois pour Chaque Année')

# Personnal'isez les libellés de l'axe X
fig.update_xaxes(ticktext=df_rendements_mensuels.index,title_text='Année')

# Définissez les noms des légendes de l'axe Y
fig.update_yaxes(title_text='Rendement Mensuel (%)')

st.plotly_chart(fig)

