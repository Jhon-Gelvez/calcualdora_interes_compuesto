import sys
import json

# Separador visual para mejorar la lectura en consola
separator = "-------------------------------"

# Lista donde se guardarán valores finales generados por el usuario
values_user = list()

# -----------------------------------------------------------
# Función: format_currency
# Convierte un número a formato monetario colombiano (COP).
# -----------------------------------------------------------
def format_currency(value):
    tmp = "{:,.2f}".format(value)
    tmp = tmp.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"COP {tmp}"


# -----------------------------------------------------------
# Función: get_float_input
# Solicita un número flotante permitiendo formatos con puntos,
# comas y miles. Limpia y normaliza el número antes de convertirlo.
# -----------------------------------------------------------
def get_float_input(prompt_message):
    while True:
        try:
            raw_input_value = input(prompt_message).strip()
            if raw_input_value == "":
                print(separator)
                print("Ingrese un numero.")
                print(separator)
                continue

            raw = raw_input_value.replace(" ", "")
            dots = raw.count('.')
            commas = raw.count(',')

            sanitized = raw

            if dots > 0 and commas > 0:
                if raw.rfind(',') > raw.rfind('.'):
                    sanitized = raw.replace('.', '')
                    sanitized = sanitized.replace(',', '.')
                else:
                    sanitized = raw.replace(',', '')
            else:
                if dots > 1 and commas == 0:
                    last_dot_pos = raw.rfind('.')
                    part_after = raw[last_dot_pos + 1:]
                    if len(part_after) < 3 and part_after.isdigit():
                        sanitized = raw[:last_dot_pos].replace('.', '') + '.' + part_after
                    else:
                        sanitized = raw.replace('.', '')
                elif commas > 1 and dots == 0:
                    last_comma_pos = raw.rfind(',')
                    part_after = raw[last_comma_pos + 1:]
                    if len(part_after) < 3 and part_after.isdigit():
                        sanitized = raw[:last_comma_pos].replace(',', '') + ',' + part_after
                    else:
                        sanitized = raw.replace(',', '')
                elif commas == 1 and dots == 0:
                    part_after = raw.split(',')[-1]
                    if len(part_after) == 3 and part_after.isdigit():
                        sanitized = raw.replace(',', '')
                elif dots == 1 and commas == 0:
                    part_after = raw.split('.')[-1]
                    if len(part_after) == 3 and part_after.isdigit():
                        sanitized = raw.replace('.', '')

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
            raw_input_value = input(prompt_message)
            sanitized_input = raw_input_value.replace(",", ".")
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

    initial_capital = get_int_input("Ingrese el capital inicial: ")
    periodic_contribution = get_int_input("Contribucion mensual: ")
    number_period = get_float_input("Cantidad de tiempo: ")

    original_number_period = number_period  # Guardar unidad real ingresada

    while True:
        time_period = get_int_input("El tiempo esta en\n1: años\n2: meses\n")
        if time_period == 1:
            time_unit_str = "años"
            break
        elif time_period == 2:
            number_period = number_period / 12
            time_unit_str = "meses"
            break
        else:
            print("El valor no es un numero")

    nominal_annual_interest = get_float_input("Tasa de interes estimada (%): ") / 100

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

    rate_per_period = nominal_annual_interest / capitalization_frequency
    periods = capitalization_frequency * number_period

    future_amount_of_initial_capitalization = initial_capital * ((1 + rate_per_period) ** periods)

    if rate_per_period == 0:
        future_amount_of_regular_capitalization = periodic_contribution * periods
    else:
        future_amount_of_regular_capitalization = periodic_contribution * (
            ((1 + rate_per_period) ** periods - 1)
        ) / rate_per_period

    total = future_amount_of_initial_capitalization + future_amount_of_regular_capitalization
    total_compound_interest = round(total, 2)

    total_contributed = periodic_contribution * periods + initial_capital
    total_interest = total_compound_interest - total_contributed

    print(separator)
    print("Informacion detallada")
    detalied_info = {
        "Inversion inicial": format_currency(initial_capital),
        "Contribucion mensual": format_currency(periodic_contribution),
        "Cantidad de tiempo": f"{original_number_period} {time_unit_str}",
        "Tasa de interes": f"{nominal_annual_interest * 100}%",
        "Frecuencia de capitalizacion": capitalization_frequency,
        "Total ahorrado (inicial + regular)": format_currency(round(total_contributed, 2)),
        "Total generado de intereses": format_currency(round(total_interest, 2)),
        "Total generado": format_currency(total_compound_interest)
    }
    print(json.dumps(detalied_info, indent=4, ensure_ascii=False))
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
            print("2. Guardar ultimo valor generado (" + format_currency(ultimo_valor) + ")")
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
                print(f"{i}: {format_currency(valor)}")
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
