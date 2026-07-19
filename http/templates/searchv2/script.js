const AUTOCOMPLETE_FILE = "/static/autocomplete/words-10k.txt";
const SEARCH_API_URL = "/api/search";
const MAX_SUGGESTIONS = 10;
const DEBOUNCE_DELAY_MS = 120;

const searchPage = document.getElementById("search-page");
const searchForm = document.getElementById("search-form");
const searchInput = document.getElementById("search-input");
const autocompleteList = document.getElementById("autocomplete-list");
const resultsBox = document.getElementById("results-box");

let autocompleteItems = [];
let activeSuggestionIndex = -1;
let debounceTimer = null;
let activeSearchController = null;

async function loadAutocompleteItems() {
    try {
        const response = await fetch(AUTOCOMPLETE_FILE);

        if (!response.ok) {
            throw new Error(`Unable to load autocomplete file: ${response.status}`);
        }

        const text = await response.text();

        autocompleteItems = text
            .split("\n")
            .map(item => item.trim())
            .filter(Boolean)
            .sort((a, b) =>
                a.localeCompare(b, undefined, { sensitivity: "base" })
            );
    } catch (error) {
        console.error(error);
        autocompleteItems = [];
    }
}

function hasSearchableText(value) {
    return /[\p{L}\p{N}]/u.test(value);
}

function prepareResultsView() {
    searchPage.classList.add("has-results");
    resultsBox.hidden = false;
    resultsBox.replaceChildren();

    const loader = document.createElement("div");
    loader.className = "results-loader";
    loader.setAttribute("role", "status");
    loader.setAttribute("aria-label", "Loading search results");

    const spinner = document.createElement("div");
    spinner.className = "loader-spinner";
    spinner.setAttribute("aria-hidden", "true");

    loader.appendChild(spinner);
    resultsBox.appendChild(loader);
}

function renderMessage(message) {
    resultsBox.replaceChildren();

    const text = document.createElement("p");
    text.className = "results-message";
    text.textContent = message;
    resultsBox.appendChild(text);
}

function normalizeResults(data) {
    if (Array.isArray(data)) {
        return data;
    }

    if (data && Array.isArray(data.results)) {
        return data.results;
    }

    return [];
}

function renderResults(results) {
    resultsBox.replaceChildren();

    if (results.length === 0) {
        renderMessage("No results found.");
        return;
    }

    const resultsList = document.createElement("div");
    resultsList.className = "results-list";

    results.forEach(result => {
        const title = String(result.title ?? "").trim();
        const href = String(result.href ?? result.url ?? "").trim();
        const body = String(result.body ?? result.description ?? "").trim();

        if (!title && !href && !body) {
            return;
        }

        const item = document.createElement("article");
        item.className = "result-item";

        if (href) {
            const url = document.createElement("span");
            url.className = "result-url";
            url.textContent = href;
            item.appendChild(url);
        }

        if (title) {
            if (href) {
                const link = document.createElement("a");
                link.className = "result-title";
                link.href = href;
                link.textContent = title;
                item.appendChild(link);
            } else {
                const heading = document.createElement("span");
                heading.className = "result-title";
                heading.textContent = title;
                item.appendChild(heading);
            }
        }

        if (body) {
            const description = document.createElement("p");
            description.className = "result-description";
            description.textContent = body;
            item.appendChild(description);
        }

        resultsList.appendChild(item);
    });

    if (!resultsList.hasChildNodes()) {
        renderMessage("No results found.");
        return;
    }

    resultsBox.appendChild(resultsList);
}

async function search(query) {
    if (activeSearchController) {
        activeSearchController.abort();
    }

    activeSearchController = new AbortController();
    const controller = activeSearchController;

    prepareResultsView();
    clearTimeout(debounceTimer);
    searchInput.value = "";
    closeAutocomplete();

    try {
        const params = new URLSearchParams({ query });
        const response = await fetch(`${SEARCH_API_URL}?${params.toString()}`, {
            method: "GET",
            signal: controller.signal
        });

        if (!response.ok) {
            throw new Error(`Search request failed: ${response.status}`);
        }

        const data = await response.json();
        renderResults(normalizeResults(data));
    } catch (error) {
        if (error.name !== "AbortError") {
            console.error(error);
            renderMessage("Unable to load search results.");
        }
    } finally {
        if (activeSearchController === controller) {
            activeSearchController = null;
        }
    }
}

