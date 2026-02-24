import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="WordCloud Online", layout="centered")

st.title("☁️ Gerador de WordCloud Avançado")
st.write("Cole um texto abaixo e gere sua nuvem de palavras.")

texto = st.text_area("Cole seu texto aqui:", height=250)

col1, col2 = st.columns(2)
with col1:
    largura = st.slider("Largura", 400, 1200, 800)
with col2:
    altura = st.slider("Altura", 200, 800, 400)

cor_fundo = st.selectbox(
    "Cor de fundo",
    ["white", "black", "gray", "lightblue"]
)

if st.button("Gerar WordCloud"):

    if texto.strip() == "":
        st.warning("Por favor, cole algum texto.")
    else:
        # 🔹 Normalizar texto
        texto = texto.lower()
        texto = re.sub(r'[^\w\s]', '', texto)  # remove pontuação

        # 🔹 Remover palavras com 3 letras ou menos
        palavras_filtradas = [
            palavra for palavra in texto.split()
            if len(palavra) > 3
        ]

        texto_limpo = " ".join(palavras_filtradas)

        # 🔹 Stopwords adicionais em português
        stopwords_pt = {
            # artigos
            "o", "a", "os", "as", "um", "uma", "uns", "umas",

            # preposições
            "de", "da", "do", "das", "dos",
            "em", "no", "na", "nos", "nas",
            "por", "para", "perante",
            "entre", "sobre", "contra",
            "desde", "durante", "atraves",

            # conjunções
            "que", "como", "porque",
            "porém", "todavia", "contudo",
            "entretanto", "logo", "pois",
            "quando", "enquanto",

            # pronomes comuns
            "ele", "ela", "eles", "elas",
            "isso", "isto", "aquilo",
            "meus", "suas", "seus"
        }

        stopwords = STOPWORDS.union(stopwords_pt)

        wordcloud = WordCloud(
            width=largura,
            height=altura,
            background_color=cor_fundo,
            stopwords=stopwords,
            colormap="viridis"
        ).generate(texto_limpo)

        fig, ax = plt.subplots(figsize=(largura/100, altura/100))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig)

        # Download
        wordcloud.to_file("wordcloud.png")
        with open("wordcloud.png", "rb") as file:
            st.download_button(
                label="📥 Baixar imagem",
                data=file,
                file_name="wordcloud.png",
                mime="image/png"
            )

        st.success("WordCloud gerada com sucesso!")
