'''
1) Hacer un programa donde se pida un nombre por teclado y se imprima “Hola 
..el_nombre_ingresado” 
'''
name = input("hello enter your name: \t")
print(f"Hello {name}")

'''
2) Hacer un programa que solicite por teclado dos números y muestre la suma , la resta ,la 
multiplicación y la división de esos números 
'''
def matematicas (num1: int, num2: int):
    suma = num1 + num2
    resta = num1 - num2
    multiplicacion = num1 * num2
    division = num1 / num2

    if num2 == 0:
        raise ZeroDivisionError("No se puede dividir por cero")
    else:
        print(f"""La suma de tus numeros es: {suma}\n
            la resta es {resta}\n 
            la multiplicacion es: {multiplicacion}\n
            la division es {division}""")

num1 = int(input("Ingresa un numero:\t"))
num2 = int(input("Ingresa un numero:\t"))

matematicas(num1, num2)

'''
3) Hacer un programa que solicite una edad y determine si es mayor de edad. 
4)Hacer un programa que solicite una edad e imprima “Es mayor” si es mayor de edad , 
sino que imprima “Es menor”.
'''

edad = int(input("Ingresa tu edad:\t"))

if edad >= 18:
    print("Eres mayor de edad")
else:
    print("Eres menor de edad")

'''
5)Hacer un programa que solicite un color por teclado e imprima “Puede pasar “ si el 
color ingresado es verde , “Precaución “ si es amarillo , “No pasar “ si es rojo o “Color 
inválido” si es cualquier otro. 
'''
def semaforo(color:str):
    if color.lower() == "verde":
        print(f"{color} - Puede pasar")
    elif color.lower() == "amarillo":
        print(f"{color} - Precaución")
    elif color.lower() == "rojo":
        print(f"{color} - No pasar")
    else:
        print(f"{color} - Color inválido")
    
color = input("Ingrese un color del semáforo:\t")
semaforo(color)

'''
6) Hacer un programa que cuente desde el 1 al 100 y los imprima uno a uno.
'''
num = [print(f"Este es el numero: {n}") for n in range(1,101) ]
print("\n")
'''
7) Hacer un programa que cuente del 1 al 100 inclusive e imprima sólo los números pares 
'''
num = [print(f"Este es el numero: {n}") for n in range(1,101) if n % 2 == 0 ]
print("\n")
'''
8) Hacer un programa que cuente del 1 al 100 inclusive e imprima los números que son 
divisibles por 2 y por 5.
'''
num = [print(f"Este es el numero: {n}") for n in range(1,101) if n % 2 == 0 and n % 5 == 0]
print("\n")

'''
9) Hacer un programa que imprima una tabla de multiplicar del 2 al 9 . Cada uno debe 
mostrar sus valores multiplicados del 1 al 9 inclusive 
'''
for n in range(2,10):
    for y in range(1,11):
        print(f" {n} x {y} = {n * y}\n")

'''
10) Hacer un programa que muestre el siguiente dibujo. 
         *  *  *  *  *  *  *  *  *  * 
         *  *  *  *  *  *  *  *  *  * 
         *  *  *  *  *  *  *  *  *  * 
         *  *  *  *  *  *  *  *  *  * 
         *  *  *  *  *  *  *  *  *  *
'''
for n in range (5):
    print("*" * 10)
print("\n")
'''
11)   Hacer un programa donde se muestre el siguiente dibujo 
          
         *  *  *  *  *  *  *  *  *  * 
         *                                    * 
         *                                    * 
         *                                    * 
         *  *  *  *  *  *  *  *  *  *
'''
for n in range(5):
    if n == 0 or n == 4:
        print("*" * 10)
    else:
        print("*           *")

print("\n")
'''
12)Hacer un programa que muestre el siguiente dibujo 
         * 
         *    * 
         *    *    * 
         *    *    *     * 
         *    *    *     *     * 
'''
for fila in range(1, 6):
    print("*" * fila)

print("\n")
'''
13) Idem  anterior con este dibujo 
         *    *     *     *     * 
         *    *     *     *     
         *    *     * 
         *    * 
         *
'''
for fila in range(5, 0, -1):
    print("*" * fila)