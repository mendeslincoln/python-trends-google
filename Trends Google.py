#Retorna Trends Topics do Google
#Alimentado pela API pytrends - https://github.com/GeneralMills/pytrends
#Lincoln Mendes - https://lincolnmendes.com.br

#LIBS
import pandas as pd                        
from pytrends.request import TrendReq
pytrend = TrendReq()
from datetime import datetime

#Retorna uma lista com range definido
def retorna_lista(inicial,final):
    lista =[]
    for i in range(inicial,final):
            lista.append(i)
       
    return lista

#TOP  20 assuntos do momento (Brasil)
def retornaTopVinteBrasil():
   
    df_trending_br_now=  pd.DataFrame(pytrend.trending_searches(pn="brazil"))
    df_trending_br_now.columns = ['Assunto']
    df_trending_br_now['Ranking'] = retorna_lista(1,21)
    
    return df_trending_br_now
    
#TOP  20 assuntos do momento (Mundo)
def retornaTopVinteWord():
    
    df_trending_word_now=  pd.DataFrame(pytrend.trending_searches())
    df_trending_word_now.columns = ['Assunto']
    df_trending_word_now['Ranking'] = retorna_lista(1,21)
    
    return df_trending_word_now


#Consultas relacionadas dos top 5 assuntos do momento
def retornaAssuntoRelacionados():
    lista=[]
    for i in range(0,5):
        lista.append(df_trending_br_now.iloc[i,0])

    pytrend.build_payload(lista, cat=0, timeframe='now 1-d', geo='BR', gprop='')
    df_aux = pd.DataFrame(pytrend.related_queries() )
    df_related_queries =pd.DataFrame()

    for i in range(0,len(lista)):
        df_related_queries[lista[i]] = df_aux[lista[i]]["top"]['query']
    
    df_related_queries = df_related_queries.T
    
    return df_related_queries

#top 10 assuntos do ano (Brasil)
def retornaTopAno():
    anos = [2015,2016,2017,2018,2019,2020]
    lista_aux = []
    df_final = pd.DataFrame({})
           
    for i in range(0,len(anos)):
        df_trending_year = pd.DataFrame(pytrend.top_charts(anos[i], hl='pt-br', tz=300, geo='BR'))
        lista_aux.append(df_trending_year.iloc[:10,0])

    df_trending_year=  pd.DataFrame(lista_aux)
    df_trending_year = df_trending_year.T
    df_trending_year.columns = [anos]
    df_trending_year['Ranking'] = retorna_lista(1,11)
    
    return df_trending_year


df_trending_br_now = retornaTopVinteBrasil()
df_trending_word_now = retornaTopVinteWord()
df_related_queries = retornaAssuntoRelacionados()
df_trending_year= retornaTopAno()
print("\n")
print("Consulta: " + datetime.today().strftime('%Y-%m-%d %H:%M'))
print("Tendências de Pesquisas Diárias (Brasil) ")
print("------------------------------------------------------------")
print(df_trending_br_now)

print("\n")
print("Consulta: " + datetime.today().strftime('%Y-%m-%d %H:%M'))
print("Tendências de Pesquisas Diárias (Mundo) ")
print("------------------------------------------------------------")
print(df_trending_word_now)


