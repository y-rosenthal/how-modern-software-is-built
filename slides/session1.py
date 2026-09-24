SESSION = {
    "n": 1,
    "title": "Choosing a Programming Language",
    "subtitle": "What software is written in, and how the choice is made",
    "sections": [
        {"id": "s1-1", "title": "1.1 What a programming language is", "slides": [
            {"title": "From human ideas to machine instructions", "bullets": [
                "Processors understand only <b>machine code</b>: numbers",
                "A <b>programming language</b> is a human-readable notation with strict grammar (<b>syntax</b>)",
                "What the programmer writes is <b>source code</b>",
                "Something must translate source code into machine code",
            ]},
            {"title": "Two ways to translate", "bullets": [
                "<b>Compiler</b>: translate the whole program ahead of time into an <b>executable</b>. Fast; tied to one platform. C, C++, Rust, Go, Swift",
                "<b>Interpreter</b>: carry out the source code on the spot. Portable; slower. Python, JavaScript, Ruby",
                "Analogy: a published translation versus a live interpreter in the room",
            ]},
            {"title": "Language, library, framework", "bullets": [
                "<b>Language</b>: the notation itself (Python)",
                "<b>Library</b>: ready-made code for one job (send email, draw a chart)",
                "<b>Framework</b>: the skeleton of a whole kind of application (Flask, React)",
                "Hundreds of languages exist because each makes one kind of work easier at the cost of another",
            ], "takeaway": "In the age of AI: syntax is the part AI has fully absorbed. The trade-offs below have not gone away."},
        ]},
        {"id": "s1-2", "title": "1.2 Fit for purpose", "slides": [
            {"title": "Was the language built for the job?", "bullets": [
                "<b>General-purpose</b> languages can write almost anything: Python, JavaScript, Java, C#, C++, Go, Rust",
                "<b>Domain-specific</b> languages do one thing superbly: SQL (database questions), HTML (structure), CSS (style)",
                "Nobody writes a website in SQL: it cannot draw a button, react to a click, or send an email",
            ]},
            {"title": "Where each language lives", "fig": "s1-2-1", "bullets": [
                "Browser: only JavaScript. Database: only SQL",
                "The server admits almost anything: that is the real choice",
            ]},
            {"title": "A product is never one language", "bullets": [
                "Typical web product: HTML + CSS + JavaScript in the browser, Python (or JS) on the server, SQL in the database",
                "Add Swift and Kotlin for native phone apps",
                "\"Choosing a language\" really means choosing the back-end language and the mobile strategy",
            ], "takeaway": "In the age of AI: fit for purpose is unchanged. Using several languages in one product is cheaper than it was."},
        ]},
        {"id": "s1-3", "title": "1.3 Popularity, maturity, and community", "slides": [
            {"title": "A language is a community, not just a notation", "bullets": [
                "<b>Hiring</b>: millions of developers versus a few thousand",
                "<b>Answers</b>: every problem in a popular language has been solved publicly",
                "<b>Longevity</b>: COBOL from the 1970s still runs banks; who maintains it now?",
                "<b>Security</b>: many eyes find and fix flaws quickly",
                "<b>Tooling</b>: editors, testing, hosting support the popular languages first",
            ]},
            {"title": "The mainstream, and the caution about the new", "bullets": [
                "Mainstream today: Python, JavaScript/TypeScript, Java, C#, C/C++, Go, SQL; Rust, Swift, Kotlin in their niches",
                "A brand-new language may be better designed and still be the wrong choice: few libraries, breaking changes, unproven survival",
                "Most successful languages needed ten years to become safe bets",
            ], "takeaway": "In the age of AI: popularity matters MORE. AI learns from public code, so mainstream, stable languages get the best help."},
        ]},
        {"id": "s1-4", "title": "1.4 The ecosystem: packages and libraries", "slides": [
            {"title": "Nobody writes it from scratch", "bullets": [
                "Email, spreadsheets, payments, images, charts: someone already wrote it and published it free",
                "The <b>ecosystem</b> = the libraries plus the tools to find and install them",
                "<b>Package manager</b>: pip (Python), npm (JavaScript). \"We added a <b>dependency</b>\"",
                "Almost all of it is <b>open source</b>, which is also a <b>supply chain</b> to watch",
            ]},
            {"title": "The ecosystem steers the choice", "table": {"head": ["If the product is mostly about…", "The ecosystem pulls toward"], "rows": [
                ["AI, machine learning, data", "Python"],
                ["Rich interactive web front end", "JavaScript / TypeScript"],
                ["Conventional web back end", "Python, JavaScript, Ruby, Java, C#, Go"],
                ["Enterprise integration", "Java, C#"],
                ["Games", "C# (Unity), C++ (Unreal)"],
                ["Native phone app", "Swift / Kotlin"],
            ]}, "takeaway": "In the age of AI: ecosystems matter as much as ever. Watch for hallucinated packages that do not exist."},
        ]},
        {"id": "s1-5", "title": "1.5 Speed and memory", "slides": [
            {"title": "The fastest language is usually the wrong question", "bullets": [
                "Compiled languages can be 10 to 100 times faster than Python at raw computation",
                "But most business apps <b>wait</b> (database, network, disk); they do not compute",
                "Developer time costs far more than machine time",
                "Python's AI libraries are C inside: \"Python is slow\" and \"Python runs AI\" are both true",
            ]},
            {"title": "When performance genuinely decides", "table": {"head": ["Situation", "Why", "Typical choice"], "rows": [
                ["Embedded devices, wearables", "Kilobytes of memory, a battery", "C, C++, Rust"],
                ["Games, video", "16 ms per frame", "C++, C#, Rust"],
                ["Trading, real-time control", "Microseconds are money or safety", "C++, Rust"],
                ["Very large services", "10× efficiency = thousands of servers", "Go, Rust, Java"],
                ["Mobile apps", "Battery and memory limits", "Swift, Kotlin"],
            ]}, "takeaway": "Build in the productive language, measure, then rewrite only the proven hot spot. In the age of AI that last step is cheap."},
        ]},
        {"id": "s1-6", "title": "1.6 Platforms and portability", "slides": [
            {"title": "A platform is processor + operating system", "bullets": [
                "Processor families: <b>x86</b> (Intel, AMD) and <b>ARM</b> (phones, Apple silicon, new servers)",
                "Operating systems: Windows, macOS, Linux, iOS, Android",
                "Machine code for one platform is gibberish to another",
                "Every extra platform is another version to build, test, and support",
            ]},
            {"title": "Three ways to reach three platforms", "fig": "s1-6-1"},
            {"title": "Recompile, virtual machine, or interpret", "bullets": [
                "<b>Recompile per platform</b> (C, C++, Rust): fastest; one build per platform. Apple's 2020 move to ARM forced every Mac app to be rebuilt",
                "<b>Compile once to bytecode</b> (Java, Kotlin, C#): \"write once, run anywhere\" on a <b>virtual machine</b>",
                "<b>Interpret the source</b> (Python, JavaScript): ship the file itself. JavaScript's interpreter is in every browser, so the web is the most portable platform ever",
            ]},
            {"title": "Phones are the special case", "bullets": [
                "Apple prefers Swift; Google prefers Kotlin. Both compiled for the phone",
                "The best app on both platforms means writing it twice",
                "<b>Cross-platform frameworks</b> (React Native, Flutter) produce both from one codebase, with some loss of polish",
                "Electron does the same for desktop (Slack, VS Code, Discord)",
            ], "takeaway": "In the age of AI: porting code between platforms is cheaper. Testing on every real device is not."},
        ]},
        {"id": "s1-7", "title": "1.7 Making the decision in the age of AI", "slides": [
            {"title": "How each factor shifts", "table": {"head": ["Factor", "Before AI", "With AI assistance"], "rows": [
                ["Fit for purpose", "Decisive", "Unchanged"],
                ["Popularity and maturity", "High", "Higher: AI quality tracks public code"],
                ["Ecosystem", "High", "Unchanged to higher; verify packages"],
                ["Speed and memory", "Decisive in a few domains", "Same domains; elsewhere lower"],
                ["Platforms", "High (duplicated work)", "Lower for writing; same for testing"],
                ["Your own familiarity", "Often decisive", "Lower, but you still review the code"],
            ]}},
            {"title": "Three conclusions", "bullets": [
                "<b>Choose mainstream.</b> Python, JavaScript/TypeScript, SQL; Java or C# when the enterprise requires; Swift and Kotlin for native mobile",
                "<b>Optimise for readability.</b> When AI writes the code, the human's job is reading it",
                "<b>The language is rarely the risk.</b> Products fail on requirements, data models, and security, not Python versus Go",
            ], "takeaway": "This module uses HTML, CSS, JavaScript in the browser; Python on the server; SQL in the database."},
        ]},
    ],
}
