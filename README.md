# Análisis de Airbnb en Madrid

Análisis exploratorio y visualización de datos de alojamiento de Airbnb en Madrid, desarrollando como proyecto individual del Bootcamp de IA de Factoría F5. El objeivo es extraer información útil para la toma de decisiones de negocio: patrones de precios, distribución por distritos, tipos de alojamiento y factores que influyen en la demanda.  

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

## Estructura del repositorio

```
Proyecto8-Modulo3-ad-Gisella/
├── data/
│   ├── raw/          Datos originales sin procesar (no versionados)
│   └── processed/    Datos limpios, listos para el análisis
├── notebooks/        Notebooks de Jupyter con el EDA y análisis
├── docs/              Documentación del proyecto
├── src/                Funciones y scripts reutilizables
├── dashboard/          Archivos del dashboard (Power BI / Tableau)
├── .gitignore
├── requirements.txt
└── README.md
```
## Tecnologías utilizadas

- Python 3.12
- Pandas / NumPy — manipulación y limpieza de datos
- Matplotlib / Seaborn / Plotly — visualización
- Jupyter Notebook — análisis exploratorio
- Power BI / Tableau — dashboard interactivo
- Git / GitHub — control de versiones

## Instalación

### Requisitos previos

- Python 3.12 o superior
- Git

### Pasos

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