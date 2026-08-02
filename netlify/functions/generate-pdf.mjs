import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';
import { findZoneById, getAllZones } from './pescaData.mjs';

// Colori coerenti con la palette del sito (style.css)
const COLORS = {
  primary: rgb(0.145, 0.388, 0.922),   // #2563eb
  dark: rgb(0.118, 0.161, 0.231),      // #1e293b
  text: rgb(0.059, 0.09, 0.165),       // #0f172a
  muted: rgb(0.392, 0.455, 0.545),     // #64748b
  light: rgb(0.973, 0.98, 0.988),      // #f8fafc
  border: rgb(0.886, 0.91, 0.941),     // #e2e8f0
  success: rgb(0.063, 0.725, 0.506),   // #10b981
  warning: rgb(0.961, 0.62, 0.043),    // #f59e0b
  white: rgb(1, 1, 1)
};

const CATEGORIA_COLORS = {
  verde: rgb(0.063, 0.725, 0.506),
  gialla: rgb(0.961, 0.62, 0.043),
  azzurra: rgb(0.055, 0.647, 0.914),
  rosa: rgb(0.925, 0.282, 0.6),
  rossa: rgb(0.937, 0.267, 0.267)
};

const PAGE = { width: 595.28, height: 841.89, margin: 48 };

// Helvetica usa la codifica WinAnsi: rimuove i caratteri non rappresentabili
function sanitize(text) {
  return String(text ?? '')
    .normalize('NFC')
    .replace(/[‘’]/g, "'")
    .replace(/[“”]/g, '"')
    .replace(/–|—/g, '-')
    .replace(/[^\x20-\x7E -ÿ€]/g, '');
}

function euro(value) {
  return `${value.toFixed(2).replace('.', ',')} EUR`;
}

class PdfBuilder {
  constructor(doc, fonts) {
    this.doc = doc;
    this.fonts = fonts;
    this.page = null;
    this.y = 0;
    this.pageCount = 0;
  }

  addPage() {
    this.page = this.doc.addPage([PAGE.width, PAGE.height]);
    this.pageCount += 1;
    this.y = PAGE.height - PAGE.margin;
    if (this.pageCount > 1) {
      this.y -= 8;
    }
    return this.page;
  }

  ensureSpace(height) {
    if (this.y - height < PAGE.margin + 24) {
      this.addPage();
    }
  }

  wrap(text, font, size, maxWidth) {
    const words = sanitize(text).split(/\s+/).filter(Boolean);
    const lines = [];
    let line = '';
    for (const word of words) {
      const candidate = line ? `${line} ${word}` : word;
      if (font.widthOfTextAtSize(candidate, size) > maxWidth && line) {
        lines.push(line);
        line = word;
      } else {
        line = candidate;
      }
    }
    if (line) lines.push(line);
    return lines;
  }

  text(str, { font = this.fonts.regular, size = 10, color = COLORS.text, x = PAGE.margin, maxWidth = PAGE.width - PAGE.margin * 2, lineGap = 3, spaceAfter = 0 } = {}) {
    const lines = this.wrap(str, font, size, maxWidth);
    for (const line of lines) {
      this.ensureSpace(size + lineGap);
      this.page.drawText(line, { x, y: this.y - size, size, font, color });
      this.y -= size + lineGap;
    }
    this.y -= spaceAfter;
  }

  rect(height, color, { x = PAGE.margin, width = PAGE.width - PAGE.margin * 2, radius = 0 } = {}) {
    this.page.drawRectangle({ x, y: this.y - height, width, height, color, borderRadius: radius });
  }

  divider() {
    this.ensureSpace(14);
    this.page.drawLine({
      start: { x: PAGE.margin, y: this.y - 6 },
      end: { x: PAGE.width - PAGE.margin, y: this.y - 6 },
      thickness: 0.75,
      color: COLORS.border
    });
    this.y -= 14;
  }
}

