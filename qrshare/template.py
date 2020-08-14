# using template string
# since change in working directory may cause templates folder to inaccesible
shared_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- <link
      rel="stylesheet"
      href="{{ url_for('static', filename='main.css') }}"
    /> -->
    <style>
      * {
        font-family: sans-serif;
        --text-primary: #cfcfcf;
        --text-secondary: #e9e9e9;
        --bg-primary: #333;
        --bg-secondary: #272727;
        --bg-accent: rgb(24, 24, 24);
      }

      body {
        background-color: var(--bg-primary);
        margin: 0;
      }

      h3 {
        margin: 0;
        padding: 1rem 0;
        color: var(--text-primary);
        background-color: var(--bg-accent);
        text-align: center;
      }

      ul {
        margin: 0;
        padding: 0;
        list-style: none;
      }

      a {
        display: block;
        text-decoration: none;
        padding: 1rem;
        text-align: center;
        color: var(--text-primary);
        background-color: var(--bg-primary);
        transition: 200ms ease-in;
      }

      li:nth-child(even) a {
        background-color: var(--bg-secondary);
      }

      a:hover {
        color: var(--text-secondary);
      }

      #da-btn {
        padding: 0.8rem;
        font-size: 0.8rem;
        font-weight: bold;
        background-color: var(--bg-accent);
      }
    </style>
    <title>QRShare</title>
  </head>
  <body>
    <div>
      <h3>Shared files</h3>
      <a href="#" id="da-btn">Download all</a>
      <ul>
        {% for link in links %}
        <li>
          <a href="/{{ link['route'] }}">
            {{ link['file'].name }}
          </a>
        </li>
        {% endfor %}
      </ul>
    </div>
  </body>
  <!-- <script src="{{ url_for('static', filename='main.js') }}"></script> -->
  <script defer>
    var links = document.getElementsByTagName("a");
    document.getElementById("da-btn").addEventListener("click", (e) => {
      e.preventDefault();

      for (let link of links) {
        link.click();
      }
    });
  </script>
</html>
"""
