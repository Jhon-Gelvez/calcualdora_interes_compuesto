import sys
import json

# Separador visual para mejorar la lectura en consola
separator = "-------------------------------"

# Lista donde se guardarán valores finales generados por el usuario
values_user = list()

# -----------------------------------------------------------
# Función: get_float_input
# Solicita un número flotante permitiendo formatos con puntos,
# comas y miles. Limpia y normaliza el número antes de convertirlo.
# -----------------------------------------------------------
def get_float_input(prompt_message):
    while True:
        try:
            raw_input = input(prompt_message).strip()

            # Evita cadenas vacías
            if raw_input == "":
                print(separator)
                print("Ingrese un numero.")
                print(separator)
                continue

            # Quitar espacios internos
            raw = raw_input.replace(" ", "")

            # Contar separadores
            dots = raw.count('.')
            commas = raw.count(',')

            sanitized = raw

            # Caso: mezcla de punto y coma
            if dots > 0 and commas > 0:
                # La coma es decimal si su posición es posterior al último punto
                if raw.rfind(',') > raw.rfind('.'):
                    sanitized = raw.replace('.', '')
                    sanitized = sanitized.replace(',', '.')
                else:
                    sanitized = raw.replace(',', '')
            
            else:
                # Solo puntos
                if dots > 1 and commas == 0:
                    last_dot_pos = raw.rfind('.')
                    part_after_last_dot = raw[last_dot_pos + 1:]

                    # Último punto es decimal
                    if len(part_after_last_dot) < 3 and part_after_last_dot.isdigit():
                        before_last_dot = raw[:last_dot_pos].replace('.', '')
                        after_last_dot = raw[last_dot_pos + 1:]
                        sanitized = before_last_dot + '.' + after_last_dot
                    else:
                        sanitized = raw.replace('.', '')

                # Solo comas
                elif commas > 1 and dots == 0:
                    last_comma_pos = raw.rfind(',')
                    part_after_last_comma = raw[last_comma_pos + 1:]

                    # Última coma es decimal
                    if len(part_after_last_comma) < 3 and part_after_last_comma.isdigit():
                        before_last_comma = raw[:last_comma_pos].replace(',', '')
                        after_last_comma = raw[last_comma_pos + 1:]
                        sanitized = before_last_comma + ',' + after_last_comma
                    else:
                        sanitized = raw.replace('.', '')

                # Un único separador: si es coma, asumimos decimal
                elif commas == 1 and dots == 0:
                    part_after = raw.split('.')[-1]
                    if len(part_after) == 3 and part_after.isdigit():
                        sanitized = raw.replace(',', '')

                # Un único punto: puede ser decimal o miles
                elif dots == 1 and commas == 0:
                    part_after = raw.split('.')[-1]
                    if len(part_after) == 3 and part_after.isdigit():
                        sanitized = raw.replace('.', '')

            # Convertir a float
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


# -----------------------------------------------------------
# Función: get_int_input
# Solicita un entero. Si ingresan decimales, toma solo la parte entera.
# -----------------------------------------------------------
def get_int_input(prompt_message):
    while True:
        try:
            raw_input = input(prompt_message)

            # Cambiar coma por punto
            sanitized_input = raw_input.replace(",", ".")

            # Eliminar decimales si existen
            if "." in sanitized_input:
                sanitized_input = sanitized_input.split(".")[0]

            valor = int(sanitized_input)
            return valor

        except ValueError:
            print(separator)
            print("¡Entrada inválida! Por favor, ingrese un número entero válido (solo dígitos).")
            print(separator)


