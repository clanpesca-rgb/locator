// Dati delle zone di pesca del Bacino n°5
// Convertito da Python a JavaScript

export const CONTRIBUTI = {
  licenza_regionale: 23.00,
  tessera_fipsas_adulti: 30.00,
    tessera_fipsas_giovani: 6.00,
  gestione_annuale: 30.00,
  gestione_ridotta: 15.00,
  natante_fipsas: 50.00
};

export const COORDINATE_BOUNDS = {
  lat_min: 45.0,
  lat_max: 46.5,
  lon_min: 8.0,
  lon_max: 10.5
};

export const ZONE_PESCA = [
  {
    id: "maggiore_riva",
    nome: "Lago Maggiore (Verbano) - Pesca da riva",
    categoria: "verde",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Varese",
    descrizione: "Pesca dalla riva nelle acque del Lago Maggiore (provincia di Varese)",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Contributo ridotto di gestione annuale", obbligatorio: true, costo: 15.00 }
    ],
    costo_totale: 68.00,
    bounding_box: {
      min: { lat: 45.7, lon: 8.5 },
      max: { lat: 46.15, lon: 8.75 }
    },
    note_particolari: "Chi ha versato il contributo di gestione annuale (€30) non deve pagare il contributo ridotto"
  },
  {
    id: "maggiore_natante",
    nome: "Lago Maggiore (Verbano) - Pesca da natante",
    categoria: "rosa",
    tipo_acqua: "A",
    tipo_pesca: "natante",
    provincia: "Varese",
    descrizione: "Pesca dalla barca nel Lago Maggiore (include Belly Boat a motore e Carp Fishing con barca)",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci specifico Lago Maggiore", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Contributo pesca da natante FIPSAS VA/NO/VCO", obbligatorio: true, costo: 50.00 }
    ],
    costo_totale: 103.00,
    bounding_box: {
      min: { lat: 45.7, lon: 8.5 },
      max: { lat: 46.15, lon: 8.75 }
    },
    note_particolari: "Richiede tesserino segnapesci specifico per Lago Maggiore approvato dalla Commissione Italo-Svizzera"
  },
  {
    id: "como_riva",
    nome: "Lago di Como (Lario) - Pesca da riva",
    categoria: "gialla",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Como/Lecco",
    descrizione: "Pesca da riva nelle acque lacustri e pesca nelle acque di tipo C",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera associativa F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 }
    ],
    costo_totale: 53.00,
    bounding_box: {
      min: { lat: 45.8, lon: 9.0 },
      max: { lat: 46.2, lon: 9.5 }
    }
  },
  {
    id: "como_barca",
    nome: "Lago di Como (Lario) - Pesca da barca",
    categoria: "azzurra",
    tipo_acqua: "B",
    tipo_pesca: "barca",
    provincia: "Como/Lecco",
    descrizione: "Pesca dalla barca nelle acque lacustri e acque di tipo B (include Belly Boat e Carp Fishing con barca)",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera associativa F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Contributo di gestione annuale", obbligatorio: true, costo: 30.00 }
    ],
    costo_totale: 83.00,
    bounding_box: {
      min: { lat: 45.8, lon: 9.0 },
      max: { lat: 46.2, lon: 9.5 }
    }
  },
  {
    id: "lugano_generale",
    nome: "Lago di Lugano (Ceresio)",
    categoria: "azzurra",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Como",
    descrizione: "Pesca nelle acque del Lago di Lugano",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera associativa F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Contributo di gestione annuale", obbligatorio: false, costo: 30.00, note: "Solo se pesca da barca" }
    ],
    costo_totale: 53.00,
    bounding_box: {
      min: { lat: 45.9, lon: 8.95 },
      max: { lat: 46.1, lon: 9.1 }
    },
    note_particolari: "Contributo di gestione necessario solo per pesca da barca"
  },
  {
    id: "varese_generale",
    nome: "Lago di Varese",
    categoria: "verde",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Varese",
    descrizione: "Pesca nel Lago di Varese",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Contributo ridotto gestione", obbligatorio: true, costo: 15.00 },
      { nome: "Permesso speciale per barca", obbligatorio: false, costo: 0.0, note: "Da richiedere se pesca da barca" }
    ],
    costo_totale: 68.00,
    bounding_box: {
      min: { lat: 45.8, lon: 8.7 },
      max: { lat: 45.85, lon: 8.8 }
    },
    note_particolari: "Per la pesca da barca è necessario permesso rilasciato da A.S.D. Sez. Prov. Varese F.I.P.S.A.S."
  },
  {
    id: "monate",
    nome: "Lago di Monate",
    categoria: "verde",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Varese",
    descrizione: "Pesca nel Lago di Monate - Solo residenti",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Residenza nei comuni rivieraschi", obbligatorio: true, costo: 0.0, note: "Obbligatoria per pesca da riva" }
    ],
    costo_totale: 53.00,
    bounding_box: {
      min: { lat: 45.75, lon: 8.63 },
      max: { lat: 45.78, lon: 8.67 }
    },
    note_particolari: "Pesca da riva riservata ai soli residenti. Pesca da barca NON consentita"
  },
  {
    id: "comabbio",
    nome: "Lago di Comabbio",
    categoria: "verde",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Varese",
    descrizione: "Pesca nel Lago di Comabbio - Solo residenti",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Tesserino segnapesci", obbligatorio: true, costo: 0.0, note: "Gratuito" },
      { nome: "Tessera F.I.P.S.A.S.", obbligatorio: true, costo: 30.00 },
      { nome: "Residenza nei comuni rivieraschi", obbligatorio: true, costo: 0.0, note: "Obbligatoria per pesca da riva" }
    ],
    costo_totale: 53.00,
    bounding_box: {
      min: { lat: 45.74, lon: 8.67 },
      max: { lat: 45.77, lon: 8.71 }
    },
    note_particolari: "Pesca da riva riservata ai soli residenti. Pesca da barca NON consentita"
  },
  {
    id: "pusiano_privato",
    nome: "Lago di Pusiano",
    categoria: "rossa",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Como",
    descrizione: "Acque a gestione privata",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Permesso del gestore", obbligatorio: true, costo: 0.0, note: "Variabile" }
    ],
    costo_totale: 0.0,
    bounding_box: {
      min: { lat: 45.80, lon: 9.26 },
      max: { lat: 45.83, lon: 9.30 }
    },
    gestori: ["Società Egirent - Tel: 342.6831440 - Email: amministrazione@lagopusiano.com"],
    note_particolari: "Necessario permesso rilasciato dalla società Egirent"
  },
  {
    id: "segrino_privato",
    nome: "Lago del Segrino",
    categoria: "rossa",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Como",
    descrizione: "Acque a gestione privata",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Permesso del gestore", obbligatorio: true, costo: 0.0, note: "Variabile" }
    ],
    costo_totale: 0.0,
    bounding_box: {
      min: { lat: 45.82, lon: 9.27 },
      max: { lat: 45.84, lon: 9.29 }
    },
    gestori: ["Azienda Agricola Gorla - Info: Redaelli Sport, via Volta 51, Canzo - Tel: 031.681637"],
    note_particolari: "Necessario permesso rilasciato dall'Azienda Agricola Gorla"
  },
  {
    id: "montorfano_privato",
    nome: "Lago di Montorfano",
    categoria: "rossa",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Como",
    descrizione: "Acque a gestione privata",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Permesso del gestore", obbligatorio: true, costo: 0.0, note: "Variabile" }
    ],
    costo_totale: 0.0,
    bounding_box: {
      min: { lat: 45.76, lon: 9.09 },
      max: { lat: 45.78, lon: 9.11 }
    },
    gestori: ["Associazione dei Pescatori del lago di Montorfano"],
    note_particolari: "Necessario permesso rilasciato dall'Associazione dei Pescatori"
  },
  {
    id: "annone_privato",
    nome: "Lago di Annone (parte a gestione privata)",
    categoria: "rossa",
    tipo_acqua: "A",
    tipo_pesca: "riva",
    provincia: "Lecco",
    descrizione: "Acque a gestione privata (esclusa porzione FIPSAS)",
    requisiti: [
      { nome: "Licenza regionale", obbligatorio: true, costo: 23.00 },
      { nome: "Permesso del gestore", obbligatorio: true, costo: 0.0, note: "Variabile" }
    ],
    costo_totale: 0.0,
    bounding_box: {
      min: { lat: 45.81, lon: 9.32 },
      max: { lat: 45.84, lon: 9.36 }
    },
    gestori: ["Amministrazione Eredi di Carlo Citterio - via Bagnolo 19, Oggiono - Tel: 349.4473337"],
    note_particolari: "Solo per la porzione non gestita da FIPSAS"
  }
];

