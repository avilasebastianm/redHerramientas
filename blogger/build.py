#!/usr/bin/env python3
"""Arma el tema de Blogger y las páginas a partir de la propuesta (index.html, donar.html, styles.css, script.js).

Uso:  python3 blogger/build.py
Genera:
  blogger/tema-redherramientas.xml   -> Tema > Restaurar
  blogger/paginas/donar.html         -> contenido (vista HTML) de la página Donar
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

# Direcciones de las páginas estáticas en Blogger
CONTACT_URL = '/p/contactanos.html'   # la página que ya existe
DONATE_URL = '/p/donar.html'          # página nueva "Donar"
# Fotos de la asociación (ejes y donar): en el repo están en img/; en Blogger se usan subidas a Blogger.
# Las que no figuran acá se buscan en IMG_BASE.
IMG_BASE = 'https://avilasebastianm.github.io/redHerramientas/img/'
IMG_URLS = {
    'eje-salud.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgepdFDsnI33_i8xqUtXURDEo3wfPdCoROejuVIq3HcCSBxE-DgtCm9CPrxyZrwOYz14Ak7ebHifQWVb3Yk3YxQD9BMTGq9mfo61rpjVdK_3mmuz242Umgkxx1yB16UFwGJt65ZSb3atnIWacG0HD2OnMdCof-2YaDeQPNFei-OpmLKChDipWhCWAef3LsG/s1600/eje-salud.jpg',
    'eje-educacion.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi5Low7BJMOSvqLN3bFaIEOIdKM_cxrPLv_fybUhGjBhJ9KghK0JkcGvMk_g8NWGtTgI0RBlEUpxjz-GYZya7flGPF7mefBroZJvg_2auFzMkT2XReeEEva1oyaNlJ2OCkHjca-3PkdAapw3dhGSt7pjHgbXwM1ZYoDUP3BqHgcTSLb23YZg1r4c4Wi60_E/s1600/eje-educacion.jpg',
    'eje-derechos.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjHcx4PSIHGOwxS5dFRWcwKZfrSC0bBWHXawJoRw9Fwzh9HcB7bnrI3FnOIoJhAV3xH84Vw2sonirr6PdjVHSv_CuWK2NA94zH-vvq0kd-UJk-sWYXkNpeOVCicdlFCt0nAg3_MHjHNyA4JeFHiaGa8tNfm5ea2Vy0Qoo2CB6kahbydTa528yJEkhmhDyS3/s1600/eje-derechos.jpg',
    'eje-ambiente.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEih_QoOzoSeyd-E46cWtOK3CPHR-w-m1Dp2MHkco26ANu_6-DaW_BB5fRHa2sD8c_gnvq1v3_vLjN2SuYa6qrXS2kBcLeDm8EgoUNBv2h0eyKdNtpQchqs-yHjIBWN1x-uxFAvcQo0JJCPZCyRVY_PTLOe73Rs3er3vPy-c8Yr-ldfUYpImMSmQsODFJXbE/s1600/eje-ambiente.jpg',
    'donar-grande.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiOCFGD7S01qqv9ndWV-k7XrYf4Xkr5oG_vWNatxhegqr2p1GBlguF9ATXBLqcmItMqiRx8fA5R0AKGCvXxj3Qbzn6c-xMEljGfCpbpQNdHmAiifsXifWjXv2XS9rU0EM67Rf3v61PUR4_pQ5IjhBTmh861k6eWriDxbotir7uXsfmcs9O1ezHOXQTNmmsG/s1600/donar-grande.jpg',
    'donar-chica-1.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiGLvIWlCxa4NTgGVuKVIu1ku_oyIdONL8hHy5rkX8WOpF3-fYu_C-YjI36DqSP49LWX47J09a3JWffyLWjYOfIsFtl-j_s6LJSNZsXZQkJTl_g-NR0l2WChjZ20fDONF76JvQ6PGoJbWCo5GAG4c6q0ozyk_cWtBIKU0XOzw7frRh6hFSqpXuZXh1pSId0/s1600/donar-chica-1.jpg',
    'donar-chica-2.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEggKl4inwo2hN_WbCH00NuAFEGpMIVC9MqzaIxMJ06gG3gkplwjoxVYgKRGVRHIFK4k1bWmjL0UO05uIBg8UIwtDEKXAOUFHmLfkgQNKQSJfFhRgNwW759o4asow7ie9uakxNrpyLMTaj7rnaFPOz6y3fUfZNw_tcaO5pdYbIi2zlyf2TETcgyhpbZv7pRg/s1600/donar-chica-2.jpg',
    'logo-footer.png': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEi1TZxdMT9YyUobCUsrSHSgpW8h6s1omzuROFh6avuOlmNQQ9eHlFnKTYRbexceLMMZ5JTei6O0w7qrdeB2vaILv5asvw4E73NXggPYD8sCXkHypNVN7TToyDAg8UMRevUBLq3VebPydnJtyzD9bKEr5jJDp5cN1pAb9N_bw4O2QjVk_sahxskfvS-eYIzL/s1600/logo-footer.png',
}
# Logo del encabezado (en la propuesta está en imgur). También es la imagen de las notas sin foto.
LOGO_IMGUR = 'https://i.imgur.com/CFM0Pcr.png'
LOGO_URL = 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiEG2E3H7aF-xvhpflHXcxgPxlbUGH3i8kP4CI1egOK_waREN5tY67vnWT1vIgKcEOhnXPxfa0auVp_W9zI4XD5oLK1xtyJyf4-Q8C6jpPR_86h2BpawEDBwzKIKfll87hGYLQgE3n4TQ_GTSnj0rLGvuqDs6cg8EVrYvlyov-hTKmSkwt0goKB1NzKpv2e/s1600/logo-header.png'


def read(name):
    return (ROOT / name).read_text(encoding='utf-8')


def between(text, start, end):
    i = text.index(start)
    j = text.index(end, i)
    return text[i:j]


def links(s):
    """Adapta los links de la propuesta a las direcciones de Blogger."""
    s = s.replace('href="index.html"', 'href="/"').replace('href="index.html#', 'href="/#')
    for anchor in ('quienes-somos', 'actividades'):
        s = s.replace('href="#%s"' % anchor, 'href="/#%s"' % anchor)
    s = s.replace('href="contacto.html"', 'href="%s"' % CONTACT_URL)
    s = s.replace('href="donar.html"', 'href="%s"' % DONATE_URL)
    for name, url in IMG_URLS.items():
        assert url, 'falta la URL de ' + name
        s = s.replace('img/' + name, url)
    s = s.replace('src="img/', 'src="' + IMG_BASE)
    s = s.replace(LOGO_IMGUR, LOGO_URL)
    # Links al blog sin dominio, así funcionan igual en el blog de pruebas y en producción
    s = s.replace('href="https://www.redherramientas.com/', 'href="/')
    s = s.replace('action="https://www.redherramientas.com/', 'action="/')
    return s


def xhtml(s):
    """HTML -> XHTML para las partes fijas del tema (Blogger exige XML bien formado)."""
    s = s.replace('&times;', '&#215;')
    s = re.sub(r'&(?!(amp|lt|gt|quot|apos|#\d+);)', '&amp;', s)

    def fix_tag(m):
        tag = m.group(0)
        if tag.startswith('<!--') or tag.startswith('</'):
            return tag
        tag = re.sub(r'\s(hidden|required|novalidate|disabled)(?=[\s>/])', r' \1="\1"', tag)
        if re.match(r'<(img|input|br|meta|link|hr|source)\b', tag) and not tag.endswith('/>'):
            tag = tag[:-1].rstrip() + '/>'
        return tag

    return re.sub(r'<!--.*?-->|<[^>]+>', fix_tag, s, flags=re.S)


def cdata(s):
    assert ']]>' not in s
    return '<![CDATA[' + s + ']]>'


index = read('index.html')
donar = read('donar.html')

# ---------- Partes de la home ----------
header = xhtml(links(between(index, '<header class="header">', '</header>') + '</header>'))
carousel = xhtml(between(index, '    <!-- Carrusel de actividades', '    <!-- Mini sección Quiénes somos'))
about = links(between(index, '    <!-- Mini sección Quiénes somos', '    <!-- Nuestros ejes'))
ejes = links(between(index, '    <!-- Nuestros ejes', '    <div class="container">\n      <div class="separator">'))
middle = between(index, '    <div class="container">\n      <div class="separator">', '    <!-- Llamado a la página de contacto')
# novedades y donar: cada uno con su barra separadora
chunks = middle.split('<div class="separator"></div>')[1:]
chunks[-1] = chunks[-1].rsplit('</div>', 1)[0]  # cierre del .container
blocks = [links('      <div class="separator"></div>' + c.rstrip() + '\n') for c in chunks]
contact_cta = xhtml(links(between(index, '    <!-- Llamado a la página de contacto', '  </main>')))
footer = xhtml(links(between(index, '  <footer class="footer">', '  <script')))

# Gadgets editables desde Diseño (ids altos para no pisar los gadgets del tema anterior)
home_widgets = [
    ('home-quienes', 'HTML101', 'Quiénes somos', about),
    ('home-ejes', 'HTML102', 'Nuestros ejes', ejes),
]
home_container_widgets = [
    ('HTML105', 'Novedades', blocks[0]),
    ('HTML106', 'Apoyá nuestro espacio (Donar)', blocks[1]),
]


def html_widget(wid, title, content):
    return f"""<b:widget id='{wid}' locked='false' title='{title}' type='HTML' version='2' visible='true'>
  <b:widget-settings>
    <b:widget-setting name='content'>{cdata(content)}</b:widget-setting>
  </b:widget-settings>
  <b:includable id='main'><data:content/></b:includable>
