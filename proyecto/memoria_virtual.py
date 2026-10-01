import sys
import time
import psutil

ELEMENTOS_POR_LOTE = 100000
LONGITUD_STRING = 50
INTERVALO_REPORTE = 5

LIMITE_RAM_PORCENTAJE = 85
LIMITE_ELEMENTOS = 20000000


def obtener_uso_ram_mb():
    proceso = psutil.Process()
    return proceso.memory_info().rss / (1024 * 1024)


def obtener_ram_sistema_porcentaje():
    return psutil.virtual_memory().percent


def main():
    print("=== Estrés de Memoria y Paginación ===")
    print(f"Este script llena una lista con strings para observar memoria virtual.")
    print(f"Límites de seguridad:")
    print(f"  - RAM del sistema <= {LIMITE_RAM_PORCENTAJE}%")
    print(f"  - Máximo {LIMITE_ELEMENTOS:,} elementos")
    print("Presiona Ctrl+C para detener anticipadamente.\n")
    time.sleep(2)

    lista_grande = []
    contador = 0
    ultimo_reporte = time.time()

    try:
        while True:
            if contador >= LIMITE_ELEMENTOS:
                print(f"\n[!] Límite de elementos alcanzado ({LIMITE_ELEMENTOS:,}). Deteniendo por seguridad.")
                break

            uso_sistema = obtener_ram_sistema_porcentaje()
            if uso_sistema >= LIMITE_RAM_PORCENTAJE:
                print(f"\n[!] Límite de RAM del sistema alcanzado ({uso_sistema:.1f}% >= {LIMITE_RAM_PORCENTAJE}%). Deteniendo por seguridad.")
                break

            lote = []
            for i in range(ELEMENTOS_POR_LOTE):
                dato = f"dato_{contador + i}_" + ("x" * LONGITUD_STRING)
                lote.append(dato)
            lista_grande.extend(lote)
            contador += ELEMENTOS_POR_LOTE

            ahora = time.time()
            if ahora - ultimo_reporte >= INTERVALO_REPORTE:
                ultimo_reporte = ahora
                ram_proceso_mb = obtener_uso_ram_mb()
                ram_sistema_pct = obtener_ram_sistema_porcentaje()
                print(f"[{time.strftime('%H:%M:%S')}] "
                      f"Elementos: {contador:>10,} | "
                      f"RAM proceso: {ram_proceso_mb:>8.1f} MB | "
                      f"RAM sistema: {ram_sistema_pct:>5.1f}%")

    except KeyboardInterrupt:
        print(f"\n\n[X] Proceso detenido por el usuario.")

    finally:
        print()
        print("=== Resumen Final ===")
        print(f"Elementos totales creados: {contador:,}")
        print(f"RAM utilizada por el proceso: {obtener_uso_ram_mb():.1f} MB")
        print(f"RAM del sistema: {obtener_ram_sistema_porcentaje():.1f}%")
        print()
        print("Nota: Observa en el Administrador de tareas cómo la memoria paginada")
        print("(memoria virtual/comitted) aumenta cuando la RAM física se llena.")


if __name__ == "__main__":
    main()
