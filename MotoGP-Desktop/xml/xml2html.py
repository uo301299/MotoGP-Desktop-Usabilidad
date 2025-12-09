import xml.etree.ElementTree as ET

class Html(object):
    """
    Clase para generar documentos HTML 5 válidos a partir de datos procesados.
    Adaptada para el esquema con namespace 'u:' (http://www.uniovi.es)
    """
    def __init__(self, titulo, archivo_css):
        self.contenido = []
        
        # Cabecera HTML5
        self.contenido.append('<!DOCTYPE HTML>')
        self.contenido.append('<html lang="es">')
        self.contenido.append('<head>')
        self.contenido.append('    <!-- Datos que describen el documento -->')
        self.contenido.append('    <meta charset="UTF-8" />')
        self.contenido.append('    <meta name="author" content="Nombre Apellido" />')
        self.contenido.append('    <meta name="description" content="Información del circuito proyecto MotoGp-Desktop" />')
        self.contenido.append('    <meta name="keywords" content="circuito, motogp, carrera, datos" />')
        self.contenido.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
        self.contenido.append(f'    <title>{titulo}</title>')
        # Enlazamos con el CSS (ruta relativa ../estilo/estilo.css)
        self.contenido.append(f'    <link rel="stylesheet" type="text/css" href="{archivo_css}" />')
        self.contenido.append('    <link rel="icon" href="../multimedia/favicon.ico" />')
        self.contenido.append('</head>')
        self.contenido.append('<body>')
        
    def add_body_start(self):
        """Genera el Header, Navegación y Breadcrumbs"""
        self.contenido.append('    <header>')
        self.contenido.append('        <!-- Datos con el contenidos que aparece en el navegador -->')
        self.contenido.append('        <h1><a href="index.html" title="Inicio de MotoGp-Desktop">MotoGP Desktop</a></h1>')
        self.contenido.append('        <nav>')
        self.contenido.append('            <a href="index.html" title="Inicio de MotoGp-Desktop">Inicio</a>')
        self.contenido.append('            <a href="piloto.html" title="Informacion del piloto">Piloto</a>')
        self.contenido.append('            <a class="activate" href="circuito.html" title="Informacion del circuito">Circuito</a>')
        self.contenido.append('            <a href="meteorologia.html" title="Información de la meteorologia">Meteorologia</a>')
        self.contenido.append('            <a href="clasificaciones.html" title="Información de las clasificaciones">Clasificaciones</a>')
        self.contenido.append('            <a href="juegos.html" title="Información de los juegos">Juegos</a>')
        self.contenido.append('            <a href="ayuda.html" title="Información de la ayuda">Ayuda</a>')
        self.contenido.append('        </nav>')
        self.contenido.append('    </header>')
        self.contenido.append('    <p>Estas en: <a href="index.html" title="Inicio de MotoGp-Desktop">Inicio</a> >> <strong>Circuito</strong></p>')
        self.contenido.append('    <main>')

    def add_header(self, nivel, texto):
        self.contenido.append(f'            <h{nivel}>{texto}</h{nivel}>')

    def add_paragraph(self, texto):
        self.contenido.append(f'            <p>{texto}</p>')

    def add_list_item(self, etiqueta, valor, unidad=""):
        texto_unidad = f" {unidad}" if unidad else ""
        self.contenido.append(f'                <li>{etiqueta}: {valor}{texto_unidad} </li>')

    def start_section(self):
        self.contenido.append('        <section>')
    
    def end_section(self):
        self.contenido.append('        </section>')

    def start_ul(self):
        self.contenido.append('            <ul>')

    def end_ul(self):
        self.contenido.append('            </ul>')

    def add_link(self, url, texto):
        self.contenido.append(f'                <li><a href="{url}" title="{texto}">{texto}</a></li>')

    def add_image(self, src, alt, titulo=""):
        self.contenido.append('            <figure>')
        self.contenido.append(f'                <img src="{src}" alt="{alt}" title="{titulo}" />')
        if titulo:
             self.contenido.append(f'                <figcaption>{titulo}</figcaption>')
        self.contenido.append('            </figure>')

    def add_video(self, src, titulo=""):
        self.contenido.append('            <section>')
        if titulo:
             self.contenido.append(f'                <h3>{titulo}</h3>')
        self.contenido.append('                <video controls preload="auto">')
        self.contenido.append(f'                    <source src="{src}" type="video/mp4" />')
        self.contenido.append('                    Tu navegador no soporta la etiqueta de video.')
        self.contenido.append('                </video>')
        self.contenido.append('            </section>')

    def add_classification_table(self, pilotos):
        self.contenido.append('            <table>')
        self.contenido.append('                <caption>Clasificación Mundial</caption>')
        self.contenido.append('                <tr>')
        self.contenido.append('                    <th scope="col">Posición</th>')
        self.contenido.append('                    <th scope="col">Piloto</th>')
        self.contenido.append('                    <th scope="col">Puntos</th>')
        self.contenido.append('                </tr>')
        
        for p in pilotos:
            self.contenido.append('                <tr>')
            self.contenido.append(f'                    <td>{p["pos"]}</td>')
            self.contenido.append(f'                    <td>{p["nombre"]}</td>')
            self.contenido.append(f'                    <td>{p["puntos"]}</td>')
            self.contenido.append('                </tr>')
        self.contenido.append('            </table>')

    def escribir(self, nombre_archivo):
        self.contenido.append('    </main>')
        self.contenido.append('</body>')
        self.contenido.append('</html>')
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.contenido))
            print(f"Archivo HTML generado correctamente: {nombre_archivo}")
        except IOError as e:
            print(f"Error escribiendo el archivo: {e}")

