// Red de Herramientas Entre Mujeres — comportamiento del sitio

// ---------- Configuración ----------
// Dentro de Blogger se usa el blog donde está instalado el tema (producción o pruebas);
// fuera de Blogger (la propuesta en GitHub Pages) se usa producción
var BLOG_URL = /\.blogspot\.com$|redherramientas\.com$/.test(location.hostname)
  ? location.origin
  : 'https://www.redherramientas.com';
var CAROUSEL_LABEL = 'Carrusel'; // etiqueta de Blogger para elegir los posteos del carrusel
var CAROUSEL_MAX = 6;
var CAROUSEL_DELAY = 5000;      // ms entre diapositivas
var NEWS_LABEL = 'Novedades';   // etiqueta de Blogger para las actividades de Novedades
var NEWS_MAX = 3;

// Si el blog no responde, se muestran estas diapositivas
var FALLBACK_SLIDES = [
  {
    title: '¿Qué es #ClicSeguroEnRED?',
    text: ['Un nuevo espacio para adultas mayores enfocado en la prevención de estafas digitales.',
           'Los facilitadores somos también mujeres mayores, lo que conlleva la empatía necesaria para generar un clima de seguridad. Hablamos de autonomía tecnológica que les permita dejar de pedir ayuda para las tareas cotidianas relacionadas con la tecnología, como pedir un turno médico o escanear una receta.'],
    image: 'https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&q=80&w=1200',
    url: BLOG_URL
  },
  {
    title: 'Talleres de Sensibilización',
    text: ['Iniciamos nuestro ciclo de talleres presenciales para el buen uso del celular.',
           'Abordamos los temores comunes, cómo configurar contraseñas seguras y reconocer mensajes engañosos por WhatsApp o SMS.'],
    image: 'https://images.unsplash.com/photo-1581056771107-24ca5f033842?auto=format&fit=crop&q=80&w=1200',
    url: BLOG_URL
  }
];

// ---------- Header ----------
function setupHeader() {
  var header = document.querySelector('.header');
  var nav = document.getElementById('nav');
  var menuBtn = document.querySelector('.menu-btn');

  function updateHeaderHeight() {
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }
  updateHeaderHeight();
  window.addEventListener('resize', updateHeaderHeight);

  function closeMenu() {
    nav.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  }

  menuBtn.addEventListener('click', function () {
    var search = document.getElementById('search');
    var searchBtn = document.querySelector('.search-btn');
    if (search && !search.hidden) {
      search.hidden = true;
      if (searchBtn) searchBtn.setAttribute('aria-expanded', 'false');
    }
    var isOpen = nav.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', String(isOpen));
  });

  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') closeMenu();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });
}