# -----------------------------------------------------------
# Función: compund_interest
# Calcula el interés compuesto con capital inicial, aportes mensuales,
# tiempo y frecuencia de capitalización. Devuelve el monto final.
# -----------------------------------------------------------
def compund_interest():
    print("Interes compuesto")
    print(separator)

    # Entradas del usuario
    initial_capital = get_int_input("Ingrese el capital inicial: ")
    periodic_contribution = get_int_input("Contribucion mensual: ")
    number_period = get_float_input("Cantidad de tiempo: ")

    # Selección del tipo de tiempo (años o meses)
    while True:
        time_period = get_int_input("El tiempo esta en\n1: años\n2: meses\n")

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

    # Tasa de interés anual
    nominal_annual_interest = get_float_input("Tasa de interes estimada (%): ") / 100

    # Selección de la frecuencia de capitalización
    while True:
        try:
            option_frecuency = int(input("Ingrese la frecuencia de capitalización\n1:anualmente\n2:semestralmente\n3:trimestralmete\n4:mensualmente\n5:diariamente\n"))

            match option_frecuency:
                case 1: capitalization_frequency = 1; break
                case 2: capitalization_frequency = 2; break
                case 3: capitalization_frequency = 4; break
                case 4: capitalization_frequency = 12; break
                case 5: capitalization_frequency = 365; break
                case _: 
                    print(separator)
                    print("Opción inválida. El número debe estar entre 1 y 5.")
                    print(separator)

        except ValueError:
            print("Valor invalido. Ingrese un numero")

    # Cálculo del interés compuesto
    future_amount_of_initial_capitalization = initial_capital * ((1 + (nominal_annual_interest / capitalization_frequency)) ** (capitalization_frequency * number_period))

    future_amount_of_regular_capitalization = periodic_contribution * (
        ((1 + (nominal_annual_interest / capitalization_frequency)) ** (capitalization_frequency * number_period) - 1)
        ) / (nominal_annual_interest / capitalization_frequency)

    total = future_amount_of_initial_capitalization + future_amount_of_regular_capitalization
    total_compound_interest = round(total)

    # Total aportado por el usuario
    total_contributed = periodic_contribution * (number_period * capitalization_frequency) + initial_capital

    # Interés generado
    total_interest = total_compound_interest - total_contributed

    # Mostrar información detallada
    print(separator)
    print("Informacion detallada")
    detalied_info = {
        "Inversion inicial": initial_capital,
        "Contribucion mensual": periodic_contribution,
        "Cantidad de tiempo": time_period,
        "Tasa de interes": nominal_annual_interest,
        "Frecuencia de capitalizacion": capitalization_frequency,
        "Total generado": total_compound_interest,
        "Total ahorrado (inicial + regular)": round(total_contributed, 2),
        "Total generado de intereses": round(total_interest, 2)
    }
    print(json.dumps(detalied_info, indent=4))
    print(separator)

    return total_compound_interest


# -----------------------------------------------------------
# Función: option_menu
# Menú principal que permite:
# 1. Calcular interés compuesto
# 2. Guardar el último valor generado
# 3. Ver valores guardados
# 4. Salir
# -----------------------------------------------------------
def option_menu():
    ultimo_valor = None

    while True:
        print("\nMENU PRINCIPAL")
        print(separator)
        print("1. Calcular nuevo interes compuesto")

        if ultimo_valor is not None:
            print("2. Guardar ultimo valor generado (" + str(ultimo_valor) + ")")
        else:
            print("2. Guardar (No disponible - Calcule primero)")

        print("3. Ver valores guardados")
        print("4. Salir")
        print(separator)

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            ultimo_valor = compund_interest()

        elif opcion == "2":
            if ultimo_valor is not None:
                values_user.append(ultimo_valor)
                print("Valor guardado correctamente.")
                ultimo_valor = None
            else:
                print("Primero debe realizar un calculo (Opcion 1).")

        elif opcion == "3":
            print("\nValores guardados:")
            if not values_user:
                print("No hay valores guardados.")
            for i, valor in enumerate(values_user, 1):
                print(f"{i}: {valor}")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            print("Saliendo...")
            sys.exit()

        else:
            print("Opcion no valida.")


# -----------------------------------------------------------
# Función principal
# -----------------------------------------------------------
def main():
    option_menu()


# Punto de entrada del programa
if __name__ == "__main__":
    main()
