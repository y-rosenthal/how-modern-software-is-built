SESSION = {
    "n": 2,
    "title": "From a File on Your Laptop to a Page on the Internet",
    "subtitle": "Browsers, the three languages of a web page, addresses, and the request–response conversation",
    "sections": [
        {"id": "s2-1", "title": "2.1 Why architecture is a business topic", "slides": [
            {"title": "Architecture is the set of decisions that are expensive to change", "bullets": [
                "What the major parts are, what each does, how they talk",
                "<b>Cost</b>: a few dollars a month or tens of thousands",
                "<b>Risk</b>: what happens when a component fails; how a breach could occur",
                "<b>Speed</b>: how fast features ship without breaking what works",
            ], "takeaway": "The person who cannot follow the conversation does not get a vote."},
        ]},
        {"id": "s2-2", "title": "2.2 Clients, servers, and programs", "slides": [
            {"title": "One computer asks, another answers", "fig": "s2-2-1", "bullets": [
                "<b>Client</b> asks; <b>server</b> waits and answers. The client always speaks first",
                "A server is an ordinary computer in a <b>data center</b>, running 24 hours a day",
            ]},
            {"title": "Two things people get wrong about servers", "bullets": [
                "A server is an ordinary computer: processor, memory, disk. Usually no screen",
                "\"Server\" also names a <b>program</b>: a <b>web server</b> program listens for requests and hands back pages",
                "The client for a website is a <b>browser</b>: Chrome, Safari, Firefox, Edge",
                "Analogy: the restaurant. You order from the menu; the kitchen cooks; you never enter the kitchen",
            ]},
        ]},
        {"id": "s2-3", "title": "2.3 A web page is three languages", "slides": [
            {"title": "A web page is a plain text file", "bullets": [
                "<b>HTML</b>: what is on the page (headings, paragraphs, images, links), marked with <b>tags</b>",
                "<b>CSS</b>: what it looks like (colors, fonts, layout, phone versus desktop)",
                "<b>JavaScript</b>: what it does (react to clicks, validate forms, load more posts)",
                "JavaScript is unrelated to Java despite the name",
            ]},
            {"title": "HTML by example", "code": "<h1>Rosenthal's Bakery</h1>\n<p>Fresh bread every morning since 1998.</p>\n<img src=\"storefront.jpg\" alt=\"Our shop\">\n<a href=\"menu.html\">See the menu</a>", "bullets": [
                "Read it aloud and it explains itself: heading, paragraph, image, link",
            ]},
            {"title": "Three files, one page", "fig": "s2-3-1", "bullets": [
                "The browser combines all three and <b>renders</b> the result",
            ]},
        ]},
        {"id": "s2-4", "title": "2.4 The static website on your own computer", "slides": [
            {"title": "The zero-infrastructure starting point", "bullets": [
                "A <b>static website</b> is fixed files sent to every visitor exactly as stored",
                "Double-click <code>index.html</code>: the browser reads it straight off your disk. Address starts with <code>file:///</code>",
                "No server, no internet, no company involved",
                "Limitation: only you can see it. Sharing needs an always-on server with an address",
            ]},
        ]},
        {"id": "s2-5", "title": "2.5 How the internet delivers a page", "slides": [
            {"title": "Anatomy of a URL", "fig": "s2-5-1", "bullets": [
                "<b>Protocol</b> (how to talk), <b>domain</b> (which server), <b>path</b> (which page), <b>query string</b> (extra details)",
            ]},
            {"title": "Finding the server: DNS", "bullets": [
                "Every machine on the internet has a numeric <b>IP address</b>, such as 142.250.72.14",
                "<b>DNS</b> is the distributed phone book: domain name in, IP address out",
                "A business rents its <b>domain</b> from a <b>registrar</b>; pointing it at a host means editing a DNS record",
                "\"DNS changes take up to 48 hours\": thousands of copies of the phone book refresh on a schedule",
            ]},
            {"title": "The conversation: HTTP", "code": "GET /menu.html HTTP/1.1\nHost: www.rosenthalsbakery.com\nUser-Agent: Chrome/128.0\n\nHTTP/1.1 200 OK\nContent-Type: text/html\n\n<!DOCTYPE html> ...", "bullets": [
                "A <b>request</b> names a method and a path plus <b>headers</b>; a <b>response</b> carries a <b>status code</b> and the content",
                "200 OK, 301 moved, 404 not found, 500 server error, 503 overloaded",
            ]},
            {"title": "What happens after you press Enter", "fig": "s2-5-2", "bullets": [
                "One page usually means 50 to 150 requests: HTML first, then CSS, JavaScript, images",
            ]},
            {"title": "HTTPS and hosting", "bullets": [
                "Plain HTTP is readable by anyone on the same Wi-Fi. <b>HTTPS</b> wraps it in <b>encryption</b>; the padlock",
                "The server proves its identity with a free <b>certificate</b>. No business reason to skip HTTPS",
                "<b>Hosting</b>: rent space on someone's always-on server. Static hosting is free or nearly so",
                "Serving static files is the easiest job a computer can do: fast, hard to hack, hard to overload",
            ]},
        ]},
        {"id": "s2-6", "title": "2.6 Front end, back end, and the limits of static", "slides": [
            {"title": "What a static site cannot do", "bullets": [
                "<b>Front end</b>: runs on the user's device. <b>Back end</b>: runs on the server, out of sight",
                "A static site is front end only, so it cannot: remember anything, personalise, keep a secret, or do work (email, charge a card)",
                "A <b>dynamic website</b> runs a program per request and can do all four",
            ]},
            {"title": "Static versus dynamic", "fig": "s2-6-1", "bullets": [
                "Most real products mix the two: static marketing pages, dynamic product behind the login",
            ]},
        ]},
        {"id": "s2-7", "title": "2.7 Where Python fits", "slides": [
            {"title": "Python runs on the server, not in the browser", "table": {"head": ["Language", "Where it runs", "Job"], "rows": [
                ["HTML, CSS", "Browser", "Content and appearance"],
                ["JavaScript", "Browser (and servers via Node.js)", "Interactivity; also back ends"],
                ["Python", "Servers and your own computer", "Back-end logic, data, AI, scripts"],
                ["SQL", "Database server", "Questions about stored data"],
                ["Swift, Kotlin", "Phones", "Native apps"],
            ]}, "takeaway": "Your Python skills are directly the skills of writing back ends. \"What's your stack?\" means \"what's your architecture?\""},
        ]},
    ],
}