// ---------- Tamaño de letra (como el menú de Lucas: Pequeña / Normal / Grande / Muy grande) ----------
function setupFontSize() {
  var toggle = document.querySelector('.font-size .icon-btn');
  var menu = document.querySelector('.font-size-menu');
  var options = menu.querySelectorAll('button');

  function apply(scale) {
    document.documentElement.style.fontSize = (scale * 100) + '%';
    options.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.scale === scale));
    });
    var header = document.querySelector('.header');
    document.documentElement.style.setProperty('--header-h', header.offsetHeight + 'px');
  }

  var saved = '1';
  try { saved = localStorage.getItem('font-scale') || '1'; } catch (e) {}
  apply(saved);

  toggle.addEventListener('click', function () {
    menu.hidden = !menu.hidden;
    toggle.setAttribute('aria-expanded', String(!menu.hidden));
  });

  options.forEach(function (b) {
    b.addEventListener('click', function () {
      apply(b.dataset.scale);
      try { localStorage.setItem('font-scale', b.dataset.scale); } catch (e) {}
      menu.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    });
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.font-size')) {
      menu.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// ---------- Buscador del header (resultados predictivos con el feed de Blogger) ----------
var SEARCH_MAX = 8;

function setupSearch() {
  var panel = document.getElementById('search');
  if (!panel) return;
  var toggle = document.querySelector('.search-btn');
  var form = panel.querySelector('.search-form');
  var input = panel.querySelector('.search-input');
  var results = document.getElementById('search-results');
  var timer = null;
  var lastQuery = '';
  var active = -1;

  form.action = BLOG_URL + '/search';

  function open() {
    // En pantallas chicas se cierra el menú para que no se superpongan
    var nav = document.getElementById('nav');
    var menuBtn = document.querySelector('.menu-btn');
    if (nav) nav.classList.remove('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');

    panel.hidden = false;
    toggle.setAttribute('aria-expanded', 'true');
    input.focus();
    if (input.value.trim().length >= 2) show();
  }

  function close() {
    panel.hidden = true;
    toggle.setAttribute('aria-expanded', 'false');
    hideResults();
  }

  function show() {
    results.hidden = false;
    input.setAttribute('aria-expanded', 'true');
  }

  function hideResults() {
    results.hidden = true;
    input.setAttribute('aria-expanded', 'false');
    input.removeAttribute('aria-activedescendant');
    active = -1;
  }

  function status(text) {
    results.innerHTML = '';
    var p = document.createElement('p');
    p.className = 'search-status';
    p.textContent = text;
    results.appendChild(p);
    show();
  }

  function allLink(query) {
    var a = document.createElement('a');
    a.className = 'search-all';
    a.id = 'search-opt-all';
    a.setAttribute('role', 'option');
    a.href = BLOG_URL + '/search?q=' + encodeURIComponent(query);
    a.textContent = 'Ver todos los resultados para “' + query + '”';
    return a;
  }

  // Resalta las palabras buscadas en el título
  function highlight(el, text, query) {
    var words = query.toLowerCase().split(/\s+/).filter(function (w) { return w.length > 1; });
    var lower = text.toLowerCase();
    var i = 0;
    while (i < text.length) {
      var best = -1, len = 0;
      words.forEach(function (w) {
        var k = lower.indexOf(w, i);
        if (k !== -1 && (best === -1 || k < best)) { best = k; len = w.length; }
      });
      if (best === -1) { el.appendChild(document.createTextNode(text.slice(i))); break; }
      if (best > i) el.appendChild(document.createTextNode(text.slice(i, best)));
      var mark = document.createElement('mark');
      mark.textContent = text.slice(best, best + len);
      el.appendChild(mark);
      i = best + len;
    }
  }

  function render(items, query) {
    results.innerHTML = '';
    active = -1;
    if (!items.length) {
      status('No encontramos resultados para “' + query + '”.');
      return;
    }
    items.forEach(function (item, i) {
      var a = document.createElement('a');
      a.className = 'search-item';
      a.id = 'search-opt-' + i;
      a.setAttribute('role', 'option');
      a.href = item.url;

      var img = document.createElement('img');
      img.src = item.image;
      img.alt = '';
      img.loading = 'lazy';
      img.width = 64;
      img.height = 64;

      var text = document.createElement('span');
      var title = document.createElement('strong');
      highlight(title, item.title, query);
      var meta = document.createElement('small');
      meta.textContent = [item.label, item.date].filter(Boolean).join(' · ');
      text.appendChild(title);
      text.appendChild(meta);

      a.appendChild(img);
      a.appendChild(text);
      results.appendChild(a);
    });
    results.appendChild(allLink(query));
    show();
  }

  function search() {
    var query = input.value.trim();
    if (query === lastQuery) return;
    lastQuery = query;
    if (query.length < 2) { hideResults(); return; }
    status('Buscando…');
    searchPosts(query, function (items) {
      if (query !== lastQuery) return;  // llegó tarde: ya se escribió otra cosa
      if (items === null) status('No pudimos buscar ahora. Probá de nuevo en un rato.');
      else render(items, query);
    });
  }

  function move(step) {
    var options = results.querySelectorAll('[role="option"]');
    if (!options.length) return;
    if (active >= 0) options[active].classList.remove('active');
    active = (active + 1 + step + options.length + 1) % (options.length + 1) - 1;
    if (active === -1) { input.removeAttribute('aria-activedescendant'); return; }
    options[active].classList.add('active');
    options[active].scrollIntoView({ block: 'nearest' });
    input.setAttribute('aria-activedescendant', options[active].id);
  }

  toggle.addEventListener('click', function () {
    if (panel.hidden) open(); else close();
  });

  input.addEventListener('input', function () {
    clearTimeout(timer);
    timer = setTimeout(search, 300);
  });
  input.addEventListener('focus', function () {
    if (input.value.trim().length >= 2 && results.childNodes.length) show();
  });

  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); if (results.hidden && results.childNodes.length) show(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter' && active >= 0) {
      e.preventDefault();
      results.querySelectorAll('[role="option"]')[active].click();
    }
  });

  form.addEventListener('submit', function (e) {
    if (input.value.trim().length < 2) e.preventDefault();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !panel.hidden) {
      close();
      toggle.focus();
    }
  });

  // Tocar fuera del header cierra el buscador
  document.addEventListener('click', function (e) {
    if (!panel.hidden && !e.target.closest('.header')) close();
  });
}

