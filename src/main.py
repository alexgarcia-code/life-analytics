### PROYECTO PERSONAL DE PYTHON PARA ANALIZAR HÁBITOS DIARIOS ###

import pandas as pd
import os
import matplotlib.pyplot as plt

# Ruta al archivo de datos
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "life_data.csv")

# Función para leer los datos del csv y convertir las fechas
def cargar_datos(ruta):
    df = pd.read_csv(ruta)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df

# Función para detectar valores nulos
def detectar_nulos(df):
    print("\nValores nulos por columna: ")
    print(df.isnull().sum(), "\n")

# Función para rellenar valores nulos (sueño y productividad = media, ejercicio y estudio = 0)
def limpiar_nulos(df):
    df["horas_sueno"] = df["horas_sueno"].fillna(df["horas_sueno"].mean())
    df["horas_ejercicio"] = df["horas_ejercicio"].fillna(0)
    df["horas_estudio"] = df["horas_estudio"].fillna(0)
    df["productividad"] = df["productividad"].fillna(df["productividad"].mean())
    return df

# Función para evitar datos absurdos
def validar_rangos(df):
    df = df[df["horas_sueno"].between(0, 12)]
    df = df[df["horas_ejercicio"].between(0, 5)]
    df = df[df["horas_estudio"].between(0, 10)]
    df = df[df["productividad"].between(1, 5)]
    return df

# Función para puntuar hábitos del 1-5
def puntuar_habito(valor, maximo):
    puntuacion = (valor/maximo) * 5

    if puntuacion < 1:
        return 1
    if puntuacion > 5:
        return 5
    
    return round(puntuacion, 1)

# Función para calcular productividad según la puntuación de los hábitos
def calcular_productividad(df):
    df = df.copy()

    df["sueno_score"] = df["horas_sueno"].apply(lambda x: puntuar_habito(x, 8))
    df["ejercicio_score"] = df["horas_ejercicio"].apply(lambda x: puntuar_habito(x, 1))
    df["estudio_score"] = df["horas_estudio"].apply(lambda x: puntuar_habito(x, 4))

    df["productividad_estimada"] = (df["sueno_score"] + df["ejercicio_score"] + df["estudio_score"]) / 3

    df["productividad_estimada"] = df["productividad_estimada"].round(1)

    return df

# Función para comparar la productividad del usuario y la calculada a partir de los hábitos
def comparar_productividades(df):
    print("\nCOMPARACIÓN PRODUCTIVIDAD REAL VS ESTIMADA")
    print("------------------------------------------")

    print(df[["fecha", "productividad", "productividad_estimada"]])
    print()

# Función para calcular la diferencia (error) entre productividades
def diferencia_productividad(df):
    df =df.copy()
    df["diferencia"] = df["productividad"] - df["productividad_estimada"]

    print("DIFERENCIA (REAL - ESTIMADA)")
    print("----------------------------")
    print(df[["fecha", "productividad", "productividad_estimada", "diferencia"]])

    print(f"\nError medio absoluto: {df["diferencia"].abs().mean():.2f}\n")

# Función para evaluar el cálculo de la productividad según el error
def evaluar_modelo(df):
    error_medio = (df["productividad"] - df["productividad_estimada"]).abs().mean()

    print("EVALUACIÓN DEL MODELO")
    print("---------------------")

    if error_medio <= 0.5:
        print("La estimación de productividad es bastante precisa.")
    elif error_medio <= 1:
        print("La estimación de productividad es aceptable, pero mejorable.")
    else:
        print("La estimación de productividad no es fiable.")

    print()

# Función para detectar fechas duplicadas
def detectar_fechas_duplicadas(df):
    duplicadas = df["fecha"].duplicated().sum()
    print(f"Fechas duplicadas: {duplicadas}\n")

# Función para calcular métricas generales (media de cada columna)
def metricas_generales(df):
    print("MÉTRICAS GENERALES")
    print("------------------")
    print(f"Productividad media: {df["productividad"].mean():.2f}")
    print(f"Media de horas de sueño: {df["horas_sueno"].mean():.2f}")
    print(f"Media de horas de ejercicio: {df["horas_ejercicio"].mean():.2f}")
    print(f"Media de horas de estudio: {df["horas_estudio"].mean():.2f}\n")

# Función para comparar hábitos según la productividad del día
def comparar_habitos(df):
    dias_buenos = df[df["productividad"] >= 4]
    dias_malos = df[df["productividad"] <= 2]

    print("COMPARACIÓN DE HÁBITOS")
    print("----------------------")

    if not dias_buenos.empty:
        print("Días productivos (4 o más): ")
        print(f"Sueño medio: {dias_buenos["horas_sueno"].mean():.2f}")
        print(f"Ejercicio medio: {dias_buenos["horas_ejercicio"].mean():.2f}")
        print(f"Estudio medio: {dias_buenos["horas_estudio"].mean():.2f}")

    if not dias_malos.empty:
        print("\nDías poco productivos (2 o menos): ")
        print(f"Sueño medio: {dias_malos["horas_sueno"].mean():.2f}")
        print(f"Ejercicio medio: {dias_malos["horas_ejercicio"].mean():.2f}")
        print(f"Estudio medio: {dias_malos["horas_estudio"].mean():.2f}\n")

