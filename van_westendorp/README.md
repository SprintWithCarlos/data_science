# Gráfico de Medición de la Sensibilidad del Precio de Van Westendorp
## Paso Previo: los datos
Para obtener el gráfico sólo hace falta el conjunto de datos de una encuesta con las siguientes preguntas:
1. ¿Cuál consideras el precio de este producto al cual ya es demasiado caro y ya no lo comprarías?
2. ¿A cuál precio consideras que comprarías el producto aunque te parezca caro?
3. ¿En qué precio seguirías comprando aún considerándolo barato?
4. ¿Cuál sería el precio en el que lo considerarías demasiado barato al punto de dudar sobre su calidad y dejarías de comprarlo?
La tabla debe tener 4 columnas:

| Demasiado Barato | Barato | Caro | Demasiado Caro |
| ---------------- | ------ | ---- | -------------- |
|        1         |    2   |  3   |          4     |

Si no tienes el archivo, puedes generar uno con data simulada, siguiendo las instrucciones del cuaderno
## Siguiente paso: ejecuta el cuaderno
La opción recomendada es en Codespaces, sólo haz click en el botón y sigue las instrucciones
[![Abrir en Codespaces](badge_es.svg)](https://codespaces.new?repo=SprintWithCarlos/van_westendorp)

Si prefieres ejecutarlo en local, clona el repositorio e instala las dependencias
```bash
pip install -r requirements.txt
```


