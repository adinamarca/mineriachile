#!/usr/bin/env python
# coding: utf-8

# # Industria minera en Chile
# 
# ### Notebook  por Alejandro Dinamarca

# La minería, de acuerdo con el “Anuario de la Minería de Chile”, realizado por el Servicio Nacional de Geología y Minería (SERNAGEOMIN), “*es una de las actividades económicas más importantes a nivel global, centrada, esencialmente, en la explotación, procesamiento y comercialización de minerales metálicos, minerales no metálicos o rocas y minerales industriales (RMI), y recursos energéticos…*” (**Anuario de la Minería de Chile 2018 – SERNAGEOMIN**).
# 
# Es decir, trata de un sector productivo que, a escala global, posee una importancia creciente, la que está ligada desde el siglo XIX al advenimiento de la Industria Eléctrica, que desde la Segunda Revolución Industrial, ha evolucionado velozmente a la par de los avances tecnológicos de la última década. Esto ha provocado la creciente demanda de metales con características competitivas, como el cobre, dominante por sus propiedades mecánicas y eléctricas, sumado a su bajo costo, y entre otros.
# 
# Por ello, y otras causas, el sector productivo y el mercado de la explotación de minas y canteras ha sufrido constantes evoluciones, siendo pilar en las transformaciones futuras de la sociedad.
# A modo explicativo, el siguiente inciso abordará la metodología con la cual se realizará el análisis del mercado nacional e internacional.
# 
# 
# Las exportaciones de minerales y metales, en Chile y en el año 2019, representan el 52.1% (en porcentaje de exportaciones de mercancías). Posicionando a Chile en primer lugar a nivel mundial como productor de cobre.
# 
# > Para el análisis, se desarrolla el siguiente notebook donde se trabajará con datos de distintas fuentes.

# ## Metodología
# 
# Previo al análisis, se debe recopilar información del sector productivo de la explotación de mineras y canteras en Chile.
# 
# Con la consecución del objetivo anterior, la información debe ser extraída, procesada y posteriormente, visualizada, de forma sencilla, a partir de gráficos.
# 
# De esa forma, no solo se logra un análisis desde el punto de vista del relator, sino también, un análisis desde el punto de vista del lector, a partir de las tendencias que dichos gráficos puedan presentar.
# 
# Debido a que se cubrirá un gran volumen de datos, se hará uso de código de programación, por lo que en orden para extraer, procesar y visualizar se utilizará Python y librerías tales como: 
# 
# * Pandas (para manejo de datos).
# 
# * Numpy (para álgebra y operaciones matriciales).
# 
# * Matplotlib o Seaborn (para visualizar a partir de los datos procesados).
# 
# * Entre otras librerías.
# 
# Sin embargo, las fuentes deben estar en archivos leíbles para computadoras:
# 
# * Archivos separados por coma (extensión .CSV).
# 
# * Planillas EXCEL exportables.
# 
# * Entre otros.
# 

# ## Librerías/paquetes

# In[103]:


# Manejo y manipulación de datos
import pandas as pd

# Álgebra
import numpy as np

# Gráficos
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import matplotlib
import matplotlib.ticker as mtick
import seaborn as sns
### Para mejor visualización
sns.set(rc={'figure.figsize':(10,8.27)})

# Otros
from IPython.display import Markdown
import json

# Traducción (no es estable, se descarta uso)
# import googletrans
# from googletrans import Translator
# translator = Translator()


# ## Obtención de datos

# In[208]:


# Manipulando datos para trabajarlos

## 9. Analizar importancia del sector productivo para el mercado nacional e internacional

### Producción de cobre por compañía (INE)
csv_compañia = pd.read_csv('./cobre/compania.csv', index_col=0)

### Producción de minerales metálicos a nivel nacional (INE)
csv_minerales = pd.read_csv('./mineral_general/mineral_produccion.csv', index_col=0)

