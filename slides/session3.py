SESSION = {
    "n": 3,
    "title": "Dynamic Websites, APIs, and Databases",
    "subtitle": "Inside the back end: server code, APIs and JSON, the relational model, and SQL by example",
    "sections": [
        {"id": "s3-1", "title": "3.1 Inside the back end: a Python web server", "slides": [
            {"title": "A complete dynamic web server", "code": "from flask import Flask\nfrom datetime import datetime\napp = Flask(__name__)\n\n@app.route(\"/hours\")\ndef hours():\n    if 7 <= datetime.now().hour < 18:\n        return \"<p>We are <b>open</b> right now!</p>\"\n    return \"<p>We are closed. Back at 7 a.m.</p>\"\n\napp.run(port=5000)", "bullets": [
                "<b>Flask</b> is a <b>framework</b>: it handles the routine parts of being a server",
                "Each <b>route</b> connects a path to a function; the function's return value is the response",
            ]},
            {"title": "Localhost, ports, and templates", "bullets": [
                "<b>localhost</b> means \"this computer\": browser and server on the same laptop",
                "A <b>port</b> is a numbered door: 443 for HTTPS, 5000 or 3000 for testing",
                "Two visitors a minute apart at 5:59 and 6:00 see different pages: that is \"dynamic\"",
                "Real back ends fill in <b>templates</b> (HTML with blanks) rather than gluing strings",
            ]},
        ]},
        {"id": "s3-2", "title": "3.2 APIs and JSON", "slides": [
            {"title": "The menu is the API", "bullets": [
                "An <b>API</b> is the defined set of requests a program accepts and the answers it gives",
                "Callers are often programs, not people: page JavaScript, a mobile app, a partner, an AI",
                "Each address in an API is an <b>endpoint</b>; answers come back as data, not designed pages",
            ]},
            {"title": "JSON: the common tongue of the web", "code": "{\n  \"products\": [\n    {\"id\": 1, \"name\": \"Sourdough loaf\", \"price\": 7.5, \"in_stock\": true},\n    {\"id\": 2, \"name\": \"Rye bread\", \"price\": 6.0, \"in_stock\": false}\n  ]\n}", "bullets": [
                "Curly braces: named values. Square brackets: lists. Almost exactly a Python dictionary and list",
            ]},
            {"title": "Verbs: nouns in the URL, verbs in the method", "table": {"head": ["Method", "Meaning", "Bakery example", "CRUD"], "rows": [
                ["GET", "Read", "GET /api/products", "Read"],
                ["POST", "Create", "POST /api/orders", "Create"],
                ["PUT / PATCH", "Update", "PATCH /api/orders/88", "Update"],
                ["DELETE", "Remove", "DELETE /api/orders/88", "Delete"],
            ]}, "takeaway": "This style is REST. Most business software is CRUD screens over a database."},
            {"title": "APIs in both directions", "fig": "s3-2-1", "bullets": [
                "You offer an API to your front ends and partners; you consume <b>third-party APIs</b> (Stripe, Claude, email) instead of building",
                "An <b>API key</b> identifies your account to a third party. It lives on your server, never in front-end code",
            ]},
        ]},
        {"id": "s3-3", "title": "3.3 Why every product needs a database", "slides": [
            {"title": "Why not just save to a file?", "bullets": [
                "<b>Many writers at once</b>: two customers buying the last challah must not both succeed",
                "<b>Speed at scale</b>: an <b>index</b> finds one order in ten million in milliseconds",
                "<b>Reliability</b>: a <b>transaction</b> is all-or-nothing, even if the power fails halfway",
                "<b>Questions</b>: \"who ordered rye three times last quarter?\" is one line",
                "The <b>database</b> is a separate program (PostgreSQL, MySQL, SQLite) your back end talks to",
            ]},
            {"title": "The relational model", "fig": "s3-3-1", "bullets": [
                "<b>Tables</b> of rows and columns; each table holds one kind of thing",
                "<b>Primary key</b>: the unique ID of a row. <b>Foreign key</b>: a column pointing at another table's row",
                "Change Dana's email once; every order she placed reflects it",
            ], "takeaway": "The table design (the schema) is really a design of the business."},
        ]},
        {"id": "s3-4", "title": "3.4 SQL by example", "slides": [
            {"title": "Reading: SELECT", "code": "SELECT name, email FROM customers WHERE city = 'Boston';\n\nSELECT status, COUNT(*) AS how_many\nFROM orders\nGROUP BY status;", "bullets": [
                "SELECT picks columns, FROM picks the table, WHERE filters rows",
                "COUNT, SUM, AVG, MIN, MAX are <b>aggregate functions</b>: every dashboard is a stack of these",
            ]},
            {"title": "Combining tables: JOIN", "code": "SELECT customers.name, products.name, orders.quantity\nFROM orders\nJOIN customers ON orders.customer_id = customers.customer_id\nJOIN products  ON orders.product_id  = products.product_id\nWHERE orders.status = 'placed';", "bullets": [
                "A <b>JOIN</b> stitches rows together using the keys, so \"Dana Levi, Rye bread, 1\" comes out readable",
            ]},
            {"title": "Writing: INSERT, UPDATE, DELETE", "code": "INSERT INTO orders (customer_id, product_id, quantity, status)\nVALUES (3, 1, 2, 'placed');\n\nUPDATE orders SET status = 'ready' WHERE order_id = 88;\n\nDELETE FROM orders WHERE order_id = 89;", "bullets": [
                "<code>DELETE FROM orders;</code> with no WHERE deletes every order in the company",
                "CREATE TABLE defines columns, <b>data types</b>, keys, and <b>constraints</b> the database enforces",
            ]},
            {"title": "Which database?", "table": {"head": ["Product", "Type", "Typical use"], "rows": [
                ["SQLite", "Relational, single file", "Prototypes, phone apps; built into Python"],
                ["PostgreSQL", "Relational server", "Default for new web products"],
                ["MySQL", "Relational server", "Older web products, WordPress"],
                ["SQL Server, Oracle", "Relational server", "Large enterprises, finance"],
                ["MongoDB", "Document (NoSQL)", "Flexible data shapes"],
                ["Redis", "Key-value, in memory", "Caching, sessions"],
            ]}, "takeaway": "You will not write SQL in this course. You will read it and say what it does."},
        ]},
        {"id": "s3-5", "title": "3.5 Beyond tables: NoSQL and ORMs", "slides": [
            {"title": "NoSQL and ORMs", "bullets": [
                "<b>NoSQL</b> relaxes the rules: a <b>document database</b> (MongoDB) stores JSON-like records with any fields",
                "Price of flexibility: fewer guarantees, clumsier joins. Rule of thumb: <b>start relational</b>",
                "An <b>ORM</b> lets Python treat rows as objects and writes the SQL behind the scenes",
                "Claude Code will almost certainly use an ORM; the concepts underneath are unchanged",
            ]},
        ]},
        {"id": "s3-6", "title": "3.6 The three-tier architecture", "slides": [
            {"title": "Presentation, application, data", "bullets": [
                "<b>Presentation tier</b>: the front end in the browser or app",
                "<b>Application tier</b>: the back-end program; where <b>business logic</b> lives (prices, permissions, workflows)",
                "<b>Data tier</b>: the database",
            ]},
            {"title": "One order through three tiers", "fig": "s3-6-1"},
            {"title": "Three consequences", "bullets": [
                "The browser never touches the database directly; the back end checks identity and applies rules",
                "Each tier can be changed independently: redesign the front end without touching the data",
                "Each tier can live on different hardware: today one laptop, tomorrow ten servers (Session 4)",
            ], "takeaway": "Anything in the browser can be altered by the user. Rules and secrets live on the server."},
        ]},
    ],
}
