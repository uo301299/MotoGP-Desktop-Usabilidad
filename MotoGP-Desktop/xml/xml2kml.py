import xml.etree.ElementTree as ET

class Kml(object):
    """
    Clase para generar archivos KML
    """
    def __init__(self):
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud):
        """
        Añade un marcador (punto)
        """
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'description').text = descripcion
        punto = ET.SubElement(pm, 'Point')
        ET.SubElement(punto, 'coordinates').text = f'{long},{lat},{alt}'
        ET.SubElement(punto, 'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade una línea (recorrido)
        """
        # Estilo para la línea
        estiloID = f"estilo_{nombre.replace(' ', '_')}"
        estilo = ET.SubElement(self.doc, 'Style', id=estiloID)
        lineaEstilo = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(lineaEstilo, 'color').text = color
        ET.SubElement(lineaEstilo, 'width').text = ancho

        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'styleUrl').text = f"#{estiloID}"
        
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellation').text = tesela
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud
        ET.SubElement(ls, 'coordinates').text = listaCoordenadas

    def escribir(self, nombreArchivoKML):
        """
        Genera el archivo físico
        """
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)

def main():
    nombreKML = "circuito.kml"
    archivoXML = "circuitoEsquema.xml"

    print(f"Leyendo archivo XML: {archivoXML}...")

    try:
        arbolXML = ET.parse(archivoXML)
        raizXML = arbolXML.getroot()

        # 1. GESTIÓN DEL NAMESPACE
        # El archivo usa el prefijo 'u' asociado a 'http://www.uniovi.es'
        ns = {'u': 'http://www.uniovi.es'}

        nuevoKML = Kml()

        # 2. Extracción de datos generales
        nombre_circuito = raizXML.find('u:nombre', ns).text
        localidad = raizXML.find('u:ubicacion/u:localidad', ns).text
        pais = raizXML.find('u:ubicacion/u:pais', ns).text
        descripcion = f"Circuito de {nombre_circuito} en {localidad}, {pais}"

        # 3. Obtener coordenadas de ORIGEN
        # Ruta: <u:geografia> -> <u:origen>
        origen = raizXML.find('u:geografia/u:origen', ns)
        
        orig_lon = origen.find('u:longitud', ns).text
        orig_lat = origen.find('u:latitud', ns).text
        orig_alt = origen.find('u:altitud', ns).text

        # Añadir marcador en la salida
        nuevoKML.addPlacemark("Línea de Meta/Salida", 
                              descripcion, 
                              orig_lon, orig_lat, orig_alt, 
                              'relativeToGround')

        # 4. Construir el recorrido (LineString)
        # Empezamos con el punto de origen
        lista_coords = [f"{orig_lon},{orig_lat},{orig_alt}"]

        # Iterar sobre los tramos para obtener los puntos finales
        tramos = raizXML.findall('u:tramos/u:tramo', ns)
        
        for i, tramo in enumerate(tramos):
            # Ruta: <u:puntoFinal>
            punto_final = tramo.find('u:puntoFinal', ns)
            
            lon = punto_final.find('u:longitud', ns).text
            lat = punto_final.find('u:latitud', ns).text
            alt = punto_final.find('u:altitud', ns).text
            
            # Añadir coordenada a la lista
            lista_coords.append(f"{lon},{lat},{alt}")

        # Convertir la lista en un string separado por espacios (formato KML)
        # Nota: KML usa espacios para separar tuplas de coordenadas, y comas para lat,lon,alt
        string_coordenadas = " \n".join(lista_coords)

        # Añadir la línea al KML (Color rojo opaco: ff0000ff)
        nuevoKML.addLineString(f"Trazado: {nombre_circuito}", 
                               "1", # extrude
                               "1", # tessellation
                               string_coordenadas, 
                               'relativeToGround', 
                               'ff0000ff', # Color (aabbggrr) -> Rojo
                               "5") # Ancho

        # 5. Escribir archivo final
        nuevoKML.escribir(nombreKML)
        print(f"¡Éxito! Archivo generado: {nombreKML} con {len(lista_coords)} puntos.")

    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo {archivoXML}")
    except ET.ParseError:
        print(f"Error: El archivo {archivoXML} no es un XML válido")
    except AttributeError as e:
        print(f"Error de estructura XML (xPath incorrecto): {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()