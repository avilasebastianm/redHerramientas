# Wiki - Red de Herramientas MVP 📚

Esta Wiki documenta el contexto, los enlaces de referencia y las decisiones de diseño tomadas para el rediseño del portal de Red de Herramientas.

## 1. Enlaces y Requerimientos de Referencia

*   📄 **Requerimiento del usuario (Documento Original):** [Ver en Google Docs](https://docs.google.com/document/d/1HCpxzlgY5GbQFjgwR5otXe_XewzKwa_SuRi9SNdSIeQ/edit?tab=t.0)
*   🌐 **Sitio Web Original:** [https://www.redherramientas.com/](https://www.redherramientas.com/)

---

## 2. Decisiones de Accesibilidad (Adultos Mayores)

Dado que el público objetivo principal son **mujeres mayores de 60 años**, se implementaron las siguientes reglas de accesibilidad:

1.  **Tipografía:** Fuentes sin serifas (`Roboto`), de tamaño grande (20px para el cuerpo, 34px para títulos) con fuerte contraste frente al fondo (Texto negro sobre fondo blanco/gris muy claro). No se emplean grises medios para lectura.
2.  **Áreas de Interacción Táctil:** Los botones y los enlaces no son simples textos. Tienen contenedores grandes (mínimo de 60-80px de altura) evitando frustraciones motrices al hacer "tap" o "clic".
3.  **Reducción de Carga Cognitiva:**
    *   No hay animaciones rápidas.
    *   No hay carruseles automáticos. Se implementaron diseños envolventes (`Wrap` adaptativo) en lugar de listas con scroll horizontal que suelen pasar desapercibidas.
4.  **Menú Homogéneo:** Se utilizó un "Menú de 3 rayas" (Hamburger / Drawer) universal tanto en Desktop como en Mobile, centralizando la navegación.

---

## 3. Resumen de Cambios Estructurales (Enhancements v1.0.0)

Según las solicitudes de reestructuración, se realizaron las siguientes modificaciones en la página principal:

### Espacios de Actividades (Grilla Central)
Se respetó el espíritu visual original de cuadros de colores (Azul, Verde, Rojo, Negro) implementando iconos vectoriales, y se actualizaron los contenidos.
*   **Conservados y actualizados:** Salud y Bienestar, Educación y Cultura (Enredos de Película / ClicSeguroen RED), Derechos, Medio ambiente (Podcast de Marta / Conferencias / Homenaje).
*   **Eliminados:** Políticas y Feminismos.

### Sidebar (Barra Lateral Derecha)
*   Se redujo considerablemente el tamaño visual del **Código QR**.
*   El antiguo botón de WhatsApp se reemplazó por un **Botón "DONAR"** gigante y colorido para fomentar el apoyo financiero.
*   Se renombró "Publicaciones Populares" a **"NOVEDADES"** para mostrar agendas de eventos dinámicos.

### Revista Colaborativa
Se sacó la revista colaborativa de la barra lateral (donde perdía relevancia) y se ubicó en un **banner horizontal enorme e ineludible** justo debajo de la Hero Section, con fondo cálido en gradiente.

### Propuestas y Recursos
*   Se listaron las propuestas acompañadas de **iconos grandes/emojis** representativos.
*   Los "Recursos destacados" se organizaron en tarjetas apilables adaptativas (sin requerir scroll horizontal escondido).
*   Se agregaron botones directos y explícitos para enlaces externos: *ENLACE A LIC TIPS, ENLACE A LAS GRABACIONES, ENLACE A DRIVE CON MATERIAL*.
