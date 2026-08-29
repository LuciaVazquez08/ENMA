# Estadística y Programación — Ejercicios Unidad 1

Resolución de los ejercicios de la Unidad 1 (mínimos cuadrados, regresión lineal,
descenso por gradiente estocástico) sobre el dataset *Prostate Cancer* de
Stamey et al. (1989), usado en el libro *The Elements of Statistical Learning*.

## Contenido

- `Ejercicios_U1.ipynb`: notebook con las resoluciones (deducciones teóricas en Markdown/LaTeX
  y código ejecutado, con sus salidas y gráficos).
- `data/prostate.csv`: dataset original (97 observaciones, 8 predictores + respuesta `lpsa`),
  con la columna `train` que indica la partición train/test (67/30) usada en el libro,
  tal como se distribuye en el paquete `ElemStatLearn` de R.

## Cómo reproducir

```bash
pip install numpy pandas scipy statsmodels scikit-learn matplotlib jupyter
jupyter nbconvert --to notebook --execute --inplace Ejercicios_U1.ipynb
```

El notebook lee `data/prostate.csv` con una ruta relativa, por lo que debe ejecutarse
desde este directorio (`estadistica_programacion/unidad1/`).