# Función que muestra algunas conclusiones según lo analizado
def conclusiones(df):
    prod_media = df["productividad"].mean()
    
    sueno_score_media = df["sueno_score"].mean()
    ejercicio_score_media = df["ejercicio_score"].mean()
    estudio_score_media = df["estudio_score"].mean()

    print("CONCLUSIONES")
    print("------------")

    if prod_media >= 4:
        print("En general, tu nivel de productividad es alto.")
    elif prod_media <= 2:
        print("En general, tu nivel de productividad es bajo.")
    else:
        print("Tu productividad media es moderada.")

    print("\nEVALUACIÓN DE HÁBITOS")

    if sueno_score_media < 3:
        print("- Deberías mejorar tus horas de sueño. Dormir más podría aumentar tu productividad.")
    else:
        print("- Tu hábito de sueño es adecuado.")

    if ejercicio_score_media < 3:
        print("- El ejercicio es bajo en promedio. Intenta moverte más durante la semana.")
    else:
        print("- Mantienes un buen nivel de actividad física. ¡Sigue así!")

    if estudio_score_media < 3:
        print("- El tiempo dedicado al estudio es mejorable.")
    else:
        print("- Tu dedicación al estudio es consistente.")

    print()

# Gráfica Productividad real vs estimada
def grafica_productividad(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["fecha"], df["productividad"], label="Productividad real")
    plt.plot(df["fecha"], df["productividad_estimada"], label="Productividad estimada")

    plt.title("Productividad real vs estimada")
    plt.xlabel("Fecha")
    plt.ylabel("Productividad (1-5)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Gráfica hábitos en el tiempo
def grafica_habitos(df):
    plt.figure(figsize=(10, 5))

    plt.plot(df["fecha"], df["horas_sueno"], label="Horas de sueño")
    plt.plot(df["fecha"], df["horas_ejercicio"], label="Horas de ejercicio")
    plt.plot(df["fecha"], df["horas_estudio"], label="Horas de estudio")

    plt.title("Evolución de hábitos diarios")
    plt.xlabel("Fecha")
    plt.ylabel("Horas")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Gráfica puntuación por hábito
def grafica_puntuaciones_medias(df):
    medias = [
        df["sueno_score"].mean(),
        df["ejercicio_score"].mean(),
        df["estudio_score"].mean()
    ]

    habitos = ["Sueño", "Ejercicio", "Estudio"]

    plt.figure(figsize=(6, 4))
    plt.bar(habitos, medias)
    plt.ylim(0, 5)

    plt.title("Puntuación media por hábito")
    plt.ylabel("Puntuación (1-5)")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

# Función para generar un reporte en .txt con algunas conclusiones
def generar_reporte(df, ruta="reporte_habitos.txt"):
    prod_media = df["productividad"].mean()

    sueno_score = df["sueno_score"].mean()
    ejercicio_score = df["ejercicio_score"].mean()
    estudio_score = df["estudio_score"].mean()

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE HÁBITOS DIARIOS\n")
        archivo.write("-------------------------\n\n")

        archivo.write(f"Productividad media: {prod_media:.2f}\n\n")

        archivo.write("PUNTUACIÓN MEDIA DE HÁBITOS\n")
        archivo.write(f"- Sueño: {sueno_score:.2f}\n")
        archivo.write(f"- Ejercicio: {ejercicio_score:.2f}\n")
        archivo.write(f"- Estudio: {estudio_score:.2f}\n\n")

        archivo.write("CONCLUSIONES\n")

        if prod_media >= 4:
            archivo.write("- Tu productividad media es alta.\n")
        elif prod_media <= 2:
            archivo.write("- Tu productividad media es baja.\n")
        else:
            archivo.write("- Tu productividad media es moderada.\n")

        if sueno_score < 3:
            archivo.write("- Deberías mejorar tus horas de sueño.\n")
        if ejercicio_score < 3:
            archivo.write("- Deberías aumentar tu nivel de ejercicio.\n")
        if estudio_score < 3:
            archivo.write("- Podrías dedicar más tiempo al estudio.\n")
        if sueno_score >= 3 and ejercicio_score >= 3 and estudio_score >= 3:
            print("Tienes muy buenos hábitos. ¡Sigue así!")


# Función principal
def main():
    df = cargar_datos(DATA_PATH)

    detectar_nulos(df)

    df = limpiar_nulos(df)

    df = validar_rangos(df)

    detectar_fechas_duplicadas(df)

    df = calcular_productividad(df)

    print(df[["fecha", "horas_sueno", "horas_ejercicio", "horas_estudio", "productividad_estimada"]])

    comparar_productividades(df)

    diferencia_productividad(df)

    evaluar_modelo(df)

    metricas_generales(df)

    comparar_habitos(df)

    grafica_productividad(df)

    grafica_habitos(df)

    grafica_puntuaciones_medias(df)

    conclusiones(df)

    generar_reporte(df)
    print("Reporte generado: reporte_habitos.txt")

if __name__ == "__main__":
    main()
