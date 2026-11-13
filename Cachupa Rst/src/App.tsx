import { useEffect, useState, type ReactNode } from "react"

type Page = "inicio" | "casa" | "galeria" | "reservas" | "contactos" | "legal" | "404"

type Artwork = {
  title: string
  technique: string
  description: string
}

const artworks: Artwork[] = [
  {
    title: "O Caldeirão da Mãe",
    technique: "Óleo sobre tela",
    description:
      "Cena íntima e comovente da preparação da cachupa no caldeirão de barro tradicional, servida com carinho pela mãe aos olhares atentos das crianças.",
  },
  {
    title: "Serenata à Luz da Lamparina",
    technique: "Óleo sobre tela",
    description:
      "Encontro comunitário numa taberna acolhedora: famílias e amigos reunidos à volta da mesa a escutar as cordas sentimentais da rabeca.",
  },
  {
    title: "O Regresso do Pescador",
    technique: "Óleo sobre tela",
    description:
      "Retrato vigoroso do pescador ao regressar da faina, com chapéu de palha e vara aos ombros, tendo por horizonte as montanhas e o mar das ilhas.",
  },
  {
    title: "As Três Graças da Terra",
    technique: "Óleo sobre tela em tríptico",
    description:
      "Tríptico com três figuras femininas em tons de barro e vestes vermelhas ondulantes, celebrando a força, a serenidade e a presença da mulher cabo-verdiana.",
  },
  {
    title: "Caminho ao Entardecer",
    technique: "Óleo sobre tela",
    description:
      "Mãe e filho de mãos dadas percorrendo a vereda dourada ao cair da tarde, com o cesto à cabeça e a cumplicidade serena dos passos partilhados.",
  },
  {
    title: "Roda e Movimento",
    technique: "Óleo sobre tela",
    description:
      "Composição de grande energia e dinamismo sobre fundo carmesim, retratando o salto acrobático e a cadência ancestral do movimento.",
  },
  {
    title: "Ritmo de Batuku",
    technique: "Óleo sobre tela",
    description:
      "A vibração autêntica do batuku: saia amarela rodada em cadência viva ao som compassado e vigoroso das mãos no tambor tradicional.",
  },
  {
    title: "Sopros da Noite",
    technique: "Óleo sobre tela",
    description:
      "Expressão plástica intensa onde trompetes e saxofones dourados ecoam melodias de sopro e mornas pelas noites quentes do arquipélago.",
  },
  {
    title: "Festa na Areia",
    technique: "Óleo sobre tela",
    description:
      "Celebração praiana repleta de sol e vento: dançarinos vestidos de branco e azul festejando ao compasso das ilhas junto ao mar aberto.",
  },
  {
    title: "Manhã no Vale Verdejante",
    technique: "Óleo sobre tela",
    description:
      "A serenidade luminosa do labor agrícola entre montanhas escarpadas, palmeiras e caminhos de pedra percorridos pela carroça tradicional.",
  },
  {
    title: "Mãos de Labuta (O Ralador)",
    technique: "Óleo sobre tela",
    description:
      "Foco escultural nas mãos calejadas a raspar a raiz no ralador rústico de folha-de-flandres, o gesto fundador que prepara os frutos da terra para a cachupa.",
  },
]

const pagePaths: Record<Exclude<Page, "404">, string> = {
  inicio: "/",
  casa: "/a-nossa-casa",
  galeria: "/galeria",
  reservas: "/reservas",
  contactos: "/contactos",
  legal: "/privacidade-e-termos",
}

const whatsappText = encodeURIComponent(
  "Olá! Gostaria de reservar uma mesa no Cachupa Rst. Data: / Hora: / Número de pessoas: / Nome:",
)
const whatsappUrl = `https://wa.me/351963572411?text=${whatsappText}`
const mapsUrl =
  "https://www.google.com/maps/search/?api=1&query=Restaurante+Cachupa+Brr"

function pathToPage(path: string): Page {
  const item = Object.entries(pagePaths).find(
    ([, value]) =>
      value === path.replace(/\/+$/, "") || (value === "/" && path === "/"),
  )
  return item?.[0] as Page ?? "404"
}

function Arrow() {
  return <span aria-hidden="true">↗</span>
}

