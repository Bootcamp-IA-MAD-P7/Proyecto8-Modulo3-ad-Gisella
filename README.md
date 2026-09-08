# Análisis de Airbnb en Madrid

Análisis exploratorio y visualización de datos de alojamiento de Airbnb en Madrid, desarrollado como proyecto individual del Bootcamp de IA de Factoría F5. El objetivo es extraer información útil para la toma de decisiones de negocio: patrones de precios, distribución por distritos, tipos de alojamiento y factores que influyen en la demanda.

## Contexto

Una startup del sector inmobiliario ha sido contratada por Airbnb para
analizar los datos de alojamientos disponibles en distintas ciudades. El
presente proyecto se centra en la ciudad de Madrid, con el objetivo de
identificar patrones de precios, detectar valores atípicos, y generar
insights que aporten valor de negocio a partir de los datos disponibles.

## Objetivos

- Realizar un análisis exploratorio de datos (EDA) completo
- Limpiar y preparar el dataset para su análisis
- Enriquecer los datos con fuentes externas (INE, Ayuntamiento de Madrid,
  datos turísticos)
- Generar visualizaciones y un dashboard interactivo
- Extraer conclusiones útiles para la toma de decisiones de negocio

## Nivel de entrega alcanzado

**Nivel Avanzado.** El proyecto incluye, además del EDA y el enriquecimiento
de datos:

- Dashboard interactivo con filtros dinámicos (distrito, tipo de alojamiento,
  rango de precio)
- Verificación de hipótesis mediante test estadístico (correlación de
  Pearson entre precio y variables socioeconómicas)
- Containerización completa con Docker y Docker Compose

## Estructura del repositorio

```
Proyecto8-Modulo3-ad-Gisella/
├── data/
│   ├── raw/          Datos originales sin procesar (no versionados)
│   └── processed/    Datos limpios y enriquecidos, listos para el análisis
├── notebooks/        Notebooks de Jupyter con la limpieza, el enriquecimiento y el EDA
├── docs/             Documentación del proyecto
├── src/              Funciones y scripts reutilizables
├── dashboard/        Dashboard interactivo (Streamlit + Plotly)
├── Dockerfile
├── docker-compose.yml
├── .gitignore
├── requirements.txt
└── README.md
```

## Tecnologías utilizadas

- Python 3.12
- Pandas / NumPy — manipulación y limpieza de datos
- Matplotlib / Seaborn / Plotly — visualización
- Jupyter Notebook — análisis exploratorio, limpieza y enriquecimiento de datos
- Streamlit — dashboard interactivo
- SciPy — test estadístico de correlación (Pearson)
- Docker / Docker Compose — containerización y despliegue reproducible
- Git / GitHub — control de versiones

## Instalación

### Requisitos previos

- Python 3.12 o superior
- Git
- Docker y Docker Compose (opcional, para ejecución containerizada)

### Opción A: entorno virtual local

1. Clonar el repositorio:

```
git clone https://github.com/Bootcamp-IA-MAD-P7/Proyecto8-Modulo3-ad-Gisella.git
cd Proyecto8-Modulo3-ad-Gisella
```

2. Crear y activar un entorno virtual:

```
python -m venv venv
source venv/Scripts/activate
```

3. Instalar las dependencias:

```
pip install -r requirements.txt
```

4. Los datos originales no están incluidos en el repositorio. Deben
   descargarse desde Inside Airbnb y colocarse en `data/raw/`.

5. Ejecutar el dashboard:

```
streamlit run dashboard/app.py
```

La aplicación se abrirá en `http://localhost:8501`.

### Opción B: con Docker

1. Clonar el repositorio (ver paso 1 anterior).

2. Levantar el contenedor:

```
docker-compose up --build
```

3. Abrir `http://localhost:8501` en el navegador.

El dashboard lee los datos desde `./data`, montada como volumen, por lo que
cualquier actualización del dataset se refleja sin necesidad de reconstruir
la imagen.

## Cómo usar el dashboard

El dashboard tiene tres pestañas, todas afectadas por los filtros de la
barra lateral (distrito, tipo de alojamiento y rango de precio):

- **Resumen general** — indicadores clave (número de alojamientos, precio
  medio y mediano, distritos representados) y una vista previa de los datos
  filtrados.
- **Precios por distrito** — distribución de precios mediante un diagrama
  de cajas (boxplot), ordenado de mayor a menor precio mediano.
- **Precio vs Renta/Población** — relación entre el precio mediano por
  distrito y una variable socioeconómica a elección (renta media del hogar,
  población total o número de viviendas de uso turístico), con el
  coeficiente de correlación de Pearson y su significancia estadística
  calculados en tiempo real.

## Metodología de trabajo

El desarrollo del proyecto sigue un flujo de ramas simulando un entorno
de trabajo profesional:

- `main` — rama de entrega final, solo recibe el código ya terminado
- `developer` — rama de integración, donde se centraliza el trabajo
- `feature/*` — ramas de trabajo individuales para cada tarea, creadas
  a partir de `developer`

Cada tarea se documenta como un issue en GitHub y se gestiona mediante
un tablero Kanban dentro del propio repositorio (pestaña Projects).
Los cambios se integran mediante Pull Requests hacia `developer`, y los
mensajes de commit siguen el formato `tipo: descripción` (por ejemplo,
`fix: correct latitude column format`).