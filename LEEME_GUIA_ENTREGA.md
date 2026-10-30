# PROYECTO: DISEÑO WEB CON PHOTOSHOP (MOCKUP 1000x2000 PX)
## "DBA TECHSTORE" - TIENDA DE TECNOLOGÍA & GADGETS PREMIUM

Este proyecto ha sido desarrollado siguiendo rigurosamente las pautas de la actividad académica de **Diseño Web con Photoshop (Mockups)**. Cumple con todos los criterios de composición, tipografía, degradados sutiles, zonas interactivas, elementos vectoriales, jerarquía visual y organización profesional de capas en Photoshop.

---

### 📁 ARCHIVOS ENTREGABLES EN ESTA CARPETA

1. **`TechStore_Mockup_1000x2000.psd`**
   - Archivo editable nativo de Photoshop en resolución exacta de **1000 x 2000 px**.
   - Posee todas las capas organizadas y agrupadas en carpetas temáticas para que el docente/evaluador revise el orden.
2. **`mockup_preview_1000x2000.png`**
   - Vista previa renderizada a resolución completa 1:1 (1000x2000 px).
3. **`index.html`**, **`styles.css`**, **`script.js`**
   - Maquetación web exportable e interactiva que replica exactamente el diseño con zonas interactivas reales, contador en vivo, filtros de productos, carrito dinámico e inspector de sectores de Photoshop (Slices).
4. **`LEEME_GUIA_ENTREGA.md`**
   - Esta memoria explicativa del proyecto y guía paso a paso de sustentación.

---

### 🎯 CUMPLIMIENTO DETALLADO DE LA RÚBRICA DE EVALUACIÓN

| Criterio Evaluado | Implementación en el Mockup DBA TechStore |
| :--- | :--- |
| **Resolución y Formato** | **1000 x 2000 px** en formato nativo **PSD** con capas y exportable a **HTML**. |
| **Menú Superior** | Menú horizontal fijo (*Header Glassmorphism*) con opciones claras: *Inicio* (estado activo con indicador cian), *Productos*, *Ofertas* (con insignia roja "HOT"), *Beneficios*, *Soporte*, *Contacto*, buscador, carrito con badge y perfil de usuario. |
| **Banner Principal** | Banner Hero con dispositivo de alta gama (Auriculares Inalámbricos Studio Ultra), con iluminación radial azul/cian, tag de lanzamiento 2026, titular impactante, bajada descriptiva, chips de especificaciones y botones de acción. |
| **Degradaciones (Gradients)** | Degradados sutiles y elegantes: desde el fondo oscuro obsidiana (`#070B14` a `#0E1726`), resplandor radial neón (`#0066FF` a `#00D2FF`) detrás del gadget, hasta los degradados lineales luminosos en los botones CTA interactivos. |
| **Tipografía y Jerarquía** | Uso de familia tipográfica sans-serif moderna, geométrica y de máxima legibilidad en pantallas (`Segoe UI` / `Plus Jakarta Sans`):<br>• Título Hero: 38-42 pt Bold<br>• Títulos de sección: 22-24 pt Bold<br>• Títulos de productos: 16 pt Bold<br>• Textos descriptivos: 11-14 pt Regular<br>• Micro-etiquetas / Badges: 9-10 pt Bold uppercase. |
| **Composición y Simetría** | Retícula simétrica estructurada: distribución equilibrada de 4 columnas en Beneficios, 3 columnas homogéneas en Productos, 2 columnas en Testimonios y 4 columnas en el Footer. |
| **Vectores y Contenido Ilustrado** | Iconografía vectorial y geométrica personalizada:<br>1. *Envío Express*: Camión con líneas de velocidad.<br>2. *Garantía 2 Años*: Escudo con checkmark.<br>3. *Pago Seguro*: Candado con cilindro de seguridad.<br>4. *Soporte 24/7*: Diadema de audio con micrófono.<br>5. Modelado visual de gadgets: Smartwatch con dial AMOLED, Auriculares inalámbricos en estuche Qi y Teclado mecánico RGB. |
| **Zonas Interactivas** | **Múltiples estados interactivos implementados:**<br>1. Botón principal *"COMPRAR AHORA $249.99 ➔"* con estado hover/click.<br>2. Botones *"Añadir al Carrito"* con respuesta visual inmediata.<br>3. Formulario interactivo con campo de texto y botón *"CANJEAR CUPÓN AHORA"*, acompañado de un contador regresivo de tiempo real (*08h : 42m : 19s*).<br>4. Pestañas de filtrado de productos por categorías. |
| **Uso Apropiado de Capas** | Estructura jerárquica limpia con carpetas nombradas cronológica y funcionalmente: `01_HEADER`, `02_BANNER_HERO`, `03_BENEFICIOS_VECTORES`, `04_PRODUCTOS_DESTACADOS`, `05_ZONA_INTERACTIVA_PROMO`, `06_TESTIMONIOS`, `07_FOOTER`, `00_FONDO_GLOBAL`. |