</b:widget>"""


home_html = ''
for sid, wid, title, content in home_widgets:
    home_html += f"<b:section class='home-section' id='{sid}' maxwidgets='1' showaddelement='no'>\n{html_widget(wid, title, content)}\n</b:section>\n"
home_html += "<div class='container'>\n<b:section class='home-section' id='home-contenido' showaddelement='yes'>\n"
home_html += '\n'.join(html_widget(w, t, c) for w, t, c in home_container_widgets)
home_html += "\n</b:section>\n</div>\n"

# ---------- Posteos, etiquetas y búsquedas ----------
blog_widget = """<b:section class='main' id='main' maxwidgets='1' showaddelement='no'>
<b:widget id='Blog1' locked='true' title='Entradas del blog' type='Blog' version='2' visible='true'>
<b:includable id='main' var='this'>
  <b:if cond='data:view.isSingleItem'>
    <b:loop values='data:posts' var='post'>
      <b:if cond='data:view.isPage and (data:post.body contains &quot;rh-full&quot;)'>
        <!-- Páginas armadas con el diseño del sitio (Contacto, Donar): van completas -->
        <data:post.body/>
      <b:else/>
        <!-- Notas y páginas: diseño editorial. La primera foto y el primer párrafo (bajada) los acomoda script.js -->
        <article class='art'>
          <nav aria-label='Ubicación' class='art-crumbs'>
            <a expr:href='data:blog.homepageUrl'>Inicio</a>
            <b:with value='data:post.labels first (l =&gt; l.name != &quot;Carrusel&quot; and l.name != &quot;Novedades&quot;)' var='tema'><b:if cond='data:tema'><span aria-hidden='true'>/</span><a class='art-section' expr:href='data:tema.url'><data:tema.name/></a></b:if></b:with>
          </nav>
          <h1 class='art-title'><b:eval expr='data:post.title ? data:post.title : &quot;Sin título&quot;'/></h1>
          <p class='art-bajada' hidden='hidden'/>
          <div class='art-meta'>
            <div class='art-byline'>
              <span aria-hidden='true' class='art-avatar'>RH</span>
              <div><strong>Red de Herramientas</strong><small><b:if cond='data:view.isPost'><data:post.date/> &#183; </b:if><span class='art-lectura'/></small></div>
            </div>
            <div class='art-share'>
              <a aria-label='Compartir por WhatsApp' class='share-icon wa' data-share='wa' expr:href='&quot;https://wa.me/?text=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z'/></svg></a>
              <a aria-label='Compartir en Facebook' class='share-icon fb' data-share='fb' expr:href='&quot;https://www.facebook.com/sharer.php?u=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M13.4 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.8v3h2.5V21z'/></svg></a>
              <button aria-label='Copiar enlace' class='share-icon copy' data-share='copy' type='button'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M3.9 12a3.1 3.1 0 0 1 3.1-3.1h4V7H7a5 5 0 0 0 0 10h4v-1.9H7A3.1 3.1 0 0 1 3.9 12zM8 13h8v-2H8v2zm9-6h-4v1.9h4a3.1 3.1 0 0 1 0 6.2h-4V17h4a5 5 0 0 0 0-10z'/></svg></button>
            </div>
          </div>
          <figure class='art-hero' hidden='hidden'/>
          <div class='post-body art-body'><data:post.body/></div>
          <b:if cond='data:post.labels any (l =&gt; l.name != &quot;Carrusel&quot; and l.name != &quot;Novedades&quot;)'>
            <div class='art-tags'>Temas: <b:loop values='data:post.labels where (l =&gt; l.name != &quot;Carrusel&quot; and l.name != &quot;Novedades&quot;)' var='label'><a expr:href='data:label.url'><data:label.name/></a></b:loop></div>
          </b:if>
          <div class='art-share-box'>
            <h2>&#191;Te sirvió esta nota? Compartila</h2>
            <div class='btns'>
              <a class='share-big wa' data-share='wa' expr:href='&quot;https://wa.me/?text=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z'/></svg>WhatsApp</a>
              <a class='share-big fb' data-share='fb' expr:href='&quot;https://www.facebook.com/sharer.php?u=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M13.4 21v-7.5h2.5l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.8 1.4-3.8 3.9v2.3H7.8v3h2.5V21z'/></svg>Facebook</a>
              <button class='share-big copy' data-share='copy' type='button'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M3.9 12a3.1 3.1 0 0 1 3.1-3.1h4V7H7a5 5 0 0 0 0 10h4v-1.9H7A3.1 3.1 0 0 1 3.9 12zM8 13h8v-2H8v2zm9-6h-4v1.9h4a3.1 3.1 0 0 1 0 6.2h-4V17h4a5 5 0 0 0 0-10z'/></svg><span class='label'>Copiar enlace</span></button>
            </div>
          </div>
          <b:with value='data:post.labels first (l =&gt; l.name != &quot;Carrusel&quot; and l.name != &quot;Novedades&quot;)' var='tema'><b:if cond='data:tema'>
            <section class='art-related' expr:data-label='data:tema.name' hidden='hidden'>
              <h2 class='block-title'>Seguí leyendo</h2>
              <div class='rel-grid'/>
            </section>
          </b:if></b:with>
        </article>
      </b:if>
    </b:loop>
  <b:elseif cond='!data:view.isHomepage'/>
    <section class='list-page'>
      <div class='container'>
        <h1 class='section-title list-title'>
          <b:if cond='data:view.search.label'><data:view.search.label/>
          <b:elseif cond='data:view.search.query'/>Resultados para &#8220;<data:view.search.query/>&#8221;
          <b:elseif cond='data:view.isArchive'/><data:view.archive.rangeMessage/>
          <b:else/>Publicaciones</b:if>
        </h1>
        <b:if cond='data:posts.empty'><p class='list-empty'>No encontramos publicaciones.</p></b:if>
        <div class='post-grid'>
          <b:loop values='data:posts' var='post'>
            <a class='post-card' expr:href='data:post.url'>
              <div class='post-card-img'>
                <b:if cond='data:post.featuredImage'>
                  <img expr:alt='data:post.title' expr:src='resizeImage(data:post.featuredImage, 640, &quot;4:3&quot;)' loading='lazy'/>
                <b:else/>
                  <img alt='' class='no-img' src='https://i.imgur.com/CFM0Pcr.png'/>
                </b:if>
              </div>
              <div class='post-card-body'>
                <b:with value='data:post.labels first (l =&gt; l.name != &quot;Carrusel&quot; and l.name != &quot;Novedades&quot;)' var='tema'><b:if cond='data:tema'><span class='chip-label'><data:tema.name/></span></b:if></b:with>
                <h2><b:eval expr='data:post.title ? data:post.title : &quot;Sin título&quot;'/></h2>
                <p class='post-card-date'><data:post.date/></p>
                <p class='post-card-snippet'><data:post.snippets.short/></p>
                <span class='post-card-more'>Leer más &#8594;</span>
              </div>
            </a>
          </b:loop>
        </div>
        <nav aria-label='Más publicaciones' class='pager'>
          <b:if cond='data:newerPageUrl'><a class='btn btn-light' expr:href='data:newerPageUrl'>&#8592; Más nuevas</a></b:if>
          <b:if cond='data:olderPageUrl'><a class='btn' expr:href='data:olderPageUrl'>Más antiguas &#8594;</a></b:if>
        </nav>
      </div>
    </section>
  </b:if>