def main():
    nombre_xml = "circuitoEsquema.xml"
    nombre_html = "InfoCircuito.html"
    
    print(f"Leyendo archivo XML: {nombre_xml}...")
    try:
        arbol = ET.parse(nombre_xml)
        raiz = arbol.getroot()
    except Exception as e:
        print(f"Error abriendo XML: {e}")
        return

    # Definimos el namespace que usa tu XML
    ns = {'u': 'http://www.uniovi.es'}

    # Instancia de Html
    doc_html = Html("Información del Circuito", "../estilo/estilo.css")
    doc_html.add_body_start()

    # --- SECCIÓN 1: DATOS GENERALES ---
    doc_html.start_section()
    
    # Nombre
    nombre = raiz.find('u:nombre', ns).text
    doc_html.add_header(2, nombre)
    
    # Ubicación
    localidad = raiz.find('u:ubicacion/u:localidad', ns).text
    pais = raiz.find('u:ubicacion/u:pais', ns).text
    descripcion = f"Información sobre el circuito {nombre}, situado en {localidad} ({pais})."
    doc_html.add_paragraph(descripcion)

    doc_html.start_ul()
    
    # Dimensiones
    longitud = raiz.find('u:dimensiones/u:longitud', ns)
    anchura = raiz.find('u:dimensiones/u:anchura', ns)
    
    # Nota: Tu XML usa 'unidad' para longitud y 'unidades' para anchura
    doc_html.add_list_item("Longitud", longitud.text, longitud.get('unidad'))
    doc_html.add_list_item("Anchura media", anchura.text, anchura.get('unidades'))

    # Fecha, Hora, Vueltas
    fecha = raiz.find('u:fecha', ns)
    hora = raiz.find('u:hora_inicio', ns)
    vueltas = raiz.find('u:vueltas', ns)

    doc_html.add_list_item("Fecha carrera", fecha.text)
    doc_html.add_list_item("Hora inicio", hora.text)
    doc_html.add_list_item("Número de vueltas", vueltas.text)
    
    doc_html.end_ul()
    
    # Imágenes (Tu XML usa 'u:galeria_fotos')
    fotos = raiz.findall('u:galeria_fotos/u:foto', ns)
    for foto in fotos:
        # En tu XML el path está en el atributo 'archivo'
        src = foto.get('archivo')
        # El título está en el texto del elemento
        titulo = foto.text
        
        # Corrección de rutas:
        # El XML trae "./multimedia/...", lo cambiamos a "../multimedia/..."
        if src.startswith('./'):
            src = src.replace('./', '../')
            
        doc_html.add_image(src, f"Foto de {nombre}", titulo)
            
    doc_html.end_section()

    # --- SECCIÓN 2: REFERENCIAS ---
    doc_html.start_section()
    doc_html.add_header(2, "Referencias")
    doc_html.add_paragraph(f"Otras páginas donde encontrar información sobre {nombre}")
    
    doc_html.start_ul()
    referencias = raiz.findall('u:referencias/u:referencia', ns)
    for ref in referencias:
        url = ref.get('url')
        texto = ref.text
        doc_html.add_link(url, texto)
    doc_html.end_ul()
    doc_html.end_section()

    # --- SECCIÓN 3: VIDEOS ---
    doc_html.start_section()
    doc_html.add_header(2, "Videos")
    # Tu XML usa 'u:galeria_videos'
    videos = raiz.findall('u:galeria_videos/u:video', ns)
    
    if videos:
        for video in videos:
            src = video.get('archivo')
            titulo = video.text
            
            # Corrección de rutas
            if src.startswith('./'):
                src = src.replace('./', '../')

            doc_html.add_video(src, titulo)
    doc_html.end_section()

    # --- SECCIÓN 4: RESULTADOS Y CLASIFICACIÓN ---
    doc_html.start_section()
    doc_html.add_header(2, "Resultados y Clasificación")
    
    # Vencedor
    vencedor = raiz.find('u:resultados/u:vencedor', ns)
    if vencedor is not None:
        # Atributos: nombre y tiempo
        nombre_vencedor = vencedor.get('nombre')
        tiempo_vencedor = vencedor.get('tiempo')
        doc_html.add_paragraph(f"<strong>Vencedor de la prueba:</strong> {nombre_vencedor} (Tiempo: {tiempo_vencedor})")

    # Tabla de clasificación
    pilotos_xml = raiz.findall('u:clasificacion_mundial/u:piloto', ns)
    if pilotos_xml:
        datos_pilotos = []
        for p in pilotos_xml:
            datos_pilotos.append({
                "pos": p.get('pos'),
                "puntos": p.get('puntos'),
                "nombre": p.text
            })
        doc_html.add_classification_table(datos_pilotos)
        
    doc_html.end_section()

    # Escribir archivo final
    doc_html.escribir(nombre_html)

if __name__ == "__main__":
    main()