
        "use strict";
        class Cronometro { 
            constructor() {
                this.tiempo = 0; 
            }
            

            arrancar(){
                if (!this.corriendo) {
                    try{
                        this.inicio = Temporal.Now.instant() - this.tiempo;
                    }catch{
                        this.inicio = Date.now() - this.tiempo;
                    }
                    this.corriendo = setInterval(this.actualizar.bind(this), 100);
                }
                
                
            }

            actualizar() {
                try {
                    this.tiempo = Temporal.Now.instant().since(this.inicio).total("milliseconds");
                } catch (e) {
                    this.tiempo = Date.now() - this.inicio;
                }
                this.mostrar();
                
            }

            mostrar(){

                const minutos = Math.floor(this.tiempo / 60000);
                const segundos = Math.floor((this.tiempo % 60000) / 1000);
                const milisegundos = Math.floor((this.tiempo % 1000)/100)

                if (minutos  < 10) var stringMinutos  = "0" + minutos;
                    else stringMinutos = minutos;
                if (segundos < 10) var stringSegundos = "0" + segundos;
                    else stringSegundos = segundos;
                const stringCronometro = stringMinutos + " : " 
                                        + stringSegundos + " : " 
                                        + milisegundos; 
                document.querySelector("main p").textContent = stringCronometro;
            }

            parar() {
                clearInterval(this.corriendo);
                this.corriendo = null;
            }

            reiniciar() {
                this.parar();
                this.tiempo = 0;
                this.mostrar();
            }                       
        }
        var cronometro = new Cronometro();
    