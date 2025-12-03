/**
 * ===============================================================================
 * MODULAR SEARCH COMPONENT
 * ===============================================================================
 * Reusable search functionality for Customer, Agent, and Vehicle entities
 * 
 * Features:
 * - Real-time search with debouncing
 * - Pagination support
 * - Integration with existing load functions
 */

/**
 * Initialize search functionality for an entity
 * 
 * @param {Object} config - Configuration object
 * @param {string} config.searchInputId - ID of the search input element
 * @param {string} config.searchEndpoint - API endpoint for search (e.g., '/api/customers/search')
 * @param {Function} config.loadFunction - Function to load/render data
 * @param {number} config.debounceDelay - Delay in ms before triggering search (default: 300)
 */
function initSearch(config) {
    const {
        searchInputId,
        searchEndpoint,
        loadFunction,
        debounceDelay = 300
    } = config;

    const searchInput = document.getElementById(searchInputId);

    if (!searchInput) {
        console.warn(`Search input with id "${searchInputId}" not found`);
        return;
    }

    let debounceTimer;
    let isSearching = false;

    // Event listener for search input
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);

        debounceTimer = setTimeout(() => {
            const query = e.target.value.trim();
            performSearch(query);
        }, debounceDelay);
    });

    /**
     * Perform search with the given query
     * @param {string} query - Search query string
     */
    async function performSearch(query) {
        isSearching = query.length > 0;

        if (!isSearching) {
            // If query is empty, reload all data
            loadFunction(1);
            return;
        }

        try {
            // Call the search endpoint
            const url = `${searchEndpoint}?q=${encodeURIComponent(query)}&page=1&limit=6`;
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Search failed: ${response.statusText}`);
            }

            const data = await response.json();

            // Use the existing load function's rendering logic
            // by temporarily overriding the data source
            renderSearchResults(data);

        } catch (error) {
            console.error('Search error:', error);
        }
    }

    /**
     * Render search results using the entity-specific rendering logic
     * @param {Object} data - Response data from search endpoint
     */
    function renderSearchResults(data) {
        // This function will be customized per entity
        // For now, we'll trigger a custom event that the entity-specific
        // JS can listen to
        const event = new CustomEvent('searchResultsReady', {
            detail: { data, isSearching }
        });
        document.dispatchEvent(event);
    }

    /**
     * Check if currently in search mode
     * @returns {boolean}
     */
    function isInSearchMode() {
        return isSearching;
    }

    // Return public API
    return {
        isInSearchMode,
        performSearch
    };
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { initSearch };
}
