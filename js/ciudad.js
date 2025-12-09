   "use strict";
   class Ciudad{

        constructor(nombre, pais, gentilicio){
            this.nombre = nombre 
            this.pais = pais
            this.gentilicio = gentilicio
            this.poblacion = null;
            this.coordenadas = null;
        }

        setPoblacion(poblacion){
            this.poblacion = poblacion;
        }

        setCoordenadas(coordenadas){
            this.coordenadas = coordenadas;
        }

        getNombre(){
            return this.nombre;
        }

        getPais(){
            return this.pais;
        }

        getExtraInfo(){

            const ul = document.createElement("ul");
            document.body.appendChild(ul);

            const gentilicio = document.createElement("li");
            gentilicio.textContent = "Gentilicio: " + this.gentilicio;
            ul.appendChild(gentilicio);

            const poblacion = document.createElement("li");
            poblacion.textContent = "Población: " + this.poblacion;
            ul.appendChild(poblacion);
      
        }

        escribirCoordenadas() {
            const mensaje = document.createElement("p");
            mensaje.textContent = "Coordenadas: ";
            document.body.appendChild(mensaje);

            const ul = document.createElement("ul");
            document.body.appendChild(ul);

            const latitud = document.createElement("li");
            latitud.textContent = "Latitud: " + this.coordenadas.latitud;
            ul.appendChild(latitud);

            const longitud = document.createElement("li");
            longitud.textContent = "Longitud: " + this.coordenadas.longitud;
            ul.appendChild(longitud);

            
        }

}