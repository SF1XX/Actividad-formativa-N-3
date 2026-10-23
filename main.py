import numpy as np
import pandas as pd

M = 5  # Cantidad de sensores
N = 1440  # Lecturas por sensor (10 días a 6 lecturas/hora)

data = []

np.random.seed(42)  # Para reproducibilidad

for sensor in range(1, M + 1):
    # Generar ciclo diario base (24 horas = 144 lecturas)
    t = np.arange(N)
    ciclo_diario = 22 + 7 * np.sin(2 * np.pi * t / 144)
    ruido = np.random.normal(0, 0.8, N)

    if sensor == 3:
        # Sensor 3 con comportamiento distinto: deriva térmica (drift)
        drift = (t / N) * 6
        valores = ciclo_diario + ruido + drift
    else:
        valores = ciclo_diario + ruido

    # Inyección de rachas anómalas
    if sensor == 2:
        # Racha A: Inicio en 400, longitud 6 (hasta 405)
        valores[399:405] = np.random.uniform(39.5, 42.0, 6)

    if sensor == 5:
        # Racha B: Inicio en 1100, longitud 8 (hasta 1107)
        valores[1099:1107] = np.random.uniform(40.0, 43.5, 8)

    for nro in range(1, N + 1):
        data.append(
            {
                "sensor": sensor,
                "nro": nro,
                "valor": round(float(valores[nro - 1]), 2),
            }
        )

df = pd.DataFrame(data)
df.to_csv("lecturas.csv", index=False)
print("Archivo 'lecturas.csv' generado exitosamente.")
print(df.head(10))