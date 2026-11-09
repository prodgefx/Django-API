const contentContainer = document.getElementById("Content-container");
const loginForm = document.getElementById("login-form");
const searchForm = document.getElementById("search-form");
const baseEndpoint = "http://localhost:8000/api";

if (loginForm) {
    loginForm.addEventListener("submit", handleLogin);
}

if (searchForm) {
    searchForm.addEventListener("submit", handleSearch);
}

function writeToContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = "<pre>" + JSON.stringify(data, null, 4) + "</pre>";
    }
}

function handleLogin(event) {
    event.preventDefault();

    const loginEndpoint = `${baseEndpoint}/token/`;
    const loginFormData = new FormData(loginForm);
    const loginObjectData = Object.fromEntries(loginFormData);

    console.log(loginObjectData);

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginObjectData)
    };

    fetch(loginEndpoint, options)
        .then(response => {
            console.log(response);

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            return response.json();
        })
        .then(authData => handleAuthData(authData, getProductList))
        .catch(err => {
            console.error(err);
        });
}

function handleSearch(event) {
    event.preventDefault()
    let formData = new FormData(searchForm)
    let data = Object.fromEntries(formData)
    let searchParams = new URLSearchParams(data)
    const endpoint = `${baseEndpoint}/search/?${searchParams}`
    const headers = {
        "Content-Type": "application/json",
    }
    const authToken = localStorage.getItem('access') 
    if (authToken) {
        headers['Authorization'] = `Bearer ${authToken}`
    }
    const options = {
        method: "GET",
        headers: headers
    }
    fetch(endpoint, options) //  Promise
    .then(response=>{
        return response.json()
    })
    .then(data => {
        const validData = isTokenNotValid(data)
        if (validData && contentContainer){
            contentContainer.innerHTML = ""
            if (data && data.hits) {
                let htmlStr  = ""
                for (let result of data.hits) {
                    htmlStr += "<li>"+ result.title + "</li>"
                }
                contentContainer.innerHTML = htmlStr
                if (data.hits.length === 0) {
                    contentContainer.innerHTML = "<p>No results found</p>"
                }
            } else {
                contentContainer.innerHTML = "<p>No results found</p>"
            }
        }
    })
    .catch(err=> {
        console.log('err', err)
    })
}


function handleAuthData(authData, callback) {
    localStorage.setItem('access', authData.access);
    localStorage.setItem('refresh', authData.refresh);

    if (callback) {
        callback();
    }
}

function getFetchOptions(method, body) {
    return {
        method: method === null ? "GET" : method,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem('access')}`
        },
        body: body ? JSON.stringify(body) : null
    };
}

function isTokenNotValid(jsonData) {
    if (jsonData.code && jsonData.code == "token_not_valid") {
        alert("Please login again");
        return false;
    }

    return true;
}

function validateJWTToken() {
    const endpoint = `${baseEndpoint}/token/verify/`;

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            token: localStorage.getItem('access')
        })
    };

    fetch(endpoint, options)
        .then(response => response.json())
        .then(x => {
            // refresh token placeholder
        });
}

function getProductList() {
    const endpoint = `${baseEndpoint}/products/`;
    const options = getFetchOptions("GET");

    fetch(endpoint, options)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            return response.json();
        })
        .then(data => {
            console.log(data);
            writeToContainer(data);
        })
        .catch(err => {
            console.error("Failed to fetch products:", err);
        });
}


const { liteClient: algoliasearch } = window["algoliasearch/lite"];

const appID = "84UVUOMXPU";
const apiKey = "965cdd15a5fb3630157167b91725171f";
const indexName = "cfe_Product";

const searchClient = algoliasearch(appID, apiKey);

const search = instantsearch({
  indexName,
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: "#searchbox",
  }),

  instantsearch.widgets.clearRefinements({
    container: "#clear-refinements"
}),


  instantsearch.widgets.refinementList({
    container: "#user-list",
    attribute: 'user'
  }),

  instantsearch.widgets.refinementList({
    container: "#public-list",
    attribute: 'public'
  }),

  instantsearch.widgets.hits({
    container: "#hits",
    templates: {
        item: `
            <div>
                <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
                <div>{{#helpers.highlight}}{ "attribute": "body" }{{/helpers.highlight}}</div>
                
                <p>{{ user }}</p><p>\${{ price }}
            
            
            </div>`
    }
  }),
]);

search.start();