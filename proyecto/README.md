# Proyecto: Gestión de Memoria, E/S y Procesos

Proyecto de estudiante con 4 scripts prácticos sobre conceptos de Sistemas Operativos.

---

## 1. Crear y activar el entorno virtual

**Windows (PowerShell):**
```powershell
cd proyecto
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
cd proyecto
python -m venv venv
venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
cd proyecto
python3 -m venv venv
source venv/bin/activate
```

---

## 2. Instalar dependencias

Con el entorno virtual activado:
```bash
pip install -r requirements.txt
```

Única dependencia: `psutil` (para monitoreo de recursos y gestión de prioridades).

---

## 3. Ejecutar cada script

### 3.1 Vigilante de Recursos (RAM y CPU)
```bash
python recursos.py
```
- Muestra uso de CPU y RAM cada 2 segundos.
- Cuando la RAM supere el 80%, muestra una alerta y la registra en `alertas_ram.txt`.
- Detener con `Ctrl+C`.

### 3.2 Simulador de Memoria Caché
```bash
python cache.py
```
- Genera un archivo de prueba de ~50 MB si no existe.
- Realiza la primera lectura desde disco (lenta).
- Las lecturas siguientes se hacen desde un diccionario en RAM (rápidas).
- Muestra la comparación de tiempos y el speedup obtenido.

### 3.3 Estrés de Memoria y Paginación
```bash
python memoria_virtual.py
```
- Llena una lista con millones de strings progresivamente.
- Muestra cada 5 segundos: elementos creados, RAM del proceso y RAM del sistema.
- Se detiene automáticamente por seguridad al alcanzar:
  - 85% de RAM del sistema, o
  - 20 millones de elementos.
- Detener anticipadamente con `Ctrl+C`.

### 3.4 Prioridad de Procesos
```bash
python prioridad.py <nivel>
```
Donde `<nivel>` puede ser: `baja`, `normal`, `alta`.

Ejemplos:
```bash
python prioridad.py baja
python prioridad.py alta
```

---

## 4. Prueba de prioridad con DOS instancias

Para comparar el efecto de la prioridad:

1. **Abre DOS terminales** (PowerShell, CMD, etc.) y activa el entorno virtual en ambas.
2. En la **primera terminal** ejecuta:
   ```bash
   python prioridad.py baja
   ```
3. Inmediatamente en la **segunda terminal** ejecuta:
   ```bash
   python prioridad.py alta
   ```
4. Espera a que ambas terminen y compara el tiempo reportado.
   - La instancia con prioridad **alta** debería tardar **menos tiempo** (o similar si el sistema está ocioso).
   - Si obtienes "permiso denegado" en la prioridad alta, ejecuta la terminal como **Administrador**.

**Ayuda visual:** Abre el **Administrador de tareas** → pestaña **Detalles** → haz clic derecho en los encabezados → **Seleccionar columnas** → marca **Prioridad base**. Allí verás la diferencia entre ambos procesos.

---

## 5. Qué observar en el Administrador de tareas (prueba de memoria virtual)

Mientras se ejecuta `memoria_virtual.py`, abre el **Administrador de tareas** → pestaña **Rendimiento** → **Memoria**, y observa:

- **En uso (memoria física):** Aumenta progresivamente a medida que crece la lista.
- **Memoria paginada / Comprometida:** Cuando la RAM física se acerca al límite, este valor seguirá creciendo, lo que indica que el sistema está usando **memoria virtual** (archivo de paginación en disco).
- **Velocidad del script:** Notarás que, al empezar a paginar a disco, el proceso se **ralentiza notablemente** (el tiempo entre reportes aumenta), porque acceder al disco es mucho más lento que a la RAM.
- **Proceso en Detalles:** Busca `python.exe` y observa cómo crece su columna **Memoria (activa privada)**.

Los límites de seguridad del script evitan que el sistema se bloquee.
