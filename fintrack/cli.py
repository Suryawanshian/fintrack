from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from fintrack.db import get_connection
from fintrack.analyze import(
    spending_by_category,
    top_merchants,
    monthly_totals,
    daily_average,
    savings_rate,
    detect_anomalies,
    budget_vs_actual

)
console = Console()
def show_summary(month: str) -> None:
    """Display spending summary for a month"""
    conn = get_connection()
    categories = spending_by_category(conn, month)
    conn.close()

    #Create the table
    table = Table(
        title=f"FinTrack - {month}",
        box=box.ROUNDED
    )

    #Add columns
    table.add_column("Category", style="cyan")
    table.add_column("Spent", style="white")
    table.add_column("Transactions", style="white")

    #Add rows
    for cat in categories:
        table.add_row(
            cat["category"],
            f"EUR {cat['total_spent']:.2f}",
            str(cat["num_transactions"])
        )

    console.print(table)

def show_top_merchants(n: int = 5) -> None:

     conn = get_connection()
     merchants = top_merchants(conn,n=n)
     conn.close()

     table = Table(
          title = f"Top {n} Merchants",
          box = box.ROUNDED
     )

     table.add_column("Merchant", style="cyan")
     table.add_column("Total Spent", style="white")
     table.add_column("Visits", style="white")

     for m in merchants:
          table.add_row(
               str(m["merchant"]),
               f"EUR {m['total_spent']:.2f}",
               str(m["num_visits"])

          )
     console.print(table)

def show_monthly_totals() -> None:
     """ Display total spending per month"""
     conn = get_connection()
     months= monthly_totals(conn)
     conn.close()

     table = Table(
          title = "Monthly Spending Totals",
          box=box.ROUNDED

     )

     table.add_column("Month", style="cyan")
     table.add_column("Total Spent", style="white")
     table.add_column("Transactions", style="white")

     for month in months:
          table.add_row(
               month["month"],
               f"EUR {month['total_spent']:.2f}",
               str(month["num_transactions"])
          )
     console.print(table)

def show_savings(month: str, income: float) -> None:
     """Display savings rate for a given month"""

     conn = get_connection()
     rate = savings_rate(conn, income, month)

     categories = spending_by_category(conn, month)
     conn.close()

     total_spent = sum(cat["total_spent"] for cat in categories)
     saved = income - total_spent

     if rate>=20:
          color="green"
     elif rate >=0:
          color="yellow" 
     else:
          color ="red"

     content = (

          f"[bold]Savings Rate: {rate}%[/bold]\n\n"
          f"Income: EUR {income:.2f}\n"
          f"Spent:  EUR {total_spent:.2f}\n"
          f"Saved: EUR {saved:.2f}"
     )

     panel=Panel(

          content,
          title=f"💰 {month} Financial Summary",
          border_style=color
     )

     console.print(panel)

def show_anomalies() -> None:
     """Display unusual transactions."""

     conn = get_connection()
     anomalies = detect_anomalies(conn)
     conn.close()

     if not anomalies:
          console.print("[green]No unusual transactions found.[/green]")
          return

     table = Table(
        title="⚠️ Unusual Transactions",
        box=box.ROUNDED
    )

     table.add_column("Date", style="cyan")
     table.add_column("Merchant", style="white")
     table.add_column("Amount", style="red")
     table.add_column("Category Avg", style="white")
     table.add_column("Times Above Avg", style="red")

     for a in anomalies:
        table.add_row(
             a["date"],
             str(a["merchant"]),
             f"EUR {a['amount']:.2f}",
             f"EUR {a['category_avg']:.2f}",
             f"{a['times_above_avg']}x"
        )
     console.print(table)

def show_budget(month: str) -> None:
     """Display budget vs actual spending for each category."""

     conn = get_connection()
     budget_data = budget_vs_actual(conn, month)
     conn.close()

     table = Table(
        title=f"Budget vs Actual — {month}",
        box=box.ROUNDED
     )

     table.add_column("Category", style="cyan")
     table.add_column("Budget", style="white")
     table.add_column("Spent", style="white")
     table.add_column("Remaining", style="white")
     table.add_column("% Used", style="white")

     for item in budget_data:
          remaining = item["remaining"]
          pct = item["pct_used"] 

          if pct > 100:
             status_color = "red"
          elif pct > 80:
               status_color = "yellow"
          else:
               status_color = "green" 

          table.add_row(
            item["category"],
            f"EUR {item['budget']:.2f}",
            f"EUR {item['total_spent']:.2f}",
            f"[{status_color}]EUR {remaining:.2f}[/{status_color}]",
            f"[{status_color}]{pct}%[/{status_color}]"
        )

     console.print(table
                   )         
if __name__== "__main__":
        show_summary("2024-01")
        show_top_merchants(5)
        show_monthly_totals()
        show_savings("2024-01", income=2500.00)
        show_anomalies()
        show_budget("2024-01")