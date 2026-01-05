// API Base URL (cambia in produzione se necessario)
const API_BASE = '/api';

// Elementi DOM
const gpsBtn = document.getElementById('gpsBtn');
const searchCoordsBtn = document.getElementById('searchCoordsBtn');
const searchNameBtn = document.getElementById('searchNameBtn');
const showAllBtn = document.getElementById('showAllBtn');
const latInput = document.getElementById('latInput');
const lonInput = document.getElementById('lonInput');
const nameInput = document.getElementById('nameInput');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsSection = document.getElementById('resultsSection');
const resultsTitle = document.getElementById('resultsTitle');
const resultsCount = document.getElementById('resultsCount');
const resultsContainer = document.getElementById('resultsContainer');

// Event Listeners
gpsBtn.addEventListener('click', handleGPSSearch);
searchCoordsBtn.addEventListener('click', handleManualCoordinatesSearch);
searchNameBtn.addEventListener('click', handleNameSearch);
showAllBtn.addEventListener('click', handleShowAll);

// Enter key per ricerca nome
nameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleNameSearch();
    }
});

// Enter key per ricerca coordinate
latInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleManualCoordinatesSearch();
    }
});

lonInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleManualCoordinatesSearch();
    }
});

/**
 * Gestisce la ricerca tramite GPS
 */
async function handleGPSSearch() {
    // Verifica se la geolocalizzazione è supportata
    if (!navigator.geolocation) {
        showError('La geolocalizzazione non è supportata dal tuo browser');
        return;
    }

    showLoading();
    gpsBtn.disabled = true;
    gpsBtn.innerHTML = '<span class="btn-icon">⏳</span>Rilevamento posizione...';

    navigator.geolocation.getCurrentPosition(
        async (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            console.log('Posizione GPS rilevata:', lat, lon);

            try {
                const response = await fetch(`${API_BASE}/search-coordinates?lat=${lat}&lon=${lon}`);
                const data = await response.json();

                if (data.success) {
                    displayResults(data.zones, `Zone trovate per la tua posizione (${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E)`);
                    
                    if (!data.isInValidRange) {
                        showWarning('La tua posizione è fuori dal range del Bacino n°5. I risultati potrebbero non essere accurati.');
                    }
                } else {
                    showError('Errore nella ricerca: ' + (data.message || 'Errore sconosciuto'));
                }
            } catch (error) {
                console.error('Errore nella chiamata API:', error);
                showError('Errore di connessione. Riprova più tardi.');
            } finally {
                hideLoading();
                resetGPSButton();
            }
        },
        (error) => {
            console.error('Errore geolocalizzazione:', error);
            hideLoading();
            resetGPSButton();

            let errorMessage = 'Impossibile ottenere la posizione GPS. ';
            switch (error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage += 'Permesso negato. Abilita la geolocalizzazione nelle impostazioni del browser.';
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage += 'Posizione non disponibile.';
                    break;
                case error.TIMEOUT:
                    errorMessage += 'Timeout nella richiesta.';
                    break;
                default:
                    errorMessage += 'Errore sconosciuto.';
            }
            showError(errorMessage);
        },
        {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 0
        }
    );
}

/**
 * Ripristina il pulsante GPS
 */
function resetGPSButton() {
    gpsBtn.disabled = false;
    gpsBtn.innerHTML = '<span class="btn-icon">📍</span>Usa la Mia Posizione GPS';
}

/**
 * Gestisce la ricerca manuale per coordinate
 */
async function handleManualCoordinatesSearch() {
    const lat = parseFloat(latInput.value);
    const lon = parseFloat(lonInput.value);

    if (isNaN(lat) || isNaN(lon)) {
        showError('Inserisci coordinate valide (numeri decimali)');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/search-coordinates?lat=${lat}&lon=${lon}`);
        const data = await response.json();

        if (data.success) {
            displayResults(data.zones, `Zone trovate per coordinate ${lat.toFixed(4)}°N, ${lon.toFixed(4)}°E`);
            
            if (!data.isInValidRange) {
                showWarning('Le coordinate inserite sono fuori dal range del Bacino n°5. I risultati potrebbero non essere accurati.');
            }
        } else {
            showError('Errore nella ricerca: ' + (data.message || 'Errore sconosciuto'));
        }
    } catch (error) {
        console.error('Errore nella chiamata API:', error);
        showError('Errore di connessione. Riprova più tardi.');
    } finally {
        hideLoading();
    }
}

/**
 * Gestisce la ricerca per nome
 */
async function handleNameSearch() {
    const searchTerm = nameInput.value.trim();

    if (!searchTerm) {
        showError('Inserisci un nome da cercare');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_BASE}/search-name?name=${encodeURIComponent(searchTerm)}`);
        const data = await response.json();

        if (data.success) {
            displayResults(data.zones, `Risultati per "${searchTerm}"`);
        } else {
            showError('Errore nella ricerca: ' + (data.message || 'Errore sconosciuto'));
        }
    } catch (error) {
        console.error('Errore nella chiamata API:', error);
        showError('Errore di connessione. Riprova più tardi.');
    } finally {
        hideLoading();
    }
}