</b:includable>
</b:widget>
</b:section>"""

# ---------- Columna de las notas: lo más leído y llamado a sumarse ----------
aside_cta = """<div class="aside-card aside-cta">
  <h2>¿Querés sumarte?</h2>
  <p>Talleres, encuentros y actividades para mujeres mayores. Escribinos y te contamos.</p>
  <a class="share-big" href="https://wa.me/5491122766776" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>Escribinos</a>
</div>"""

popular_widget = """<b:widget id='PopularPosts1' locked='false' title='Lo más leído' type='PopularPosts' version='2' visible='true'>
<b:widget-settings>
  <b:widget-setting name='numItemsToShow'>5</b:widget-setting>
  <b:widget-setting name='showThumbnails'>true</b:widget-setting>
  <b:widget-setting name='showSnippets'>false</b:widget-setting>
  <b:widget-setting name='timeRange'>ALL_TIME</b:widget-setting>
</b:widget-settings>
<b:includable id='main' var='this'>
  <b:if cond='data:view.isSingleItem and !data:posts.empty'>
    <div class='aside-card'>
      <h2 class='block-title'><data:title/></h2>
      <ol class='mas-leido'>
        <b:loop values='data:posts' var='post'>
          <li><a expr:href='data:post.url'>
            <span><data:post.title/></span>
            <b:if cond='data:post.featuredImage'>
              <img alt='' expr:src='resizeImage(data:post.featuredImage, 144, &quot;1:1&quot;)' loading='lazy'/>
            <b:else/>
              <img alt='' src='https://i.imgur.com/CFM0Pcr.png' style='object-fit:contain'/>
            </b:if>
          </a></li>
        </b:loop>
      </ol>
    </div>
  </b:if>
