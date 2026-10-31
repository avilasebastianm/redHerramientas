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
IMG_BASE = 'https://avilasebastianm.github.io/redHerramientaslucas/img/'
IMG_URLS = {
    'eje-salud.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgwTggGgg6RwR_EEwx8UwvlFIhKgOqRW5K-JmMrqWYi3uaKwtKVp3Wm0e1XP8dub5s0-Lx11s1VcWYQTpn9tneABCHqkag91JEKpphWRa7B0VY2ca7WTIZ0I4DUS76oscEWVtHEWEuxYXoXEDW6PMGkO4NDoD-d5sZ4q0a3yjjQy1LObHXFZqhU3IcxjuM/s1600/eje-salud.jpg',
    'eje-educacion.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEirHuX3S_j-FN_O2caq88egGcpyXyFyUWrPr7dSKBgaYbBQwfOgUQkIk_FGyRFp_JMi_L1QdcfTtLMrcNN-iY29M90_ZrYAUuyTB-wIR164oGInNZXHSx3lzrjjrnWS38E_Ag_GJsPy3YuIeXm8rO9Gdnf0f8KZ9dz_O7RxA_kTeWrR0EDSfBfAi6kp1fI/s1600/eje-educacion.jpg',
    'eje-derechos.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhcdPWEbSj9Y9JbonZZJaSRPbWVz2V17xNES6TMw70yaE7xUxGXpFP-vVf-vtq58zGWnXkBBBsIAn-A6DSaQcgKsn7NwIIA75T7ltukSdSnvDMpwDNvN7squZKjdovuRkWDBwHjZuqYSwkQvvkteHhkPjSV8kKSfvZGyzTIqGcTfOPaA6S_QXsBvFV5YOk/s1600/eje-derechos.jpg',
    'eje-ambiente.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhubcac_kZPG96ARw1F2VjoZ1uH8c4B9W3DdVskMgV5qj9EMrigmpOO6_-lV13nkdGIConSVq5l-Nw5HuIs4Kb9mHrPSOrt6Eyy7avZirtnR6KhvBVy5kI_yGdrmDEOETdZv5jQNbG-kq-KJhwM6zPn2sN4XVRlVmXD4Qm_S5Drv6qJ8pvLCdk00PaJh2E/s1600/eje-ambiente.jpg',
    'donar-grande.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEheQehahNzg2ayXj1M-KjRJ3S2ZS_P-3QjYaKkZYZ7yO7zLXGW74LU6RnNQFsldTXrptCkj6Wkrvbpo5HZtUtJ2fP9WqJ9EBY9oSyHkU2w2paeTlgL008yPt-28cvmBVswSvmgz0fvFgicjpxDZ24o2nhBK012YG_HIiquj1IOAuEP2vZzzacwO3H8qfkQ/s1600/donar-grande.jpg',
    'donar-chica-1.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjVI7Lmp9WvHr7WPLaeQMyST1f0p0VC5lFuJzMXYJnE5847sgZGfViUrpzMWkvNTjeLyM3u5E0KU9BO8CbTNTuRbOUur6wPLwKzOJ9qqSy_4SJkbk-yCAug6CkfMItYaNzdigVpb80FkV_9aHUnmYE0LBT82-sy_Ah5IujtV189q8H8v8y-HAIFYwB-fZM/s1600/donar-chica-1.jpg',
    'donar-chica-2.jpg': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEicV5j3PS-m5k1pfhXXADBQgN2syo9cmc_IH7DDNn2KtJXJqXMd0w2tFGgku04zIkwi1NP5FTjw-BGCxq4_DdajBMZTqvbpkGVDEdluzY2iNckqUTxGlaBaZLad91uVRduhyux7qXk2W-RD6QMXS5gSYRr3Y-oDoXw9YOjJvyYFIJYUJZ6y9GU-9JBJL_A/s1600/donar-chica-2.jpg',
    'logo-footer.png': 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgbxEmeatlpRVtwtQEmVQltrVh7KdvhL7OI2DDGpo_L45WIZ9V8Nj_2h0sHVHIi7NHKU9O1hfG-xV5xPtVWhIFRGiJ59XqZU3anOgP7dIFYq6PCSn-KO21g2QMOu8LP2BZ0iEFkTsNoVcNTts1PcNwC7suhpmpeSecOcY7vQ6m2T-iMgBOZzVroZu9I5wI/s1600/logo-footer.png',
}


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
              <a aria-label='Compartir por WhatsApp' class='share-icon wa' data-share='wa' expr:href='&quot;https://wa.me/?text=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.38A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 15l-.3-.2-3.1.8.83-3-.2-.32A8.1 8.1 0 0 1 12.04 3.8zM8.6 7.5c-.2 0-.5.07-.75.35-.25.27-1 1-1 2.4s1.03 2.8 1.17 3c.15.2 2 3.2 4.9 4.36 2.4.95 2.9.76 3.4.72.52-.05 1.7-.7 1.93-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.2-.55-.34-.3-.15-1.7-.84-1.96-.94-.27-.1-.46-.15-.65.14-.2.3-.75.94-.9 1.13-.17.2-.33.22-.62.07-.3-.14-1.2-.44-2.3-1.4-.85-.76-1.42-1.7-1.6-1.98-.16-.3 0-.45.13-.6.14-.13.3-.34.44-.5.15-.17.2-.3.3-.5.1-.2.05-.36-.02-.5-.07-.15-.65-1.6-.9-2.17-.23-.55-.47-.48-.65-.49h-.55z'/></svg></a>
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
              <a class='share-big wa' data-share='wa' expr:href='&quot;https://wa.me/?text=&quot; + data:post.url.canonical' rel='noopener' target='_blank'><svg aria-hidden='true' viewBox='0 0 24 24'><path d='M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.38A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 15l-.3-.2-3.1.8.83-3-.2-.32A8.1 8.1 0 0 1 12.04 3.8zM8.6 7.5c-.2 0-.5.07-.75.35-.25.27-1 1-1 2.4s1.03 2.8 1.17 3c.15.2 2 3.2 4.9 4.36 2.4.95 2.9.76 3.4.72.52-.05 1.7-.7 1.93-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.2-.55-.34-.3-.15-1.7-.84-1.96-.94-.27-.1-.46-.15-.65.14-.2.3-.75.94-.9 1.13-.17.2-.33.22-.62.07-.3-.14-1.2-.44-2.3-1.4-.85-.76-1.42-1.7-1.6-1.98-.16-.3 0-.45.13-.6.14-.13.3-.34.44-.5.15-.17.2-.3.3-.5.1-.2.05-.36-.02-.5-.07-.15-.65-1.6-.9-2.17-.23-.55-.47-.48-.65-.49h-.55z'/></svg>WhatsApp</a>
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
  <a class="share-big" href="https://wa.me/5491122766776" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.38A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 15l-.3-.2-3.1.8.83-3-.2-.32A8.1 8.1 0 0 1 12.04 3.8zM8.6 7.5c-.2 0-.5.07-.75.35-.25.27-1 1-1 2.4s1.03 2.8 1.17 3c.15.2 2 3.2 4.9 4.36 2.4.95 2.9.76 3.4.72.52-.05 1.7-.7 1.93-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.2-.55-.34-.3-.15-1.7-.84-1.96-.94-.27-.1-.46-.15-.65.14-.2.3-.75.94-.9 1.13-.17.2-.33.22-.62.07-.3-.14-1.2-.44-2.3-1.4-.85-.76-1.42-1.7-1.6-1.98-.16-.3 0-.45.13-.6.14-.13.3-.34.44-.5.15-.17.2-.3.3-.5.1-.2.05-.36-.02-.5-.07-.15-.65-1.6-.9-2.17-.23-.55-.47-.48-.65-.49h-.55z"/></svg>Escribinos</a>
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
(OUT / 'tema-redherramientas.xml').write_text(theme, encoding='utf-8')

# ---------- Páginas estáticas ----------
pages = OUT / 'paginas'
pages.mkdir(exist_ok=True)
# paginas/contacto.html no se genera: es la página que armó Lucas en Blogger (con sus propios estilos)
donate_body = between(donar, '  <main id="contenido">', '  <footer').replace('  <main id="contenido">', '', 1).replace('  </main>\n', '', 1)
(pages / 'donar.html').write_text('<div class="rh-full">\n' + links(donate_body) + '</div>\n', encoding='utf-8')

print('Listo:', (OUT / 'tema-redherramientas.xml').relative_to(ROOT), '+', ', '.join(str(p.relative_to(ROOT)) for p in sorted(pages.iterdir())))
