import sys
import json

# Separador visual para mejorar la lectura en consola
separator = "-------------------------------"

# Lista donde se guardarán valores finales generados por el usuario
values_user = list()

# -----------------------------------------------------------
# Función: get_int_input
# Solicita un entero. Si ingresan decimales, toma solo la parte entera.
# -----------------------------------------------------------
def get_int_input(prompt_message: str):
    while True:
        try:
            prompt_message = input(prompt_message).strip()
            prompt_message = prompt_message.replace(".", "")
            prompt_message = prompt_message.replace(",", "")
            prompt_message = int(prompt_message)
            return prompt_message
            
        except ValueError:
            print(separator)
            print("¡Entrada inválida! Por favor, ingrese un número entero válido (solo dígitos).")
            print(separator)
            
# -----------------------------------------------------------
# Función: get_float_input
# Solicita un número flotante permitiendo formatos con puntos,
# comas y miles. Limpia y normaliza el número antes de convertirlo.
# -----------------------------------------------------------
# -----------------------------------------------------------
# Función: get_float_input (CORREGIDA)
# Solicita un número flotante. Asume coma (,) como separador decimal
# y punto (.) como separador de miles.
# -----------------------------------------------------------
def get_float_input(prompt_message: str):
    while True:
        user_input = input(prompt_message).strip()
        
        try:
            # 1. Limpiar separador de miles (PUNTO)
            # Ejemplo: '1.000.000,50' -> '1000000,50'
            # clean_input = user_input.replace(".", "")
            
            # 2. Reemplazar separador decimal regional (COMA) por el estándar de Python (PUNTO)
            # Ejemplo: '1000000,50' -> '1000000.50'
            clean_input = user_input.replace(",", ".")
            
            # 3. Intentar convertir a float
            number = float(clean_input)
            return number
            
        except ValueError:
            print(separator)
            print("¡Entrada inválida! Por favor, ingrese un número válido (ej: 12.5 o 12,5 para decimales; use puntos para miles, ej: 1.000.000).")
            print(separator)

# -----------------------------------------------------------
# Función: compund_interest
# Calcula el interés compuesto con capital inicial, aportes mensuales,
# tiempo y frecuencia de capitalización. Devuelve el monto final.
# -----------------------------------------------------------
def compund_interest():
    print("Interes compuesto")
    print(separator)

    # Capital y contribucion mensual
    initial_capital = get_int_input("Ingrese el capital inicial (solo números separados por punto): ")
    periodic_contribution = get_int_input("Contribucion mensual (solo números separados por punto): ")

    # Tiempo
    while True:
        # unidad
        while True:
            time_period = get_int_input(
                "La unidad de tiempo sera\n"
                "1: años\n"
                "2: meses\n"
            )
            
            if  time_period in (1, 2):
                break
            else:
                print(separator)
                print(f"¡Opción inválida! Debe ser 1 o 2, no '{time_period}'.")
                print(separator)
                
        number_period = get_float_input("Cantidad de tiempo (puede usar 12, 12.5, 44.6): ")
        original_number_period = number_period
        
        if time_period == 1:
            time_unit_str = "años"
            break
        else:
            number_period = number_period / 12
            time_unit_str = "meses"
            break

    # Interes
    nominal_annual_interest = get_float_input(
        "Tasa de interes estimada (%) (ej: 12, 12.5, 0.5): "
    ) / 100

    # Frecuencia de capitalización
    while True:
        try:
            option_frecuency = int(input(
                "Ingrese la frecuencia de capitalización\n"
                "1: anualmente\n"
                "2: semestralmente\n"
                "3: trimestralmente\n"
                "4: mensualmente\n"
                "5: diariamente\n"
            ))

            frequency_name = ""
            
            match option_frecuency:
                case 1: 
                    capitalization_frequency = 1
                    frequency_name = "1 vez al año (Anual)"
                    break
                case 2: 
                    capitalization_frequency = 2
                    frequency_name = "2 veces al año (Semestral)"
                    break
                case 3: 
                    capitalization_frequency = 4
                    frequency_name = "4 veces al año (Trimestral)"
                    break
                case 4: 
                    capitalization_frequency = 12
                    frequency_name = "12 veces al año (Mensual)"
                    break
                case 5: 
                    capitalization_frequency = 365
                    frequency_name = "365 veces al año (Diaria)"
                    break
                case _:
                    print(separator)
                    print("Opción inválida. El número debe estar entre 1 y 5.")
                    print(separator)
        except ValueError:
            print("Valor invalido. Ingrese un numero")

    # Tasa por periodo
    rate_per_period = nominal_annual_interest / capitalization_frequency

    # Periodos de capitalización (interés)
    periods_interest = capitalization_frequency * number_period

    # Convertir aporte mensual → aporte por periodo de capitalización
    # Son dos valores independientes que debe normalizarse a los periodos
    # Aporte mensual * (12 / capitalizaciones_por_año)
    contribution_per_period = periodic_contribution * (12 / capitalization_frequency)

    # Capital inicial compuesto
    future_initial = initial_capital * ((1 + rate_per_period) ** periods_interest)

    # Fondo acumulado por aportes periódicos (aportes periódicos + sus intereses)
    if rate_per_period == 0:
        future_contributions = contribution_per_period * periods_interest
    else:
        future_contributions = contribution_per_period * (
            ((1 + rate_per_period)**periods_interest - 1) / rate_per_period
        )

    # Total final
    total = future_initial + future_contributions
    total_compound_interest = round(total, 2)

    # Total aportado 
    total_contributed = initial_capital + (periodic_contribution * (number_period * 12))

    # Intereses reales generados
    total_interest = round(total_compound_interest - total_contributed, 2)

    # Output
    print(separator)
    print("Informacion detallada")
    detalied_info = {
        "Inversion inicial": initial_capital,
        "Contribucion mensual": periodic_contribution,
        "Cantidad de tiempo": f"{original_number_period} {time_unit_str}",
        "Tasa de interes": f"{nominal_annual_interest * 100}%",
        "Frecuencia de capitalizacion": frequency_name,
        "Total ahorrado (inicial + regular)": round(total_contributed, 2),
        "Total generado de intereses": total_interest,
        "Total generado": total_compound_interest
    }
    print(json.dumps(detalied_info, indent=4, ensure_ascii=False))
    print(separator)

    return total_compound_interest

# -----------------------------------------------------------
# Función: option_menu
# Menú principal actualizado con instrucciones claras.
# -----------------------------------------------------------
def option_menu():
    ultimo_valor = None

    while True:
        print("\nMENU PRINCIPAL")
        print(separator)
        print("1. Calcular nuevo interes compuesto")
        print("   (Debe ingresar números limpios: 1000 o 1.000)")

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
