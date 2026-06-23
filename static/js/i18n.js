/**
 * AgriPredict AI - Multi-Language Support (i18n)
 * Loads translations from JSON files and applies them to the DOM.
 * Saves the selected language in localStorage.
 */

const SUPPORTED_LANGS = {
    'en': 'English',
    'te': 'తెలుగు',
    'hi': 'हिंदी',
    'ta': 'தமிழ்',
    'kn': 'ಕನ್ನಡ'
};

let currentTranslations = {};

/**
 * Fetches the JSON translation file and applies translations.
 * @param {string} lang - Language code (e.g. 'te', 'hi')
 */
async function setLanguage(lang) {
    if (!SUPPORTED_LANGS[lang]) lang = 'en';

    try {
        const response = await fetch(`/static/lang/${lang}.json?v=${Date.now()}`);
        if (!response.ok) throw new Error('Translation file not found');
        currentTranslations = await response.json();
    } catch (e) {
        console.warn(`Could not load language: ${lang}. Falling back to English.`, e);
        lang = 'en';
        const resp = await fetch(`/static/lang/en.json`);
        currentTranslations = await resp.json();
    }

    // Apply translations to all elements with data-i18n attribute
    applyTranslations();
    populateCommodities();
    populateStates();

    // Notify other scripts (e.g. dashboard topbar) that language is ready
    document.dispatchEvent(new CustomEvent('i18nReady', { detail: { lang } }));

    // Persist the choice
    localStorage.setItem('agriLang', lang);

    // Update the active state of the dropdown
    document.querySelectorAll('.lang-option').forEach(el => {
        el.classList.toggle('active-lang', el.dataset.lang === lang);
    });

    // Also update sidebar lang options if present
    document.querySelectorAll('.sidebar-nav-item.dropdown-toggle + .dropdown-menu .lang-option').forEach(el => {
        el.classList.toggle('active-lang', el.dataset.lang === lang);
    });

    // Update the navbar flag & label
    const langBtnLabel = document.getElementById('langBtnLabel');
    if (langBtnLabel) {
        langBtnLabel.textContent = SUPPORTED_LANGS[lang];
    }
    const sidebarLangLabel = document.getElementById('sidebarLangLabel');
    if (sidebarLangLabel) {
        sidebarLangLabel.textContent = SUPPORTED_LANGS[lang];
    }
}

/**
 * Populates the state dropdown with translated state names.
 * The `value` stays in English so Flask routing works correctly.
 */
function populateStates() {
    const stateSelects = [
      document.getElementById('p_state'),
      document.getElementById('mkt_state')
    ];
    
    stateSelects.forEach(stateSelect => {
      if (!stateSelect) return;

    const states = [
        'Andhra Pradesh', 'Telangana', 'Karnataka', 'Tamil Nadu', 'Maharashtra'
    ];

    const currentVal = stateSelect.value;
    // Clear all except the disabled placeholder (index 0)
    while (stateSelect.options.length > 1) stateSelect.remove(1);

    states.forEach(name => {
        const option = document.createElement('option');
        option.value = name;
        option.textContent = currentTranslations[`state_${name}`] || name;
        stateSelect.appendChild(option);
    });

    if (currentVal) {
        stateSelect.value = currentVal;
        // Re-populate districts for the selected state with new language
        if (currentVal) window.updateDistricts && window.updateDistricts(true, (stateSelect.id.indexOf('mkt') === 0 ? 'mkt' : 'p'));
    }
  });
}

/**
 * Translates district names when a state is selected.
 * Called from inline onchange in dashboard.html.
 */
window.updateDistricts = function(preserveSelection, prefix) {
    prefix = prefix || 'p'; // default to prediction form
    const stateSelect = document.getElementById(prefix + '_state');
    const districtSelect = document.getElementById(prefix + '_district');
    if (!stateSelect || !districtSelect || !window._locationsData) return;

    const selectedState = stateSelect.value;
    const placeholderText = currentTranslations['dash_district_placeholder'] || 'Choose your district...';

    districtSelect.innerHTML = `<option value="" selected disabled>${placeholderText}</option>`;

    const savedDistrict = preserveSelection ? districtSelect.dataset.lastVal : null;

    if (selectedState && window._locationsData[selectedState]) {
        window._locationsData[selectedState].forEach(district => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = currentTranslations[`district_${district}`] || district;
            districtSelect.appendChild(option);
        });
        districtSelect.disabled = false;
        if (savedDistrict) districtSelect.value = savedDistrict;
    } else {
        districtSelect.disabled = true;
    }
    // Save last selection for language switch re-render
    districtSelect.dataset.lastVal = districtSelect.value;
};

// Listen for district select changes to save the value
document.addEventListener('change', function(e) {
    if (e.target && (e.target.id === 'p_district' || e.target.id === 'mkt_district')) {
        e.target.dataset.lastVal = e.target.value;
    }
});

/**
 * Populates the commodity dropdown with translated names.
 * The `value` stays in English so the ML model receives the correct input.
 * The displayed text is translated via the i18n JSON files.
 */
