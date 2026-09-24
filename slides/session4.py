SESSION = {
    "n": 4,
    "title": "Hosting, Scaling, and the Cloud",
    "subtitle": "From one rented server to the distributed architecture behind products serving millions",
    "sections": [
        {"id": "s4-1", "title": "4.1 From localhost to production", "slides": [
            {"title": "Deploying, and the three environments", "table": {"head": ["Environment", "Who uses it", "Purpose"], "rows": [
                ["Development", "Each programmer, own machine", "Write and try code; break things"],
                ["Staging", "The team, testers", "Private replica of production to check a release"],
                ["Production", "Real customers", "The actual business; real, protected data"],
            ]}, "bullets": [
                "<b>Deployment</b>: putting a version where real users can reach it",
                "\"It works on my machine\" is why staging exists",
            ]},
            {"title": "Uptime and latency", "table": {"head": ["Uptime", "Downtime per year", "Typical of"], "rows": [
                ["99%", "About 3.7 days", "Hobby site on one cheap server"],
                ["99.9%", "About 8.8 hours", "Small business with sensible hosting"],
                ["99.99%", "About 53 minutes", "Payments, banking, large SaaS"],
                ["99.999%", "About 5 minutes", "Telecom; very expensive"],
            ]}, "takeaway": "Each extra nine costs dramatically more. Latency: users notice anything over ~100 ms."},
        ]},
        {"id": "s4-2", "title": "4.2 Step 1: everything on one server", "slides": [
            {"title": "Rent one computer and install everything", "fig": "s4-2-1", "bullets": [
                "A <b>VPS</b> for 5 to 50 dollars a month, running <b>Linux</b>: web server (Nginx) + Python app + PostgreSQL",
                "Enough for tens of thousands of visits a day",
            ]},
            {"title": "Why it eventually breaks", "bullets": [
                "<b>Single point of failure</b>: disk dies, site and data vanish together",
                "<b>Resource contention</b>: a heavy report query slows the website for everyone",
                "<b>Hard ceiling</b>: the only upgrade is a bigger machine",
                "<b>Security blast radius</b>: break into the web server, you are sitting on the customer data",
            ], "takeaway": "Take each next step when the problem is real, not before."},
        ]},
        {"id": "s4-3", "title": "4.3 Step 2: the database gets its own machine", "slides": [
            {"title": "Separate the data tier", "fig": "s4-3-1", "bullets": [
                "The <b>database server</b> sits on a <b>private network</b>; a <b>firewall</b> lets only the web server connect",
                "No path from the internet to the data",
            ]},
            {"title": "Why the second bill is worth it", "bullets": [
                "Right-sized hardware: databases want memory and fast disks; web servers want cores and <b>bandwidth</b>",
                "Security: a second wall for an attacker; nobody stumbles across the records from outside",
                "Independent maintenance: rebuild the web server without touching a byte of data",
                "It unlocks Step 3: many web servers sharing one database",
                "In practice: a <b>managed database</b> (RDS, Supabase, Neon) with backups, patches, and <b>failover</b> done for you",
            ]},
        ]},
        {"id": "s4-4", "title": "4.4 Step 3: many web servers behind a load balancer", "slides": [
            {"title": "Two ways to add capacity", "fig": "s4-4-1", "bullets": [
                "<b>Vertical scaling</b>: a bigger machine. Simple; a ceiling; still one of it",
                "<b>Horizontal scaling</b>: more identical machines. No ceiling in principle; losing one is survivable",
            ]},
            {"title": "Horizontal scaling with a load balancer", "fig": "s4-4-2", "bullets": [
                "The <b>load balancer</b> owns the public address and spreads requests; <b>health checks</b> skip a dead server",
            ]},
            {"title": "The catch: servers must be stateless", "bullets": [
                "Dana logs in on server 1; her next click lands on server 2, which has never heard of her",
                "<b>Stateless</b> servers remember nothing between requests; shared facts live in the database or Redis",
                "Interchangeable servers can be added at 9 a.m. and removed after lunch: costs become <b>elastic</b>",
                "Duplicates at every layer = <b>high availability</b>: how three and four nines are bought",
            ], "takeaway": "Ask before launch: \"Can we run two copies of this?\""},
        ]},
        {"id": "s4-5", "title": "4.5 Step 4: caches, CDNs, and storage", "slides": [
            {"title": "Four more components", "bullets": [
                "<b>Cache</b>: a fast temporary copy of something expensive (a product list in Redis for 60 seconds). Hard problem: <b>staleness</b>",
                "<b>CDN</b>: copies of images, CSS, JS in hundreds of cities; Singapore gets the image from Singapore",
                "<b>Object storage</b> (S3): unlimited files by URL; uploads never live on a web server's disk",
                "<b>Read replica</b>: a live copy of the database that answers reads and stands by as a spare",
            ]},
            {"title": "The standard architecture of a serious web product", "fig": "s4-5-1", "bullets": [
                "Still three tiers: each one now duplicated, cached, or moved closer to the user",
            ]},
        ]},
        {"id": "s4-6", "title": "4.6 The cloud menu", "slides": [
            {"title": "How much of the work do you want to do yourself?", "table": {"head": ["Layer", "You get", "You manage", "Examples"], "rows": [
                ["IaaS", "Virtual machines, disks", "Everything on them", "EC2, DigitalOcean"],
                ["PaaS", "\"Here is my code; run it\"", "Just code and data", "Render, Railway, Vercel, Fly.io"],
                ["SaaS", "A finished product", "Your settings", "Gmail, Shopify, Slack"],
                ["Serverless", "Run this function on demand", "The function", "AWS Lambda, Cloudflare Workers"],
            ]}, "takeaway": "Pizza: rent a kitchen, a meal kit, delivery, or a vending machine that bakes one slice."},
            {"title": "Containers, and the advice for this course", "bullets": [
                "A <b>container</b> (Docker) packages a program with everything it needs, so it runs identically everywhere",
                "Kubernetes runs thousands of containers; almost never the right first choice for a small team",
                "For a Claude Code prototype: a PaaS plus a managed database, 0 to 50 dollars a month, no servers to log into",
            ]},
        ]},
        {"id": "s4-7", "title": "4.7 Shipping code safely", "slides": [
            {"title": "How code reaches customers", "fig": "s4-7-1", "bullets": [
                "<b>Version control</b> (Git, GitHub): every change recorded and reversible",
                "<b>CI/CD</b>: tests run on every change; if they pass, it deploys. Small, frequent, low-risk releases",
                "<b>Monitoring</b> and logs: find out about outages before customers do",
            ]},
        ]},
    ],
}