// Funzione helper per verificare se le coordinate sono valide
export function isCoordinateValid(lat, lon) {
  return (
    lat >= COORDINATE_BOUNDS.lat_min &&
    lat <= COORDINATE_BOUNDS.lat_max &&
    lon >= COORDINATE_BOUNDS.lon_min &&
    lon <= COORDINATE_BOUNDS.lon_max
  );
}

// Funzione helper per verificare se una coordinata è in un bounding box
export function isInBoundingBox(lat, lon, bbox) {
  return (
    lat >= bbox.min.lat &&
    lat <= bbox.max.lat &&
    lon >= bbox.min.lon &&
    lon <= bbox.max.lon
  );
}

// Funzione per cercare zone per coordinate
export function findZonesByCoordinates(lat, lon) {
  return ZONE_PESCA.filter(zona => 
    isInBoundingBox(lat, lon, zona.bounding_box)
  );
}

// Funzione per cercare zone per nome
export function findZonesByName(searchTerm) {
  const term = searchTerm.toLowerCase();
  return ZONE_PESCA.filter(zona => 
    zona.nome.toLowerCase().includes(term)
  );
}

// Funzione per ottenere tutte le zone
export function getAllZones() {
  return ZONE_PESCA;
}

// Funzione per cercare zona per ID
export function findZoneById(id) {
  return ZONE_PESCA.find(zona => zona.id === id);
}