</b:includable>
</b:widget>"""

# En notas y páginas, el contenido va al lado de la columna; en el resto, la columna queda vacía
blog_layout = f"""<div expr:class='data:view.isSingleItem ? &quot;post-layout container&quot; : &quot;&quot;'>
{blog_widget}
<aside class='post-aside' aria-label='Recomendados'>
<b:section class='aside-section' id='lateral' showaddelement='yes'>
{popular_widget}
{html_widget('HTML110', 'Sumate (columna de las notas)', aside_cta)}
</b:section>
</aside>
</div>"""

css = read('styles.css') + '\n' + (OUT / 'blogger.css').read_text(encoding='utf-8')
js = read('script.js')
assert '</script' not in js and ']]>' not in js and ']]>' not in css

theme = f"""<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE html>
<!-- Tema de Red de Herramientas Entre Mujeres. Generado con blogger/build.py: no editar a mano. -->
<html b:css='false' b:defaultwidgetversion='2' b:layoutsVersion='3' b:responsive='true' b:templateVersion='1.0.0' expr:dir='data:blog.languageDirection' lang='es-AR' xmlns='http://www.w3.org/1999/xhtml' xmlns:b='http://www.google.com/2005/gml/b' xmlns:data='http://www.google.com/2005/gml/data' xmlns:expr='http://www.google.com/2005/gml/expr'>
<head>
<meta content='width=device-width, initial-scale=1' name='viewport'/>
<b:include data='blog' name='all-head-content'/>
<title><b:if cond='data:view.isHomepage'><data:blog.title.escaped/><b:else/><data:view.title.escaped/> | <data:blog.title.escaped/></b:if></title>
<link href='https://fonts.googleapis.com' rel='preconnect'/>
<link href='https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,500&amp;family=Roboto:wght@400;500;600;700;900&amp;display=swap' rel='stylesheet'/>
<b:skin version='1.0.0'><![CDATA[/* Los estilos están en el <style> de abajo */]]></b:skin>
<b:template-skin><![CDATA[
body#layout .carousel, body#layout .to-top {{ display: none; }}
body#layout .header {{ position: static; }}
body#layout .rh-descartados {{ display: block !important; }}
body#layout .rh-descartados::before {{ content: 'Gadgets del tema anterior: no se ven en el sitio. Se pueden borrar.'; display: block; padding: 8px; font-weight: bold; }}
]]></b:template-skin>
<style>/*<![CDATA[*/
{css}
/*]]>*/</style>
</head>
<body>
<!-- Al subir el tema, Blogger manda los gadgets del tema anterior a la primera sección que acepta gadgets: esta, que no se ve en el sitio. Se borran desde Diseño -->
<div class='rh-descartados'>
<b:section id='descartados' showaddelement='yes'/>
</div>
<a class='skip' href='#contenido'>Saltar al contenido</a>