### Producción de minerales no metálicos a nivel nacional (INE)
csv_minerales_no = pd.read_csv('./mineral_general/mineral_produccion_no.csv', index_col=0)

### Producción de cobre por región (datos.gob.cl)
csv_region = pd.read_csv('./cobre/region.csv', index_col=0)

### Producción de Cu, Ag, Au, Mo y Fe
v = ['cu', 'ag', 'au', 'mo', 'fe']
for minerale in v:
    exec("""csv_{} = pd.read_csv("./paises/compartepais_{}.csv", sep=';', skiprows=1, index_col=0)""".format(minerale, minerale))

### Producción de minerales y metales por país ()

## 10. Variación del precio de los últimos cinco años y causa de este cambio

### Saldo balanza comercial
csv_balanza = pd.read_csv("./paises/Balanza_comercial.csv", sep=';', skiprows=4, index_col=0, usecols=range(10),
                         encoding='latin-1', )

### Exportaciones (Databank)
csv_export = pd.read_csv('./paises/exportacionpais.csv', skiprows=4)

### Aporte al PIB (Databank)
csv_pib = pd.read_csv('./paises/pibpais.csv', skiprows=4)

### Precio del cobre (Macrotrends)
csv_pcobre = pd.read_csv('./cobre/precios.csv', skiprows=15)


# ## Manipulando datos

# In[308]:


# Manipulando datos (para inciso 9)

## Producción de cobre por compañía
compañia = csv_compañia

### Limpiando carácteres indeseados
compañia['2018'] = csv_compañia['2018'].replace(
    '\.', '', regex=True).replace(',', '.', regex=True)
compañia = compañia.transpose()
compañia.iloc[1:].index = pd.DatetimeIndex(compañia.index[1:]).year
### Limpiando comas indeseadas
compañia = compañia.replace(',','.', regex=True).replace('-',0, regex=True).astype(float)
compañia_cumsum = compañia.cumsum()

### Producción por mineral metálico
minerales = csv_minerales.groupby(['Year', 'Metallic and non-metallic minerals'], as_index=False
                                 ).sum().drop(['Flag Codes', 'Flags'], axis=1)
### Traduciendo
minerales.columns = ['Año', 'Categoría', 'Valor total']
trad = {'Copper':'Cobre', 'Gold':'Oro', 'Iron':'Hierro', 'Lead':'Plomo', 'Manganese':'Manganeso', 'Molybdenum':'Molibdeno',
        'Silver':'Plata', 'Zinc':'Zinc' }
minerales['Categoría'] = minerales['Categoría'].apply(lambda x: trad[x])
minerales.index = minerales['Año']
minerales.drop('Año', axis=1, inplace=True)

### Producción por mineral no metálico
minerales_no = csv_minerales_no.groupby(['Year', 'Metallic and non-metallic minerals'], as_index=False
                                 ).sum().drop(['Flag Codes', 'Flags'], axis=1)
### Traduciendo
minerales_no.columns = ['Año', 'Categoría', 'Valor total']
trad__no = minerales_no['Categoría'].unique() + ['" : "Barita', '" : "Compuestos de boro', '" : "Carbonato de calcio', '" : "Arcillas',
        '" : "Diatomita', '" : "Dolomita', '" : "Feldespato', '" : "Yodo', '" : "Compuestos de litio',
        '" : "Nitratos', '" : "Rocas ornamentales', '" : "Rocas fosfóricas', '" : "Yeso',
        '" : "Compuestos de potasio', '" : "Pumicita', '" : "Pirofilita',
        '" : "Recursos de silicio', '" : "Cloruro de sodio', '" : "Sulfato de sodio', '" : "Talco',
        '" : "Zeolitas', '" : "Sulfato de cobre', '" : "Compuestos de azufre', '" : "Turba',
        '" : "Perlita']