function populateCommodities() {
    const selects = [
      document.getElementById('p_commodity'),
      document.getElementById('mkt_commodity'),
      document.getElementById('calc_commodity')
    ];
    
    selects.forEach(select => {
      if (!select) return; // Not on the dashboard page

    // All commodity keys — English values used by the ML model
    const commodities = [
        'Apple', 'Banana', 'Brinjal', 'Cabbage', 'Carrot', 'Cauliflower',
        'Garlic', 'Ginger', 'Green Chilli', 'Grapes', 'Mango', 'Onion',
        'Orange', 'Papaya', 'Pomegranate', 'Potato', 'Spinach', 'Tomato', 'Watermelon'
    ];

    // Remember the currently selected value before rebuilding
    const currentVal = select.value;

    // Clear existing options (except the first disabled placeholder)
    while (select.options.length > 1) select.remove(1);

    // Re-add options with translated display text
    commodities.forEach(name => {
        const option = document.createElement('option');
        option.value = name; // English value — sent to Flask/ML model
        option.textContent = currentTranslations[`commodity_${name}`] || name;
        select.appendChild(option);
    });

    // Restore selection if it was previously set
    if (currentVal) select.value = currentVal;
  });
}

/**
 * Applies the loaded translations to all matching elements in the DOM.
 */
function applyTranslations() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = currentTranslations[key];
        if (!translation) return;

        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
            el.placeholder = translation;
        } else if (el.tagName === 'OPTION') {
            el.textContent = translation;
        } else {
            el.textContent = translation;
        }
    });

    document.querySelectorAll('[data-i18n-label]').forEach(el => {
        const key = el.getAttribute('data-i18n-label');
        const translation = currentTranslations[key];
        if (translation) el.textContent = translation;
    });

    // Build advisory message in selected language
    applyAdvisory();
    // Translate market names with local suffix
    applyMarketNames();
    // Translate results subtitle (commodity and location)
    applySubtitle();
}

/**
 * Translates the commodity and location names in the results subtitle.
 */
function applySubtitle() {
    const el = document.getElementById('resultsSubtitle');
    if (!el) return;

    const commodity = el.dataset.commodity;
    const location = el.dataset.location;

    const commName = el.querySelector('.commodity-name');
    const locName = el.querySelector('.location-name');

    if (commName) commName.textContent = currentTranslations[`commodity_${commodity}`] || commodity;
    if (locName) {
        // Location can be State or District. Check both.
        const translatedLoc = currentTranslations[`district_${location}`] || 
                            currentTranslations[`state_${location}`] || 
                            location;
        locName.textContent = translatedLoc;
    }
}

/**
 * Builds the farmer advisory text using template keys from the JSON file.
 * The advisory element carries data-adv-* attributes set by Flask.
 */
function applyAdvisory() {
    const el = document.getElementById('advisoryText');
    if (!el) return;

    const type = el.dataset.advType;              // e.g. "increasing_storable"
    const severityKey = el.dataset.advSeverity;   // "slightly" | "moderately" | "significantly"
    const pct = el.dataset.advPct;                // e.g. "8.3"
    const commodity = el.dataset.advCommodity;    // English name e.g. "Tomato"
    const weatherKey = el.dataset.advWeather;     // "" | "heavy_rain" | "monsoon_rain" | "high_humidity"

    const templateKey = `adv_${type}`;
    let template = currentTranslations[templateKey];
    if (!template) return; // Fallback: keep existing text

    const severityText = currentTranslations[`adv_sev_${severityKey}`] || severityKey;
    const weatherText  = weatherKey ? (currentTranslations[`adv_weather_${weatherKey}`] || '') : '';

    // Translate commodity name for display
    const commodityDisplay = currentTranslations[`commodity_${commodity}`] || commodity;

    // Replace template placeholders
    const advisory = template
        .replace(/\{commodity\}/g, commodityDisplay)
        .replace(/\{severity\}/g, severityText)
        .replace(/\{pct\}/g, pct)
        .replace(/\{weather\}/g, weatherText);

    el.textContent = advisory;
}

/**
 * Translates market name labels on the results page.
 * Each .market-name element has data-district and data-is-selected attributes.
 */
function applyMarketNames() {
    const suffix  = currentTranslations['market_suffix']   || 'Market';
    const selected = currentTranslations['market_selected'] || '(Selected)';

    document.querySelectorAll('.market-name').forEach(el => {
        const district = el.dataset.district;
        const isSelected = el.dataset.isSelected === 'true';
        const districtName = currentTranslations[`district_${district}`] || district;
        el.textContent = `${districtName} ${suffix}${isSelected ? ' ' + selected : ''}`;
    });
}

/**
 * Initializes the language system on page load.
 */
function initLanguage() {
    const savedLang = localStorage.getItem('agriLang') || 'en';
    setLanguage(savedLang);
}

// Ensure we re-apply when charts or dynamic content render
document.addEventListener('DOMContentLoaded', () => {
    initLanguage();

    // Bind click events for language switcher items
    document.querySelectorAll('.lang-option').forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            setLanguage(el.dataset.lang);
        });
    });
});

// Expose helper for use in templates
window.i18n = (key) => currentTranslations[key] || key;
