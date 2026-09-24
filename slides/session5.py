SESSION = {
    "n": 5,
    "title": "Identity, Security, and Software Beyond the Browser",
    "subtitle": "How the server knows who is asking, how to keep it safe, and how phones, desktops, devices, and AI fit in",
    "sections": [
        {"id": "s5-1", "title": "5.1 Authentication versus authorization", "slides": [
            {"title": "Two questions", "bullets": [
                "<b>Authentication</b>: \"Who are you?\" Password, phone code, fingerprint, Google login",
                "<b>Authorization</b>: \"What may you do?\" May Dana see order 90? Sam's order 88? Issue a refund?",
                "Office building: the badge check is authentication; which doors open is authorization",
                "Authorization is organised by <b>roles</b>: customer, staff, manager, administrator",
            ], "takeaway": "Every request touching a record must check that THIS user may touch THIS record. Forgetting that has caused huge leaks."},
        ]},
        {"id": "s5-2", "title": "5.2 Passwords done right", "slides": [
            {"title": "Never store the password", "bullets": [
                "Store a <b>hash</b>: a one-way scramble that cannot be reversed. Check a login by hashing what was typed",
                "A stolen database then reveals no passwords. (Salted, with slow algorithms such as bcrypt)",
                "If a company can email you your old password, it is doing this wrong",
                "<b>Multi-factor authentication</b>: something you know + something you have (or are). Require it for staff",
                "<b>Passkeys</b>: a device-held key unlocked by fingerprint or face; no password at all",
            ]},
        ]},
        {"id": "s5-3", "title": "5.3 Staying logged in: cookies, sessions, tokens", "slides": [
            {"title": "How a login survives stateless HTTP", "fig": "s5-3-1", "bullets": [
                "The password is sent once. A random <b>session ID</b> in a <b>cookie</b> stands in for it afterwards",
                "Any web server in the pool looks the ID up in the shared session store",
            ]},
            {"title": "Consequences", "bullets": [
                "The cookie is as good as the password while it lasts: HTTPS-only, invisible to JavaScript, re-ask for sensitive actions",
                "This is exactly what lets stateless, load-balanced servers work",
                "The same mechanism lets advertisers track browsers across sites: hence consent banners",
                "Apps and APIs often use a signed <b>token</b> (a <b>JSON Web Token</b>) sent in a header instead of a cookie",
            ]},
        ]},
        {"id": "s5-4", "title": "5.4 HTTP Basic Authentication and API keys", "slides": [
            {"title": "The simplest scheme, built into HTTP", "fig": "s5-4-1", "bullets": [
                "<b>Basic Auth</b> sends username:password on every request, encoded in <b>Base64</b>, which anyone can decode",
                "Only over HTTPS; only for staging sites, internal tools, and some APIs",
            ]},
            {"title": "API keys are passwords for programs", "bullets": [
                "A long random secret a provider issues so it knows whom to bill",
                "Stored in server configuration (<b>environment variables</b>, a <code>.env</code> file); never in front-end code; never in Git",
                "Bots scan GitHub constantly for leaked keys and can spend thousands within minutes",
            ], "takeaway": "The single most important habit when building with Claude Code and the Claude API."},
        ]},
        {"id": "s5-5", "title": "5.5 OAuth: how \"Sign in with Google\" works", "slides": [
            {"title": "The problem OAuth solves", "bullets": [
                "New apps want login without another password; apps want to use your Google Calendar or bank on your behalf",
                "Typing your Google password into a third-party app would give it everything, forever",
                "<b>OAuth 2.0</b>: the user approves a limited request at the trusted service; the app gets a valet key",
                "Four roles: <b>resource owner</b> (you), <b>client</b> (the app), <b>authorization server</b> (Google login), <b>resource server</b> (Google's API)",
            ]},
            {"title": "The authorization-code flow", "fig": "s5-5-1"},
            {"title": "Why the roundabout design", "bullets": [
                "The password is typed only at Google; the app never sees it",
                "<b>Scopes</b> limit what the <b>access token</b> can do; the user sees them on the <b>consent screen</b>",
                "The one-time code is swapped for the token server-to-server, using the app's <b>client secret</b>",
                "Tokens expire in about an hour; the user can revoke any app with one click",
                "<b>OpenID Connect</b> adds an ID token for login; <b>single sign-on</b> lets employees use one company identity everywhere",
            ], "takeaway": "Offer \"Sign in with Google\": higher conversion, no password liability. And always read the scopes."},
        ]},
        {"id": "s5-6", "title": "5.6 Security basics every product owner should know", "slides": [
            {"title": "Six ideas that catch most mistakes", "bullets": [
                "Encrypt in transit (HTTPS) and at rest (encrypted disks)",
                "Never trust the front end: prices, permissions, secrets live on the server",
                "<b>SQL injection</b>: user text pasted into a query. Typing <code>' OR 1=1 --</code> logs in as everyone. Frameworks prevent it with <b>parameterised queries</b>",
                "<b>Least privilege</b>: every person, program, and key gets the minimum access",
                "Secrets out of code and out of Git; rotate anything exposed",
                "Patch software and test that backups restore",
            ], "takeaway": "\"Have we reviewed against the OWASP Top Ten?\" is a question any engineer or AI assistant can act on."},
        ]},
        {"id": "s5-7", "title": "5.7 Beyond the browser: mobile, desktop, embedded", "slides": [
            {"title": "Where the front end runs", "table": {"head": ["Kind", "Front end runs", "Built with", "Distributed"], "rows": [
                ["Web app", "Browser", "HTML, CSS, JavaScript", "A URL; updates instantly"],
                ["Native mobile", "Phone, installed", "Swift (iOS), Kotlin (Android)", "App stores; 15 to 30% commission"],
                ["Cross-platform", "Phone, installed", "React Native, Flutter", "App stores"],
                ["Progressive web app", "Browser, installable", "Web technologies", "A URL, no store"],
                ["Desktop", "Laptop, installed", "Native or Electron", "Download, installer"],
                ["Embedded", "Inside a device", "C, C++, Rust", "Shipped in the hardware"],
            ]}},
            {"title": "One back end, many clients", "fig": "s5-7-1", "bullets": [
                "Different front ends are different faces on the same product; the API and database do not change",
            ]},
            {"title": "What this explains", "bullets": [
                "\"We need an app\" is a new front end if the API exists, and secretly a back-end project if it does not",
                "Companies start with the web: no store review, no commission, one codebase, instant updates",
                "The API outlives several generations of front ends",
                "Embedded devices are the exception: a 2026 thermostat must work in 2036; a mistake is a recall, not a redeploy",
            ]},
        ]},
        {"id": "s5-8", "title": "5.8 Where AI fits", "slides": [
            {"title": "An AI model is a third-party API called from your back end", "fig": "s5-8-1", "bullets": [
                "The key and the model call stay on the server; the browser talks only to your back end",
            ]},
            {"title": "Three practical consequences", "bullets": [
                "The API key stays on the server: a call from the browser exposes it to every visitor",
                "Your data is the differentiator: add this customer's history and your catalogue to the <b>prompt</b> (<b>RAG</b>)",
                "AI calls cost money per <b>token</b>, take seconds, and can fail: cache, monitor, and give them a fallback",
            ], "takeaway": "Claude itself is served through exactly this architecture. Now you know what is on the other end of the request."},
        ]},
    ],
}