i = 0
trad_no = ''
for val in trad__no.tolist():
    if i == 0:
        trad_no += '{'
    if i < 1:
        trad_no += '"' + '"'.join([val])
    else:
        trad_no += '", "' + '"'.join([val])
    i += 1
trad_no += '"}'
trad_no_metalicos = json.loads(trad_no)
minerales_no['Categoría'] = minerales_no['Categoría'].apply(lambda x: trad_no_metalicos[x])
minerales_no.index = minerales_no['Año']
minerales_no.drop('Año', axis=1, inplace=True)

## Proporción de distintos minerales por país en torno a producción mundial

### Corrigiendo comas
for minerale in v:
    exec("""{} = csv_{}.replace(',', '.', regex=True).drop(['Rank 2018', 'unit', 'Production 2019', 'Share cum.%', 'Share HHI'], axis=1, )
    """.format(minerale, minerale))

# Manipulando datos (para inciso 10)

### Balanza comercial
### Filas útiles
balanza = csv_balanza[1:223]
### Nombre de columnas
balanza.columns = ['Mes', 'Exportaciones Mensuales', 'Exportaciones Acumuladas Anuales', 'Importaciones Mensuales',
                  'Importaciones Acumuladas Anuales', 'Saldo Mensual Balanza Comercial', 
                   'Saldo Acumulado Anual Balanza Comercial', 'Saldo Mensual Balanza Pagos', 
                   'Saldo Acumulado Anual Balanza Pagos']
### Diccionario para meses
meses = {'Enero': 1, 'Enero ': 1, 'Febrero': 2, 'Febrero ': 2, 'Marzo': 3, 'Marzo ': 3,
         'Abril': 4, 'Abril ': 4, 'Mayo': 5, 'Mayo ': 5,
         'Junio': 6, 'Junio ': 6, 'Julio': 7, 'Julio ': 7, 'Agosto': 8, 'Agosto ': 8,
         'Septiembre': 9, 'Septiembre ': 9, 'Octubre': 10, 'Octubre ': 10,
         'Noviembre': 11, 'Noviembre ': 11, 'Diciembre': 12, 'Diciembre ': 12}
balanza.Mes = balanza.Mes.apply(lambda x: meses[x])
### Para rellenar años
añito = balanza.index.to_frame().fillna(method='ffill')
balanza.index = añito['Año']
### Juntando fechitas
balanza.index = pd.to_datetime(balanza.index + '-' + balanza.Mes.astype(str))
### Columna de estado de balanza comercial
balanza['Resultado'] = ['Superávit comercial o neutro' if x > 0 else 'Déficit comercial' for x in balanza['Saldo Mensual Balanza Comercial']]

## Exportaciones
export = csv_export[csv_export['Country Name'] == 'Chile'][csv_export.columns[4:-1]].transpose()[37]

## Aporte al PIB
pib = csv_pib[csv_pib['Country Name'] == 'Chile'][csv_pib.columns[4:-1]].transpose()[37]

## Precio del cobre
pcobre = csv_pcobre
pcobre.index = pd.to_datetime(pcobre['date'])
pcobre.index = pd.DatetimeIndex(pcobre.index).year
pcobre = pcobre.groupby(pcobre.index).mean()[1:-1]
pcobre.index = pib.index

## Datos
data = pd.DataFrame([export, pib, pcobre[' value']]).transpose()
data.columns = ['Exportaciones (%)', 'Aporte PIB (%)', 'Precio del cobre (dólares)']
data.index = pd.to_datetime(csv_export.columns[4:-1]).transpose()
display(Markdown('## Exportaciones y otros del cobre'), data, 
        Markdown('## Producción de cobre en miles de TM por compañía por año'), compañia,
        Markdown('## Producción de cobre en miles de TM por compañía acumulada por año'), compañia_cumsum,
        Markdown('## Producción de minerales metálicos en Chile, por año y categoría'), minerales,
        Markdown('## Producción de minerales no metálicos en Chile, por año y categoría'), minerales_no)

