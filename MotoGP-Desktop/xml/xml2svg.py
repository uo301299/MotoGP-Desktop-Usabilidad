import xml.etree.ElementTree as ET

class Svg(object):
    """
    Clase para generar archivos SVG con formas básicas
    @version 1.0
    """
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")
        # Definimos el tamaño del lienzo
        self.raiz.attrib['width'] = "1000"
        self.raiz.attrib['height'] = "500"
        self.raiz.attrib['viewBox'] = "0 0 1000 500"
        # Fondo blanco
        ET.SubElement(self.raiz, 'rect', x="0", y="0", width="1000", height="500", fill="white")

    def addRect(self, x, y, width, height, fill, stroke_width, stroke):
        ET.SubElement(self.raiz, 'rect',
                      x=str(x), y=str(y),
                      width=str(width), height=str(height),
                      fill=fill,
                      **{'stroke-width': str(stroke_width)},
                      stroke=stroke)

    def addCircle(self, cx, cy, r, fill, stroke="none", stroke_width="0"):
        ET.SubElement(self.raiz, 'circle',
                      cx=str(cx), cy=str(cy),
                      r=str(r),
                      fill=fill,
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)})

    def addLine(self, x1, y1, x2, y2, stroke, stroke_width):
        ET.SubElement(self.raiz, 'line',
                      x1=str(x1), y1=str(y1),
                      x2=str(x2), y2=str(y2),
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)})

    def addPolyline(self, points, stroke, stroke_width, fill):
        ET.SubElement(self.raiz, 'polyline',
                      points=points,
                      stroke=stroke,
                      **{'stroke-width': str(stroke_width)},
                      fill=fill)

    def addText(self, texto, x, y, font_family, font_size, fill="black"):
        t = ET.SubElement(self.raiz, 'text',
                          x=str(x), y=str(y),
                          **{'font-family': font_family},
                          **{'font-size': str(font_size)},
                          fill=fill)
        t.text = texto

    def escribir(self, nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)

def main():
    nombreSVG = "altimetria.svg"
    archivoXML = "circuitoEsquema.xml"
    
    print(f"Leyendo archivo XML: {archivoXML}...")

    try:
        arbolXML = ET.parse(archivoXML)
        raizXML = arbolXML.getroot()

        # 1. GESTIÓN DEL NAMESPACE
        # Este XML usa el prefijo 'u' para 'http://www.uniovi.es'
        ns = {'u': 'http://www.uniovi.es'}

        # Datos Generales
        nombre_circuito = raizXML.find('u:nombre', ns).text
        
        # 2. OBTENER DATOS DE ALTIMETRÍA
        # Altitud inicial en <u:geografia><u:origen><u:altitud>
        alt_inicial = float(raizXML.find('u:geografia/u:origen/u:altitud', ns).text)
        
        puntos_grafica = [] 
        distancia_acumulada = 0.0
        
        # Punto 0 (Salida)
        puntos_grafica.append((distancia_acumulada, alt_inicial))

        # Recorrer tramos para obtener distancia y altitud final
        tramos = raizXML.findall('u:tramos/u:tramo', ns)
        
        for tramo in tramos:
            dist = float(tramo.find('u:distancia', ns).text)
            
            # La altitud está en <u:puntoFinal><u:altitud>
            punto_final = tramo.find('u:puntoFinal', ns)
            alt = float(punto_final.find('u:altitud', ns).text)
            
            distancia_acumulada += dist
            puntos_grafica.append((distancia_acumulada, alt))

        # 3. CÁLCULOS DE ESCALA (Mapping)
        ancho_canvas = 1000
        alto_canvas = 500
        margen_x = 50
        margen_y = 60 # Un poco más de margen arriba para título
        
        max_dist = puntos_grafica[-1][0] 
        altitudes = [p[1] for p in puntos_grafica]
        min_alt = min(altitudes)
        max_alt = max(altitudes)
        diff_alt = max_alt - min_alt if max_alt != min_alt else 1
        
        scale_x = (ancho_canvas - 2 * margen_x) / max_dist
        # Ajustamos para que la gráfica ocupe el 80% de la altura disponible
        scale_y = ((alto_canvas - 2 * margen_y) * 0.8) / diff_alt

        print(f"Circuito: {nombre_circuito}")
        print(f"Longitud Total: {max_dist:.2f} m")
        print(f"Altitud: Min {min_alt} m, Max {max_alt} m")

        # 4. GENERACIÓN DE PUNTOS SVG
        coords_svg = []
        polyline_string = ""
        
        # Nivel base visual (suelo del gráfico)
        suelo_grafico = alto_canvas - margen_y

        for dist, alt in puntos_grafica:
            px = margen_x + (dist * scale_x)
            # Invertimos Y: cuanto más alto, menor valor Y
            # Restamos la altura relativa al suelo gráfico
            altura_relativa = (alt - min_alt) * scale_y
            py = suelo_grafico - altura_relativa
            
            coords_svg.append((px, py))
            polyline_string += f"{px},{py} "

        # Polígono de relleno (para dar efecto montaña)
        polygon_string = polyline_string + f"{coords_svg[-1][0]},{suelo_grafico} {coords_svg[0][0]},{suelo_grafico}"

        # 5. DIBUJAR SVG
        miSVG = Svg()

        # Título
        miSVG.addText(f"Perfil Altimétrico: {nombre_circuito}", 
                      margen_x, 40, "Verdana", 24, "darkblue")

        # Relleno gris suave
        miSVG.addPolyline(polygon_string, "none", 0, "#e0e0e0")

        # Línea del perfil (azul gruesa)
        miSVG.addPolyline(polyline_string, "blue", 3, "none")

        # Ejes
        miSVG.addLine(margen_x, suelo_grafico, ancho_canvas - margen_x, suelo_grafico, "black", 2) # X
        miSVG.addLine(margen_x, margen_y, margen_x, suelo_grafico, "black", 2) # Y

        # Etiquetas Eje X (Cada km)
        for i in range(0, int(max_dist) + 1, 1000):
            px = margen_x + (i * scale_x)
            miSVG.addLine(px, suelo_grafico, px, suelo_grafico + 5, "black", 1)
            miSVG.addText(f"{i//1000}km", px - 10, suelo_grafico + 20, "Arial", 10)

        # Etiquetas Eje Y (Altitud Min y Max)
        # Mínima
        miSVG.addText(f"{min_alt:.1f}m", 5, suelo_grafico, "Arial", 10)
        # Máxima
        py_max = suelo_grafico - ((max_alt - min_alt) * scale_y)
        miSVG.addLine(margen_x - 5, py_max, margen_x, py_max, "black", 1)
        miSVG.addText(f"{max_alt:.1f}m", 5, py_max + 5, "Arial", 10)

        # Marcador de Salida
        miSVG.addCircle(coords_svg[0][0], coords_svg[0][1], 5, "red")
        miSVG.addText("Salida", coords_svg[0][0], coords_svg[0][1] - 10, "Arial", 10, "red")

        # Marcador de Meta (Final)
        miSVG.addCircle(coords_svg[-1][0], coords_svg[-1][1], 5, "red")
        miSVG.addText("Meta", coords_svg[-1][0] - 30, coords_svg[-1][1] - 10, "Arial", 10, "red")

        # Guardar archivo
        miSVG.escribir(nombreSVG)
        print(f"¡Éxito! Archivo generado: {nombreSVG}")

    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {archivoXML}")
    except ET.ParseError:
        print(f"Error: El archivo XML no es válido.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()