function drawHeader(builder, nome, contesto, dataStr) {
  const { page, fonts } = builder;
  page.drawRectangle({ x: 0, y: PAGE.height - 118, width: PAGE.width, height: 118, color: COLORS.dark });
  page.drawText('REPORT PRONTA-PESCA', {
    x: PAGE.margin, y: PAGE.height - 52, size: 24, font: fonts.bold, color: COLORS.white
  });
  page.drawText(sanitize('Cartina del Pescatore - Bacino n. 5 - Verbano, Lario, Ceresio'), {
    x: PAGE.margin, y: PAGE.height - 72, size: 11, font: fonts.regular, color: rgb(0.75, 0.82, 0.9)
  });
  const dedica = nome ? `Preparato per ${nome} il ${dataStr}` : `Generato il ${dataStr}`;
  page.drawText(sanitize(dedica), {
    x: PAGE.margin, y: PAGE.height - 92, size: 10, font: fonts.oblique, color: rgb(0.6, 0.68, 0.78)
  });
  builder.y = PAGE.height - 118 - 24;

  if (contesto) {
    builder.text(`Ricerca: ${contesto}`, { font: fonts.oblique, size: 10, color: COLORS.muted, spaceAfter: 10 });
  }
}

function drawZone(builder, zona) {
  const { fonts } = builder;
  builder.ensureSpace(120);

  // Barra colorata della categoria + titolo
  const catColor = CATEGORIA_COLORS[zona.categoria] || COLORS.muted;
  builder.page.drawRectangle({ x: PAGE.margin, y: builder.y - 16, width: 4, height: 16, color: catColor });
  builder.text(zona.nome, { font: fonts.bold, size: 14, x: PAGE.margin + 12, maxWidth: PAGE.width - PAGE.margin * 2 - 12, spaceAfter: 2 });

  const meta = `Categoria ${zona.categoria.toUpperCase()}  |  Provincia: ${zona.provincia}  |  Acque tipo ${zona.tipo_acqua}  |  Pesca: ${zona.tipo_pesca.replace('_', ' ')}`;
  builder.text(meta, { size: 8.5, color: COLORS.muted, x: PAGE.margin + 12, spaceAfter: 6 });

  builder.text(zona.descrizione, { size: 10, spaceAfter: 8 });

  builder.text('Documenti e requisiti necessari', { font: fonts.bold, size: 10.5, spaceAfter: 3 });
  for (const req of zona.requisiti) {
    const costo = req.costo > 0 ? ` - ${euro(req.costo)}` : ' - gratuito';
    const nota = req.note && req.note.toLowerCase() !== 'gratuito' ? ` (${req.note})` : '';
    const facolt = req.obbligatorio ? '' : ' [facoltativo]';
    builder.text(`• ${req.nome}${costo}${nota}${facolt}`, { size: 9.5, x: PAGE.margin + 12, maxWidth: PAGE.width - PAGE.margin * 2 - 12, lineGap: 2.5 });
  }
  builder.y -= 6;

  const costoTot = zona.costo_totale > 0 ? `Costo totale stimato: ${euro(zona.costo_totale)}` : 'Costo variabile: contattare i gestori';
  builder.ensureSpace(24);
  builder.rect(20, COLORS.light, { radius: 4 });
  builder.page.drawText(sanitize(costoTot), {
    x: PAGE.margin + 10, y: builder.y - 14, size: 10.5, font: fonts.bold, color: COLORS.primary
  });
  builder.y -= 26;

  if (zona.gestori && zona.gestori.length > 0) {
    builder.text('Gestori', { font: fonts.bold, size: 10, spaceAfter: 2 });
    for (const g of zona.gestori) {
      builder.text(`• ${g}`, { size: 9, x: PAGE.margin + 12, maxWidth: PAGE.width - PAGE.margin * 2 - 12 });
    }
    builder.y -= 4;
  }

  if (zona.note_particolari) {
    builder.text(`Attenzione: ${zona.note_particolari}`, { font: fonts.oblique, size: 9, color: COLORS.warning, spaceAfter: 4 });
  }

  builder.divider();
}

