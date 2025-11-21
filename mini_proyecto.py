import tkinter as tk
from tkinter import ttk

# --- Diccionarios de colores ---
digit_colors = {
    "Negro": 0, "Marrón": 1, "Rojo": 2, "Naranja": 3, "Amarillo": 4,
    "Verde": 5, "Azul": 6, "Violeta": 7, "Gris": 8, "Blanco": 9
}

multiplier_colors = {
    "Negro": 1, "Marrón": 10, "Rojo": 100, "Naranja": 1_000, "Amarillo": 10_000,
    "Verde": 100_000, "Azul": 1_000_000, "Violeta": 10_000_000,
    "Gris": 100_000_000, "Blanco": 1_000_000_000, "Dorado": 0.1, "Plateado": 0.01
}

tolerance_colors = {
    "Marrón": "±1%", "Rojo": "±2%", "Verde": "±0.5%", "Azul": "±0.25%",
    "Violeta": "±0.1%", "Gris": "±0.05%", "Dorado": "±5%", "Plateado": "±10%"
}

tcr_colors = {
    "Negro": "250 ppm/K", "Marrón": "100 ppm/K", "Rojo": "50 ppm/K",
    "Naranja": "15 ppm/K", "Amarillo": "25 ppm/K", "Azul": "10 ppm/K", "Violeta": "5 ppm/K"
}

color_hex = {
    "Negro": "#000000", "Marrón": "#5A2E0A", "Rojo": "#FF0000", "Naranja": "#FFA500",
    "Amarillo": "#FFFF00", "Verde": "#008000", "Azul": "#0000FF", "Violeta": "#800080",
    "Gris": "#808080", "Blanco": "#FFFFFF", "Dorado": "#DAA520", "Plateado": "#C0C0C0"
}

# --- Funciones ---
def actualizar_bandas(*_):
    """Actualiza los combos al cambiar la cantidad de bandas"""
    for widget in frame_bandas.winfo_children():
        widget.destroy()

    n = int(combo_bandas.get())
    combos.clear()

    for i in range(n):
        if n == 4 and i == 3:
            texto = "Tolerancia"
            valores = list(tolerance_colors.keys())
        elif n == 5 and i == 4:
            texto = "Tolerancia"
            valores = list(tolerance_colors.keys())
        elif n == 6 and i == 5:
            texto = "TCR"
            valores = list(tcr_colors.keys())
        elif i == n - 2:
            texto = "Multiplicador"
            valores = list(multiplier_colors.keys())
        else:
            texto = f"Banda {i+1}"
            valores = list(digit_colors.keys())

        ttk.Label(frame_bandas, text=texto + ":").grid(row=i, column=0, padx=5, pady=3, sticky="e")
        combo = ttk.Combobox(frame_bandas, values=valores, state="readonly", width=12)
        combo.grid(row=i, column=1, padx=5, pady=3)
        combo.bind("<<ComboboxSelected>>", calcular_resistencia)
        combos.append(combo)

    etiqueta_resultado.config(text="Seleccione los colores")
    dibujar_resistencia(n, inicial=True)

def calcular_resistencia(*_):
    """Calcula el valor según los colores seleccionados"""
    n = int(combo_bandas.get())
    if not all(combo.get() for combo in combos):
        dibujar_resistencia(n)
        etiqueta_resultado.config(text="Seleccione todos los colores.")
        return

    try:
        if n == 4:
            d1 = digit_colors[combos[0].get()]
            d2 = digit_colors[combos[1].get()]
            mult = multiplier_colors[combos[2].get()]
            tol = tolerance_colors[combos[3].get()]
            valor = (d1 * 10 + d2) * mult
        elif n == 5:
            d1 = digit_colors[combos[0].get()]
            d2 = digit_colors[combos[1].get()]
            d3 = digit_colors[combos[2].get()]
            mult = multiplier_colors[combos[3].get()]
            tol = tolerance_colors[combos[4].get()]
            valor = (d1 * 100 + d2 * 10 + d3) * mult
        elif n == 6:
            d1 = digit_colors[combos[0].get()]
            d2 = digit_colors[combos[1].get()]
            d3 = digit_colors[combos[2].get()]
            mult = multiplier_colors[combos[3].get()]
            tol = tolerance_colors[combos[4].get()]
            tcr = tcr_colors[combos[5].get()]
            valor = (d1 * 100 + d2 * 10 + d3) * mult
        else:
            return

        # Formato de valor
        if valor >= 1_000_000:
            valor_str = f"{valor / 1_000_000:.2f} MΩ"
        elif valor >= 1_000:
            valor_str = f"{valor / 1_000:.2f} kΩ"
        else:
            valor_str = f"{valor:.0f} Ω"

        texto = f"Valor: {valor_str} {tol}"
        if n == 6:
            texto += f" | {tcr_colors.get(combos[5].get(), '')}"

        etiqueta_resultado.config(text=texto)
        dibujar_resistencia(n)

    except Exception:
        etiqueta_resultado.config(text="Error en el cálculo")

def dibujar_resistencia(n, inicial=False):
    """Dibuja el cuerpo de la resistencia y las bandas seleccionadas"""
    canvas.delete("all")

    # Cables
    canvas.create_line(20, 50, 100, 50, width=4, fill="black")
    canvas.create_line(300, 50, 380, 50, width=4, fill="black")

    # Cuerpo base
    canvas.create_rectangle(100, 30, 300, 70, fill="#E0E0E0", outline="black", width=2)

    # Posiciones predefinidas para cada cantidad de bandas
    posiciones = {
        4: [130, 160, 190, 250],
        5: [125, 150, 175, 200, 260],
        6: [120, 145, 170, 195, 220, 280]
    }

    # Dibujar bandas solo si no es inicial
    if not inicial:
        for i, combo in enumerate(combos):
            color = combo.get()
            if color:
                hex_color = color_hex.get(color, "#000000")
                x = posiciones[n][i]
                canvas.create_rectangle(x, 30, x + 10, 70, fill=hex_color, outline="black")

# --- Interfaz principal ---
root = tk.Tk()
root.title("Lector de Código de Colores de Resistencia")
root.geometry("440x520")

ttk.Label(root, text="Cantidad de Bandas:").pack(pady=5)
combo_bandas = ttk.Combobox(root, values=["4", "5", "6"], state="readonly", width=5)
combo_bandas.pack()

frame_bandas = ttk.Frame(root)
frame_bandas.pack(pady=10)

etiqueta_resultado = ttk.Label(root, text="Seleccione los colores", font=("Arial", 14))
etiqueta_resultado.pack(pady=10)

canvas = tk.Canvas(root, width=400, height=100, bg="white")
canvas.pack(pady=10)

combos = []

# Configuración inicial
combo_bandas.set("4")
actualizar_bandas()
combo_bandas.bind("<<ComboboxSelected>>", actualizar_bandas)

root.mainloop()