function LinkButton({
  page,
  children,
  secondary = false,
}: {
  page: Page
  children: ReactNode
  secondary?: boolean
}) {
  return (
    <PageLink
      page={page}
      className={secondary ? "button button--secondary" : "button"}
    >
      {children}
    </PageLink>
  )
}

function PageLink({
  page,
  children,
  className = "",
}: {
  page: Page
  children: ReactNode
  className?: string
}) {
  return (
    <a
      href={page === "404" ? "/404" : pagePaths[page]}
      className={className}
      data-nav
    >
      {children}
    </a>
  )
}

function Placeholder({
  className = "",
  label,
}: {
  className?: string
  label?: string
}) {
  return (
    <figure
      className={`placeholder ${className}`}
      aria-label={
        label
          ? `Espaço reservado para: ${label}`
          : "Espaço reservado para imagem"
      }
    >
      <span aria-hidden="true">Espaço reservado</span>
    </figure>
  )
}

function Eyebrow({ children }: { children: ReactNode }) {
  return <p className="eyebrow">{children}</p>
}

function Header({
  page,
  open,
  setOpen,
}: {
  page: Page
  open: boolean
  setOpen: (value: boolean) => void
}) {
  const links: [Page, string][] = [
    ["inicio", "Início"],
    ["casa", "A nossa casa"],
    ["galeria", "Galeria"],
    ["contactos", "Contactos"],
  ]
  return (
    <header className="site-header">
      <div className="nav-shell">
        <PageLink page="inicio" className="brand">
          <span>Cachupa</span>
          <b>RST</b>
        </PageLink>
        <nav
          className={`main-nav ${open ? "is-open" : ""}`}
          aria-label="Navegação principal"
        >
          {links.map(([target, label]) => (
            <PageLink
              key={target}
              page={target}
              className={page === target ? "active" : ""}
            >
              {label}
            </PageLink>
          ))}
          <PageLink page="reservas" className="nav-reserve">
            Reservar <Arrow />
          </PageLink>
        </nav>
        <button
          className="menu-button"
          aria-expanded={open}
          aria-label={open ? "Fechar menu" : "Abrir menu"}
          onClick={() => setOpen(!open)}
        >
          <span />
          <span />
        </button>
      </div>
    </header>
  )
}

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-intro">
        <p className="footer-brand">
          Cachupa Rst <i>·</i> Cozinha cabo-verdiana
        </p>
        <h2>Volte com fome.</h2>
        <p className="footer-invite">Sente-se. Há lugar à mesa.</p>
        <p>
          Acolhimento autêntico no Barreiro, com paredes de pedra rústica,
          cachupa confecionada ao lume brando e galeria viva de pintura
          original.
        </p>
      </div>
      <div className="footer-grid">
        <div>
          <h3>Visitar</h3>
          <p>
            Segunda a Domingo
            <br />
            <strong>11:00 às 23:00</strong>
          </p>
          <ul className="plain-list">
            <li>Cozinha em serviço contínuo</li>
            <li>Esplanada &amp; sala acolhedora</li>
            <li>Opções vegetarianas &amp; veganas</li>
            <li>Noites com música ao vivo</li>
          </ul>
        </div>
        <div>
          <h3>Encontrar</h3>
          <address>
            R. Alm. Reis 22 B<br />
            2830-326 Barreiro
          </address>
          <a href="tel:+351963572411">963 572 411</a>
          <a href={mapsUrl} target="_blank" rel="noreferrer">
            Restaurante Cachupa Brr no Google Maps <Arrow />
          </a>
          <PageLink page="reservas">
            Pedir reserva de mesa <Arrow />
          </PageLink>
        </div>
        <div>
          <h3>Navegar</h3>
          <PageLink page="inicio">Início</PageLink>
          <PageLink page="casa">A nossa casa</PageLink>
          <PageLink page="galeria">Galeria</PageLink>
          <PageLink page="reservas">Reservas</PageLink>
          <PageLink page="contactos">Contactos</PageLink>
        </div>
        <div>
          <h3>Transparência</h3>
          <PageLink page="legal">Privacidade &amp; RGPD</PageLink>
          <PageLink page="legal">Ausência de Cookies</PageLink>
          <PageLink page="legal">Termos &amp; Reservas</PageLink>
          <a
            href="https://www.livroreclamacoes.pt"
            target="_blank"
            rel="noreferrer"
          >
            Livro de Reclamações <Arrow />
          </a>
          <PageLink page="legal">Resolução de Litígios (RAL)</PageLink>
          <PageLink page="legal">Acessibilidade (WCAG 2.1 AA)</PageLink>
        </div>
      </div>
      <div className="transparency">
        Transparência Digital: Sem cookies de rastreio ou perfilamento ·
        Tipografia e ficheiros 100% locais · Dados salvaguardados pelo RGPD.
      </div>
      <div className="footer-bottom">
        <p>
          © 2026 Cachupa Rst · Cozinha tradicional de Cabo Verde. Todos os
          direitos reservados.
        </p>
        <p>Obras de arte originais em exposição da autoria de Lito Silva.</p>
        <p>Barreiro · Margem Sul · Portugal</p>
      </div>
    </footer>
  )
}

