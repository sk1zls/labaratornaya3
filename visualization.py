import matplotlib.pyplot as plt
from typing import Dict

def show_pie_chart(by_category: Dict[str, float], title: str = "Расходы по категориям"):
    if not by_category:
        print("Нет данных для визуализации.")
        return
    labels = list(by_category.keys())
    sizes = list(by_category.values())
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.show()