## Otros datos
elementos = [ag, au, fe, mo, cu]
for minerale in v:
    display(Markdown('## Ranking de producción de {} por país en proporción a producción mundial'.format(minerale)))
    exec('display({}[:10])'.format(minerale))
display(Markdown('## Balanza comercial Chile'), balanza)


# ## Función para graficar

# In[107]:


### Definiendo función para graficar
def dispersion(x, y, data, tamaño=(9, 6), res=100, 
               color=None , titulo=None, xlabel=None, ylabel=None, sym=None
               ):
    fig, ax = plt.subplots(figsize=tamaño, dpi=res)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(symbol=sym))
    plt.scatter(x=x, y=y, color=color, data=data)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()
    
def bar(data, tamaño=(9, 6), res=100, x=None, y=None,
               color=None , titulo=None, xlabel=None, ylabel=None, rot=0, ci=None, offset=True
               ):
    fig, ax = plt.subplots(figsize=tamaño, dpi=res)
    sns.barplot(data=data, x=x, y=y, hue=color, ci=ci)
    plt.title(titulo)
    plt.xticks(rotation=rot)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.show()
    
def lin(data, tamaño=(9, 6), res=100, 
               color=None , titulo=None, xlabel=None, ylabel=None, rot=0
               ):
    fig, ax = plt.subplots(figsize=tamaño, dpi=res)
    sns.lineplot(data=data)
    ax.get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    plt.xticks(rotation=rot)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# ## Mercado nacional
# 
# La gran minería en Chile, de acuerdo con el Consejo Minero, se sitúa en siete regiones a lo largo del país, aportando, con un poco más del 10% al PIB nacional (Minería en Números 2020 – Consejo Minero).
# Por otro lado, según datos recabados desde The World Bank, sitúa a Chile con un aporte de los recursos metales y minerales al PIB levemente inferior al 12.5%, de forma similar a  **SERNAGEOMIN** en el “Anuario de la Minería 2020 en Chile”. El gráfico de tendencia se puede apreciar a continuación, en la Figura 1.

# In[108]:


# Gráfico simple de aporte al PIB de las exportaciones de recursos naturales
dispersion(x=data.index, y='Aporte PIB (%)', data=data, color='tab:orange',
          xlabel='Año', ylabel='Aporte al PIB en porcentaje', 
          titulo='Aporte al PIB de los recursos naturales en Chile (%)', sym='%')


# ### Producción nacional de minerales metálicos
# 
# Dentro de los minerales metálicos en el país, se produce cobre y molibdeno en mayor proporción, seguido de oro, plata, hierro, manganeso, plomo y zinc, los cuales se encuentran en distintos tipos de yacimientos a lo largo del territorio. Asimismo, Chile cuenta con mineralizaciones de distinta importancia de cobalto, tungsteno, titanio, cromo, uranio y mercurio, los que, de acuerdo al SERNAGEOMIN en 2015, aún no estaban siendo explotados.
# Con respecto a la producción de la minería a gran, mediana y pequeña escala, se adjunta el siguiente gráfico de producción total agrupados por mineral y año, a partir de los datos dispuestos por el Instituto Nacional de Estadísticas de Chile en su portal (ine.stat).

# In[109]:


bar(data=minerales[-35:], x='Categoría', y='Valor total', color=minerales[-35:].index,
   titulo='Producción chilena de minerales metálicos (2015 a 2019)',
   xlabel='Mineral', ylabel='Producción (millones de toneladas métricas finas)',
   tamaño=(10, 6))


# En el caso del cobre, se puede apreciar que, el año 2018 se alcanzó el máximo de producción de los últimos cinco años, siguiendo el más cercano, el 2019.
# Por otra parte, el hierro es el mineral metálico con mayor producción en Chile. De acuerdo a un reportaje de Minería Chilena, “el país solo produce el 0.38% de este mineral a nivel mundial, que no solo le permiten autoabastecerse, sino que también destinar una parte a la exportación, principalmente, al mercado asiático” (El nuevo impulso del hierro en Chile - Minería Chilena).
# 
# Por otro lado, el oro, plomo, molibdeno, plata y zinc no se aprecian en el gráfico - por la escala de producción del hierro y el cobre -, por lo que, realizaremos un gráfico comparativo entre los minerales con menor producción.
# 