function getSuggestions(query) {
    const trimmedQuery = query.trimStart();

    if (!trimmedQuery) {
        return [];
    }

    const endsWithSpace = /\s$/.test(query);
    const words = trimmedQuery.trimEnd().split(/\s+/);
    const fixedWords = endsWithSpace ? words : words.slice(0, -1);
    const partialWord = endsWithSpace ? "" : (words.at(-1) ?? "");
    const normalizedPartial = partialWord.toLocaleLowerCase();
    const prefixMatches = [];
    const containsMatches = [];

    for (const item of autocompleteItems) {
        const normalizedItem = item.toLocaleLowerCase();

        if (!normalizedPartial || normalizedItem.startsWith(normalizedPartial)) {
            prefixMatches.push(item);
        } else if (normalizedItem.includes(normalizedPartial)) {
            containsMatches.push(item);
        }
    }

    return [...prefixMatches, ...containsMatches]
        .slice(0, MAX_SUGGESTIONS)
        .map(match => [...fixedWords, match].join(" "));
}

function renderSuggestions(suggestions) {
    autocompleteList.replaceChildren();
    activeSuggestionIndex = -1;

    if (suggestions.length === 0) {
        closeAutocomplete();
        return;
    }

    const fragment = document.createDocumentFragment();

    suggestions.forEach((suggestion, index) => {
        const item = document.createElement("li");
        item.className = "autocomplete-item";
        item.setAttribute("role", "option");
        item.setAttribute("data-index", String(index));

        const icon = document.createElement("i");
        icon.className = "fa-solid fa-magnifying-glass";
        icon.setAttribute("aria-hidden", "true");

        const text = document.createElement("span");
        text.textContent = suggestion;

        item.append(icon, text);
        item.addEventListener("mousedown", event => {
            event.preventDefault();
            selectSuggestion(suggestion);
        });

        fragment.appendChild(item);
    });

    autocompleteList.appendChild(fragment);
    autocompleteList.hidden = false;
    searchInput.setAttribute("aria-expanded", "true");
}

function selectSuggestion(suggestion) {
    searchInput.value = suggestion;
    closeAutocomplete();
    searchInput.focus();
}

function closeAutocomplete() {
    autocompleteList.hidden = true;
    autocompleteList.replaceChildren();
    activeSuggestionIndex = -1;
    searchInput.setAttribute("aria-expanded", "false");
    searchInput.removeAttribute("aria-activedescendant");
}

function updateActiveSuggestion(items) {
    items.forEach((item, index) => {
        const isActive = index === activeSuggestionIndex;
        item.classList.toggle("active", isActive);
        item.setAttribute("aria-selected", String(isActive));

        if (isActive) {
            item.id = "active-autocomplete-option";
            searchInput.setAttribute(
                "aria-activedescendant",
                "active-autocomplete-option"
            );
            item.scrollIntoView({ block: "nearest" });
        } else {
            item.removeAttribute("id");
        }
    });
}

searchForm.addEventListener("submit", event => {
    event.preventDefault();

    const query = searchInput.value.trim();
    if (!hasSearchableText(query)) {
        return;
    }

    search(query);
});

searchInput.addEventListener("input", () => {
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(() => {
        const query = searchInput.value.trim();

        if (!query || autocompleteItems.length === 0) {
            closeAutocomplete();
            return;
        }

        renderSuggestions(getSuggestions(query));
    }, DEBOUNCE_DELAY_MS);
});

searchInput.addEventListener("keydown", event => {
    const items = Array.from(
        autocompleteList.querySelectorAll(".autocomplete-item")
    );

    if (items.length === 0) {
        return;
    }

    if (event.key === "ArrowDown") {
        event.preventDefault();
        activeSuggestionIndex = (activeSuggestionIndex + 1) % items.length;
        updateActiveSuggestion(items);
    } else if (event.key === "ArrowUp") {
        event.preventDefault();
        activeSuggestionIndex =
            (activeSuggestionIndex - 1 + items.length) % items.length;
        updateActiveSuggestion(items);
    } else if (event.key === "Enter" && activeSuggestionIndex >= 0) {
        event.preventDefault();
        selectSuggestion(
            items[activeSuggestionIndex].querySelector("span").textContent
        );
    } else if (event.key === "Escape") {
        closeAutocomplete();
    }
});

document.addEventListener("click", event => {
    if (!event.target.closest(".search-container")) {
        closeAutocomplete();
    }
});

loadAutocompleteItems();
