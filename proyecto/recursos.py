import psutil
import time
from datetime import datetime

LOG_FILE = "alertas_ram.txt"
INTERVALO_SEGUNDOS = 2
LIMITE_RAM = 80


def registrar_alerta(porcentaje_ram):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensaje = f"[{fecha_hora}] ALERTA: Uso de RAM = {porcentaje_ram:.1f}% (supera el {LIMITE_RAM}%)\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(mensaje)
    print(mensaje.strip())


def main():
    print("=== Vigilante de Recursos ===")
    print(f"Monitoreando cada {INTERVALO_SEGUNDOS} segundos...")
    print(f"Límite de RAM para alerta: {LIMITE_RAM}%")
    print("Presiona Ctrl+C para detener.\n")

    try:
        while True:
            uso_cpu = psutil.cpu_percent(interval=None)
            memoria = psutil.virtual_memory()
            uso_ram = memoria.percent

            fecha_hora = datetime.now().strftime("%H:%M:%S")
            print(f"[{fecha_hora}] CPU: {uso_cpu:5.1f}%  |  RAM: {uso_ram:5.1f}%", end="")

            if uso_ram > LIMITE_RAM:
                print("  [!] ALERTA: RAM sobre el limite!")
                registrar_alerta(uso_ram)
            else:
                print()

            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\n\nMonitoreo detenido por el usuario.")


if __name__ == "__main__":
    main()
