import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="Questionário EFCA", layout="centered")

opcoes = {"Nunca": 1, "Raras vezes": 2, "Às vezes": 3, "Quase sempre": 4, "Sempre": 5}

perguntas = {
    2: "Acalmo minhas emoções com comida.",
    4: "Tenho o hábito de beliscar.",
    7: "Belisco entre as refeições por ansiedade, tédio, solidão, medo, raiva, tristeza ou cansaço.",
    10: "Como nos momentos em que estou emocionalmente abalado.",
    1: "Como até me sentir muito cheio.",
    3: "Peço mais comida quando termino meu prato.",
    6: "Costumo comer mais de um prato nas refeições principais.",
    5: "Quando começo a comer algo que gosto muito, tenho dificuldade em parar.",
    8: "Sinto-me tentado a comer ao ver/cheirar comida de que gosto.",
    12: "Quando estou diante de algo que gosto muito, mesmo sem fome, acabo por comê-la.",
    14: "Quando como algo que gosto, finalizo toda a porção.",
    9: "Tomo café da manhã todos os dias (pontuação invertida).",
    11: "Pulo alguma refeição principal.",
    16: "Passo mais de 5 horas do dia sem comer.",
    13: "Como muita comida em pouco tempo.",
    15: "Quando como algo que gosto muito, como muito rápido."
}

respostas = {}
st.title("Escala de Fenótipos de Comportamento Alimentar (EFCA)")
st.write("Responda cada pergunta:")

for idx in sorted(perguntas.keys()):
    escolha = st.radio(perguntas[idx], list(opcoes.keys()), key=idx)
    valor = opcoes[escolha]
    if idx == 9:
        valor = 6 - valor
    respostas[idx] = valor

def calcular_resultados(respostas):
    resultados = {}
    resultados['Comer Emocional'] = sum(respostas[i] for i in [2,4,7,10])
    resultados['Hiperfagia'] = sum(respostas[i] for i in [1,3,6])
    resultados['Comer Hedônico'] = sum(respostas[i] for i in [5,8,12,14])
    resultados['Comer Desorganizado'] = sum(respostas[i] for i in [9,11,16])
    resultados['Comer Compulsivo'] = sum(respostas[i] for i in [13,15])
    return resultados

def classificar(valor, limites):
    if valor <= limites[0]:
        return "Baixo"
    elif limites[0] < valor <= limites[1]:
        return "Médio"
    else:
        return "Alto"

def gerar_pdf(respostas, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Questionário EFCA - Resultados", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(0, 10, "Respostas:", ln=True)
    for idx in sorted(respostas.keys()):
        pdf.multi_cell(0, 8, f"{idx}) {perguntas[idx]} - Nota: {respostas[idx]}")

    pdf.ln(5)
    pdf.cell(0, 10, "Resultados:", ln=True)
    classificacoes = {
        'Comer Emocional': (8,12),
        'Hiperfagia': (5,8),
        'Comer Hedônico': (11,14),
        'Comer Desorganizado': (4,6),
        'Comer Compulsivo': (3,6)
    }
    for dominio, score in resultados.items():
        faixa = classificacoes[dominio]
        categoria = classificar(score, faixa)
        pdf.cell(0, 8, f"{dominio}: {score} pontos - {categoria}", ln=True)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    return pdf_output

if st.button("Gerar PDF"):
    resultados = calcular_resultados(respostas)
    pdf_file = gerar_pdf(respostas, resultados)
    st.download_button(
        label="📄 Baixar Resultados em PDF",
        data=pdf_file,
        file_name="resultados_efca.pdf",
        mime='application/pdf'
    )
