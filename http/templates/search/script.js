const AUTOCOMPLETE_FILE = "/static/autocomplete/words-10k.txt";
const MAX_SUGGESTIONS = 10;
const DEBOUNCE_DELAY_MS = 120;

const searchInput = document.getElementById("search-input");
const autocompleteList = document.getElementById("autocomplete-list");

let autocompleteItems = [];
let activeSuggestionIndex = -1;
let debounceTimer = null;

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
            .filter(Boolean);

        // Sorting allows prefix matches to appear predictably.
        autocompleteItems.sort((a, b) =>
            a.localeCompare(b, undefined, { sensitivity: "base" })
        );
    } catch (error) {
        console.error(error);
        autocompleteItems = [];
    }
}

function Search(event) {
    if (event) {
        event.preventDefault();
    }

    const searchText = searchInput.value.trim();
    closeAutocomplete();

    if(searchText.length == 0) return

    resp = GetSearch(searchText);

    alert(`Search: ${resp.term}`)
}

function GetSearch(text){
    
    return TestResp(text)

}

function TestResp(text){

    let resp = {
        term:text,
        info:{total:30, count:10},
        results:[
            {title:"Google", url:"https://www.google.com"},
            {title:"Gmail", url:"https://www.gmail.com"},
            {title:"Wikipedia", url:"https://www.wikipedia.com"}
        ]
    }
    return results
    
}

function getSuggestions(query) {
    const trimmedQuery = query.trimStart();

    if (!trimmedQuery) {
        return [];
    }

    const endsWithSpace = /\s$/.test(query);
    const words = trimmedQuery.split(/\s+/);

    let fixedWords;
    let partialWord;

    if (endsWithSpace) {
        // The user has completed the current phrase and is starting a new word.
        fixedWords = words;
        partialWord = "";
    } else {
        // Preserve all completed words and autocomplete only the final word.
        fixedWords = words.slice(0, -1);
        partialWord = words.at(-1) ?? "";
    }

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

        if (prefixMatches.length >= MAX_SUGGESTIONS) {
            break;
        }
    }

    const matches = [
        ...prefixMatches,
        ...containsMatches
    ].slice(0, MAX_SUGGESTIONS);

    return matches.map(match => {
        return [...fixedWords, match].join(" ");
    });
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
        activeSuggestionIndex =
            (activeSuggestionIndex + 1) % items.length;
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
