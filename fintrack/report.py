import os
from datetime import datetime
from jinja2 import Environment,FileSystemLoader
from fintrack.db import get_connection
from fintrack.analyze import (
    spending_by_category,
    top_merchants,
    detect_anomalies,
    savings_rate
)
def generate_report(month: str, income: float) -> str:
     """
    Generate an HTML report for a given month.
    Returns the path to the generated file.
    """
     # Step 1 - collect data from database
     conn = get_connection()
     categories = spending_by_category(conn, month)
     merchants = top_merchants(conn, n=10)
     anomalies = detect_anomalies(conn)
     rate = savings_rate(conn, income, month)
     conn.close()

     # calculate summary numbers
     total_spent = sum(cat["total_spent"] for cat in categories)
     saved = round(income - total_spent, 2)

     # Step 2 - load Jinja2 template
     template_dir = os.path.join("fintrack","templates")
     env = Environment(loader=FileSystemLoader(template_dir))
     template = env.get_template("report.html")

     # Step 3 - fill template with data
     html_content = template.render(
        month=month,
        income=income,
        total_spent=round(total_spent, 2),
        saved=saved,
        savings_rate=rate,
        categories=categories,
        merchants=merchants,
        anomalies=anomalies,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

      # Step 4 - save as HTML file
     output_path = f"report_{month.replace('-', '_')}.html"
     with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

     return output_path

if __name__ == "__main__":
    path = generate_report("2024-01", income=2500.00)
    print(f"Report generated: {path}")
     