/**
 * Mostra tutte le zone
 */
async function handleShowAll() {
    showLoading();

    try {
        const response = await fetch(`${API_BASE}/all-zones`);
        const data = await response.json();

        if (data.success) {
            displayResults(data.zones, 'Tutte le Zone Disponibili');
        } else {
            showError('Errore nel caricamento: ' + (data.message || 'Errore sconosciuto'));
        }
    } catch (error) {
        console.error('Errore nella chiamata API:', error);
        showError('Errore di connessione. Riprova più tardi.');
    } finally {
        hideLoading();
    }
}

/**
 * Visualizza i risultati
 */
function displayResults(zones, title) {
    resultsTitle.textContent = title;
    resultsCount.textContent = `${zones.length} ${zones.length === 1 ? 'zona' : 'zone'}`;
    resultsContainer.innerHTML = '';

    if (zones.length === 0) {
        resultsContainer.innerHTML = `
            <div class="zone-card text-center">
                <h3>❌ Nessuna zona trovata</h3>
                <p class="text-muted">Prova a modificare i criteri di ricerca</p>
            </div>
        `;
    } else {
        zones.forEach(zone => {
            const zoneCard = createZoneCard(zone);
            resultsContainer.appendChild(zoneCard);
        });
    }

    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Crea una card per una zona
 */
function createZoneCard(zone) {
    const card = document.createElement('div');
    card.className = 'zone-card';

    const categoriaClass = `badge-${zone.categoria}`;
    const costoDisplay = zone.costo_totale > 0 
        ? `€ ${zone.costo_totale.toFixed(2)}` 
        : 'Variabile - contattare i gestori';

    let requisitiHTML = '<ul class="requirements-list">';
    zone.requisiti.forEach(req => {
        const optionalClass = req.obbligatorio ? '' : 'requirement-optional';
        const costoText = req.costo > 0 ? ` (€ ${req.costo.toFixed(2)})` : '';
        const noteText = req.note ? ` - ${req.note}` : '';
        requisitiHTML += `<li class="${optionalClass}">${req.nome}${costoText}${noteText}</li>`;
    });
    requisitiHTML += '</ul>';

    let gestoriHTML = '';
    if (zone.gestori && zone.gestori.length > 0) {
        gestoriHTML = `
            <div class="zone-section">
                <h4>👥 Gestori</h4>
                <ul class="requirements-list">
                    ${zone.gestori.map(g => `<li>${g}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    let noteHTML = '';
    if (zone.note_particolari) {
        noteHTML = `
            <div class="note-warning">
                <strong>⚠️ Nota:</strong> ${zone.note_particolari}
            </div>
        `;
    }

    card.innerHTML = `
        <div class="zone-header">
            <div>
                <h3 class="zone-title">🎣 ${zone.nome}</h3>
                <div class="zone-meta">
                    <span class="badge ${categoriaClass}">${zone.categoria.toUpperCase()}</span>
                    <span class="zone-tag">📫 ${zone.provincia}</span>
                    <span class="zone-tag">🌊 Tipo ${zone.tipo_acqua}</span>
                    <span class="zone-tag">🎣 ${zone.tipo_pesca.replace('_', ' ')}</span>
                </div>
            </div>
        </div>
        
        <p class="zone-description">${zone.descrizione}</p>
        
        <div class="zone-section">
            <h4>✅ Requisiti Necessari</h4>
            ${requisitiHTML}
        </div>
        
        <div class="cost-highlight">
            💰 Costo totale stimato: ${costoDisplay}
        </div>
        
        ${gestoriHTML}
        ${noteHTML}
    `;

    return card;
}

/**
 * Mostra l'indicatore di caricamento
 */
function showLoading() {
    loadingIndicator.style.display = 'block';
    resultsSection.style.display = 'none';
}

/**
 * Nasconde l'indicatore di caricamento
 */
function hideLoading() {
    loadingIndicator.style.display = 'none';
}

/**
 * Mostra un messaggio di errore
 */
function showError(message) {
    resultsTitle.textContent = 'Errore';
    resultsCount.textContent = '';
    resultsContainer.innerHTML = `
        <div class="zone-card">
            <h3 style="color: var(--danger-color);">❌ ${message}</h3>
        </div>
    `;
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Mostra un avviso
 */
function showWarning(message) {
    const warningDiv = document.createElement('div');
    warningDiv.className = 'note-warning';
    warningDiv.innerHTML = `<strong>⚠️ Attenzione:</strong> ${message}`;
    resultsContainer.insertBefore(warningDiv, resultsContainer.firstChild);
}

// Log di inizializzazione
console.log('🎣 Cartina del Pescatore - App caricata');
console.log('API Base URL:', API_BASE);
