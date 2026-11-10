from servicios.indicadores_service import consultar_indicador, obtener_historial

def menu_indicadores():
    print("\n--- MENÚ INDICADORES ---")
    print("1. Consultar valor actualizado (API)")
    print("2. Ver historial guardado (Local)")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        resultado = consultar_indicador()
        dato = resultado["dato"]
        if dato:
            print(f"\nDólar: {dato.valor} {dato.unidad}")
            print(f"Fecha del dato: {dato.fecha}")
            print(f"Origen: {resultado['origen']}")
            print(f"Estado: {resultado['mensaje']}")
        else:
            print(f"\n[!] Error: {resultado['mensaje']}")
            
    elif opcion == "2":
        historial = obtener_historial()
        print("\n--- HISTORIAL DE DÓLAR ---")
        if not historial:
            print("No hay registros en la base de datos.")
        for dato in historial:
            print(f"{dato.fecha} | {dato.valor} {dato.unidad} (Actualizado: {dato.verificado_en})")