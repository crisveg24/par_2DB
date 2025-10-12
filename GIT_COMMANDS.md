# 🚀 Guía de Comandos Git para el Proyecto

Este archivo contiene todos los comandos Git necesarios para gestionar el proyecto con al menos 2 ramas y 5+ commits.

## 📋 Configuración Inicial

```bash
# 1. Inicializar repositorio Git (si aún no existe)
cd C:\Users\crsti\proyectos\par_2DB
git init

# 2. Configurar usuario (si es primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"

# 3. Agregar todos los archivos
git add .

# 4. Primer commit
git commit -m "📦 Initial commit: Estructura base del proyecto ETL"
```

## 🌿 Crear Ramas

```bash
# Crear rama develop
git checkout -b develop

# Ver todas las ramas
git branch
```

## 📝 Commits Descriptivos (≥5 commits)

```bash
# COMMIT 1: Módulo Extract
git add Extract/
git commit -m "🔧 feat: Implementar módulo Extract para lectura de CSV

- Crear clase StockExtractor
- Métodos extract_data(), get_data_info(), preview_data()
- Validación de archivos y manejo de errores
- Soporte para análisis de 6,087 registros"

# COMMIT 2: Módulo Transform
git add Transform/
git commit -m "✨ feat: Implementar módulo Transform con limpieza de datos

- Crear clase StockTransformer
- 7 transformaciones: normalización, conversión tipos, manejo nulos
- Creación de 6 features temporales (year, month, day, etc.)
- Eliminación de duplicados y validación de fechas
- Reportes detallados de transformaciones"

# COMMIT 3: Módulo Load
git add Load/
git commit -m "💾 feat: Implementar módulo Load (CSV, Parquet, SQLite)

- Crear clase StockLoader
- Soporte para 3 formatos de salida
- Índices optimizados en SQLite (date, label)
- Compresión Snappy para Parquet
- Método query_sqlite() para consultas"

# COMMIT 4: Script principal y requirements
git add main.py requirements.txt
git commit -m "🎯 feat: Crear script principal main.py y requirements.txt

- Pipeline ETL completo end-to-end
- Manejo de errores robusto
- Reportes detallados de cada fase
- Dependencias: pandas, numpy, matplotlib, seaborn, plotly"

# COMMIT 5: Notebook ETL
git add notebooks/01_etl.ipynb
git commit -m "📊 feat: Crear notebook ETL interactivo (01_etl.ipynb)

- Pipeline ETL paso a paso con visualizaciones
- Documentación inline detallada
- Comparaciones antes/después de transformaciones
- Validación de datos cargados en SQLite"

# COMMIT 6: Notebook EDA con 7 gráficas
git add notebooks/02_eda.ipynb
git commit -m "📈 feat: Implementar EDA con 7 visualizaciones originales

Visualizaciones creadas:
1. Pie Chart: Distribución de sentimientos
2. Line Chart: Evolución temporal
3. Stacked Bar: Sentimientos por día de semana
4. Heatmap: Sentimientos por mes y año
5. Horizontal Bar: Top 20 palabras frecuentes
6. Grouped Bar: Distribución por trimestre
7. Correlation Heatmap: Features temporales

Insights y conclusiones documentados"

# COMMIT 7: README completo
git add README.md
git commit -m "📝 docs: Agregar README completo con documentación

- Descripción del proyecto y objetivos
- Estructura del proyecto detallada
- Instrucciones de instalación y uso
- Explicación exhaustiva del pipeline ETL
- Documentación de las 7 visualizaciones
- Resultados, conclusiones e insights
- Referencias y tecnologías utilizadas"

# COMMIT 8: .gitignore
git add .gitignore
git commit -m "🔧 config: Agregar .gitignore para Python y Jupyter

- Excluir __pycache__, .ipynb_checkpoints
- Excluir entornos virtuales
- Excluir archivos del sistema operativo
- Configuración para IDEs"

# COMMIT 9: Documentación de Git
git add GIT_COMMANDS.md
git commit -m "📚 docs: Agregar guía de comandos Git

- Instrucciones paso a paso
- Flujo de trabajo Git Flow
- Comandos útiles para el proyecto
- Estrategia de branches y commits"

# COMMIT 10: Validación final
git add .
git commit -m "✅ test: Validar pipeline completo end-to-end

- Probar extracción de 6,087 registros
- Verificar 7 transformaciones aplicadas
- Validar generación de 3 formatos de salida
- Confirmar 0 valores nulos y 0 duplicados
- Pipeline ETL funcionando correctamente"
```

## 🔀 Merge a Main

```bash
# Cambiar a main
git checkout main

# Hacer merge de develop
git merge develop

# Ver log de commits
git log --oneline --graph --all
```

## 🔄 Flujo de Trabajo Completo

```bash
# 1. Trabajar en develop
git checkout develop

# 2. Hacer cambios y commits
git add <archivos>
git commit -m "mensaje descriptivo"

# 3. Cuando esté listo, merge a main
git checkout main
git merge develop

# 4. Crear tag de versión
git tag -a v1.0 -m "Versión 1.0: Pipeline ETL completo"
```

## 🌐 Subir a GitHub

```bash
# 1. Crear repositorio en GitHub (desde la web)

# 2. Agregar remote
git remote add origin https://github.com/tu_usuario/par_2DB.git

# 3. Subir main
git push -u origin main

# 4. Subir develop
git push -u origin develop

# 5. Subir tags
git push --tags
```

## 📊 Comandos Útiles

```bash
# Ver estado
git status

# Ver historial
git log --oneline --graph --all --decorate

# Ver diferencias
git diff

# Ver ramas remotas
git branch -a

# Ver commits de una rama
git log develop --oneline

# Ver archivos cambiados
git diff --name-only

# Ver estadísticas
git log --stat

# Ver último commit
git show HEAD

# Deshacer último commit (mantener cambios)
git reset --soft HEAD~1

# Ver quién modificó cada línea
git blame <archivo>
```

## 🎯 Verificación de Requisitos

```bash
# Verificar número de commits (debe ser ≥5)
git log --oneline | wc -l

# Verificar número de ramas (debe ser ≥2)
git branch | wc -l

# Ver todos los commits con detalles
git log --pretty=format:"%h - %an, %ar : %s"

# Ver estadísticas por autor
git shortlog -sn
```

## ✅ Checklist Final

- [x] Repositorio Git inicializado
- [x] Al menos 2 ramas (main, develop)
- [x] Al menos 5 commits descriptivos
- [x] Commits siguen convenciones (feat, fix, docs, etc.)
- [x] README.md completo
- [x] .gitignore configurado
- [x] Código documentado
- [x] Pipeline ETL funcional

## 📝 Notas

- Los mensajes de commit usan emojis para claridad visual
- Se sigue la convención de commits semánticos
- Cada commit tiene un mensaje descriptivo de lo que hace
- El flujo Git Flow facilita el trabajo colaborativo
- Las ramas permiten desarrollo paralelo y estable

---

**Fecha de última actualización:** Octubre 2025
