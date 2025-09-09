# Calculadora PRN - Entrega completa

## Estructura

- main.py: Aplicación principal con GUI basada en tkinter y pestañas.
- algorithms/: módulos de los algoritmos (cuadrados, productos, multiplicador).
- pruebas.py: funciones de prueba (Medias, Varianza, K-S).
- utils/: utilidades de exportación (CSV/XLSX).

## Requisitos

- Python 3.10+
- pip install -r requirements.txt

## Ejecutar

1. Crear y activar entorno virtual (recomendado)

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate # macOS/Linux
```

2. Instalar dependencias

```bash
pip install -r requirements.txt
```

3. Ejecutar

```bash
python main.py
```

## Contenido mínimo en la demo
- Generar secuencia con cada algoritmo.
- Ejecutar pruebas (Medias, Varianza, K-S).
- Mostrar histograma y tabla de frecuencias.
- Exportar CSV/XLSX.

## Bitácora 
📓 Bitácora del Proyecto

Clase 1 - 13/08/2025: Presentación de la materia y explicación de los objetivos del proyecto de generadores pseudoaleatorios.

Clase 2 - 20/08/2025: Desarrollo de los algoritmos de cuadrados medios y productos medios.

Clase 3 - 27/08/2025: Desarrollo del algoritmo de multiplicador constante y aplicación de las pruebas de medias y pruebas de varianza.

Clase 4 - 03/09/2025: Ejecución de pruebas de uniformidad para validar la distribución de los números generados.