# In[110]:


bar(data=minerales[(minerales.loc[:, 'Categoría'] != 'Cobre') &
          (minerales.loc[:, 'Categoría'] != 'Hierro') ][-25:], x='Categoría', y='Valor total', 
    color=minerales[(minerales.loc[:, 'Categoría'] != 'Cobre') &
          (minerales.loc[:, 'Categoría'] != 'Hierro') ][-25:].index,
   titulo='Producción chilena de minerales metálicos (2015 a 2019), excluyendo cobre y hierro',
   xlabel='Mineral', ylabel='Producción (millones de toneladas métricas finas)',
   tamaño=(10, 6))


# ### Producción nacional de minerales no metálicos
# 
# En cuanto los minerales no metálicos, y de acuerdo al SERNAGEOMIN en Chile país minero, además de cobre, “en el país existen del orden de 40 recursos, ubicados en diferentes tipos de yacimientos localizados en distintas regiones del territorio nacional” (CHILE-PAIS-MINERO-ADEMAS-DE-COBRE.pdf).
# 
# De acuerdo a la misma fuente, los recursos de mayor importancia tecnológica y económica – en cuanto a sus usos y propiedades -, corresponden a los recursos que se ubican en campos de nitratos y en los salares del norte de Chile, los que se encuentran en la Depresión Intermedia de las Regiones de Tarapacá, como también, de Antofagasta, las que contienen nitratos, yodo y sulfato de sodio, de los que cuales, los nitratos y el yodo son explotados por diversas empresas nacionales y extranjeras, produciendo diferentes productos finales entre los que se encuentran el nitrato de sodio, nitrato de potasio, entre otros.
# 
# Además, en los salares, existen recursos tales como cloruro de sodio y sulfato de sodio en los salares de la cordillera de la Costa y de la Depresión Intermedia. De hecho, en la Región de Tarapacá, se encuentran sales de litio, potasio y boro.
# 
# Por supuesto, falta por añadir los recursos de rocas y minerales industriales, los que, en gran parte se destinan a consumo interno para construcción, como también, los recursos del sector Minero Metalúrgico, como las calizas y cuarzo, usados en la propia metalurgia del cobre, oro y hierro.
# 

# In[111]:


bar(data=minerales_no[356:], x='Categoría', y='Valor total', color=minerales_no[356:].index,
   titulo='Producción chilena de minerales no metálicos (2015 a 2019)',
   xlabel='Mineral', ylabel='Producción (millones de toneladas métricas finas)',
   tamaño=(10, 6),
   rot=90)


# A partir de la visualización, el cloruro de sodio es el mineral no metálico más producido en Chile a lo largo de los años, el cual, de acuerdo al Anuario de la Minería de Chile, edición del 2019, del SERNAGEOMIN, es prácticamente 100% producido en la Región de Tarapacá. Incluso, desde el 2009 es el recurso de mayor volumen de producción en Chile, superando por poco al hierro y ampliamente al cobre en tonelaje (contrastando con el gráfico de minerales metálicos).

# ### Cobre
# 
# A modo de reducir el análisis, y considerando que la mayor producción de Chile es cobre, se adjunta un gráfico en la Figura 2, a partir del repositorio de datos abiertos centralizado del Estado, diferenciando por cada una de las mineras y sus subdivisiones que estuvieron o están activas, desde 1998 al 2018, con cifras acumulativas de producción de cobre fino en miles de toneladas.
# 

# In[112]:


### Gráficamos aquellas compañías mineras con producción acumulada sobre las 8000 miles de toneladas de cobre fino
lin(data=compañia_cumsum.loc[:, (compañia_cumsum[compañia_cumsum.columns]  > 8000).any()].iloc[:, :-1],
   rot=45,
   titulo='Serie de tiempo de producción de cobre por minera en Chile (1998 a 2018)',
   xlabel='Año',
   ylabel='Producción de cobre fino en miles de toneladas (total)')


# In[113]:


### Gráfico comparativo de producción de cobre por minera en Chile
bar(data=compañia.iloc[:, :-1].sum().to_frame().transpose(), ci=None,
   titulo='Producción de cobre por minera en Chile (1998 a 2018)',
   xlabel='Minera', ylabel='Producción de cobre fino en miles de toneladas (total)',
   tamaño=(10, 6), rot=90)


# In[114]:


### Gráfico comparativo de Divisiones de Codelco (entidad pública)
bar(data=compañia.iloc[:, :-1].iloc[:, compañia.iloc[:, :-1].columns.str.
                contains('División')].sum().to_frame().transpose(), ci=None,
   titulo='Producción de cobre por divisiones de CODELCO en Chile (1998 a 2018)',
   xlabel='División', ylabel='Producción de cobre fino en miles de toneladas (total)',
   tamaño=(10, 6), rot=45)


# In[115]:


display(Markdown('> En total, CODELCO suma **{}** miles de toneladas de cobre fino.'.format(compañia.iloc[:, :-1]
                 .iloc[:, compañia.iloc[:, :-1].sum().to_frame().
                 transpose().columns.str.contains('División')].sum().sum())))


# In[116]:


elementos = [ag, au, fe, mo, cu]
nomb = ['Plata', 'Oro', 'Hierro', 'Molibdeno', 'Cobre']
i = 0
for el in elementos:
    if nomb[i] == 'Hierro':
        fig, ax = plt.subplots()
        ax.pie(el[:16]['Share in %'], labels=el[:16].Country, autopct='%1.1f%%',
                 startangle=5, explode=[0.05]*16, labeldistance=1.05, radius=1, pctdistance=1.4)
        plt.title('Gráfico de torta de producción mundial de {}'.format(nomb[i]), pad=60, loc='left')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
    else:
        fig, ax = plt.subplots()
        ax.pie(el[:10]['Share in %'], labels=el[:10].Country, autopct='%1.1f%%',
                 startangle=10, explode=[0.15]*10, labeldistance=1.2, radius=2)
        plt.title('Gráfico de torta de producción mundial de {}'.format(nomb[i]), pad=40, loc='left')
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()
    i += 1


# In[365]:


ax = sns.displot(data=balanza, 
                x=balanza.index,
                hue='Resultado', kde=True)
plt.title('Distribución de resultados de balanza comercial en Chile a lo largo de los años')
ax.set(xlabel='Año', ylabel='Conteo de resultados mensuales por año')
plt.show()


# In[364]:


ax = sns.scatterplot(data=balanza, 
                x=balanza.index, y='Saldo Mensual Balanza Comercial',
                hue='Resultado')
plt.title('Saldo de balanza comercial en millones de dólares (fob) en Chile')
ax.set(xlabel='Año', ylabel='Conteo de resultados mensuales por año')
plt.show()


# In[118]:


# Gráfico simple de exportaciones chilenas
dispersion(x=data.index, y='Exportaciones (%)', data=data, color='tab:blue',
          xlabel='Año', ylabel='Exportaciones de minerales y metales', 
          titulo='Porcentaje de exportaciones chilenas de minerales y metales (% de exportaciones totales)',
          sym='%')


# In[119]:


# Gráfico simple del precio del cobre en dólares
dispersion(x=data.index, y='Precio del cobre (dólares)', data=data, color='tab:green',
          xlabel='Año', ylabel='Precio en dólares', 
          titulo='Precio del cobre en dólares histórico', sym='US')


# In[368]:


data.corr()

