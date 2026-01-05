import { findZonesByCoordinates, isCoordinateValid } from './pescaData.mjs';

export default async (req, context) => {
  // Gestisci CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      }
    });
  }

  try {
    let lat, lon;

    // Supporta sia GET che POST
    if (req.method === 'GET') {
      const url = new URL(req.url);
      lat = parseFloat(url.searchParams.get('lat'));
      lon = parseFloat(url.searchParams.get('lon'));
    } else if (req.method === 'POST') {
      const body = await req.json();
      lat = parseFloat(body.lat);
      lon = parseFloat(body.lon);
    }

    // Validazione input
    if (isNaN(lat) || isNaN(lon)) {
      return new Response(
        JSON.stringify({
          error: 'Parametri non validi',
          message: 'Latitudine e longitudine devono essere numeri validi'
        }),
        {
          status: 400,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
          }
        }
      );
    }

    // Verifica se le coordinate sono nel range valido
    const isValid = isCoordinateValid(lat, lon);
    
    // Cerca le zone
    const zones = findZonesByCoordinates(lat, lon);

    return new Response(
      JSON.stringify({
        success: true,
        coordinates: { lat, lon },
        isInValidRange: isValid,
        zones: zones,
        totalFound: zones.length
      }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );

  } catch (error) {
    console.error('Errore nella ricerca per coordinate:', error);
    
    return new Response(
      JSON.stringify({
        error: 'Errore interno del server',
        message: error.message
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    );
  }
};

export const config = {
  path: "/api/search-coordinates"
};
