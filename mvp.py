#Loading libraries
import streamlit as st
import numpy as np 
import pandas as pd
import pickle
import os
import math
import pycaret
from pycaret.regression import load_model
from pycaret.regression import *
from pathlib import Path
from pprint import pformat

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()

st.markdown("<h1 style='text-align: center; color: #1088ff;'>RankMyPosition</h1>", unsafe_allow_html=True)
st.markdown("Esta aplicação tem como objetivo prever a posição da categoria de acordo com a categoria do AIS" +
"\n com base na entrada dos dados. Vale destacar que este é um MVP e que sugestões e melhorias são válidas!")
st.markdown("---")
info = st.checkbox("ℹ️ Informações Úteis ")
dict_check = st.checkbox("📕 Dicionário de Dados")
dict_markdown = read_markdown_file("dicionario.md")
info_markdown = read_markdown_file("info.md")
if dict_check:
    st.markdown(dict_markdown, unsafe_allow_html=True)
if info:
  st.markdown(info_markdown, unsafe_allow_html = True)

def _fix_category_appear(my_categorie, other_categories, df):
  zero = 0
  one = 1
  df['Category_AUTO_AND_VEHICLES'] = zero
  df['Category_BUSINESS'] = zero 
  df['Category_FINANCE'] = zero 
  df['Category_HEALTH_AND_FITNESS'] = zero 
  df['Category_LIFESTYLE'] = zero 
  df['Category_SHOPPING'] = zero 
  df['Category_SPORTS'] = zero
  if my_categorie == "AUTO_AND_VEHICLES":    
    print("entrou aqui ")
    df['Category_AUTO_AND_VEHICLES'] = one
    df['Category_BUSINESS'] = zero 
    df['Category_FINANCE'] = zero 
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = zero
  elif my_categorie == "BUSINESS":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = one
    df['Category_FINANCE'] = zero 
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = zero
  elif my_categorie == "FINANCE":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = one 
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = zero
  elif my_categorie == "HEALTH_AND_FITNESS":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero
    df['Category_HEALTH_AND_FITNESS'] = one 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = zero
  elif my_categorie == "LIFESTYLE":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = one 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = zero
  elif my_categorie == "SHOPPING":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = one 
    df['Category_SPORTS'] = zero
  elif my_categorie == "SPORTS":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero
    df['Category_HEALTH_AND_FITNESS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_SPORTS'] = one
  return df

