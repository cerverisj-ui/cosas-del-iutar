import math
import random
import tkinter as tk

ANCHO, ALTO = 800, 550
PISTAS = {
    "1": {"nombre": "Asfalto", "cielo": "#87ceeb", "pasto": "#2e8b57", "via": "#37373e", "vel": 180.0, "agarre": 1.0},
    "2": {"nombre": "Tierra", "cielo": "#d2b991", "pasto": "#a06e3c", "via": "#7d5028", "vel": 140.0, "agarre": 0.65},
    "3": {"nombre": "Hielo", "cielo": "#c3d7eb", "pasto": "#ebf2fa", "via": "#b9d2eb", "vel": 165.0, "agarre": 0.35},
}

st = {"p": "1", "z": 0.0, "v": 0.0, "x": 0.0, "vx": 0.0, "luz": True, "lenta": False, "t": 0.0}
teclas = set()
trafico = [{"z": 200.0, "x": -0.4, "v": 70.0, "c": "#c82828"}, {"z": 480.0, "x": 0.4, "v": 80.0, "c": "#286ed2"}]

root = tk.Tk()
root.title("Simulador 3D - Sedan con Chofer")
canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="#87ceeb", highlightthickness=0)
canvas.pack()


def key_down(e):
    k = e.keysym.lower()
    teclas.add(k)
    if k in PISTAS:
        st["p"] = k
    if k == "l":
        st["luz"] = not st["luz"]
    if k == "g":
        st["lenta"] = not st["lenta"]
    if k == "r":
        st["v"], st["x"], st["vx"] = 0.0, 0.0, 0.0


def key_up(e):
    teclas.discard(e.keysym.lower())


root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)


def dibujar_carro(cx, cy, giro):
    inc = giro * 8
    y = cy + (math.sin(st["t"] * 24) * 1.5 if st["v"] > 5 else 0)
    canvas.create_oval(cx - 110, y + 40, cx + 110, y + 70, fill="#18181c", outline="")
    canvas.create_rectangle(cx - 100, y + 18, cx - 72, y + 60, fill="#141416", outline="")
    canvas.create_rectangle(cx + 72, y + 18, cx + 100, y + 60, fill="#141416", outline="")
    canvas.create_polygon(cx - 95, y + 42, cx + 95, y + 42, cx + 90, y + 5, cx - 90, y + 5, fill="#1e1e22", outline="")
    canvas.create_polygon(cx - 90, y + 5, cx + 90, y + 5, cx + 80, y - 15, cx - 80, y - 15, fill="#735c41", outline="")
    canvas.create_polygon(cx - 76 + inc, y - 15, cx + 76 + inc, y - 15, cx + 58 + inc, y - 58, cx - 58 + inc, y - 58, fill="#735c41", outline="")
    canvas.create_polygon(cx - 66 + inc, y - 18, cx + 66 + inc, y - 18, cx + 50 + inc, y - 50, cx - 50 + inc, y - 50, fill="#2d3e4e", outline="")
    canvas.create_rectangle(cx + 14 + inc, y - 34, cx + 38 + inc, y - 18, fill="#85858a", outline="")
    canvas.create_rectangle(cx - 38 + inc, y - 34, cx - 14 + inc, y - 18, fill="#85858a", outline="")
    px = cx - 26 + inc + giro * 4
    canvas.create_oval(px - 14, y - 35, px + 14, y - 17, fill="#c32328", outline="")
    canvas.create_oval(px - 8, y - 49, px + 8, y - 33, fill="#e1b491", outline="")
    canvas.create_arc(px - 8, y - 51, px + 8, y - 35, start=0, extent=180, fill="#231914", outline="")
    canvas.create_rectangle(cx - 80, y - 22, cx + 80, y - 16, fill="#141416", outline="")
    cs = "#ff1e1e" if st["luz"] else "#780f0f"
    canvas.create_rectangle(cx - 86, y + 6, cx - 46, y + 18, fill=cs, outline="")
    canvas.create_rectangle(cx + 46, y + 6, cx + 86, y + 18, fill=cs, outline="")
    canvas.create_rectangle(cx - 20, y + 11, cx + 20, y + 23, fill="#ebebeb", outline="")


def loop():
    dt = 0.016 * (0.35 if st["lenta"] else 1.0)
    st["t"] += dt
    p = PISTAS[st["p"]]
    hy = int(ALTO * 0.45)

    acel = (1 if "w" in teclas or "up" in teclas else 0) - (1 if "s" in teclas or "down" in teclas else 0)
    giro = (1 if "d" in teclas or "right" in teclas else 0) - (1 if "a" in teclas or "left" in teclas else 0)

    st["v"] = max(0.0, min(p["vel"], st["v"] + (90 * dt if acel > 0 else (-140 * dt if acel < 0 else -45 * dt))))
    st["vx"] = (st["vx"] + giro * 2.8 * p["agarre"] * dt) * math.pow(0.02, p["agarre"] * dt)
    if st["v"] > 2:
        st["x"] = max(-1.1, min(1.1, st["x"] + st["vx"] * (st["v"] / 100.0) * dt * 2.4))
    st["z"] += st["v"] * dt * 4.5

    canvas.delete("all")
    canvas.create_rectangle(0, 0, ANCHO, hy, fill=p["cielo"], outline="")
    nf = ALTO - hy
    for y in range(0, nf, 5):
        py = hy + y
        pr = (y + 1) / float(nf)
        alt = int(((1.0 / pr) * 18.0 + st["z"]) * 0.4) % 2 == 0
        canvas.create_rectangle(0, py, ANCHO, py + 5, fill=p["pasto"] if alt else "#1f6b40", outline="")
        av = 45 + pr * (ANCHO * 0.65)
        cx = ANCHO / 2 - st["x"] * pr * (ANCHO * 0.28)
        canvas.create_rectangle(cx - av / 2 - 12, py, cx + av / 2 + 12, py + 5, fill="#dcdcdc" if alt else "#b42828", outline="")
        canvas.create_rectangle(cx - av / 2, py, cx + av / 2, py + 5, fill=p["via"] if alt else "#2c2c32", outline="")
        if alt:
            canvas.create_rectangle(cx - 4, py, cx + 4, py + 5, fill="#f0c828", outline="")

    for a in trafico:
        a["z"] += a["v"] * dt * 4.5
        if a["z"] - st["z"] < -20:
            a["z"], a["x"] = st["z"] + random.uniform(400, 700), random.choice([-0.5, 0.0, 0.5])
        rz = a["z"] - st["z"]
        if 8 < rz < 420:
            esc = 18.0 / rz
            py = hy + esc * nf
            av = 45 + esc * (ANCHO * 0.65)
            px = (ANCHO / 2 - st["x"] * esc * (ANCHO * 0.28)) + a["x"] * (av * 0.4)
            aw, ah = max(14, 160 * esc), max(10, 85 * esc)
            canvas.create_rectangle(px - aw / 2, py - ah, px + aw / 2, py, fill=a["c"], outline="#111")

    dibujar_carro(ANCHO / 2, ALTO - 110, giro)
    canvas.create_rectangle(10, 10, ANCHO - 10, 45, fill="#14161c", outline="#ffd700")
    canvas.create_text(25, 28, anchor="w", fill="#ffd700", font=("Arial", 13, "bold"), text=f"Pista: {p['nombre']} | Velocidad: {int(st['v'])} km/h | [1-3] Pista [L] Luces [G] Lento")
    root.after(16, loop)


loop()
root.mainloop()
