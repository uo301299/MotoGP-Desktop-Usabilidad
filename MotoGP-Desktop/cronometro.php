<!DOCTYPE HTML>

<html lang="es">
<head>
    <!-- Datos que describen el documento -->
    <meta charset="UTF-8" />
    <title>MotoGP-Piloto</title>
	<meta name ="author" content="Iyan Alvarez Casasnovas"/>
	<meta name="descrption" content="Informacion sobre el piloto del proyecto MotoGP-Desktop"/>
	<meta name="keywords" content="moto, motoGP"/>
	<meta name="viewport" content="width=device-width, initial-scale=1.0"/>	
		
	<link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
	<link rel="stylesheet" type="text/css" href="estilo/layout.css" />

	<link rel="icon" type="image/ico" href="multimedia/favicon.ico" />
</head>

    <?php
        class Cromometro{
            protected $tiempo;
            protected $inicio;


            public function __construct(){
                $this->tiempo = 0;
            }

            public function arrancar(){
                $this->inicio = microtime(true);
            }

            public function parar(){
                $this->tiempo = microtime(true) - $this->inicio;
            }

            public function mostrar(){
                $min   = floor($tiempo / 60);
                $seg   = floor($tiempo % 60);
                $dec   = floor(($tiempo - floor($tiempo)) * 10);
                return "<p>".$min.":".$seg.":".$dec."</p>";
            }

        }
    ?>


<body>
    <!-- Datos con el contenidos que aparece en el navegador -->
	<header>
		<h1><a href="index.html">MotoGP-Desktop</a></h1>
		<nav>
			<a href="index.html" title="Inicio">Inicio</a>
			<a href="piloto.html" class="active" title="Informacion del piloto">Piloto</a>
			<a href="circuito.html" title="Informacion del circuito">Circuito</a>
			<a href="meteorologia.html" title="Informacion del meteorologia">Meteorologia</a>
			<a href="clasificaciones.html" title="Informacion del clasificaciones">Clasificaciones</a>
			<a href="juegos.html" title="Informacion del juegos">Juegos</a>
			<a href="ayuda.html" title="Informacion del ayuda">Ayuda</a>
		</nav>
	</header>
	
	<nav><p>
		Estás en: <a href="index.html">Inicio</a> >> <a href="juegos.html">Juegos</a> >> <strong>Cronometro</strong>
	</p></nav>

    
    


</body>
</html>