// Busca en el feed del blog (JSONP). Devuelve null si el blog no respondió
function searchPosts(query, callback) {
  var name = 'blogSearch' + Date.now() + Math.floor(Math.random() * 1000);
  var script = document.createElement('script');
  var timeout = setTimeout(function () { finish(null); }, 8000);

  function finish(items) {
    clearTimeout(timeout);
    window[name] = function () {};
    script.remove();
    callback(items);
  }

  window[name] = function (data) {
    var entries = (data && data.feed && data.feed.entry) || [];
    finish(entries.map(function (entry) {
      var link = (entry.link || []).filter(function (l) { return l.rel === 'alternate'; })[0];
      var image = entry.media$thumbnail ? entry.media$thumbnail.url : '';
      image = image.replace(/\/s\d+(-[a-z0-9-]+)?\//, '/s128-c/').replace(/=s\d+(-[a-z0-9-]+)?$/, '=s128-c');
      var published = entry.published ? new Date(entry.published.$t) : null;
      return {
        title: entry.title.$t || 'Sin título',
        url: link ? link.href : BLOG_URL,
        image: image || 'https://i.imgur.com/CFM0Pcr.png',
        label: topicLabel(entry.category),
        date: published && !isNaN(published) ? published.toLocaleDateString('es-AR', { day: 'numeric', month: 'short', year: 'numeric' }) : ''
      };
    }));
  };
  script.onerror = function () { finish(null); };
  script.src = BLOG_URL + '/feeds/posts/summary?alt=json-in-script&max-results=' + SEARCH_MAX +
    '&q=' + encodeURIComponent(query) + '&callback=' + name;
  document.head.appendChild(script);
}

// ---------- Nota (posteo): foto principal, bajada, tiempo de lectura, compartir y "Seguí leyendo" ----------
var ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 14.9L2 22l5.25-1.38A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 15l-.3-.2-3.1.8.83-3-.2-.32A8.1 8.1 0 0 1 12.04 3.8zM8.6 7.5c-.2 0-.5.07-.75.35-.25.27-1 1-1 2.4s1.03 2.8 1.17 3c.15.2 2 3.2 4.9 4.36 2.4.95 2.9.76 3.4.72.52-.05 1.7-.7 1.93-1.36.24-.67.24-1.24.17-1.36-.07-.12-.26-.2-.55-.34-.3-.15-1.7-.84-1.96-.94-.27-.1-.46-.15-.65.14-.2.3-.75.94-.9 1.13-.17.2-.33.22-.62.07-.3-.14-1.2-.44-2.3-1.4-.85-.76-1.42-1.7-1.6-1.98-.16-.3 0-.45.13-.6.14-.13.3-.34.44-.5.15-.17.2-.3.3-.5.1-.2.05-.36-.02-.5-.07-.15-.65-1.6-.9-2.17-.23-.55-.47-.48-.65-.49h-.55z"/></svg>';

function setupArticle() {
  // Contacto y Donar van a todo el ancho (para navegadores sin :has)
  var full = document.querySelector('.post-layout .rh-full');
  if (full) full.closest('.post-layout').classList.add('is-full');

  var art = document.querySelector('.art');
  if (!art) return;
  var body = art.querySelector('.art-body');
  if (!body) return;

  // 1) Foto principal: la primera imagen de la nota, si está al principio, pasa arriba con su epígrafe
  var hero = art.querySelector('.art-hero');
  var img = body.querySelector('img');
  if (hero && img) {
    var table = img.closest('table.tr-caption-container');
    var block = table || img;
    while (!table && block.parentNode !== body && block.parentNode.textContent.trim() === '') block = block.parentNode;
    var before = document.createRange();
    before.setStart(body, 0);
    before.setEndBefore(block);
    if (before.toString().trim().length < 400) {
      var photo = document.createElement('img');
      photo.src = img.src.replace(/\/s\d+(-[a-z0-9-]+)?\//, '/s1600/').replace(/=s\d+(-[a-z0-9-]+)?$/, '=s1600');
      photo.alt = img.alt || '';
      hero.appendChild(photo);
      var caption = table ? table.querySelector('.tr-caption') : null;
      if (caption && caption.textContent.trim()) {
        var fc = document.createElement('figcaption');
        fc.textContent = caption.textContent.trim();
        hero.appendChild(fc);
      }
      removeWithEmptyParents(block, body);
      hero.hidden = false;
    }
  }

  // 2) Direcciones escritas como texto (notas viejas): se convierten en un botón para abrirlas
  linkifyUrls(body);

  // 3) Bajada: el primer párrafo de la nota (si es corto y no es solo un link)
  var bajada = art.querySelector('.art-bajada');
  var first = htmlToText(body.innerHTML)[0] || '';
  if (bajada && first && first.length <= 350 && !/^https?:\/\//i.test(first)) {
    var target = null;
    body.querySelectorAll('*').forEach(function (el) {
      if (el.textContent.trim() === first && (!target || target.contains(el))) target = el;
    });
    var onlyLink = target && (target.closest('a') ||
      Array.prototype.some.call(target.querySelectorAll('a'), function (a) { return a.textContent.trim() === first; }));
    if (target && !onlyLink && !target.querySelector('img, iframe')) {
      removeWithEmptyParents(target, body);
      bajada.textContent = first;
      bajada.hidden = false;
    }
  }

  // 4) Tiempo de lectura (unas 200 palabras por minuto)
  var reading = art.querySelector('.art-lectura');
  if (reading) {
    var words = (body.textContent || '').trim().split(/\s+/).length;
    reading.textContent = 'Lectura de ' + Math.max(1, Math.round(words / 200)) + ' min';
  }

  // 5) Compartir: WhatsApp y Facebook con el título y la dirección, y "Copiar enlace"
  var url = (document.querySelector('link[rel="canonical"]') || {}).href || location.href;
  var title = (art.querySelector('.art-title') || {}).textContent || document.title;
  art.querySelectorAll('[data-share="wa"]').forEach(function (a) {
    a.href = 'https://wa.me/?text=' + encodeURIComponent(title.trim() + ' ' + url);
  });
  art.querySelectorAll('[data-share="fb"]').forEach(function (a) {
    a.href = 'https://www.facebook.com/sharer.php?u=' + encodeURIComponent(url);
  });
  art.querySelectorAll('[data-share="copy"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var label = btn.querySelector('.label');
      function done(ok) {
        if (label) {
          var original = label.dataset.text || (label.dataset.text = label.textContent);
          label.textContent = ok ? '¡Enlace copiado!' : 'No se pudo copiar';
          setTimeout(function () { label.textContent = original; }, 2500);
        } else {
          btn.setAttribute('aria-label', ok ? 'Enlace copiado' : 'No se pudo copiar');
        }
      }
      if (navigator.clipboard) navigator.clipboard.writeText(url).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  });

  // 6) Seguí leyendo: otras notas de la misma etiqueta
  var related = art.querySelector('.art-related');
  if (related && related.dataset.label) {
    var here = url.replace(/[?#].*$/, '').replace(/^https?:\/\/[^/]+/, '');
    loadPosts(related.dataset.label, function (posts) {
      posts = posts.filter(function (p) { return p.url.replace(/[?#].*$/, '').replace(/^https?:\/\/[^/]+/, '') !== here; }).slice(0, 3);
      if (!posts.length) return;
      var grid = related.querySelector('.rel-grid');
      posts.forEach(function (p) {
        var a = document.createElement('a');
        a.className = 'rel-card';
        a.href = p.url;
        var im = document.createElement('img');
        im.src = p.image;
        im.alt = '';
        im.loading = 'lazy';
        var h = document.createElement('h3');
        h.textContent = p.title;
        a.appendChild(im);
        a.appendChild(h);
        grid.appendChild(a);
      });
      related.hidden = false;
    });
  }
}

// Convierte las direcciones escritas como texto en un botón ("Abrir el documento PDF", "Abrir el enlace")
function linkifyUrls(root) {
  var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  var nodes = [];
  var node;
  while ((node = walker.nextNode())) {
    if (/https?:\/\//i.test(node.nodeValue) && !node.parentNode.closest('a')) nodes.push(node);
  }
  nodes.forEach(function (textNode) {
    var parts = textNode.nodeValue.split(/(https?:\/\/[^\s<>"]+)/i);
    var frag = document.createDocumentFragment();
    parts.forEach(function (part) {
      if (!/^https?:\/\//i.test(part)) {
        if (part) frag.appendChild(document.createTextNode(part));
        return;
      }
      var url = part.replace(/[.,;:)]+$/, '');
      var rest = part.slice(url.length);
      var host = url.replace(/^https?:\/\/(www\.)?/i, '').split('/')[0];
      var a = document.createElement('a');
      a.className = 'art-doc';
      a.href = url;
      a.target = '_blank';
      a.rel = 'noopener';
      a.textContent = (/\.pdf($|[?#])/i.test(url) ? 'Abrir el documento PDF' : 'Abrir el enlace') + ' (' + host + ')';
      frag.appendChild(a);
      if (rest) frag.appendChild(document.createTextNode(rest));
    });
    textNode.parentNode.replaceChild(frag, textNode);
  });
}

// ---------- Volver arriba ----------
function setupToTop() {
  var btn = document.querySelector('.to-top');
  window.addEventListener('scroll', function () {
    btn.classList.toggle('show', window.scrollY > 500);
  });
  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// ---------- Carrusel ----------
function setupCarousel() {
  var carousel = document.querySelector('.carousel');
  if (!carousel) return;

  var slidesEl = carousel.querySelector('.slides');
  var dotsEl = carousel.querySelector('.dots');
  var current = 0;
  var total = 0;
  var timer = null;
  var paused = false;

  function play() {
    stop();
    if (paused || total < 2) return;
    timer = setInterval(function () { goTo(current + 1); }, CAROUSEL_DELAY);
  }

  function stop() {
    clearInterval(timer);
  }

  function goTo(index) {
    current = (index + total) % total;
    slidesEl.style.transform = 'translateX(-' + (current * 100) + '%)';
    for (var i = 0; i < total; i++) {
      dotsEl.children[i].classList.toggle('active', i === current);
      slidesEl.children[i].setAttribute('aria-hidden', String(i !== current));
    }
    paused = false;
    play();
  }

  // Abre la nota ampliada y pausa el carrusel hasta que se cierre
  function open(item) {
    paused = true;
    stop();
    openNota(item, function () {
      paused = false;
      play();
    });
  }

  function makeSlide(item) {
    var slide = document.createElement('article');
    slide.className = 'slide';

    var media = document.createElement('a');
    media.className = 'slide-media';
    media.href = item.url;
    media.setAttribute('aria-label', 'Ver la nota: ' + item.title);
    media.addEventListener('click', function (e) {
      e.preventDefault();
      open(item);
    });
    var blur = document.createElement('div');
    blur.className = 'blur';
    blur.style.backgroundImage = 'url("' + item.image + '")';
    var img = document.createElement('img');
    img.src = item.image;
    img.alt = '';
    media.appendChild(blur);
    media.appendChild(img);

    var box = document.createElement('div');
    box.className = 'slide-box';

    var title = document.createElement('h2');
    title.textContent = item.title;
    box.appendChild(title);

    if (item.epigrafe) {
      var desc = document.createElement('p');
      desc.className = 'slide-desc';
      desc.textContent = item.epigrafe;
      box.appendChild(desc);
    }

    var actions = document.createElement('div');
    actions.className = 'slide-actions';
    var more = document.createElement('button');
    more.type = 'button';
    more.className = 'btn slide-more';
    more.textContent = 'Ver más';
    more.addEventListener('click', function () { open(item); });
    actions.appendChild(more);
    box.appendChild(actions);

    slide.appendChild(media);
    slide.appendChild(box);
    return slide;
  }

  function render(items) {
    stop();
    slidesEl.innerHTML = '';
    dotsEl.innerHTML = '';
    total = items.length;
    current = 0;

    items.forEach(function (item, i) {
      slidesEl.appendChild(makeSlide(item));
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.setAttribute('aria-label', 'Ir a la actividad ' + (i + 1));
      dot.addEventListener('click', function () { goTo(i); });
      dotsEl.appendChild(dot);
    });

    carousel.querySelectorAll('.carousel-arrow, .dots').forEach(function (el) {
      el.style.display = total < 2 ? 'none' : '';
    });
    goTo(0);
  }

  carousel.querySelector('.prev').addEventListener('click', function () { goTo(current - 1); });
  carousel.querySelector('.next').addEventListener('click', function () { goTo(current + 1); });
  carousel.addEventListener('mouseenter', stop);
  carousel.addEventListener('mouseleave', play);

  // Mientras cargan los posteos no se muestran flechas ni puntos
  carousel.querySelectorAll('.carousel-arrow, .dots').forEach(function (el) {
    el.style.display = 'none';
  });

  // Posteos del blog: primero los de la etiqueta del carrusel; si no hay, los últimos.
  // Las actividades de ejemplo solo se muestran si no se pudo cargar ninguno
  loadPosts(CAROUSEL_LABEL, function (posts) {
    if (posts.length) return render(posts);
    loadPosts('', function (latest) {
      render(latest.length ? latest : FALLBACK_SLIDES.map(fallbackItem));
    });
  });
}

// Primera etiqueta que es un tema (Carrusel y Novedades solo eligen dónde aparece la entrada)
function topicLabel(categories) {
  var topic = (categories || []).filter(function (c) {
    return c.term !== CAROUSEL_LABEL && c.term !== NEWS_LABEL;
  })[0];
  return topic ? topic.term : '';
}

// ---------- Novedades ----------
var NEWS_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M19 4h-1V2h-2v2H8V2H6v2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 16H5V10h14v10z"/></svg>';

function setupNews() {
  var section = document.getElementById('novedades');
  if (!section) return;
  var list = section.querySelector('.news');
  // La barra separadora de arriba solo se ve si hay novedades
  var separator = section.previousElementSibling;
  if (separator && !separator.classList.contains('separator')) separator = null;
  if (separator) separator.hidden = true;

  loadPosts(NEWS_LABEL, function (posts) {
    if (!posts.length) return;
    list.innerHTML = '';
    posts.forEach(function (post) {
      var card = document.createElement('article');
      card.className = 'news-card';
      var title = document.createElement('h3');
      var link = document.createElement('a');
      link.href = post.url;
      link.textContent = post.title;
      title.appendChild(link);
      card.appendChild(title);
      if (post.date) {
        var date = document.createElement('p');
        date.className = 'news-date';
        date.innerHTML = NEWS_ICON;
        date.appendChild(document.createTextNode(post.date));
        card.appendChild(date);
      }
      list.appendChild(card);
    });
    section.hidden = false;
    if (separator) separator.hidden = false;
  }, NEWS_MAX);
}

// Lee el feed de Blogger (JSONP: funciona dentro de Blogger y desde cualquier dominio)
function loadPosts(label, callback, max) {
  var name = 'blogFeed' + Date.now() + Math.floor(Math.random() * 1000);
  var script = document.createElement('script');
  var timeout = setTimeout(function () { finish([]); }, 8000);

  function finish(posts) {
    clearTimeout(timeout);
    window[name] = function () {};
    script.remove();
    callback(posts);
  }

  window[name] = function (data) { finish(parseFeed(data)); };
  script.onerror = function () { finish([]); };
  script.src = BLOG_URL + '/feeds/posts/default' +
    (label ? '/-/' + encodeURIComponent(label) : '') +
    '?alt=json-in-script&max-results=' + (max || CAROUSEL_MAX) + '&callback=' + name;
  document.head.appendChild(script);
}

function parseFeed(data) {
  var entries = (data && data.feed && data.feed.entry) || [];
  return entries.map(function (entry) {
    var html = (entry.content || entry.summary || {}).$t || '';
    var link = (entry.link || []).filter(function (l) { return l.rel === 'alternate'; })[0];
    var image = entry.media$thumbnail ? entry.media$thumbnail.url : '';
    if (!image) {
      var match = html.match(/<img[^>]+src="([^"]+)"/i);
      image = match ? match[1] : '';
    }
    // Las miniaturas vienen chicas (s72-c): se pide la versión de 1200px
    image = image.replace(/\/s\d+(-[a-z0-9-]+)?\//, '/w1200/').replace(/=s\d+(-[a-z0-9-]+)?$/, '=w1200');

    var parts = splitNota(html);
    var published = entry.published ? new Date(entry.published.$t) : null;
    return {
      title: entry.title.$t,
      date: published && !isNaN(published) ? published.toLocaleDateString('es-AR', { day: 'numeric', month: 'long', year: 'numeric' }) : '',
      epigrafe: parts.epigrafe,
      body: parts.body,
      photo: image,
      image: image || 'https://i.imgur.com/CFM0Pcr.png',
      url: link ? link.href : BLOG_URL
    };
  });
}

// Diapositivas de ejemplo (texto plano) al mismo formato que los posteos
function fallbackItem(item) {
  var body = item.text.slice(1).map(function (t) {
    var p = document.createElement('p');
    p.textContent = t;
    return p.outerHTML;
  }).join('');
  return { title: item.title, epigrafe: item.text[0], body: body, photo: item.image, image: item.image, url: item.url };
}

// Separa la nota: el primer párrafo es el epígrafe y el resto es la nota completa
function splitNota(html) {
  var lines = htmlToText(html);
  var epigrafe = lines.length ? lines[0] : '';
  var doc = new DOMParser().parseFromString(html, 'text/html');
  var body = doc.body;
  body.querySelectorAll('script, style').forEach(function (el) { el.remove(); });

  if (epigrafe) {
    // El elemento más interno cuyo texto es justo el epígrafe (un <p>, un <div>, una negrita...)
    var target = null;
    body.querySelectorAll('*').forEach(function (el) {
      if (el.textContent.trim() === epigrafe && (!target || target.contains(el))) target = el;
    });
    if (target) {
      removeWithEmptyParents(target, body);
    } else {
      // Texto suelto, sin párrafos: se saca hasta el primer salto de línea
      var walker = doc.createTreeWalker(body, NodeFilter.SHOW_TEXT);
      var node;
      while ((node = walker.nextNode())) {
        if (!node.nodeValue.trim()) continue;
        if (node.nodeValue.trim() === epigrafe) {
          var next = node.nextSibling;
          while (next && next.nodeName === 'BR') {
            var after = next.nextSibling;
            next.remove();
            next = after;
          }
          node.remove();
        }
        break;
      }
    }
  }

  // La primera foto se muestra arriba de la nota ampliada: se saca del cuerpo para no repetirla
  var firstImg = body.querySelector('img');
  if (firstImg) removeWithEmptyParents(firstImg, body);

  // Los links de la nota se abren en otra pestaña para no perder la home
  body.querySelectorAll('a[href]').forEach(function (a) {
    a.target = '_blank';
    a.rel = 'noopener';
  });
  return { epigrafe: epigrafe, body: body.innerHTML.trim() };
}

// Saca un elemento y los contenedores que quedan vacíos (el párrafo o el bloque de la imagen)
function removeWithEmptyParents(el, root) {
  var parent = el.parentNode;
  el.remove();
  while (parent && parent !== root && !parent.textContent.trim() && !parent.querySelector('img, iframe, video')) {
    var up = parent.parentNode;
    parent.remove();
    parent = up;
  }
}

// ---------- Nota ampliada (ventana con barra de desplazamiento al costado) ----------
var notaModal = null;

function openNota(item, onClose) {
  if (!notaModal) notaModal = buildNotaModal();
  var m = notaModal;
  m.photo.hidden = !item.photo;
  if (item.photo) m.photo.src = item.photo; else m.photo.removeAttribute('src');
  m.title.textContent = item.title;
  m.epigrafe.textContent = item.epigrafe || '';
  m.epigrafe.hidden = !item.epigrafe;
  m.body.innerHTML = item.body || '';
  m.link.href = item.url;
  m.onClose = onClose;
  m.lastFocus = document.activeElement;

  m.el.hidden = false;
  document.documentElement.classList.add('nota-abierta');
  m.scroll.scrollTop = 0;
  m.close.focus();
}

function closeNota() {
  var m = notaModal;
  if (!m || m.el.hidden) return;
  m.el.hidden = true;
  document.documentElement.classList.remove('nota-abierta');
  m.body.innerHTML = '';  // corta videos que estuvieran reproduciéndose
  if (m.lastFocus && m.lastFocus.focus) m.lastFocus.focus();
  if (m.onClose) m.onClose();
}

function buildNotaModal() {
  var el = document.createElement('div');
  el.className = 'nota-modal';
  el.hidden = true;
  el.innerHTML =
    '<div class="nota-panel" role="dialog" aria-modal="true" aria-labelledby="nota-titulo">' +
      '<button class="nota-close" type="button" aria-label="Cerrar la nota">' +
        '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>' +
      '</button>' +
      '<div class="nota-scroll" tabindex="0">' +
        '<img class="nota-foto" alt="">' +
        '<div class="nota-content">' +
        '<h2 class="nota-title" id="nota-titulo"></h2>' +
        '<p class="nota-epigrafe"></p>' +
        '<div class="nota-body"></div>' +
        '<p class="nota-footer"><a class="btn btn-outline-dark nota-link" href="#">Abrir la nota en su página</a></p>' +
        '</div>' +
      '</div>' +
    '</div>';
  document.body.appendChild(el);

  var m = {
    el: el,
    scroll: el.querySelector('.nota-scroll'),
    photo: el.querySelector('.nota-foto'),
    title: el.querySelector('.nota-title'),
    epigrafe: el.querySelector('.nota-epigrafe'),
    body: el.querySelector('.nota-body'),
    link: el.querySelector('.nota-link'),
    close: el.querySelector('.nota-close')
  };

  m.close.addEventListener('click', closeNota);
  // Tocar afuera de la nota la cierra
  el.addEventListener('click', function (e) {
    if (e.target === el) closeNota();
  });
  document.addEventListener('keydown', function (e) {
    if (el.hidden) return;
    if (e.key === 'Escape') closeNota();
    // El foco queda dentro de la nota mientras está abierta
    if (e.key === 'Tab') {
      var items = el.querySelectorAll('button, a[href], iframe, [tabindex="0"]');
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });
  return m;
}

function htmlToText(html) {
  html = html.replace(/<br\s*\/?>/gi, '\n').replace(/<\/(p|div|h\d|li)>/gi, '\n');
  var doc = new DOMParser().parseFromString(html, 'text/html');
  return (doc.body.textContent || '')
    .split('\n')
    .map(function (line) { return line.trim(); })
    .filter(function (line) { return line; });
}

// ---------- Formulario de contacto (FormSubmit → info@redherramientas.com) ----------
function setupContactForm() {
  var form = document.getElementById('contact-form');
  if (!form) return;
  var msg = document.getElementById('form-msg');
  var button = form.querySelector('button[type="submit"]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    button.disabled = true;
    msg.className = 'form-msg';
    msg.textContent = 'Enviando...';

    fetch('https://formsubmit.co/ajax/info@redherramientas.com', {
      method: 'POST',
      headers: { 'Accept': 'application/json' },
      body: new FormData(form)
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (String(data.success) !== 'true') throw new Error(data.message);
        form.reset();
        msg.className = 'form-msg ok';
        msg.textContent = '¡Gracias! Recibimos tu mensaje y te vamos a responder a la brevedad.';
      })
      .catch(function () {
        msg.className = 'form-msg error';
        msg.textContent = 'No pudimos enviar el mensaje. Probá de nuevo o escribinos por WhatsApp.';
      })
      .finally(function () {
        button.disabled = false;
      });
  });
}

// ---------- Copiar datos bancarios (página de donación) ----------
function setupCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(function (btn) {
    var value = document.querySelector('[data-value="' + btn.dataset.copy + '"]');
    // Mientras el dato no esté cargado, no se muestra el botón
    if (!value || value.classList.contains('pending')) {
      btn.hidden = true;
      return;
    }
    btn.addEventListener('click', function () {
      navigator.clipboard.writeText(value.textContent.trim()).then(function () {
        btn.textContent = '¡Copiado!';
        setTimeout(function () { btn.textContent = 'Copiar'; }, 2000);
      });
    });
  });
}

// ---------- Modales de datos bancarios (página de donación) ----------
function setupModals() {
  document.querySelectorAll('[data-modal]').forEach(function (btn) {
    var modal = document.getElementById(btn.dataset.modal);
    btn.addEventListener('click', function () { modal.showModal(); });
  });
  document.querySelectorAll('.modal').forEach(function (modal) {
    modal.querySelector('.modal-close').addEventListener('click', function () { modal.close(); });
    // Clic afuera del cuadro: cierra
    modal.addEventListener('click', function (e) {
      var r = modal.getBoundingClientRect();
      var outside = e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
      if (outside) modal.close();
    });
  });
}

// ---------- Inicio ----------
setupHeader();
setupSearch();
setupFontSize();
setupToTop();
setupCarousel();
setupNews();
setupArticle();
setupContactForm();
setupCopyButtons();
setupModals();
