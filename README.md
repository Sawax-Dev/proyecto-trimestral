# Proyecto trimestral: Punto de pago.

El proyectol trimestral se basa en un sistema de facturación desarrollado con python-flask, el cual permitirá realizar toda la gestión de facturación y la administración de usuarios, tal como funciona un sistema de pago comúnmente.

## Comenzando

El propósito del siguiente documento es dar una introducción básica al proyecto que se está elaborando y también contienene las instrucciones para poder ejecutar una acción pull y mostrar el proceso de arranque del proyecto.

### Prerequisites

Para clonar el repositorio en tu local, necesitarás tener las siguientes dependencias/paquetes o software instalado:

```
git
python/pip - pip --version
flask - pip install flask
motor de mysql
```

### Installing

A continuación se darán una serie de pasos los cuales indicarán como se puede instalar el proyecto en su local.

Paso 1. Clonar el repositorio.
```
git clone https://github.com/Sawax-Dev/proyecto-trimestral.git
```

Paso 2. Installar los paquetes del proyecto.
```
pip install pandas, flask, pymysql
```

Paso 3. Arrancar el archivo main.py (raíz del proyecto).
```
py main.py
```

Paso 4. Configurar la conexión de la base de datos en el archivo db.py.
```
Abrir src/db.py
pymysql.connect(host='YOUR HOST', port=3306, user='YOUR USER', passwd='YOUR PASSWORD', db='YOUR DATABASE')
```

## Built With

* [Flask](https://flask.palletsprojects.com/) - Framework web.
* [Jinja](https://jinja.palletsprojects.com/) - Motor de plantillas HTML.
* [Git](https://git-scm.com/) - Controlador de dependencias.
* [MYSQL](https://www.mysql.com/) - Motor de base de datos. 

## Contributing

Para contribuir en el proyecto se deben cumplir los criterios de:

* Pertenecer al equipo de desarrollo.

## Authors

* **Brian Castro** - *Full stack developer* - [Swyme](https://github.com/Sawax-Dev)
* **Anderson Méndez** - *Backend developer/Documentation* - [Anderson](https://github.com/Anderson735)

Puedes revisar la lista de [contribuidores](https://github.com/Sawax-Dev/contributors) que participaron en este proyecto.

## License

En redacción [LICENSE.md](LICENSE.md)

## Acknowledgments

* Agradecimientos especiales a los contribuyentes.