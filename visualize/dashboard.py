import json

def generate_html(companies):
    blocks = ""

    for i, c in enumerate(companies, 1):
        rc = c.get("role_counts", {})
        timeline = c.get("signals", {}).get("timeline", [])

        blocks += f"""
        <div class="card">
          <h2>#{i}. {c.get('name')}</h2>

          <p>
            <b>DTS:</b> {c.get('score',0)} |
            <b>Confidence:</b> {c.get('confidence',0)} |
            <b>Stage:</b> {c.get('stage','Unknown')}
          </p>

          <p><b>Sector:</b> {c.get('sector','Unknown')}</p>

          <h4>Role Distribution</h4>
          <canvas id="roles{i}" height="120"></canvas>

          <h4>Hiring Timeline</h4>
          <svg width="300" height="80">
            {''.join(
              f"<rect x='{j*14}' y='{80-p['count']*5}' width='10' height='{p['count']*5}' fill='#4f46e5'/>"
              for j,p in enumerate(timeline)
            )}
          </svg>

          <pre>{json.dumps(c.get('explainability', {}), indent=2)}</pre>

          <script>
          new Chart(document.getElementById("roles{i}"), {{
            type: 'bar',
            data: {{
              labels: {json.dumps(list(rc.keys()))},
              datasets: [{{
                label: 'Role Distribution',
                data: {json.dumps(list(rc.values()))},
                backgroundColor: '#4f46e5'
              }}]
            }}
          }});
          </script>
          <h4>Why this company is included</h4>
          <p style="line-height:1.6">
            {c.get("evidence_summary", "No detailed evidence available.")}
          </p>

        </div>
        """

    return f"""
    <html>
    <head>
      <title>Digitally Transforming Companies — Middle East</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        body {{ font-family: Arial; background:#f4f6fa; padding:20px }}
        .card {{ background:white; padding:20px; margin-bottom:30px;
                 border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,.1) }}
      </style>
    </head>
    <body>
      <h1>🏆 Digitally Transforming Companies — Middle East</h1>
      {blocks}
    </body>
    </html>
    """
