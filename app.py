import pandas as pd
import streamlit as st
import plotly.express as px

# Lendo a base de dados
df = pd.read_csv("acidentes2022.csv", on_bad_lines="skip", sep=";")

df["vitimasfatais"] = df["vitimasfatais"].str.replace(",", ".").astype(float)
df["vitimas"] = df["vitimas"].str.replace(",", ".").astype(float)

clima = df["tempo_clima"].value_counts().sort_values(ascending=False)

bairro = df["bairro"].value_counts().head(10).sort_values(ascending=True)


# alterando coluna de data para datetime
df["data"] = pd.to_datetime(df["data"])

# Criando coluna de mês
df["Mês_Acidente"] = df["data"].dt.month

total_mes = df["Mês_Acidente"].value_counts().reset_index()
total_mes = total_mes.sort_values(by="index")

def main():

    st.header("Acidentes de Trânsito em Recife - 2022")
    #st.markdown("<h1 style='text-align: center;'>Acidentes de trânsito em Recife</h1>", #unsafe_allow_html=True)

    total_acidentes = df.shape[0]
    total_com_vitimas = "{:.0f}".format(df["vitimas"].sum())
    total_vitimas_fatais = "{:.0f}".format(df["vitimasfatais"].sum())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Acidentes 🚦", total_acidentes)

    with col2:
        st.metric("Total com vítimas🚨", total_com_vitimas)

    with col3:
        st.metric("Total com vítimas fatais🪦", total_vitimas_fatais)



    fig = px.bar(clima, text=clima.values, color_discrete_sequence=["#FF4500"])
    fig.update_layout(title="Total de acidentes por Clima", title_x=0.1)
    st.plotly_chart(fig)

    fig1 = px.bar(bairro, text=bairro.values,
             color_discrete_sequence=["#FF4500"], orientation="h")
    fig1.update_layout(title="Top 10 acidentes por Bairro", title_x=0.1)
    st.plotly_chart(fig1)

   st.write(total_mes)
    fig2 = px.line(total_mes, x="Mês_Acidente", y="count",
              color_discrete_sequence=["#FF4500"], markers=True,
              text="count", labels={"Mês":"Mês Acidente", "Total":"Total Acidentes"})
    fig2.update_layout(title='Total de acidentes por mês', title_x=0.5)
    fig2.update_traces(textposition='top center')

    st.plotly_chart(fig2)

if __name__ == "__main__":
    main()
