import sys
import time
import psutil

NUM_ITERACIONES = 10000000


def calculo_pesado(n):
    total = 0.0
    for i in range(1, n + 1):
        total += (i ** 0.5) * (i % 3 + 1)
        if i % 100000 == 0:
            pass
    return total


def establecer_prioridad(nivel):
    proceso = psutil.Process()
    try:
        if sys.platform == "win32":
            if nivel == "baja":
                proceso.nice(psutil.IDLE_PRIORITY_CLASS)
                print("Prioridad establecida: BAJA (IDLE_PRIORITY_CLASS)")
            elif nivel == "alta":
                try:
                    proceso.nice(psutil.HIGH_PRIORITY_CLASS)
                    print("Prioridad establecida: ALTA (HIGH_PRIORITY_CLASS)")
                except (psutil.AccessDenied, PermissionError):
                    print("[!] No se pudo establecer HIGH_PRIORITY_CLASS (permiso denegado).")
                    print("   Intentando ABOVE_NORMAL_PRIORITY_CLASS...")
                    proceso.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
                    print("Prioridad establecida: MEDIA-ALTA (ABOVE_NORMAL_PRIORITY_CLASS)")
            elif nivel == "normal":
                proceso.nice(psutil.NORMAL_PRIORITY_CLASS)
                print("Prioridad establecida: NORMAL")
            else:
                print(f"Nivel '{nivel}' no reconocido. Usando NORMAL.")
                proceso.nice(psutil.NORMAL_PRIORITY_CLASS)
        else:
            if nivel == "baja":
                proceso.nice(19)
                print("Prioridad establecida: BAJA (nice=19)")
            elif nivel == "alta":
                try:
                    proceso.nice(-20)
                    print("Prioridad establecida: ALTA (nice=-20)")
                except (psutil.AccessDenied, PermissionError):
                    print("[!] No se pudo establecer nice=-20. Intentando nice=-10...")
                    proceso.nice(-10)
                    print("Prioridad establecida: MEDIA-ALTA (nice=-10)")
            else:
                proceso.nice(0)
                print("Prioridad establecida: NORMAL (nice=0)")
    except Exception as e:
        print(f"[!] Error al establecer prioridad: {e}")
        print("   Continuando con prioridad por defecto.")


def main():
    print("=== Prioridad de Procesos (Scheduling) ===")
    print()

    if len(sys.argv) < 2:
        print("Uso: python prioridad.py <nivel>")
        print("  <nivel> puede ser: baja, normal, alta")
        print()
        print("Ejemplos:")
        print("  python prioridad.py baja")
        print("  python prioridad.py alta")
        sys.exit(1)

    nivel = sys.argv[1].lower()
    if nivel not in ("baja", "normal", "alta"):
        print(f"Error: nivel '{nivel}' inválido. Usa: baja, normal, alta")
        sys.exit(1)

    establecer_prioridad(nivel)

    pid = psutil.Process().pid
    print(f"PID del proceso: {pid}")
    print(f"Cálculo a realizar: {NUM_ITERACIONES:,} iteraciones matemáticas")
    print()

    print("Iniciando cálculo... (observar tiempos y Administrador de tareas)")
    inicio = time.time()
    resultado = calculo_pesado(NUM_ITERACIONES)
    fin = time.time()

    tiempo_total = fin - inicio

    print()
    print("=== Resultados ===")
    print(f"Nivel de prioridad: {nivel.upper()}")
    print(f"PID: {pid}")
    print(f"Resultado del cálculo: {resultado:.4e}")
    print(f"Tiempo total de ejecución: {tiempo_total:.2f} segundos")
    print()
    print("Tip: Ejecuta dos instancias al mismo tiempo (una con 'baja' y otra con 'alta')")
    print("     y compara los tiempos. En el Administrador de tareas podrás ver la diferencia")
    print("     de prioridad en la columna 'Prioridad base' o similar.")


if __name__ == "__main__":
    main()
