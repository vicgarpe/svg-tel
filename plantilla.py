#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
hola esto está modificado
generador_soporte_TODO.py
================================
Proyecto docente para aprender FUNCIONES en Python generando un SVG
con las piezas de un soporte de móvil listo para corte láser.

🧭 Cómo usarlo en clase
1) Ejecuta el archivo para comprobar que genera un SVG inicial (placeholder).
2) Completa los TODO en orden (1 → 11).
3) Tras cada TODO, ejecuta y observa el cambio en el SVG.
4) Activa los mini-tests (assert) cuando implementes las funciones.

🎯 Objetivos
- Entender def, parámetros, return.
- Distinguir funciones "puras" (cálculo) de funciones con efectos (E/S).
- Encadenar funciones pequeñas para producir un entregable (SVG).
- Pasar parámetros por línea de comandos (argparse).

📦 No requiere librerías externas.
"""

from typing import Tuple
import argparse


# ============================================================
#            UTILIDADES SVG (TODO 1–4)
# ============================================================

def svg_header(width_mm: float, height_mm: float) -> str:
    """
    TODO 1: DEVOLVER la cabecera de un SVG en milímetros.

    ✔️ Qué debe hacer:
       - Abrir la etiqueta <svg> con atributos:
           xmlns="http://www.w3.org/2000/svg"
           width="Xmm" height="Ymm"
           viewBox="0 0 X Y"
           version="1.1"
       - Abrir un grupo <g> con estilo por defecto:
           fill="none" stroke="black" stroke-width="0.1"

    💡 Pista:
       Usa f-strings para insertar width_mm y height_mm.
       Ejemplo de inicio (no copiar literal):
         f'<svg ... width="{width_mm}mm" ...>\\n<g ...>\\n'

    🔄 Resultado:
       Una cadena con la cabecera, terminada en nueva línea \\n.
    """
    # 👇 De momento devolvemos una cabecera mínima para que todo ejecute.
    #    Sustitúyela por la versión completa según las instrucciones.
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width_mm}mm" height="{height_mm}mm" '
        f'viewBox="0 0 {width_mm} {height_mm}" version="1.1">\n'
        f'<g fill="none" stroke="black" stroke-width="0.1">\n'
    )


def svg_footer() -> str:
    """
    TODO 2: CERRAR etiquetas de grupo y svg.

    ✔️ Qué debe hacer:
       - Devolver el cierre del grupo y del svg:
         </g> y </svg> (con saltos de línea).

    🔄 Resultado:
       "</g>\\n</svg>\\n"
    """
    return "</g>\n</svg>\n"


def rect(x: float, y: float, w: float, h: float, r: float = 0.0) -> str:
    """
    TODO 3: DEVOLVER un rectángulo SVG.

    ✔️ Qué debe hacer:
       - Crear un elemento <rect> con atributos:
         x, y, width, height, rx, ry (siendo rx=ry=r).
       - Terminar en \\n.

    📏 Unidades:
       Estamos trabajando en mm porque el viewBox coincide con mm.

    🧪 Mini-prueba visual:
       Tras implementarla, dibuja un rectángulo desde main()
       para ver algo en el SVG.
    """
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" ry="{r}"/>\n'


def text(x: float, y: float, contenido: str, tam: float = 6.0) -> str:
    """
    TODO 4: DEVOLVER texto SVG visible.

    ✔️ Qué debe hacer:
       - Crear un elemento <text> con:
         x, y, font-family="monospace", font-size=tam,
         fill="black", stroke="none"
       - Contenido entre > ... </text>
       - Terminar en \\n.

    🧪 Mini-prueba:
       Añade un texto "Hola SVG" y verifica que lo ves.
    """
    return (f'<text x="{x}" y="{y}" font-family="monospace" '
            f'font-size="{tam}" fill="black" stroke="none">{contenido}</text>\n')


# ============================================================
#            GEOMETRÍA DEL SOPORTE (TODO 5–9)
# ============================================================

def compensa_kerf(ancho_nominal: float, kerf: float) -> float:
    """
    TODO 5: AJUSTAR ancho de ranura por kerf.

    🧠 Concepto:
       El láser "se come" material → la ranura resultará más ancha.
       Estrategia didáctica: ranura = ancho_nominal + kerf.

    ✔️ Qué debe hacer:
       - Devolver max(0.1, ancho_nominal + kerf) para evitar ceros/negativos.

    🔬 Opcional:
       Usa assert para asegurar que kerf >= 0 (solo en desarrollo).
    """
    # assert kerf >= 0, "El kerf no puede ser negativo"
    return max(0.1, ancho_nominal + kerf)


def ranura_centrada(pieza_w: float, pieza_h: float,
                    ranura_w: float, ranura_h: float,
                    offset_y: float) -> Tuple[float, float, float, float]:
    """
    TODO 6: CALCULAR (x, y, w, h) de una ranura centrada en X.

    ✔️ Qué debe hacer:
       x = (pieza_w - ranura_w) / 2.0
       y = offset_y
       w = ranura_w
       h = ranura_h

    🧪 Mini-test esperado:
       ranura_centrada(100, 50, 10, 5, 20) → x = 45.0
    """
    x = (pieza_w - ranura_w) / 2.0
    y = offset_y
    return x, y, ranura_w, ranura_h


def pieza_base(x0: float, y0: float, w: float, h: float,
               t_material: float, kerf: float, radio: float) -> str:
    """
    TODO 7: DIBUJAR la pieza base (rectángulo + ranura vertical centrada).

    ✔️ Pasos:
       1) Dibuja el rectángulo base con rect(x0, y0, w, h, radio).
       2) Calcula ranura_w = compensa_kerf(t_material, kerf)
          y ranura_h = 0.35 * h
       3) Centra en X y colócala verticalmente centrada:
          offset_y = (h - ranura_h) / 2
          x_r, y_r, w_r, h_r = ranura_centrada(w, h, ranura_w, ranura_h, offset_y)
       4) Dibuja la ranura sumando al svg el rectángulo de la ranura:
          rect(x0 + x_r, y0 + y_r, w_r, h_r, 0)

    🔎 Sugerencia:
       Construye la cadena svg por partes y concatena.
    """
    svg = rect(x0, y0, w, h, radio)
    ranura_w = compensa_kerf(t_material, kerf)
    ranura_h = h * 0.35
    x_r, y_r, w_r, h_r = ranura_centrada(w, h, ranura_w, ranura_h, (h - ranura_h) / 2)
    svg += rect(x0 + x_r, y0 + y_r, w_r, h_r, 0)
    return svg


def pieza_espaldar(x0: float, y0: float, w: float, h: float,
                   t_material: float, kerf: float, radio: float,
                   grosor_movil: float) -> str:
    """
    TODO 8: DIBUJAR la pieza espaldar (rectángulo + ranura horizontal + muesca móvil).

    ✔️ Pasos:
       1) Rectángulo principal: rect(x0, y0, w, h, radio).
       2) Ranura horizontal:
          - ranura_h = compensa_kerf(t_material, kerf)
          - ranura_w = 0.4 * w
          - offset_y = 0.65 * h
          - céntrala con ranura_centrada(w, h, ranura_w, ranura_h, offset_y)
            y dibújala.
       3) Muesca de apoyo del móvil:
          - holgura = 4.0
          - m_w = grosor_movil + holgura
          - m_h = 8.0
          - centrada: m_x = x0 + (w - m_w)/2
                      m_y = y0 + 0.45 * h
          - dibuja rect(m_x, m_y, m_w, m_h, r=1.5)

    🎯 Resultado:
       Un string con los elementos SVG concatenados.
    """
    svg = rect(x0, y0, w, h, radio)
    ranura_h = compensa_kerf(t_material, kerf)
    ranura_w = w * 0.4
    x_r, y_r, w_r, h_r = ranura_centrada(w, h, ranura_w, ranura_h, h * 0.65)
    svg += rect(x0 + x_r, y0 + y_r, w_r, h_r, 0)

    holgura, m_h = 4.0, 8.0
    m_w = grosor_movil + holgura
    m_x = x0 + (w - m_w) / 2
    m_y = y0 + h * 0.45
    svg += rect(m_x, m_y, m_w, m_h, 1.5)
    return svg


def ensamblado_svg(params: dict) -> str:
    """
    TODO 9: ENSAMBLAR el plano completo (dos piezas + etiquetas).

    ✔️ Parámetros esperados en params:
       - t (espesor), kerf, radio, grosor_movil
       - plano_w, plano_h  (tamaño del lienzo, en mm)

    ✔️ Composición sugerida:
       - W,H = params["plano_w"], params["plano_h"]
       - margen (mx,my) = (10,10)
       - base: 120x80  en (mx, my)
       - espaldar: 80x130 en (mx + base_w + 20, my)
       - Añade un texto etiqueta con t y kerf, debajo de la base.

    🧪 Prueba:
       Cambia t y kerf y observa el efecto en el SVG.
    """
    W, H = params["plano_w"], params["plano_h"]
    svg = svg_header(W, H)

    mx, my = 10.0, 10.0
    base_w, base_h = 120.0, 80.0
    esp_w, esp_h = 80.0, 130.0

    svg += pieza_base(mx, my, base_w, base_h,
                      params["t"], params["kerf"], params["radio"])

    svg += pieza_espaldar(mx + base_w + 20.0, my, esp_w, esp_h,
                          params["t"], params["kerf"], params["radio"],
                          params["grosor_movil"])

    svg += text(mx, my + base_h + 15, f"Soporte v1  t={params['t']}mm  kerf={params['kerf']}mm", 5.5)

    svg += svg_footer()
    return svg


# ============================================================
#            ENTRADA/SALIDA (ya hecho)
# ============================================================

def guardar_svg(nombre: str, contenido: str) -> None:
    """
    Función con EFECTO: escribe el archivo SVG en disco.
    """
    with open(nombre, "w", encoding="utf-8") as f:
        f.write(contenido)


# ============================================================
#            PROGRAMA PRINCIPAL (TODO 10–11)
# ============================================================

def parse_args() -> argparse.Namespace:
    """
    (Opcional avanzado) Parser de argumentos.
    Puedes usarlo ya si quieres pasar parámetros desde terminal.
    """
    p = argparse.ArgumentParser(description="Genera un SVG de un soporte de móvil paramétrico (TODO).")
    p.add_argument("--espesor", "-t", type=float, default=3.0, help="Espesor del material (mm).")
    p.add_argument("--kerf", "-k", type=float, default=0.15, help="Compensación de kerf (mm).")
    p.add_argument("--radio", "-r", type=float, default=3.0, help="Radio de esquina (mm).")
    p.add_argument("--grosor-movil", type=float, default=9.0, help="Grosor aproximado del móvil (mm).")
    p.add_argument("--plano-w", type=float, default=220.0, help="Ancho del plano (mm).")
    p.add_argument("--plano-h", type=float, default=160.0, help="Alto del plano (mm).")
    p.add_argument("--salida", "-o", type=str, default="soporte.svg", help="Nombre del archivo SVG de salida.")
    return p.parse_args()


def main() -> None:
    """
    TODO 10: Crear el diccionario params con valores por defecto.

      params = dict(
          t=3.0,
          kerf=0.15,
          radio=3.0,
          grosor_movil=9.0,
          plano_w=220.0,
          plano_h=160.0,
      )

    TODO 11: Llamar a ensamblado_svg(params), guardar_svg("soporte.svg", svg),
             y hacer un print de confirmación.

    🧪 Tip:
      Ejecuta y abre soporte.svg. Tras cada TODO deberías ver más elementos.
    """
    # Si quieres usar argumentos desde terminal, descomenta estas líneas:
    args = parse_args()
    params = dict(
        t=args.espesor,
        kerf=args.kerf,
        radio=args.radio,
        grosor_movil=args.grosor_movil,
        plano_w=args.plano_w,
        plano_h=args.plano_h,
    )

    svg = ensamblado_svg(params)
    guardar_svg(args.salida, svg)
    print(f"[OK] Generado '{args.salida}' — t={params['t']} mm, kerf={params['kerf']} mm.")


if __name__ == "__main__":
    # ============================================================
    #      MINI–TESTS (actívalos cuando implementes funciones)
    # ============================================================
    # assert compensa_kerf(3.0, 0.15) > 3.0, "La ranura debe ensancharse"
    # assert ranura_centrada(100, 50, 10, 5, 20)[0] == 45.0, "La ranura debería quedar centrada"
    main()
