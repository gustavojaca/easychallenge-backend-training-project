# EasyChallenge client handler api

El objetivo de este repositorio es proveer un ejercicio que puede ser utilizado para pulir skills de desarrollo backend como diseño de sistemas, diseño de bases de datos relacionales, diseños de bases de datos en memoria, despliegue y escalamiento de servicios utilizando Kubernetes.

Se espera que el desafío propuesto en este repositorio se implemente utilizando las mejores prácticas posibles en el ámbito de la ingeniería de software, como aplicaciones de clean architecture, principios SOLID, patrones de diseño, unit/integration testing, entre otras.

## Descripción del problema

_EasyChallenge_ es una startup que ha desarrollado un algoritmo para generar desafíos computacionales que se usan para añadir una capa más de seguridad a las llamadas HTTP en las aplicaciones de sus clientes.

Esta startup tiene implementada una api llamada _challenge-generator_ que expone un endpoint que al hacerle una llamada devuelve una cadena que corresponde al desafío (challenge) y otra cadena que es la resolución (solution) del mismo.

Por cuestiones de seguridad de _EasyChallenge_, _challenge-generator_ es la única aplicación que puede generar desafíos. Sin embargo, la generación de challenges es un proceso costoso que requiere procesamiento y llamadas a otros servicios internos de la empresa, por lo tanto, esta api no escala bien. Además, cuando se implementó esta api no se tuvo en cuenta cuestiones de seguridad, asi que actualmente esta desplegada en un servicio oculto dentro de una red privada de la startup.

Más alla de esto, como los challenges estan atados a una vida útil o un numero máximo de usos (lo que primero ocurra), un astuto ingeniero de _EasyChallenge_ se dio cuenta de que es posible implementar un nuevo servicio que use _challenge-generator_ para generar desafíos, pero que implemente todo lo que la api existente no hace:

- Seguridad utilizando api keys
- Lógica para límite de tiempo de los desafíos
- Lógica para límite por cantidad de usos de los desafíos
- Soporte para muchos clientes concurrentes

El problema, es que el ingeniero no tiene tiempo para implementar este nuevo servicio dado tiene que enfocarse en mejorar el rendimiento de _challenge-generator_, es por esto que te contacto a _vos_ para que implementes este nuevo servicio llamado _challenge-client-handler_ utilizando los más altos estándares de la industria.

## Requerimientos básicos

- Implementar una api (con cualquier tecnología) que exponga 2 endpoints:
  - `GET /challenge`: Endpoint que devuelve la cadena _challenge_ de un desafío.
  - `POST /challenge`: Endpoint que reciba las cadenas _challenge_ y _solution_ de un desafío e indique si la resolución fue correcta.
- Los desafíos tienen una vida util de 10 segundos o 50 usos (lo que primero ocurra). Una vez expirado, se deben rechazar todas las peticiones que usen ese desafío. Sin embargo, una vez asignado un challenge a un cliente, ese desafío debe ser válido para ese cliente aunque el tiempo haya expirado.
- Se debe utilizar _challenge-generator_ para generar nuevos desafíos (teniendo en cuenta que esta api es lenta).
- La api tiene que estar protegida por un api key (provista a través del header `x-api-key`) que será único para cada cliente.

## Tecnologías solicitadas

Si bien el ingeniero te dijo que no había problema con respecto al lenguaje o framework con el que implementar el servicio, si te solicitó lo siguiente:

- Utilizar Redis para la corroboración de desafíos (dada su velocidad para este tipo de operaciones)
- Utilizar PostgreSQL para el almacenamiento de api keys (dado que a futuro esto despues lo integrarán en otra base de datos donde centralizaran las api keys de distintos productos)
- Utilizar Kubernetes (minikube) para desplegar el servicio dado que esta tecnología es estándar en los distintos proveedores cloud.

## Consideraciones generales

- El servicio tiene que soportar ráfagas de peticiones dado que algunos clientes no la utilizarán las 24 horas, si no que en momentos específicos del día. El ingeniero calcula que que de media habrá unas 100 peticiones concurrentes pero por momentos puede escalar hasta 25 veces más.
- El proyecto `challenge-client-handler-example-api` incluye una api de ejemplo del contrato entre api/cliente.
- El proyecto `client` puede utilizarse como cliente. Este tiene dos modos de ejecución:
  - `npm run client`: Para correr un cliente.
  - `npm run burst`: Para correr una ráfaga ascendente y descendente de clientes.
- En el proyecto `client`, pueden especificarse las api keys validas en un archivo llamado `api-keys.txt` de la manera que esta descripta en `api-keys.example.txt`.

## Resolución de los desafíos

Si bien la resolución de los desafíos se encuentra implementada en el cliente provisto (`client`), el algoritmo consta de realizar dos operaciones sobre la cadena de texto _challenge_:

- Generar un UUID v5 utilizando como namespace `6edc495c-860c-4917-921f-3c9a04636d74`.
- Al UUID v5 generado aplicarle un hash SHA256 y utilizar la versión hexadecimal del mismo.
