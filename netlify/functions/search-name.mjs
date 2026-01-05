import { findZonesByName } from './pescaData.mjs';

export const handler = async (event, context) => {
  // Gestisci CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
      body: ''
    };
  }

  try {
    let searchTerm;

    // Supporta sia GET che POST
    if (event.httpMethod === 'GET') {
      searchTerm = event.queryStringParameters?.name || event.queryStringParameters?.q;
    } else if (event.httpMethod === 'POST') {
      const body = JSON.parse(event.body);
      searchTerm = body.name || body.q;
    }

    // Validazione input
    if (!searchTerm || searchTerm.trim() === '') {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          success: false,
          error: 'Parametro mancante',
          message: 'Specificare un nome da cercare (parametro "name" o "q")'
        })
      };
    }

    // Cerca le zone
    const zones = findZonesByName(searchTerm);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        searchTerm: searchTerm,
        zones: zones,
        totalFound: zones.length
      })
    };

  } catch (error) {
    console.error('Errore nella ricerca per nome:', error);
    
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: false,
        error: 'Errore interno del server',
        message: error.message
      })
    };
  }
};
