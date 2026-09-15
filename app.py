from http.server import BaseHTTPRequestHandler, HTTPServer
from html import escape
import json
import os
import urllib.request

PRODUCT_URL = os.getenv("ProductCatalogUrl", "http://espresso-shop-product-catalog-svc:8091")
REVIEWS_URL = os.getenv("ReviewsUrl", "http://espresso-shop-reviews-svc:8092")


def fetch_json(url):
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            return json.loads(response.read().decode())
    except Exception as error:
        return {"error": str(error)}


def product_cards(products_response):
    products = products_response.get("products", [])
    if not products:
        return '<div class="card muted">No products available right now.</div>'

    cards = []
    for product in products:
        name = escape(str(product.get("name", "Coffee")))
        price = escape(str(product.get("price", "N/A")))
        cards.append(f"""
        <article class="card">
          <span class="badge">Coffee</span>
          <h3>{name}</h3>
          <p>Freshly prepared and served hot.</p>
          <strong>${price}</strong>
        </article>
        """)
    return "".join(cards)


def review_cards(reviews_response):
    reviews = reviews_response.get("reviews", [])
    version = escape(str(reviews_response.get("serviceVersion", "unknown")))

    cards = [f'<div class="version">Reviews service version: {version}</div>']
    for review in reviews:
        user = escape(str(review.get("user", "Guest")))
        rating = escape(str(review.get("rating", "5")))
        comment = escape(str(review.get("comment", "Great coffee.")))
        cards.append(f"""
        <article class="review">
          <strong>{user}</strong>
          <span>{rating}/5</span>
          <p>{comment}</p>
        </article>
        """)
    return "".join(cards)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        products = fetch_json(PRODUCT_URL)
        reviews = fetch_json(REVIEWS_URL)

        html_page = f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Espresso Shop</title>
  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: #26160f;
      background: #f7f1ea;
    }}

    .hero {{
      min-height: 78vh;
      background:
        linear-gradient(rgba(0, 0, 0, .46), rgba(0, 0, 0, .52)),
        url("https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1600&q=80");
      background-size: cover;
      background-position: center;
      display: flex;
      align-items: center;
      padding: 56px;
      color: white;
    }}

    .hero-content {{
      max-width: 720px;
    }}

    .eyebrow {{
      text-transform: uppercase;
      font-weight: 700;
      font-size: 14px;
      letter-spacing: 2px;
      color: #f4c27a;
    }}

    h1 {{
      margin: 14px 0;
      font-size: 64px;
      line-height: 1;
    }}

    .hero p {{
      font-size: 22px;
      line-height: 1.5;
      max-width: 620px;
    }}

    .section {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 48px 24px;
    }}

    .section h2 {{
      font-size: 34px;
      margin: 0 0 22px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 18px;
    }}

    .card,
    .review {{
      background: white;
      border: 1px solid #eadfd3;
      border-radius: 8px;
      padding: 22px;
      box-shadow: 0 10px 24px rgba(39, 22, 15, .08);
    }}

    .card h3 {{
      margin: 12px 0 8px;
      font-size: 24px;
    }}

    .card p,
    .review p {{
      color: #6b5547;
      line-height: 1.5;
    }}

    .card strong {{
      display: block;
      margin-top: 14px;
      font-size: 22px;
      color: #9b4f18;
    }}

    .badge,
    .version {{
      display: inline-block;
      background: #2e1b13;
      color: #f4c27a;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: 13px;
      font-weight: 700;
    }}

    .review {{
      margin-bottom: 14px;
    }}

    .review span {{
      float: right;
      color: #9b4f18;
      font-weight: 700;
    }}

    .muted {{
      color: #6b5547;
    }}

    footer {{
      padding: 28px 24px;
      text-align: center;
      background: #26160f;
      color: #f7f1ea;
    }}

    @media (max-width: 700px) {{
      .hero {{
        min-height: 70vh;
        padding: 36px 24px;
      }}

      h1 {{
        font-size: 44px;
      }}

      .hero p {{
        font-size: 18px;
      }}
    }}
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-content">
      <div class="eyebrow">Kubernetes powered coffee</div>
      <h1>Espresso Shop</h1>
      <p>Fresh coffee, smooth cappuccino, warm reviews, and a microservice architecture running on Kubernetes.</p>
    </div>
  </header>

  <main>
    <section class="section">
      <h2>Products</h2>
      <div class="grid">
        {product_cards(products)}
      </div>
    </section>

    <section class="section">
      <h2>Reviews</h2>
      {review_cards(reviews)}
    </section>
  </main>

  <footer>
    Espresso Shop running with Helm on Kubernetes
  </footer>
</body>
</html>
"""

        body = html_page.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