{header}

<main id='contenido'>
<b:if cond='data:view.isHomepage'>
{carousel}
{home_html}
</b:if>

{blog_layout}

<b:if cond='data:view.isHomepage'>
{contact_cta}
</b:if>
</main>

{footer}

<script>//<![CDATA[
{js}
//]]></script>
</body>
</html>
"""

# El tema tiene que ser XML válido o Blogger lo rechaza
ET.fromstring(theme.split('\n', 1)[1].replace('<!DOCTYPE html>', '', 1).encode('utf-8'))
theme = theme.replace(LOGO_IMGUR, LOGO_URL)
(OUT / 'tema-redherramientas.xml').write_text(theme, encoding='utf-8')

# ---------- Páginas estáticas ----------
pages = OUT / 'paginas'
pages.mkdir(exist_ok=True)
# paginas/contacto.html no se genera: es la página que armó Lucas en Blogger (con sus propios estilos)
donate_body = between(donar, '  <main id="contenido">', '  <footer').replace('  <main id="contenido">', '', 1).replace('  </main>\n', '', 1)
(pages / 'donar.html').write_text('<div class="rh-full">\n' + links(donate_body) + '</div>\n', encoding='utf-8')

print('Listo:', (OUT / 'tema-redherramientas.xml').relative_to(ROOT), '+', ', '.join(str(p.relative_to(ROOT)) for p in sorted(pages.iterdir())))
