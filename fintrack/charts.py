import os
import matplotlib
matplotlib.use('Agg') # non-interactive backend for saving files
import matplotlib.pyplot as plt

def generate_category_pie_chart(categories: list, output_path: str) -> str:
    """
    Generate a pie chart of spending by category.
    Saves as PNG file and returns the file path.
    """
    # extract labels and values
    labels = [cat["category"] for cat in categories]
    amount = [cat["total_spent"] for cat in categories]

    # create the chart

    fig, ax = plt.subplots(figsize=(8,6))
    ax.pie(

        amount,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
    )
    ax.set_title("Spending by Category", fontsize=14, fontweight="bold")

    # save and close
    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches="tight")
    plt.close()

    return output_path

def generate_monthly_bar_chart(monthly_data: list, output_path: str) -> str:
    """
    Generate a bar chart of monthly spending.
    Saves as PNG file and returns the file path.
    """
    months = [m["month"] for m in monthly_data]
    amounts = [m["total_spent"] for m in monthly_data]

    fig, ax = plt.subplots(figsize=(10,6))
    bars = ax.bar(months, amounts, color="#3498db", edgecolor="white")

    # add value labels on top of each bar
    for bar, amount in zip(bars, amounts):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 10,
            f"EUR {amount:.0f}",
            ha="center",
            va="bottom",
            fontsize=10

        )

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Spent (EUR)", fontsize=12)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=100, bbox_inches="tight")
    plt.close()

    return output_path