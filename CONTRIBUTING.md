# Guía de contribución

Gracias por mantener este proyecto. Esta guía resume cómo trabajar en el código
de forma consistente.

## Flujo de trabajo

1. Crea una rama a partir de `main` con un nombre descriptivo
   (`etapa-rectoria`, `fix-ingreso-neto`).
2. Haz cambios pequeños y enfocados.
3. Asegúrate de que las pruebas pasen: `pytest -q`.
4. Abre un pull request describiendo qué cambia y por qué.

## Estándares de código

- Sigue las convenciones descritas en `docs/manual_tecnico.md`
  ("Convenciones de código").
- Toda regla de negocio nueva o modificada debe tener su prueba en `tests/`.
- No pongas lógica de negocio en la interfaz ni en el núcleo: va en `dominio/`.
- Las funciones de dominio son puras (no tocan disco, no mutan su entrada).

## Antes de abrir un pull request

- [ ] `pytest -q` pasa localmente.
- [ ] Agregaste o actualizaste pruebas para tus cambios.
- [ ] Actualizaste la documentación si cambió el comportamiento.
- [ ] Actualizaste `CHANGELOG.md`.

## Reglas de negocio sensibles

Las reglas hardcodeadas (`dominio/columnas.py`: ajustes por estudiante, filas a
eliminar, correcciones por año) provienen del proceso financiero. **No las
cambies por tu cuenta**: valida cualquier ajuste con el área financiera y déjalo
documentado en el pull request.

## Diagramas

Los diagramas están en `docs/diagramas/` en formato PlantUML (texto). Si cambias
la arquitectura, actualiza el diagrama correspondiente en el mismo pull request.
