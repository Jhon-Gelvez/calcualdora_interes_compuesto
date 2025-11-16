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

def get_float_input(prompt_message):
    while True:
        try:
            raw_input = input(prompt_message + ": ").strip()
            if raw_input == "":
                print(separator)
                print("Ingrese un numero.")
                print(separator)
                continue

            # eliminar espacios internos
            raw = raw_input.replace(" ", "")

            # contar separadores
            dots = raw.count('.')
            commas = raw.count(',')

            sanitized = raw

            # Caso: hay tanto puntos como comas -> decidir por la posición del último separador
            if dots > 0 and commas > 0:
                # si la última coma está después del último punto: coma = decimal (ej: 1.000,50)
                if raw.rfind(',') > raw.rfind('.'):
                    sanitized = raw.replace('.', '')        # quitar miles
                    sanitized = sanitized.replace(',', '.') # coma -> punto decimal
                else:
                    # si el último punto está después: punto = decimal (ej: 1,000.50)
                    sanitized = raw.replace(',', '')        # quitar comas miles
                    # punto ya está como decimal
            else:
                # Solo puntos
                if dots > 1 and commas == 0:
                    # probablemente puntos como separador de miles: 1.000.000 -> 1000000 !!que pasa si es 1.000.35
                    sanitized = raw.replace('.', '')
                # Solo comas
                elif commas > 1 and dots == 0:
                    # probablemente comas como separador de miles: 1,000,000 -> 1000000
                    sanitized = raw.replace(',', '')
                # Un único separador (o ninguno): si es una coma asumimos decimal (ej: 1000,50)
                elif commas == 1 and dots == 0:
                    part_after = raw.split('.')[-1]
                     if len(part_after) == 3 and part_after.isdigit():
                         sanitized = raw.replace(',', '')
                # caso: un solo punto y ninguna coma -> puede ser decimal o miles (1000.50 o 1000)
                # lo dejamos como está (float aceptará 1000.50). Si es "1.000" y significa 1000,
                # esto podría interpretarse como 1.0 en algunos locales; para evitar ambigüedad
                # tratamos "1.000" como 1000 (si después del punto hay exactamente 3 dígitos)
                elif dots == 1 and commas == 0:
                    part_after = raw.split('.')[-1]
                    if len(part_after) == 3 and part_after.isdigit():
                        # 1.000 -> 1000
                        sanitized = raw.replace('.', '')
                    # else: dejamos el punto como decimal (ej: 1000.50)

            # intento de conversión
            valor = float(sanitized)

            if valor < 0:
                print(separator)
                print("¡Entrada inválida! Por favor, ingrese un número no negativo.")
                print(separator)
                continue

            return valor

        except ValueError:
            print(separator)
            print("¡Entrada inválida! Por favor, ingrese un número válido.")
            print(separator)


def get_int_input(prompt_message):
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
            print("¡Entrada inválida! Por favor, ingrese un número entero válido (solo dígitos).")
            print(separator)

def compund_interest():
    print("Interes compuesto")

    print(separator)
    
    initial_capital = get_int_input("Ingrese el capital inicial")

    periodic_contribution = get_int_input("Contribucion mensual")

    number_period = get_float_input("Cantidad de tiempo")
    # periodo de tiempo
    while True:

        time_period = get_int_input("El tiempo esta en\n1: años\n2:meses\n")

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

    nominal_annual_interest = get_float_input("Tasa de interes estimada: ") / 100

    #fecuencia de capitalizacion
    while True:
        try:
            # capitalization_frequency = get_int_input("Ingrese la frecuencia de capitalización ")
            option_frecuency = int(input("Ingrese la frecuencia de capitalización\n1:anualmente\n2:semestralmente\n3:trimestralmete\n4:mensualmente\n5:diariamente\n"))

            if type(option_frecuency) != int:
                raise ValueError("Valor invalido. Ingrese un numero")

            match option_frecuency:
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
                    print("Opción inválida. El número debe estar entre 1 y 5.")
                    print(separator)               
        except ValueError as e:
            print(e)
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

    print(f"El total del ahorro en {number_period:.0f} es: {total_compound_interest}")
    print(f"Total aportado: {total_contributed}")
    print(f"El interes total generado ( - tus ahorros): {total_interest:.2f}")
    print(separator)
    print("Informacion detallada")
    detalied_info = {
        "Inversion inicial" : initial_capital,
        "Contribucion mensual" : periodic_contribution,
        "Cantidad de tiempo" : time_period,
        "Tasa de interes" : nominal_annual_interest,
        "Frecuencia de capitalizacion" : capitalization_frequency,
        "Total generado"  : total_compound_interest,
        "Total ahorrado (inicial + regular)" : total_contributed,
        "Total generado de intereses" : total_interest
    }
    print(detalied_info)
    print(separator)

    if input("Desea calcular otro valor (s/n)") == "n":
        return detalied_info
    else:
        return main()

        
def main():
    compund_interest()

if __name__ == "__main__":
    main()

#diccionario con los valores ingresados e incluir listas
