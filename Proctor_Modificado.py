import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression


peso_molde_suelo = np.array([11345, 11562, 11770, 11785])
peso_molde = np.array([6737, 6737, 6737, 6737])
#Usamos el metodo "subtract" de Numpy para restar los elementos de 2 matrices
peso_suelo_compactado = np.subtract(peso_molde_suelo, peso_molde)
volumen_molde = np.array([2121,2121,2121,2121])
#Usamos el metodo "divide" de Numpy para dividir los elementos de 2 matrices
densidad_humeda = np.divide (peso_suelo_compactado, volumen_molde)
peso_suelo_humedo_tara = np.array([524.3, 501.4, 467, 415])
peso_suelo_seco_tara = np.array([515, 484, 442, 386])
#Restamos las matrices peso_suelo_humedo_tara  y peso_suelo_seco_tara
peso_agua = np.subtract(peso_suelo_humedo_tara, peso_suelo_seco_tara)
peso_tara = np.array([0,0,0,0])
peso_suelo_seco = np.subtract(peso_suelo_seco_tara, peso_tara)
#Contenido de humedad es el peso de agua multiplicado x 100 y dividido entre el peso de suelo seco
contenido_humedad = np.divide(peso_agua*100,peso_suelo_seco)
contenido_humedad_0 = contenido_humedad/100
unidad = np.array([1,1,1,1])
contenido_humedad_1 = np.add(contenido_humedad_0 , unidad)
#La Densidad Seca es igual a la Densidad Humeda entre ( 1 mas el contenido de humedad)
densidad_seca = np.divide(densidad_humeda,contenido_humedad_1)

# Hacemos un ajuste polinomial de grado 3 a los datos contenido_Humedad y densidad_Seca y guarda los coeficientes en la variable coeficientes.
coeficientes = np.polyfit(contenido_humedad,densidad_seca,3)
#Con los coeficientes formamos nuestro polinomio el cual sera ecuacion de nuestra funcion o curva de compacatcion
poly = np.poly1d(coeficientes)
# Calculamos la primera derivada para halla el optimo contenido de humedad
derivada = np.polyder(poly)
# La primera derivada lo igualamos a cero y obtenemos las raices de la ecuacion
raices = np.roots(derivada)
optimo_contenido_humedad = np.max(raices)
# La maxima Densidad Seca lo obtenemos luego de evaluar el optimo contenido de humedad en la ecuacion almacenada en la variable "poly"
maxima_densidad_seca = poly(optimo_contenido_humedad)

# Calcularemos el optimo contenido de humedad  y maxima densidad seca de forma estadistica, crearemos 100 puntos equidistantes entre el minimo y maximo valor de contenido de humedad.
contenido_humedad_rango = np.linspace(min(contenido_humedad), max(contenido_humedad),100)

# Cada uno de los 100 puntos lo evaluamos en nuestra funcion almacenada en "poly" y esos resusltados lo almacenamos en la variable "prediccion_densidad_seca"
prediccion_densidad_seca = poly(contenido_humedad_rango)

#Calculamos la maxima densidad seca aplicando la funcion max a los 100 valores alamcenados en prediccion_densidad_seca
max_densidad_seca = np.max(prediccion_densidad_seca)

# Encuentra el índice del valor máximo de densidad seca entre los valores predichos.
indice_max = np.argmax(prediccion_densidad_seca)

# Encuentra el valor de contenido de humedad correspondiente al máximo de densidad seca.
optimo_contenido_Humedad = contenido_humedad_rango[indice_max]

# Graficamos los puntos de dispersion y la curva de nuestra funcion
plt.scatter(contenido_humedad, densidad_seca)
plt.plot(contenido_humedad_rango, prediccion_densidad_seca)

# Calcular las coordenadas de los puntos máximos
x_max= optimo_contenido_Humedad
y_max= max_densidad_seca

# Agregar líneas verticales y horizontales que llegan solo hasta el punto máximo de la curva, para eso usamos los metodos axvline y axhline
plt.axvline(x = x_max, ymin= 0 , ymax = y_max, color ='red', linestyle='--')
plt.axhline(y = y_max, xmin= 0 , xmax = x_max, color ='red', linestyle='--')


# Le agregamos a nuestro grafico las etiquetes en los ejes X e Y y un titulo
plt.xlabel('CONTENIDO DE HUMEDAD (%)')
plt.ylabel('DENSIDAD SECA (gr/cm3)')
plt.title('CURVA DE COMPACTACION')

# Agregar leyenda con el valor de la máxima densidad seca y el contenido óptimo de humedad, con bbox agregamos estilos a la leyenda.
plt.text(0.03, 0.85, f' Optimo Contenido Humedad(%):{optimo_contenido_Humedad:.2f}\nMaxima Densidad Seca(gr/cm3):{max_densidad_seca:.2f}', horizontalalignment = 'left', verticalalignment = 'top', transform = plt.gca().transAxes, bbox = dict(facecolor='green', alpha=0.5, edgecolor='black', boxstyle ='round, pad=0.6'))

# Le agregamos los grid horizontales y verticales a nuestro grafico
plt.grid(True)

plt.show()