function drawInfoFinali(builder) {
  const { fonts } = builder;
  builder.ensureSpace(180);

  builder.text('Esenzioni', { font: fonts.bold, size: 12, color: COLORS.dark, spaceAfter: 3 });
  builder.text('Esonerati dalla licenza regionale: minorenni, over 65, diversamente abili. Esenti dai contributi: giovani nati dopo il 01/01/2008 (alcuni contributi) e disabili con Legge 104 art. 3 c. 3.', { size: 9.5, spaceAfter: 10 });

  builder.text('Contatti utili', { font: fonts.bold, size: 12, color: COLORS.dark, spaceAfter: 3 });
  builder.text('• A.P.S. Como F.I.P.S.A.S. - Tel: 031.302747 - info@aps-como.it', { size: 9.5, x: PAGE.margin + 12 });
  builder.text('• Sez. Prov. Lecco F.I.P.S.A.S. - Tel: 0341.350117 - fipsaslecco@libero.it', { size: 9.5, x: PAGE.margin + 12 });
  builder.text('• Sez. Prov. Varese F.I.P.S.A.S. - Tel: 0332.280386 - varese@fipsas.it', { size: 9.5, x: PAGE.margin + 12, spaceAfter: 10 });

  builder.text('Avvertenza', { font: fonts.bold, size: 10, color: COLORS.muted, spaceAfter: 2 });
  builder.text('Documento informativo generato automaticamente da dati pubblici A.T.S. delle Prealpi Lombarde F.I.P.S.A.S. Verifica sempre regolamenti e tariffe aggiornate sui canali ufficiali prima di pescare. Rispetta l\'ambiente e le normative vigenti.', { size: 8.5, color: COLORS.muted, spaceAfter: 14 });

  // Box promo Clan Pesca
  builder.ensureSpace(64);
  builder.rect(56, COLORS.dark, { radius: 6 });
  builder.page.drawText(sanitize('Ti è stato utile? Seguici su Instagram: @clanpesca'), {
    x: PAGE.margin + 14, y: builder.y - 22, size: 11, font: fonts.bold, color: COLORS.white
  });
  builder.page.drawText(sanitize('Tutorial, montaggi e spot sui laghi lombardi. E per andare sul serio: la Guida completa allo Spinning al Luccio - link in bio.'), {
    x: PAGE.margin + 14, y: builder.y - 40, size: 8.5, font: fonts.regular, color: rgb(0.75, 0.82, 0.9)
  });
  builder.y -= 62;
}

function drawFooters(doc, fonts) {
  const pages = doc.getPages();
  pages.forEach((page, i) => {
    page.drawText(sanitize(`Report Pronta-Pesca - clanpesca - pagina ${i + 1} di ${pages.length}`), {
      x: PAGE.margin, y: 24, size: 7.5, font: fonts.regular, color: COLORS.muted
    });
  });
}

async function buildPdf({ nome, zones, contesto }) {
  const doc = await PDFDocument.create();
  doc.setTitle('Report Pronta-Pesca - Bacino n. 5');
  doc.setAuthor('Clan Pesca');
  doc.setSubject('Zone di pesca, permessi e costi');

  const fonts = {
    regular: await doc.embedFont(StandardFonts.Helvetica),
    bold: await doc.embedFont(StandardFonts.HelveticaBold),
    oblique: await doc.embedFont(StandardFonts.HelveticaOblique)
  };

  const builder = new PdfBuilder(doc, fonts);
  builder.addPage();

  const dataStr = new Date().toLocaleDateString('it-IT', {
    day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Rome'
  });

  drawHeader(builder, nome, contesto, dataStr);

  builder.text(
    zones.length === 1
      ? 'Ecco tutto quello che ti serve per pescare in questa zona: documenti, costi e contatti in un unico foglio, da tenere con te anche offline.'
      : `Ecco tutto quello che ti serve per pescare nelle ${zones.length} zone trovate: documenti, costi e contatti in un unico documento, da tenere con te anche offline.`,
    { size: 10.5, spaceAfter: 12 }
  );

  for (const zona of zones) {
    drawZone(builder, zona);
  }

  drawInfoFinali(builder);
  drawFooters(doc, fonts);

  return doc.save();
}

export default async (req) => {
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  };

  if (req.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders });
  }

  if (req.method !== 'POST') {
    return new Response(
      JSON.stringify({ error: 'Metodo non consentito', message: 'Usa POST con un body JSON' }),
      { status: 405, headers: { 'Content-Type': 'application/json', ...corsHeaders } }
    );
  }

  try {
    const body = await req.json();
    const nome = sanitize(body.nome || '').slice(0, 60).trim();
    const contesto = sanitize(body.contesto || '').slice(0, 160).trim();
    const zoneIds = Array.isArray(body.zoneIds) ? body.zoneIds.slice(0, 20) : [];

    let zones = zoneIds.map(id => findZoneById(String(id))).filter(Boolean);
    if (zones.length === 0) {
      zones = getAllZones();
    }

    const pdfBytes = await buildPdf({ nome, zones, contesto });

    return new Response(pdfBytes, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="report-pronta-pesca.pdf"',
        ...corsHeaders
      }
    });
  } catch (error) {
    console.error('Errore nella generazione del PDF:', error);
    return new Response(
      JSON.stringify({ error: 'Errore interno del server', message: error.message }),
      { status: 500, headers: { 'Content-Type': 'application/json', ...corsHeaders } }
    );
  }
};

export const config = {
  path: '/api/generate-pdf'
};