---

### 🗂️ ESTRUCTURA DE CAPAS EN EL ARCHIVO PSD

Al abrir **`TechStore_Mockup_1000x2000.psd`** en Adobe Photoshop o Photopea, encontrarás esta organización:

```text
📁 01_HEADER
   ├── 📄 Iconos_Acciones_Usuario (Buscador, Carrito con badge 3, Avatar)
   ├── 📄 Menu_Navegacion_Interactivo (Inicio, Productos, Ofertas, Soporte...)
   ├── 📄 Logo_DBA_TechStore (Isotipo hexagonal + Tipografía corporativa)
   └── 📄 Fondo_Header_Glassmorphism (Barra oscura translúcida con borde cian)

📁 02_BANNER_HERO
   ├── 📄 Botones_CTA_Hero_Interactivo (Botón Comprar Ahora + Ver Specs)
   ├── 📄 Textos_Titulos_Hero (Tag Lanzamiento, Titular 8D, Bajada y Chips)
   ├── 📄 Ilustracion_Gadget_Headphones (Auriculares Studio con reflejos)
   └── 📄 Resplandor_Neon_Hero (Degradado radial azul y cian)

📁 03_BENEFICIOS_VECTORES
   ├── 📄 Iconos_Vectores_Hexagonos (4 vectores: Camión, Escudo, Candado, Diadema)
   ├── 📄 Textos_Beneficios (Títulos y descripciones de valor)
   └── 📄 Tarjetas_Base_Beneficios (Contenedores con bordes redondeados)

📁 04_PRODUCTOS_DESTACADOS
   ├── 📄 Tarjeta_Producto_01_Apex (Smartwatch AMOLED + Precio + Botón)
   ├── 📄 Tarjeta_Producto_02_Nova (Earbuds inalámbricos + Precio + Botón)
   ├── 📄 Tarjeta_Producto_03_CyberMech (Teclado Gamer RGB + Precio + Botón)
   └── 📄 Encabezado_y_Filtros_Productos (Titular + Filtros: Todos, Audio...)

📁 05_ZONA_INTERACTIVA_PROMO
   └── 📄 Caja_Oferta_Flash_y_Formulario_Interactivo (Contador + Formulario)

📁 06_TESTIMONIOS
   └── 📄 Tarjetas_Testimonios_Comunidad (2 reseñas con avatares y estrellas)

📁 07_FOOTER
   └── 📄 Contenido_Footer_Completo (Logo, columnas, pagos, redes y copyright)

📁 00_FONDO_GLOBAL
   └── 📄 Malla_Fondo_Oscura_Tech (Degradado vertical y viñeta ambiente)
```

---

### 🌐 CÓMO EXPORTAR A HTML DESDE ADOBE PHOTOSHOP (MÉTODO SECTORES / SLICES)

Si en clase te piden explicar cómo Photoshop exporta un mockup a HTML:
1. Abre el archivo `TechStore_Mockup_1000x2000.psd` en **Adobe Photoshop**.
2. Selecciona la herramienta **Sector (Slice Tool)** presionando la tecla `C` o `Shift + C`.
3. Puedes crear sectores para cada sección (`01_header`, `02_hero`, `03_benefits`, `04_products`, `05_promo`, `06_testimonials`, `07_footer`).
4. Ve al menú superior: **Archivo > Exportar > Guardar para Web (Heredado)...** (atajo: `Ctrl + Alt + Shift + S`).
5. En formato selecciona **PNG-24** o **JPEG Máxima**.
6. En la parte inferior, en la opción **Formato de exportación**, elige **"HTML e imágenes"**.
7. Haz clic en **Guardar**. Photoshop generará automáticamente una página HTML y una carpeta con los recortes (`images/`).
8. También puedes abrir directamente nuestro archivo **`index.html`** incluido en esta entrega, pulsar el botón superior **"Alternar Sectores (Slices)"** y verás proyectada la cuadrícula exacta de sectores de Photoshop en vivo.
