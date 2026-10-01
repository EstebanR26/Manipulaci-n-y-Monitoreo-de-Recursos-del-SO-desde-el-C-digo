import os
import time

ARCHIVO_PRUEBA = "archivo_grande_prueba.txt"
TAMANO_ARCHIVO_MB = 50
NUM_LECTURAS_CACHE = 5

cache_ram = {}


def generar_archivo_grande(ruta, tamano_mb):
    if os.path.exists(ruta):
        tamano_actual = os.path.getsize(ruta) / (1024 * 1024)
        if tamano_actual >= tamano_mb - 1:
            print(f"Archivo de prueba ya existe ({tamano_actual:.1f} MB).")
            return
    print(f"Generando archivo de prueba de ~{tamano_mb} MB...")
    linea = "Esta es una línea de datos de ejemplo para simular un archivo grande.\n"
    tamano_linea = len(linea.encode("utf-8"))
    lineas_necesarias = int((tamano_mb * 1024 * 1024) / tamano_linea)
    with open(ruta, "w", encoding="utf-8") as f:
        for _ in range(lineas_necesarias):
            f.write(linea)
    print("Archivo generado correctamente.\n")


def leer_desde_disco(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return f.read()


def leer_con_cache(ruta):
    if ruta in cache_ram:
        return cache_ram[ruta], True
    contenido = leer_desde_disco(ruta)
    cache_ram[ruta] = contenido
    return contenido, False


def main():
    print("=== Simulador de Memoria Caché (L1/L2 vs RAM) ===")
    print()

    generar_archivo_grande(ARCHIVO_PRUEBA, TAMANO_ARCHIVO_MB)

    print(f"Tamaño del archivo: {os.path.getsize(ARCHIVO_PRUEBA) / (1024*1024):.2f} MB")
    print()

    print(f"--- Lectura 1 (desde DISCO, simula acceso lento) ---")
    inicio = time.time()
    _, desde_cache = leer_con_cache(ARCHIVO_PRUEBA)
    fin = time.time()
    tiempo_disco = fin - inicio
    print(f"Desde caché: {desde_cache}")
    print(f"Tiempo de lectura: {tiempo_disco:.4f} segundos")
    print()

    tiempos_cache = []
    for i in range(2, NUM_LECTURAS_CACHE + 2):
        print(f"--- Lectura {i} (desde RAM/caché) ---")
        inicio = time.time()
        _, desde_cache = leer_con_cache(ARCHIVO_PRUEBA)
        fin = time.time()
        t = fin - inicio
        tiempos_cache.append(t)
        print(f"Desde caché: {desde_cache}")
        print(f"Tiempo de lectura: {t:.6f} segundos")
        print()

    print("=== Resumen de tiempos ===")
    print(f"Lectura desde DISCO:       {tiempo_disco:.4f} s")
    if tiempos_cache:
        promedio_cache = sum(tiempos_cache) / len(tiempos_cache)
        print(f"Promedio lecturas caché:   {promedio_cache:.6f} s")
        if promedio_cache > 0:
            print(f"Speedup (disco/caché):     {tiempo_disco / promedio_cache:.1f}x más rápido en caché")
    print()
    print("Observación: La primera lectura accede al disco (lento).")
    print("Las lecturas siguientes usan el diccionario en RAM, siendo notablemente más rápidas.")


if __name__ == "__main__":
    main()
