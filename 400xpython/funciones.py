'''
Funciones  
14)Crea un función EscribirCentrado, que reciba como parámetro un texto y lo escriba 
centrado en pantalla (suponiendo una anchura de 80 columnas;  
pista: deberás escribir 40 - longitud/2 espacios antes del texto). Además subraya el mensaje 
utilizando el carácter =. 
'''
def EscribirCentrado(texto: str) -> str:
    longitud: int = len(texto)

    espacios_antes_del_texto: int = 40 - longitud // 2
    espacios_vacios: str = " " * espacios_antes_del_texto
    subrayado: str = "=" * longitud

    if longitud == 0:
        raise ValueError("Escribe algo")
    
    if espacios_antes_del_texto < 0:
        raise ValueError("Algo malió sal")
    return f"{espacios_vacios}{texto}{espacios_vacios}\n{espacios_vacios}{subrayado}{espacios_vacios}"

texto: str = input("A ver...escribe algo\n")
print(EscribirCentrado(texto))
print("\n")
'''
15)Crea un programa que pida dos número enteros al usuario y diga si alguno de ellos es 
múltiplo del otro. Crea una función EsMultiplo que reciba  
los dos números, y devuelve si el primero es múltiplo del segundo. 
'''
def EsMultiplo(num1: int, num2: int) -> bool:
    if num1 % num2 == 0:
        return num1 % num2 == 0
    else:
        return False

num1 = int(input("Ingresa un numero>\t"))
num2 = int(input("Ingresa un numero>\t"))
print(EsMultiplo(num1, num2))
'''
16)Crear una función que calcule la temperatura media de un día a partir de la temperatura 
máxima y mínima.  
Crear un programa principal, que utilizando la función anterior, vaya pidiendo la 
temperatura máxima y mínima de cada día y vaya mostrando la media.  
El programa pedirá el número de días que se van a introducir. 
'''
def temperaturaDelDia(max: float, min: float) -> float:
    return (max + min) / 2

def main(numDias:int):
    resultados:list = []
    for dia in range(numDias):
        temperaturaMax: float = float(input("Ingresa la termperatura maxima:\t"))
        temperaturaMin: float = float(input("Ingresa la termperatura minima:\t"))
        media: float = temperaturaDelDia(temperaturaMax, temperaturaMin)
        resultados.append(f"el dia {dia + 1} se registro una temperatura media de {media} grados")
    return "\n".join(resultados)

numDias: int = int(input("ingresa el numero de dias:\t"))
print(main(numDias))

'''
17)Crea un función “ConvertirEspaciado”, que reciba como parámetro un texto y devuelve una 
cadena con un espacio adicional tras cada letra.  
Por ejemplo, “Hola, tú” devolverá “H o l a , t ú “. Crea un programa principal donde se use 
dicha función. 
'''
def ConvertirEspaciado(texto:str)->str:
    return "".join([f"{t} " for t in texto])

frase:str = input("dí algo:\t")
print(ConvertirEspaciado(frase))
'''
18)Crea una función “calcularMaxMin” que recibe una lista con valores numéricos y devuelve 
el valor máximo y el mínimo.  
Crea un programa que pida números por teclado y muestre el máximo y el mínimo, 
utilizando la función anterior. 
19)Diseñar una función que calcule el área y el perímetro de una circunferencia. Utiliza dicha 
función en un programa principal que lea el radio de  
una circunferencia y muestre su área y perímetro. 
20)Crear una subrutina llamada “Login”, que recibe un nombre de usuario y una contraseña y 
te devuelve Verdadero si el nombre de usuario es “usuario1” 
y la contraseña es “asdasd”. Además recibe el número de intentos que se ha intentado 
hacer login y si no se ha podido hacer login incremente este valor. 
Crear un programa principal donde se pida un nombre de usuario y una contraseña y se 
intente hacer login, solamente tenemos tres oportunidades  
para intentarlo. 
21)Crear una función recursiva que permita calcular el factorial de un número. Realiza un 
programa principal donde se lea un entero y se muestre el resultado  
del factorial. 
22)Crear una función que calcule el MCD de dos número por el método de Euclides. El método 
de Euclides es el siguiente: 
Se divide el número mayor entre el menor. 
Si la división es exacta, el divisor es el MCD. 
Si la división no es exacta, dividimos el divisor entre el resto obtenido y se continúa de esta 
forma hasta obtener una división exacta, siendo el último divisor el MCD. 
Crea un programa principal que lea dos números enteros y muestre el MCD. 
23 Escribir dos funciones que permitan calcular: 
La cantidad de segundos en un tiempo dado en horas, minutos y segundos. 
La cantidad de horas, minutos y segundos de un tiempo dado en segundos. 
Escribe un programa principal con un menú donde se pueda elegir la opción de convertir a 
segundos, convertir a horas,minutos y segundos o salir del programa. 
24)El día juliano correspondiente a una fecha es un número entero que indica los días que han 
transcurrido desde el 1 de enero del año indicado.  
Queremos crear un programa principal que al introducir una fecha nos diga el día juliano 
que corresponde. Para ello podemos hacer las siguientes subrutinas: 
LeerFecha: Nos permite leer por teclado una fecha (día, mes y año). 
DiasDelMes: Recibe un mes y un año y nos dice los días de ese mes en ese año. 
EsBisiesto: Recibe un año y nos dice si es bisiesto. 
Calcular_Dia_Juliano: recibe una fecha y nos devuelve el día juliano. 
25) Vamos a mejorar el ejercicio anterior haciendo una función para validar la fecha. De tal 
forma que al leer una fecha se asegura que es válida. 
26)Queremos crear un programa que trabaje con fracciones a/b. Para representar una fracción 
vamos a utilizar dos enteros: numerador y denominador. 
27) Definir una función max() que tome como argumento dos números y devuelva el mayor de 
ellos.(Es cierto que python tiene una función max() incorporada, pero hacerla nosotros mismos 
es un muy buen ejercicio. 
28) Definir una función max_de_tres(), que tome tres números como argumentos y devuelva 
el mayor de ellos. 
29) Definir una función que calcule la longitud de una lista o una cadena dada. (Es cierto que 
Python tiene la función len() incorporada, pero escribirla por nosotros mismos resulta un muy 
buen ejercicio. 
30)- Escribir una función que tome un carácter y devuelva True si es una vocal, de lo contrario 
devuelve False. 
31) Escribir una funcion sum() y una función multip() que sumen y multipliquen 
respectivamente todos los números de una lista. Por ejemplo: sum([1,2,3,4]) debería devolver 
10 y multip([1,2,3,4])debería devolver 24. 
32) Definir una función inversa() que calcule la inversión de una cadena. Por ejemplo la cadena 
"estoy probando" debería devolver la cadena "odnaborp yotse" 
33) Definir una función es_palindromo() que reconoce palíndromos (es decir, palabras que 
tienen el mismo aspecto escritas invertidas), ejemplo: es_palindromo ("radar") tendría que 
devolver True. 
34)Definir una función superposicion() que tome dos listas y devuelva True si tienen al menos 
1 miembro en común o devuelva False de lo contrario. Escribir la función usando el bucle for 
anidado. 
35) Definir una función generar_n_caracteres() que tome un entero n y devuelva el carácter 
multiplicado por n. Por ejemplo: generar_n_caracteres(5, "x") debería devolver "xxxxx". 
36) Definir un histograma procedimiento() que tome una lista de números enteros e imprima 
un histograma en la pantalla. Ejemplo: procedimiento([4, 9, 7]) debería imprimir lo siguiente: 
**** 
********* 
******* 
'''