function Home({ openArtwork }: { openArtwork: (index: number) => void }) {
  const news = [
    [
      "Especial",
      "Cachupa Rica ao Fim de Semana",
      "Preparada lentamente em lume brando durante horas com carnes nobres e feijão da terra, servida fumegante em barro aos sábados e domingos.",
    ],
    [
      "Cultura",
      "Telas Originais de Lito Silva na Sala",
      "As paredes da nossa casa acolhem pinturas a óleo originais dedicadas à cozinha, à música e às gentes de Cabo Verde. Uma exposição viva enquanto almoça ou janta.",
    ],
    [
      "Aviso",
      "Reservas para Grupos & Famílias",
      "Para mesas de 4 ou mais pessoas ou celebrações familiares, recomendamos a mensagem prévia no WhatsApp para prepararmos o melhor acolhimento para si.",
    ],
  ]
  return (
    <>
      <section className="hero">
        <div className="hero-copy">
          <Eyebrow>Barreiro · Cozinha de Cabo Verde</Eyebrow>
          <h1>
            Cabo Verde,
            <br />
            <em>à mesa.</em>
          </h1>
          <p>
            A cachupa dá o nome à nossa casa. O cozimento lento, os ingredientes
            das ilhas e o carinho da tradição dão-lhe a alma.
          </p>
          <div className="actions">
            <LinkButton page="reservas">
              Ver reservas <Arrow />
            </LinkButton>
            <LinkButton page="casa" secondary>
              Conhecer a casa
            </LinkButton>
          </div>
        </div>
        <Placeholder
          className="hero-visual"
          label="imagem principal do restaurante"
        />
        <p className="hero-note">
          Todos os dias
          <br />
          <strong>11:00—23:00</strong>
        </p>
      </section>

      <section className="section split">
        <div>
          <Placeholder
            className="portrait"
            label="A autêntica Cachupa Rica tradicional de carne com feijão pedra e carnes nobres"
          />
          <p className="caption">
            A autêntica Cachupa Rica tradicional de carne com feijão pedra e
            carnes nobres.
          </p>
        </div>
        <div className="copy-block">
          <Eyebrow>O prato que dá nome à casa</Eyebrow>
          <h2>A cachupa, no centro da mesa.</h2>
          <p>
            O prato mais emblemático de Cabo Verde é preparado aqui como manda a
            tradição: milho quebrado selecionado, feijão pedra, carnes nobres e
            tempero aromático cozinhados em lume brando durante horas.
          </p>
          <p>
            Servida bem quente em autênticas caçarolas de barro, cada garfada é
            uma viagem aos sabores e à hospitalidade das ilhas.
          </p>
          <PageLink page="casa" className="text-link">
            Conhecer a nossa história <Arrow />
          </PageLink>
        </div>
      </section>

      <section className="section specialties">
        <div className="section-heading">
          <div>
            <Eyebrow>Sabores da casa</Eyebrow>
            <h2>
              As nossas
              <br />
              <em>especialidades.</em>
            </h2>
          </div>
          <div>
            <p>
              Da autêntica Cachupa de Polvo e Marisco à clássica Cachupa
              Refogada com ovos estrelados, chouriço e queijo de cabra. Sabores
              genuínos que reconfortam a alma.
            </p>
            <PageLink page="reservas" className="text-link">
              Reservar mesa para provar <Arrow />
            </PageLink>
          </div>
        </div>
        <div className="specialty-grid">
          <div>
            <Placeholder
              className="landscape"
              label="Cachupa de Polvo e Marisco"
            />
            <h3>Mar &amp; lume brando</h3>
            <p className="caption">
              Cachupa de Polvo e Marisco em lume brando com tomate cereja.
            </p>
          </div>
          <div>
            <Placeholder className="square" label="Cachupa Refogada clássica" />
            <h3>O clássico da casa</h3>
            <p className="caption">
              Cachupa Refogada clássica com ovos estrelados, chouriço corado e
              queijo da terra.
            </p>
          </div>
        </div>
      </section>

      <section className="news section">
        <div className="news-title">
          <div>
            <Eyebrow>À mesa, agora</Eyebrow>
            <h2>
              Novidades &amp;
              <br />
              Avisos da Casa
            </h2>
          </div>
          <PageLink page="reservas" className="text-link">
            Ver reservas <Arrow />
          </PageLink>
        </div>
        <div className="news-list">
          {news.map((item, i) => (
            <article key={item[1]}>
              <span>0{i + 1}</span>
              <div>
                <Eyebrow>{item[0]}</Eyebrow>
                <h3>{item[1]}</h3>
              </div>
              <p>{item[2]}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section house-panel">
        <div className="copy-block">
          <Eyebrow>Uma casa no Barreiro</Eyebrow>
          <h2>
            Conheça a<br />
            nossa casa.
          </h2>
          <p>
            Um espaço acolhedor com paredes de pedra rústica, mesas de madeira,
            luz calorosa e o aroma inconfundível da cachupa acabada de apurar.
          </p>
          <p>
            Aqui encontra o conforto e a hospitalidade de uma verdadeira casa
            cabo-verdiana no Barreiro, onde a boa comida se junta à arte e à
            simpatia.
          </p>
          <blockquote>
            Sente-se.
            <br />
            <em>Há lugar à mesa.</em>
          </blockquote>
          <PageLink page="casa" className="text-link">
            Ver mais sobre a casa <Arrow />
          </PageLink>
        </div>
        <Placeholder className="tall" label="ambiente da sala" />
      </section>

      <section className="section gallery-preview">
        <div className="section-heading">
          <div>
            <Eyebrow>Galeria Cachupa Rst</Eyebrow>
            <h2>
              Um lugar para
              <br />
              <em>a pintura.</em>
            </h2>
          </div>
          <div>
            <p>
              Uma galeria viva nas paredes do restaurante com pinturas a óleo
              que retratam a história, a música e a alma do povo cabo-verdiano.
            </p>
            <PageLink page="galeria" className="text-link">
              Visitar a galeria completa <Arrow />
            </PageLink>
          </div>
        </div>
        <div className="preview-grid">
          {artworks.slice(0, 3).map((art, i) => (
            <button
              className="art-card"
              key={art.title}
              onClick={() => openArtwork(i)}
            >
              <Placeholder className={`art-${i + 1}`} label={art.title} />
              <span>
                <strong>{art.title}</strong>
                <small>Lito Silva · {art.technique}</small>
              </span>
            </button>
          ))}
        </div>
      </section>

      <section className="visit">
        <Placeholder
          className="visit-visual"
          label="Cachupa rica de frango tenro dourado em lume lento com cebola caramelizada"
        />
        <div className="visit-copy">
          <Eyebrow>Rua Almirante Reis · Barreiro</Eyebrow>
          <h2>
            Puxe uma
            <br />
            <em>cadeira.</em>
          </h2>
          <p>
            Esperamos por si de portas abertas na Rua Almirante Reis, no
            Barreiro. Com esplanada acolhedora, opções veganas e noites de
            música ao vivo.
          </p>
          <div className="actions">
            <LinkButton page="reservas">
              Ver reservas <Arrow />
            </LinkButton>
            <LinkButton page="contactos" secondary>
              Contactos e localização
            </LinkButton>
          </div>
        </div>
        <p className="caption visit-caption">
          Cachupa rica de frango tenro dourado em lume lento com cebola
          caramelizada.
        </p>
      </section>
    </>
  )
}

function PageHero({
  eyebrow,
  title,
  intro,
  visual,
}: {
  eyebrow: string
  title: string
  intro: string
  visual?: boolean
}) {
  return (
    <section className={`page-hero ${visual ? "has-visual" : ""}`}>
      <div>
        <Eyebrow>{eyebrow}</Eyebrow>
        <h1>{title}</h1>
        <p>{intro}</p>
      </div>
      {visual && (
        <Placeholder className="page-hero-visual" label="ambiente da sala" />
      )}
    </section>
  )
}

function House() {
  return (
    <>
      <PageHero
        eyebrow="A nossa casa"
        title="Uma casa cabo-verdiana."
        intro="A cachupa, o espaço e a arte que fazem parte da nossa identidade."
        visual
      />
      <section className="section split">
        <div>
          <Placeholder className="portrait" label="A Cozinheira da Terra" />
          <p className="caption">
            A Cozinheira da Terra — Óleo sobre tela assinado por Lito Silva,
            exposto na sala.
          </p>
        </div>
        <div className="copy-block">
          <Eyebrow>História &amp; ambiente</Eyebrow>
          <h2>
            À mesa, na
            <br />
            nossa casa.
          </h2>
          <p>
            Criámos este restaurante com um propósito simples: trazer a
            verdadeira hospitalidade e a gastronomia de Cabo Verde para a mesa.
          </p>
          <p>
            Cada detalhe — das caçarolas de barro fumegantes aos quadros de Lito
            Silva pintados à mão sobre paredes de pedra — foi pensado para que
            se sinta em casa.
          </p>
          <blockquote>
            Comida, arte
            <br />
            <em>e hospitalidade.</em>
          </blockquote>
        </div>
      </section>
      <section className="section kitchen">
        <div className="section-heading">
          <div>
            <Eyebrow>Cozinha tradicional</Eyebrow>
            <h2>
              Do tacho
              <br />
              <em>ao prato.</em>
            </h2>
          </div>
          <p>
            Pratos confeccionados com paixão, paciência e respeito absoluto pela
            receita tradicional.
          </p>
        </div>
        <div className="kitchen-grid">
          <div>
            <Placeholder className="landscape" label="Cachupa de Marisco" />
            <p className="caption">
              Cachupa de Marisco em barro com camarão tigre grelhado e coentros
              frescos.
            </p>
          </div>
          <div>
            <Placeholder
              className="portrait-short"
              label="Cachupa Rica tradicional"
            />
            <p className="caption">
              A autêntica Cachupa Rica tradicional de carne com feijão pedra e
              carnes nobres.
            </p>
          </div>
        </div>
      </section>
      <section className="statement">
        <Eyebrow>O nosso convite</Eyebrow>
        <p>
          Uma casa faz-se de quem chega,
          <br />
          de quem fica e de quem volta.
        </p>
        <LinkButton page="reservas">
          Reservar mesa <Arrow />
        </LinkButton>
      </section>
    </>
  )
}

function Gallery({ openArtwork }: { openArtwork: (index: number) => void }) {
  return (
    <>
      <PageHero
        eyebrow="Galeria · Lito Silva"
        title="Arte que merece tempo."
        intro="Pinturas a óleo expostas nas paredes da sala de refeições, no seu espaço natural."
      />
      <section className="artist-intro">
        <span>LS</span>
        <div>
          <Eyebrow>O artista</Eyebrow>
          <h2>Lito Silva</h2>
          <p>
            Pintor cabo-verdiano cujas telas a óleo retratam com calor, cor e
            emoção a vida quotidiana, as gentes e a alma de Cabo Verde.
          </p>
        </div>
      </section>
      <section className="section exhibition">
        <div className="exhibition-title">
          <Eyebrow>Exposição permanente</Eyebrow>
          <h2>
            Onze obras
            <br />
            <em>originais.</em>
          </h2>
          <p>Selecione uma obra para abrir a respetiva ficha completa.</p>
        </div>
        <div className="art-grid">
          {artworks.map((art, i) => (
            <button
              className={`artwork artwork-${(i % 4) + 1}`}
              onClick={() => openArtwork(i)}
              key={art.title}
            >
              <Placeholder label={art.title} />
              <span className="art-number">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="art-meta">
                <strong>{art.title}</strong>
                <small>{art.technique}</small>
              </span>
            </button>
          ))}
        </div>
      </section>
    </>
  )
}

function Reservations() {
  return (
    <>
      <PageHero
        eyebrow="Reservas"
        title="Até à mesa."
        intro="Peça a sua reserva pelo WhatsApp. A equipa confirma a disponibilidade consigo."
      />
      <section className="reservation-panel">
        <div className="reservation-intro">
          <Eyebrow>Contacto direto</Eyebrow>
          <h2>
            Uma conversa,
            <br />
            <em>uma mesa.</em>
          </h2>
          <p>
            Fale diretamente com a equipa para pedir uma reserva. A
            disponibilidade é confirmada na conversa.
          </p>
        </div>
        <div className="channels">
          <a href={whatsappUrl} target="_blank" rel="noreferrer">
            <span>01</span>
            <div>
              <small>Canal recomendado</small>
              <strong>WhatsApp</strong>
            </div>
            <Arrow />
          </a>
          <a href="tel:+351963572411">
            <span>02</span>
            <div>
              <small>Telefone</small>
              <strong>963 572 411</strong>
            </div>
            <Arrow />
          </a>
          <div className="channel-muted">
            <span>03</span>
            <div>
              <small>Email</small>
              <strong>Disponível quando configurado</strong>
            </div>
          </div>
        </div>
      </section>
      <section className="section steps">
        <Eyebrow>Como pedir</Eyebrow>
        <div className="steps-grid">
          {[
            "Contacte a equipa por WhatsApp, telefone ou email.",
            "Indique o dia, a hora e o número de pessoas.",
            "Aguarde a resposta da equipa para confirmar.",
          ].map((step, i) => (
            <article key={step}>
              <span>0{i + 1}</span>
              <p>{step}</p>
            </article>
          ))}
        </div>
        <div className="notice">
          <strong>Importante</strong>
          <p>
            O pedido só fica confirmado depois da resposta da equipa. Este site
            não envia mensagens nem confirma reservas.
          </p>
        </div>
      </section>
    </>
  )
}

function Contacts() {
  const days = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo",
  ]
  return (
    <>
      <PageHero
        eyebrow="Contactos"
        title="Encontre a nossa casa."
        intro="Localização, horários e contactos da nossa casa no Barreiro."
      />
      <section className="contact-grid">
        <div className="contact-location">
          <Eyebrow>Localização</Eyebrow>
          <h2>
            R. Alm. Reis 22 B,
            <br />
            2830-326 Barreiro
          </h2>
          <p>Barreiro · Margem Sul · Portugal</p>
          <a className="button" href={mapsUrl} target="_blank" rel="noreferrer">
            Abrir no Google Maps <Arrow />
          </a>
          <Placeholder className="map-space" label="mapa de localização" />
        </div>
        <div className="contact-details">
          <div>
            <Eyebrow>Contacto direto</Eyebrow>
            <a className="phone" href="tel:+351963572411">
              963 572 411
            </a>
            <a
              href={whatsappUrl}
              target="_blank"
              rel="noreferrer"
              className="text-link"
            >
              Pedir por WhatsApp <Arrow />
            </a>
            <p className="muted">Email disponível quando configurado.</p>
          </div>
          <div className="schedule">
            <Eyebrow>Horário semanal</Eyebrow>
            {days.map((day) => (
              <p key={day}>
                <span>{day}</span>
                <strong>11:00–23:00</strong>
              </p>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}

function Legal() {
  const sections = [
    [
      "1. Proteção de Dados Pessoais (RGPD)",
      [
        "No Cachupa Restaurante, a sua privacidade é um compromisso fundamental. Recolhemos apenas os dados estritamente necessários para a gestão do seu pedido de reserva de mesa ou resposta às suas dúvidas (nome, telefone e email, facultados voluntariamente).",
        "Os seus dados nunca são comercializados, cedidos a terceiros ou utilizados para envio de publicidade não solicitada. São conservados unicamente pelo período indispensável ao atendimento.",
        "Ao abrigo do RGPD (Regulamento Geral sobre a Proteção de Dados — Regulamento UE 2016/679), tem o direito de aceder, retificar ou solicitar a eliminação dos seus dados a qualquer momento, bastando contactar-nos pelo telefone 963 572 411 ou presencialmente no nosso restaurante no Barreiro.",
      ],
    ],
    [
      "2. Ausência Total de Cookies de Rastreio & Fontes Locais",
      [
        "Este website foi intencionalmente concebido segundo princípios rigorosos de privacidade por conceção. Não utilizamos quaisquer cookies de rastreio, pixéis de seguimento, ferramentas de perfilamento ou analítica invasiva de visitas.",
        "Todas as tipografias e ficheiros do website são alojados e servidos diretamente pelo nosso próprio servidor local, sem qualquer contacto com servidores externos de terceiros (como Google Fonts ou CDNs externos), salvaguardando a privacidade do seu endereço IP.",
        "Por não utilizarmos cookies não essenciais, a navegação neste espaço digital dispensa banners ou pedidos de consentimento intrusivos, garantindo uma experiência direta, rápida e transparente.",
      ],
    ],
    [
      "3. Termos de Utilização & Política de Reservas",
      [
        "O pedido de reserva efetuado através dos nossos canais de contacto (WhatsApp, telefone ou correio eletrónico) constitui uma solicitação de disponibilidade sujeita a validação manual. A reserva só fica garantida após confirmação direta e expressa por parte da equipa.",
        "De forma a garantir o melhor acolhimento de todos os clientes, agradecemos aviso prévio em caso de alteração no horário ou número de pessoas. É concedida uma tolerância de 15 minutos em relação à hora acordada, finda a qual a mesa poderá ser reatribuída.",
        "A identidade visual, logótipos e textos deste site pertencem ao Cachupa Restaurante. As obras de arte pictóricas expostas na sala de refeições e representadas na nossa galeria digital são criações artísticas originais da autoria do artista Lito Silva, protegidas pela legislação de direitos de autor.",
      ],
    ],
    [
      "4. Livro de Reclamações & Resolução Alternativa de Litígios (RAL)",
      [
        "Em cumprimento do Decreto-Lei n.º 74/2017, disponibilizamos o acesso direto à plataforma oficial do Livro de Reclamações Eletrónico, onde qualquer cidadão pode submeter a sua reclamação ou elogio.",
        "Em caso de litígio de consumo, o cliente pode recorrer a uma entidade de Resolução Alternativa de Litígios de Consumo (RAL). O Cachupa Restaurante insere-se na área de competência do CNIACC — Centro Nacional de Informação e Arbitragem de Conflitos de Consumo.",
        "Pode consultar a lista atualizada de todas as entidades RAL de Portugal no Portal do Consumidor oficial.",
      ],
    ],
    [
      "5. Declaração de Acessibilidade Digital (WCAG 2.1 AA)",
      [
        "Trabalhamos continuamente para assegurar que este website seja totalmente acessível a todas as pessoas, incluindo cidadãos com limitações visuais, auditivas, motoras ou cognitivas, em conformidade com as normas internacionais WCAG 2.1 nível AA.",
        "O desenvolvimento prioriza: código semântico HTML5, rácios de contraste de cor elevados superiores a 7:1 em textos principais, navegação integral através do teclado com foco destacado (:focus-visible), alvos tácteis otimizados para dispositivos móveis (mínimo de 44x44 píxeis) e textos alternativos em elementos visuais.",
        "Se detetar alguma falha de acessibilidade ou tiver dificuldade em consultar qualquer conteúdo, entre em contacto direto connosco através do 963 572 411 para que possamos prestar apoio imediato e corrigir a situação.",
      ],
    ],
  ]
  return (
    <>
      <PageHero
        eyebrow="Legal & transparência"
        title="Transparência, Privacidade & Termos."
        intro="Conheça com clareza as nossas práticas de proteção de dados, ausência de cookies de rastreio, condições de reserva, livro de reclamações e compromisso de acessibilidade."
      />
      <section className="legal-layout">
        <aside>
          <p>Nesta página</p>
          {sections.map((s, i) => (
            <a href={`#legal-${i + 1}`} key={s[0]}>
              {s[0]}
            </a>
          ))}
        </aside>
        <div className="legal-content">
          {sections.map((section, i) => (
            <article id={`legal-${i + 1}`} key={section[0]}>
              <h2>{section[0]}</h2>
              {section[1].map((p) => (
                <p key={p}>{p}</p>
              ))}
              {i === 2 && (
                <div className="inline-links">
                  <PageLink page="galeria">
                    Consultar Galeria de Arte <Arrow />
                  </PageLink>
                  <PageLink page="reservas">
                    Pedir Reserva de Mesa <Arrow />
                  </PageLink>
                </div>
              )}
              {i === 3 && (
                <div className="inline-links">
                  <a
                    href="https://www.livroreclamacoes.pt"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Livro de Reclamações Eletrónico <Arrow />
                  </a>
                  <a
                    href="https://www.cniacc.pt"
                    target="_blank"
                    rel="noreferrer"
                  >
                    Centro Nacional de Arbitragem de Conflitos <Arrow />
                  </a>
                </div>
              )}
              {i === 4 && (
                <div className="inline-links">
                  <PageLink page="contactos">
                    Contactar a Gerência <Arrow />
                  </PageLink>
                </div>
              )}
            </article>
          ))}
        </div>
      </section>
    </>
  )
}

function NotFound() {
  return (
    <section className="not-found">
      <Eyebrow>Erro 404</Eyebrow>
      <h1>
        Esta página
        <br />
        <em>não está aqui.</em>
      </h1>
      <p>Regresse ao início para conhecer a casa, a cozinha e a galeria.</p>
      <LinkButton page="inicio">
        Voltar ao início <Arrow />
      </LinkButton>
    </section>
  )
}

function ArtworkModal({
  index,
  close,
  move,
}: {
  index: number
  close: () => void
  move: (amount: number) => void
}) {
  const art = artworks[index]
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") close()
      if (event.key === "ArrowLeft") move(-1)
      if (event.key === "ArrowRight") move(1)
    }
    document.addEventListener("keydown", onKey)
    document.body.classList.add("modal-open")
    return () => {
      document.removeEventListener("keydown", onKey)
      document.body.classList.remove("modal-open")
    }
  }, [close, move])
  return (
    <div
      className="modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="art-title"
    >
      <button className="modal-close" onClick={close}>
        Fechar <span aria-hidden="true">×</span>
      </button>
      <div className="modal-visual">
        <Placeholder label={art.title} />
      </div>
      <div className="modal-copy">
        <p className="eyebrow">
          {String(index + 1).padStart(2, "0")} / {artworks.length}
        </p>
        <h2 id="art-title">{art.title}</h2>
        <p className="technique">{art.technique}</p>
        <p>{art.description}</p>
        <small>
          Lito Silva · Obra original · Exposta na sala · Galeria Cachupa Rst
        </small>
        <div className="modal-nav">
          <button onClick={() => move(-1)}>← Anterior</button>
          <button onClick={() => move(1)}>Seguinte →</button>
        </div>
      </div>
    </div>
  )
}

function MobileBar() {
  return (
    <div className="mobile-bar">
      <a href={whatsappUrl} target="_blank" rel="noreferrer">
        Reservar mesa
      </a>
      <a href={mapsUrl} target="_blank" rel="noreferrer">
        Como chegar <Arrow />
      </a>
    </div>
  )
}

export default function App() {
  const [page, setPage] = useState<Page>(() =>
    pathToPage(window.location.pathname),
  )
  const [menuOpen, setMenuOpen] = useState(false)
  const [modalIndex, setModalIndex] = useState<number | null>(null)

  useEffect(() => {
    const click = (event: MouseEvent) => {
      const link = (event.target as HTMLElement).closest<HTMLAnchorElement>(
        "a[data-nav]",
      )
      if (!link || event.metaKey || event.ctrlKey || event.shiftKey) return
      event.preventDefault()
      const next = pathToPage(new URL(link.href).pathname)
      history.pushState({}, "", link.href)
      setPage(next)
      setMenuOpen(false)
      window.scrollTo({ top: 0, behavior: "smooth" })
    }
    const pop = () => {
      setPage(pathToPage(window.location.pathname))
      setMenuOpen(false)
      window.scrollTo(0, 0)
    }
    document.addEventListener("click", click)
    window.addEventListener("popstate", pop)
    return () => {
      document.removeEventListener("click", click)
      window.removeEventListener("popstate", pop)
    }
  }, [])

  const moveArtwork = (amount: number) =>
    setModalIndex((current) =>
      current === null
        ? null
        : (current + amount + artworks.length) % artworks.length,
    )
  const pages: Record<Page, ReactNode> = {
    inicio: <Home openArtwork={setModalIndex} />,
    casa: <House />,
    galeria: <Gallery openArtwork={setModalIndex} />,
    reservas: <Reservations />,
    contactos: <Contacts />,
    legal: <Legal />,
    "404": <NotFound />,
  }
  return (
    <>
      <a href="#conteudo" className="skip-link">
        Saltar para o conteúdo
      </a>
      <Header page={page} open={menuOpen} setOpen={setMenuOpen} />
      <main id="conteudo">{pages[page]}</main>
      {page !== "404" && <Footer />}
      <MobileBar />
      {modalIndex !== null && (
        <ArtworkModal
          index={modalIndex}
          close={() => setModalIndex(null)}
          move={moveArtwork}
        />
      )}
    </>
  )
}