def _fix_category_improve(my_categorie, other_categories, df):
  zero = 0
  one = 1
  df['Category_AUTO_AND_VEHICLES'] = zero
  df['Category_BUSINESS'] = zero 
  df['Category_FINANCE'] = zero 
  df['Category_EVENTS'] = zero 
  df['Category_LIFESTYLE'] = zero 
  df['Category_SHOPPING'] = zero 
  df['Category_TRAVEL_AND_LOCAL'] = zero
  df['Category_MAPS_AND_NAVIGATION'] = zero
  if my_categorie == 'AUTO_AND_VEHICLES':
    df['Category_AUTO_AND_VEHICLES'] = one
    df['Category_BUSINESS'] = zero 
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "BUSINESS":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = one
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "FINANCE":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = one 
    df['Category_EVENTS'] = zero 
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "EVENTS":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = one
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "LIFESTYLE":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero
    df['Category_LIFESTYLE'] = one 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "SHOPPING":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = one 
    df['Category_TRAVEL_AND_LOCAL'] = zero 
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "TRAVEL_AND_LOCAL":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = one  
    df['Category_MAPS_AND_NAVIGATION'] = zero
  elif my_categorie == "MAPS_AND_NAVIGATION":
    df['Category_AUTO_AND_VEHICLES'] = zero
    df['Category_BUSINESS'] = zero
    df['Category_FINANCE'] = zero 
    df['Category_EVENTS'] = zero
    df['Category_LIFESTYLE'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_TRAVEL_AND_LOCAL'] = zero  
    df['Category_MAPS_AND_NAVIGATION'] = one
  return df


def _fix_category_scale(my_categorie, other_categories, df):
  zero = 0
  one = 1
  df['Category_FINANCE'] = zero
  df['Category_MAPS_AND_NAVIGATION'] = zero 
  df['Category_SHOPPING'] = zero 
  df['Category_FOODS_AND_DRINK'] = zero

  if my_categorie == "FINANCE":
    df['Category_FINANCE'] = one
    df['Category_MAPS_AND_NAVIGATION'] = zero 
    df['Category_SHOPPING'] = zero 
    df['Category_FOODS_AND_DRINK'] = zero
  elif my_categorie == "MAPS_AND_NAVIGATION":
    df['Category_FINANCE'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = one 
    df['Category_SHOPPING'] = zero 
    df['Category_FOODS_AND_DRINK'] = zero
  elif my_categorie == "SHOPPING":
    df['Category_FINANCE'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
    df['Category_SHOPPING'] = one 
    df['Category_FOODS_AND_DRINK'] = zero
  elif my_categorie == "FOODS_AND_DRINK":
    df['Category_FINANCE'] = zero
    df['Category_MAPS_AND_NAVIGATION'] = zero
    df['Category_SHOPPING'] = zero 
    df['Category_FOODS_AND_DRINK'] = one
  return df



def fix_category(my_categorie, other_categories,df):
  print("minha categoria é" + my_categorie)                                                                                                                                                                                                                                                                                                                                                                                                                                   
  df = pd.DataFrame({},index = [0])
  
  
  if ais == 'Appear':
    df = _fix_category_appear(my_categorie, other_categories, df)                                                                                         
  elif ais == 'Improve':
    df = _fix_category_improve(my_categorie,other_categories,df)
  elif ais == 'Scale':
    df = _fix_category_scale(my_categorie,other_categories,df)
  return df 
##Entrada de dados

with st.beta_container():
    st.sidebar.image('images/logo_horizontal_branca_png.png',use_column_width=True)
    ativos = st.sidebar.number_input("Por Favor, informe o número de Usuários Ativos (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f", step = 1.0)
    ativos = int(ativos)
    anr = st.sidebar.number_input("Número de ANRs (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f", step = 1.0)
    anr = int(anr)
    falhas = st.sidebar.number_input("Número de Falhas (no dia da observação)",min_value=0.0, max_value=99999999999999.9, format="%1f", step = 1.0)
    falhas = int(falhas)
    installs = st.sidebar.number_input("Número de Instalações (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    installs = int(installs)
    fiveStars = st.sidebar.number_input("Total acumulado de 5 estrelas, métrica retirada na Tool em Rating Analysis (no dia da observação)",min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    fiveStars = int(fiveStars)
    fourStars = st.sidebar.number_input('Total acumulado de 4 estrelas, métrica retirada na Tool em Rating Analysis (no dia da observação)', min_value=0.0, max_value=99999999999999.9, format="%1f", step = 1.0)
    fourStars = int(fourStars)
    threeStars = st.sidebar.number_input("Total acumulado de 3 estrelas, métrica retirada na Tool em Rating Analysis (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    threeStars = int(threeStars)
    twoStars = st.sidebar.number_input("Total acumulado de 2 estrelas, métrica retirada na Tool em Rating Analysis (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    twoStars = int(twoStars)
    oneStar = st.sidebar.number_input("Total acumulado de 1 estrela, métrica retirada na Tool em Rating Analysis (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    total = (fiveStars + fourStars + threeStars + twoStars + oneStar)
    oneStar = int(oneStar)
    score = st.sidebar.number_input("Average Rating,  métrica retirada na Tool em Rating Analysis (no dia da observação).",min_value = 0.0, max_value = 5.0, format = "%.3f")
    score = float(score)
    print(score)
    aquisicao = st.sidebar.number_input("Número de Aquisição de Usuários (no dia da observação)", min_value=0.0, max_value=99999999999999.9, format="%1f",  step = 1.0)
    aquisicao = int(aquisicao)
    nota = st.sidebar.number_input('Nota média do aplicativo (no dia da observação)')
    nota = float(nota)
    print(nota)
    desinstalacoes =0
    #desinstalacoes = int(desinstalacoes)

st.markdown(
    """
<style>
.reportview-container .markdown-text-container {
    font-family: "Ubuntu";
}
.sidebar .sidebar-content {
    background-image: linear-gradient(#1088ff,#0bd6d4);
    color: white;
    font-family: "Ubuntu";
}
.Widget>label {
    
    font-family: "Ubuntu";
}
[class^="st-b"]  {
    
    font-family:"Ubuntu";
}
header .decoration {
    background-image: none;
}
strong {
  color: #1088ff
}
h4 {
  text-align: center;
}
#feedback {
  text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)

### Escolha das Categorias
ais_string = "Informe a Fase do AIS do seu App"
ais = st.selectbox(ais_string,("Appear",'Improve','Scale'))
category_string = "Informe a Categoria do seu App"
if ais == 'Appear': 
    other_categories = ["AUTO_AND_VEHICLES","BUSINESS",
    "FINANCE","HEALTH_AND_FITNESS","LIFESTYLE","SHOPPING","SPORTS"]
    category = st.selectbox(category_string,("AUTO_AND_VEHICLES","BUSINESS",
    "FINANCE","HEALTH_AND_FITNESS","LIFESTYLE","SHOPPING","SPORTS"))
    categories_df = fix_category(category,other_categories, ais)
elif ais == "Improve":
    categories_improve = ('AUTO_AND_VEHICLES', 'BUSINESS',
       'EVENTS', 'FINANCE', 'LIFESTYLE',
       'MAPS_AND_NAVIGATION', 'SHOPPING',
       'TRAVEL_AND_LOCAL')
    category = st.selectbox(category_string,categories_improve)
    other_categories = ['AUTO_AND_VEHICLES', 'BUSINESS',
       'EVENTS', 'FINANCE', 'LIFESTYLE',
       'MAPS_AND_NAVIGATION', 'SHOPPING',
       'TRAVEL_AND_LOCAL']
    categories_df = fix_category(category, other_categories, ais)
elif ais == "Scale":
    categories_scale = ("FINANCE","MAPS_AND_NAVIGATION","SHOPPING","FOODS_AND_DRINK")
    category = st.selectbox(category_string,categories_scale)
    other_categories = ["FINANCE","MAPS_AND_NAVIGATION","SHOPPING","FOODS_AND_DRINK"]
    categories_df = fix_category(category, other_categories, ais)
##container
input_dict = {"Category": category, "Ativos": ativos,
            "ANR": anr, "Falhas": falhas, "Instalações": installs,
            "fiveStars": fiveStars, "fourStars": fourStars,
            "threeStars": threeStars, "twoStars": twoStars,
            "oneStar": oneStar, "total": total,
            "score": score, "Aquisição de Usuários": aquisicao,
            "Nota Média": nota, "Desinstalações": desinstalacoes,
            }
            
df = pd.DataFrame(input_dict, index = [0])
aux_df = pd.concat([df,categories_df],axis = 1)

def dealing_with_appear_regressor(df):
  
  columns = ['Ativos', 'ANR', 'Falhas', 'Instalações', 'fiveStars', 'fourStars',
       'threeStars', 'twoStars', 'oneStar', 'total', 'score',
       'Aquisição de Usuários', 'Nota Média', 'Category_AUTO_AND_VEHICLES', 'Category_BUSINESS',
       'Category_FINANCE', 'Category_HEALTH_AND_FITNESS', 'Category_LIFESTYLE',
       'Category_SHOPPING', 'Category_SPORTS']
  _df = df[columns]
  total = _df["total"]
  _df['oneStarProp'] = round(_df['oneStar']/ total, 2)
  _df['twoStarsProp'] = round(_df['twoStars'] / total, 2)
  _df['threeStarsProp'] = round(_df['threeStars'] / total, 2)
  _df['fourStarsProp'] = round(_df['fourStars'] / total, 2)
  _df['fiveStarsProp'] = round(_df['fiveStars'] / total , 2)
  x_file = open(os.path.join("modelos/", "model_appear_new.pkl"), "rb")
  regressor = pickle.load(x_file)
  x_file.close()
  predictions = regressor.predict(_df)
  return round(predictions[0])

def dealing_with_improve_regressor(df):
  columns = ['Ativos', 'ANR', 'Falhas', 'Instalações', 'fiveStars', 'fourStars',
       'threeStars', 'twoStars', 'oneStar', 'total', 'score',
       'Aquisição de Usuários', 'Nota Média','Desinstalações','Category_EVENTS', 'Category_FINANCE',
       'Category_LIFESTYLE', 'Category_MAPS_AND_NAVIGATION','Category_SHOPPING', 'Category_TRAVEL_AND_LOCAL']
  _df = df[columns]
  x_file = open(os.path.join("", "model_improve_new.pkl"), "rb")
  regressor = pickle.load(x_file)
  x_file.close()
  predictions = regressor.predict(_df)
  print(predictions[0])
  return round(predictions[0])

def dealing_with_scale_regressor(df):
  columns = ['Ativos', 'ANR', 'Falhas', 'Instalações', 'fiveStars', 'fourStars',
       'threeStars', 'twoStars', 'oneStar', 'total', 'score',
       'Aquisição de Usuários', 'Nota Média',
  'Category_FINANCE','Category_FOODS_AND_DRINK','Category_MAPS_AND_NAVIGATION',	'Category_SHOPPING']
  _df = df[columns]
  #x_file = open(os.path.join("modelos/", "model_scale.pkl"), "rb")
  regressor = load_model("modelos/model_scale_sem_desinstalacoes")
  predictions = predict_model(regressor,_df)
  return predictions['Label'].iloc[0].astype(int)
mae = 0
predicted = 0 
lower_bound = 0
upper_bound = 0
if ais == "Appear":
  try:
    mae = 15
    predicted = dealing_with_appear_regressor(aux_df)
    lower_bound = predicted - mae
    upper_bound = predicted + mae
  except ValueError:
    pass
elif ais == 'Improve':
  print("entrou")
  try:
    mae = 5
    predicted = dealing_with_improve_regressor(aux_df)
    lower_bound = predicted - mae
    upper_bound = predicted + mae
  except ValueError:
    pass
elif ais == "Scale":
  print("entrou")
  try:
    mae = 3
    predicted = dealing_with_scale_regressor(aux_df)
    lower_bound = predicted - mae
    if lower_bound <= 0:
      lower_bound = 1
    upper_bound = predicted + mae
  except ValueError:
    pass

if (ativos == 0 and anr == 0 and falhas == 0 and installs == 0 and fiveStars == 0 and fourStars == 0 and threeStars == 0 and twoStars == 0 
    and total == 0 and oneStar == 0 and score == 0.00 and aquisicao == 0 and nota == 0.00 and desinstalacoes ==0):
        st.markdown("<h4>" + "A posição na Categoria do seu App será <strong>" +  str(0)+"</strong>" + "</h4>", unsafe_allow_html=True)
else:
  st.markdown("<h4>" + "A posição na Categoria do seu App estará entre <strong>" + str(int(lower_bound)) +" </strong> à " + "<strong>" +  str(int(upper_bound))+"</strong>" + "</h4>", unsafe_allow_html=True)

st.markdown("<span> </span>", unsafe_allow_html=True)
st.markdown("<span> </span>", unsafe_allow_html=True)
st.markdown("<span> </span>", unsafe_allow_html=True)
st.markdown("<span> </span>", unsafe_allow_html=True)
st.markdown('<h4> Possui alguma sugestão ou melhoria para o RankMyPosition?  <a href = "https://forms.gle/6zSukezWNSrJGfYo7" id = "feedback">' + str("Clique Aqui.") + "</a> </h4>",unsafe_allow_html=True )
