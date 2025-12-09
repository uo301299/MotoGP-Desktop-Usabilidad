   "use strict";
   class Memoria{
        constructor(){
            this.tablero_bloqueado = false;
            this.primera_carta = null;
            this.segunda_carta = null;
            this.barajarCartas();
        }

        voltearCarta(carta) {
            if (carta.getAttribute("data-estado") === "revelada") return;

            if (carta.getAttribute("data-estado") === "volteada") return;

            if (this.tablero_bloqueado) return;

            carta.dataset.estado = "volteada";

            if (!this.primera_carta) {
                this.primera_carta = carta;
                return;
            }

            this.segunda_carta = carta;
            this.tablero_bloqueado = true;

            this.comprobarPareja();

        }

        comprobarPareja(){
            setTimeout(function(){

                const img1 = this.primera_carta.querySelector("img").getAttribute("src");
                const img2 = this.segunda_carta.querySelector("img").getAttribute("src");
                if (img1 === img2) {
                    this.desHabilitarCarta();    
                } else {
                    this.cubrirCartas();
                }
            }.bind(this), 1500);
        }

        barajarCartas(){
            const contenedor = document.querySelector("main"); 
            const c = contenedor.querySelectorAll("article");
            const cartas = Array.from(c);
            for (let i = cartas.length - 1; i > 0; i--) {
                let j = Math.floor(Math.random() * (i + 1));
                [cartas[i], cartas[j]] = [cartas[j], cartas[i]];
            }
            cartas.forEach(carta => contenedor.appendChild(carta));
        }

        reiniciarAtributos(){
            this.tablero_bloqueado = false;
            this.primera_carta = null;
            this.segunda_carta = null;
        }

        desHabilitarCarta(){
            this.primera_carta.dataset.estado = "revelada";
            this.segunda_carta.dataset.estado = "revelada";
            this.comprobarJuego();
            this.reiniciarAtributos();
        }

        comprobarJuego() {
            const cartas = document.querySelectorAll("main article");
            let todasReveladas = true;
            cartas.forEach(carta => {
                if (carta.getAttribute("data-estado") !== 'revelada') todasReveladas = false;
            });

            if (todasReveladas) {
                this.tablero_bloqueado = true;
            }
        }

        cubrirCartas() {
            if (this.primera_carta && this.primera_carta.dataset.estado !== "revelada") {
                this.primera_carta.removeAttribute("data-estado");
            }

            if (this.segunda_carta && this.segunda_carta.dataset.estado !== "revelada") {
                this.segunda_carta.removeAttribute("data-estado");
            }
            this.reiniciarAtributos();
        }
   }

    const juegoMemoria = new Memoria();