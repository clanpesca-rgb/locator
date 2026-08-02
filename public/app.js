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
const pdfCta = document.getElementById('pdfCta');
const downloadPdfBtn = document.getElementById('downloadPdfBtn');
const pdfModal = document.getElementById('pdfModal');
const pdfModalClose = document.getElementById('pdfModalClose');
const pdfModalForm = document.getElementById('pdfModalForm');
const pdfModalThanks = document.getElementById('pdfModalThanks');
const pdfNome = document.getElementById('pdfNome');
const pdfEmail = document.getElementById('pdfEmail');
const pdfConsent = document.getElementById('pdfConsent');
const pdfModalError = document.getElementById('pdfModalError');
const pdfGenerateBtn = document.getElementById('pdfGenerateBtn');

// Ultima ricerca: serve per generare il PDF personalizzato
let lastZones = [];
let lastContext = '';

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

    lastZones = zones;
    lastContext = title;
    pdfCta.style.display = zones.length > 0 ? 'flex' : 'none';

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
    pdfCta.style.display = 'none';
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

// ===== Download PDF personalizzato =====

downloadPdfBtn.addEventListener('click', openPdfModal);
pdfModalClose.addEventListener('click', closePdfModal);
pdfModal.addEventListener('click', (e) => {
    if (e.target === pdfModal) closePdfModal();
});
pdfGenerateBtn.addEventListener('click', handlePdfDownload);
pdfEmail.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handlePdfDownload();
});

function openPdfModal() {
    pdfModalForm.style.display = 'block';
    pdfModalThanks.style.display = 'none';
    pdfModalError.style.display = 'none';
    pdfModal.style.display = 'flex';
    pdfEmail.focus();
}

function closePdfModal() {
    pdfModal.style.display = 'none';
}

function showPdfError(message) {
    pdfModalError.textContent = message;
    pdfModalError.style.display = 'block';
}

/**
 * Registra il contatto su Netlify Forms.
 * Se fallisce (es. in sviluppo locale) non blocca il download.
 */
async function submitLead(nome, email, contesto) {
    try {
        await fetch('/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                'form-name': 'lead-pdf',
                nome,
                email,
                contesto
            }).toString()
        });
    } catch (error) {
        console.warn('Invio lead non riuscito:', error);
    }
}

async function handlePdfDownload() {
    const email = pdfEmail.value.trim();
    const nome = pdfNome.value.trim();

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
        showPdfError('Inserisci un indirizzo email valido');
        return;
    }
    if (!pdfConsent.checked) {
        showPdfError('Per scaricare il PDF devi accettare la casella qui sopra');
        return;
    }

    pdfModalError.style.display = 'none';
    pdfGenerateBtn.disabled = true;
    pdfGenerateBtn.textContent = 'Preparo il tuo PDF...';

    try {
        await submitLead(nome, email, lastContext);

        const response = await fetch(`${API_BASE}/generate-pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nome,
                contesto: lastContext,
                zoneIds: lastZones.map(z => z.id)
            })
        });

        if (!response.ok) {
            throw new Error(`Errore del server (${response.status})`);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'report-pronta-pesca.pdf';
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(url);

        pdfModalForm.style.display = 'none';
        pdfModalThanks.style.display = 'block';
    } catch (error) {
        console.error('Errore nella generazione del PDF:', error);
        showPdfError('Non sono riuscito a generare il PDF. Riprova tra qualche istante.');
    } finally {
        pdfGenerateBtn.disabled = false;
        pdfGenerateBtn.textContent = 'Scarica il PDF';
    }
}

// Log di inizializzazione
console.log('🎣 Cartina del Pescatore - App caricata');
console.log('API Base URL:', API_BASE);
