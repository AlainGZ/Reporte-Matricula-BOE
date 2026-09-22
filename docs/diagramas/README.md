# Diagramas (PlantUML)

Diagramas del proyecto en formato **PlantUML** (texto plano, `.puml`). Son texto
para que se versionen junto al código y se puedan revisar en los pull requests.

| Archivo | Tipo | Muestra |
|---------|------|---------|
| `01_flujo_proceso.puml` | Flujo (actividad) | El proceso de negocio de principio a fin, con el punto de revisión del usuario. |
| `02_arquitectura_componentes.puml` | Componentes | Las cuatro capas (interfaz, etapas, núcleo, dominio) y sus dependencias. |
| `03_clases.puml` | Clases | Las clases principales del núcleo, las etapas y la interfaz. |
| `04_secuencia_etapa1.puml` | Secuencia | El recorrido de una ejecución de la Etapa 1 con revisión. |
| `05_estados_orquestador.puml` | Estados | El ciclo del orquestador y sus puntos de pausa. |

## Cómo verlos

Los archivos `.puml` son texto: se pueden leer directamente. Para verlos como
imagen, cualquiera de estas opciones:

- **VS Code** con la extensión *PlantUML* (vista previa con `Alt+D`).
- **En línea:** pegar el contenido en <https://www.plantuml.com/plantuml>.
- **Línea de comandos** (requiere Java y `plantuml.jar`):

  ```bash
  java -jar plantuml.jar docs/diagramas/*.puml
  ```

## Al cambiar la arquitectura

Actualiza el diagrama correspondiente en el mismo pull request que el cambio de
código, para que no se desactualicen.
