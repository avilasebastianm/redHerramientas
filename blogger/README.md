# Tema de Blogger

El tema se genera a partir de la propuesta (`index.html`, `contacto.html`, `donar.html`, `styles.css`, `script.js`). Después de cambiar algo, regenerarlo:

```
python3 blogger/build.py
```

Genera:
- `tema-redherramientas.xml`: el tema.
- `paginas/donar.html`: el contenido de la página Donar (generado).
- `paginas/contacto.html`: la página Contacto que armó Lucas en Blogger (copiada de ahí el 24/10, no se genera: si se cambia en Blogger, volver a copiarla).

Los estilos que solo se usan en Blogger (posteos, listados y ajustes) están en `blogger.css`.

## Instalación
1. **Copia de seguridad del tema actual:** Blogger → Tema → flecha junto a "Personalizar" → Copia de seguridad → Descargar.
2. **Subir el tema:** Tema → flecha → Restablecer → Subir → `tema-redherramientas.xml`. Blogger no pregunta qué hacer con los gadgets del tema anterior: los manda a la sección oculta `descartados` (arriba de todo en Diseño). No se ven, pero sus scripts siguen corriendo, así que hay que borrarlos desde Diseño (lápiz → Quitar).
3. **Página Contacto:** Páginas → "Contactanos" → vista HTML (ícono `<>`) → reemplazar todo por el contenido de `paginas/contacto.html`.
4. **Página Donar:** Páginas → Nueva página → título "Donar" (tiene que quedar en `/p/donar.html`) → vista HTML → pegar `paginas/donar.html`.
5. **Carrusel:** a los posteos que tienen que aparecer en el carrusel se les agrega la etiqueta `Carrusel`. Si ninguno la tiene, se muestran los últimos.
6. **Novedades:** muestra las últimas 3 entradas con la etiqueta `Novedades`. Si no hay ninguna, la sección no aparece.

Las fotos y logos del diseño están subidos en la entrada borrador "Imágenes del sitio (no publicar ni borrar)" de redherramientas.com; sus direcciones están en `IMG_URLS` y `LOGO_URL` de `build.py`.

## Cómo se ve cada parte
- **Home:** el carrusel, Quiénes somos, los ejes, Novedades, Donar y la franja de contacto.
- **Posteos:** diseño editorial con migas, título, fecha y tiempo de lectura, foto principal, bajada, botones para compartir, "Seguí leyendo" y la columna "Lo más leído" / "¿Querés sumarte?".
- **Etiquetas, búsquedas y archivo** (por ejemplo, los links de los ejes): una grilla de tarjetas con imagen, título y resumen, más "Más antiguas / Más nuevas".
- **Página 404 y búsquedas sin resultados:** un mensaje con links a los ejes, al inicio y a Contacto.
- **Páginas** como Quiénes somos: el mismo formato que los posteos. Las que empiezan con `<div class="rh-full">`, como Contacto y Donar, se muestran a página completa.

## Editar la home sin tocar código
En Blogger → **Diseño**, cada sección de la home es un gadget HTML: Quiénes somos, Nuestros ejes, Novedades y Apoyá nuestro espacio. Se editan con el lápiz, y en el último bloque se pueden reordenar o agregar gadgets.

Ojo: si después se vuelve a subir el tema, puede que Blogger conserve el contenido editado o que lo reemplace por el de `index.html`. Conviene pasar los cambios también a `index.html`.

## Clases para usar al escribir una página
Las variables de color y tipografía están todas en el `:root` de `styles.css`. Al armar el HTML de una página o un gadget, usar estas clases en vez de estilos sueltos:

| Para | Clase |
|---|---|
| Página a todo el ancho, sin columna lateral | `<div class="rh-full">` envolviendo todo |
| Contenido centrado con márgenes | `container` |
| Título de sección | `section-title` |
| Barra rosa entre secciones | `separator` |
| Botón principal (rosa) | `btn` |
| Botón sobre fondo de color | `btn btn-outline` |
| Botón destacado (mostaza, como Donar) | `btn btn-mustard` |
| Botón claro con borde rosa | `btn btn-light` |
| Etiqueta / tema (rosa, en mayúsculas) | `chip-label` |
| Ventana con datos (como la de Donar) | `<dialog class="modal">` + un botón con `data-modal="id-de-la-ventana"` |
| Botón para copiar un dato | `copy-btn` con `data-copy="nombre"` y el dato en `<span data-value="nombre">` |

## Pendiente
- Comentarios en los posteos: el tema no los muestra.
