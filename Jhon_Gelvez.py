#calculadora interes compuesto Cde n = C de o * (1+ i )**n
# Variable,Nombre,Descripción
# Cn​,Capital Final o Monto,"El valor total al final de la inversión o préstamo, es decir, el capital inicial más todos los intereses generados."
# C0​,Capital Inicial o Principal,La cantidad de dinero invertida o prestada al comienzo de la operación.
# i,Tasa de Interés por período,"La tasa de interés aplicada, expresada en formato decimal (ej. 5% se escribe como 0.05). Debe estar ajustada al período de capitalización (ver nota abajo)."
# n,Número de Períodos,La cantidad total de veces que el interés se capitaliza (se suma al capital).

# entrada de datos por el usuario 
# aporte_inicial 
# aporte_adicional #valor mensual o anual 
# tasa de interes - anual o mensual
# numero de periodos 

# imprimir el total en aportes 
# el total de interes se calcula cada mes y se suma para obtener este dato
# total
# una grafica 
# opcional una tabla

separator = "-------------------------------"


def get_numeric_input(prompt_message):
    while True:
        try:
            # 1. Obtener la entrada del usuario como una cadena de texto (str)
            raw_input = input(prompt_message + ": ")
            
            # 2. Reemplazar comas por puntos (unificar el separador a punto)
            sanitized_input = raw_input.replace(",", ".")
            
            # 3. Eliminar la parte decimal si existe
            # Buscar la posición del primer punto
            if "." in sanitized_input:
                # Si hay un punto, nos quedamos solo con la parte ANTES del punto
                # Por ejemplo: "10.99" se convierte en "10"
                sanitized_input = sanitized_input.split(".")[0]
            
            # 4. Intentar convertir la cadena resultante a un número entero (int)
            # Esta conversión fallará si la cadena está vacía o contiene letras.
            valor = int(sanitized_input)
            
            return valor # Si la conversión es exitosa, retorna el valor y sale del bucle
            
        except ValueError:
            # Si la conversión falla (porque quedó una cadena vacía o tiene letras, etc.)
            print(separator)
            print("❌ ¡Entrada inválida! Por favor, ingrese un número entero válido (solo dígitos).")
            print(separator)

def compund_interest():
    print("Interes compuesto")

    print(separator)
    
    initial_capital = get_numeric_input("Ingrese el capital inicial")

    periodic_contribution = get_numeric_input("Contribucion mensual")

    number_period = get_numeric_input("Cantidad de tiempo")
    # periodo de tiempo
    while True:

        time_period = get_numeric_input("El tiempo esta en\n1: años\n2:meses\n")

        if time_period == 1:

            year = True
            month = False
            break

        elif time_period == 2:  

            number_period = number_period / 12
            month = True
            year = False
            break
        else:
            print("El valor no es un numero")

    nominal_annual_interest = get_numeric_input("Tasa de interes estimada (valor entero)") / 100

    #fecuencia de capitalizacion
    while True:
        try:
            # capitalization_frequency = get_numeric_input("Ingrese la frecuencia de capitalización ")
            option_frecuenci = input("Ingrese la frecuencia de capitalización\n1:anualmente\n2:semestralmente\n3:trimestralmete\n4:mensualmente\n5:diariamente")

            if type(option_frecuenci) == int:
                raise ValueError("Valor invalido. Ingrese un numero")

            match option_frecuenci:
                case 1:
                    capitalization_frequency = 1
                    break # Opción válida, salimos del bucle
                case 2:
                    capitalization_frequency = 2
                    break
                case 3:
                    capitalization_frequency = 4  # 4 trimestres en un año
                    break
                case 4:
                    capitalization_frequency = 12 # 12 meses en un año
                    break
                case 5:
                    capitalization_frequency = 365 # 365 días en un año
                    break
                case _:
                    # Esto se activa si el usuario ingresa 6, 7, 0, etc.
                    print(separator)
                    print("❌ Opción inválida. El número debe estar entre 1 y 5.")
                    print(separator)               
        except:
            pass

    # Fórmula CORRECTA para el capital inicial
    future_amount_of_initial_capitalization = initial_capital * ((1 + (nominal_annual_interest / capitalization_frequency)) ** (capitalization_frequency * number_period))

    future_amount_of_regular_capitalization = periodic_contribution * (((1 + (nominal_annual_interest / capitalization_frequency)) ** (capitalization_frequency * number_period)-1)) / (nominal_annual_interest / capitalization_frequency)

    total = future_amount_of_initial_capitalization + future_amount_of_regular_capitalization

    total_compound_interest = round(total)

    #total aportado
    total_contributed = periodic_contribution * (number_period * capitalization_frequency) + initial_capital #----------REVISAR

    #total generado de interes
    total_interest = total_compound_interest - total_contributed

    print(f"El total del ahorro en {number_period} es: {total_compound_interest}")
    print(f"Total aportado: {total_contributed}")
    print(f"El interes total generado (- tus ahorros): {total_interest}")
        
def main():
    compund_interest()

if __name__ == "__main__":
    main()