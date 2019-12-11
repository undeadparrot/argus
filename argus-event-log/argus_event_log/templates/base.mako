<html>
<head>
    <title></title>
    <link rel="stylesheet" href="https://unpkg.com/sakura.css/css/sakura.css" type="text/css">
    <style>
        nav ul li {
            display: inline;
        }
        .success {
            border: 2px solid green;
            border-radius: 3pt;
            padding: 2em;
            padding-top: 0.5em;
        }
    </style>
</head>
<body>
<header>
    <h1>Argus Events</h1>
    <nav>
        <ul>
            <li><a href="events">Events</a></li>
            <li><a href="topics">Topics</a></li>
            <li><a href="tokens">API Tokens</a></li>
        </ul>
    </nav>
    <hr/>
</header>
% if error:
<div class="error">
    <header>Error</header>
    <p>${error}</p>
</div>
% endif
<main>
    ${self.body()}
</main>
<footer>
    <hr/>
</footer>
</body>
</html>