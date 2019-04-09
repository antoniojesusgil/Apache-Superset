# Extender d3-format
### by Antonio Jesús Gil

D3 es una librería Javascript para manipular documentos basados en datos, conforme versa en su [web oficial](https://d3js.org/):

D3 allows you to bind arbitrary data to a Document Object Model (DOM), and then apply data-driven transformations to the document. For example, you can use D3 to generate an HTML table from an array of numbers. Or, use the same data to create an interactive SVG bar chart with smooth transitions and interaction.

D3 is not a monolithic framework that seeks to provide every conceivable feature. Instead, D3 solves the crux of the problem: efficient manipulation of documents based on data. This avoids proprietary representation and affords extraordinary flexibility, exposing the full capabilities of web standards such as HTML, SVG, and CSS. With minimal overhead, D3 is extremely fast, supporting large datasets and dynamic behaviors for interaction and animation.


### Módulo d3-format
Permite el formateo numérico, de fechas y tiempo adaptándolo a locales o modificándose en función de unos requisitos concretos. 

[d3-format oficial web](https://github.com/d3/d3-format)

### Versión d3-format 

Partimos de la versión oficial 0.27.0 de Superset. La interfaz FrontEnd está construida en React e implementa la versión 3.5.17 de d3 conforme al archivo `package.json`

```json
 "dependencies": {
    "@data-ui/event-flow": "^0.0.54",
    "@data-ui/sparkline": "^0.0.54",
    "@vx/responsive": "0.0.153",
    "babel-register": "^6.24.1",
    "bootstrap": "^3.3.6",
    "bootstrap-slider": "^10.0.0",
    "brace": "^0.11.1",
    "brfs": "^1.4.3",
    "classnames": "^2.2.5",
    "d3": "^3.5.17",
    "d3-cloud": "^1.2.1",
    "d3-hierarchy": "^1.1.5",
    "d3-sankey": "^0.4.2",
    "d3-svg-legend": "^1.x",
    "d3-tip": "^0.9.1",
```
### es-ES locale format
```json
{
  "decimal": ",",
  "thousands": ".",
  "grouping": [3],
  "currency": ["", "€"],
  "dateTime": "%a %b %e %X %Y",
  "date": "%d/%m/%Y",
  "time": "%H:%M:%S",
  "periods": ["AM", "PM"],
  "days": ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
  "shortDays": ["Dom", "Lun", "Mar", "Mi", "Jue", "Vie", "Sab"],
  "months": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
  "shortMonths": ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
}
```