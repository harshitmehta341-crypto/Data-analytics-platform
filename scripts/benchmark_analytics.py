
import sqlite3
import tempfile
import time
from pathlib import Path

RECORD_COUNT = 50_000
RUNS = 10

QUERIES = {
    "Category analytics": """
        SELECT category, COUNT(id), SUM(quantity * unit_price)
        FROM sales_records
        GROUP BY category
    """,
    "Top products": """
        SELECT product, SUM(quantity * unit_price)
        FROM sales_records
        GROUP BY product
    """,
}


def benchmark(connection, query):
    # Warm up the query before timing it.
    connection.execute(query).fetchall()

    start = time.perf_counter()
    for _ in range(RUNS):
        connection.execute(query).fetchall()

    return (time.perf_counter() - start) * 1000 / RUNS


with tempfile.TemporaryDirectory() as directory:
    db_path = Path(directory) / "benchmark.db"
    connection = sqlite3.connect(db_path)

    connection.execute("""
        CREATE TABLE sales_records (
            id INTEGER PRIMARY KEY,
            product TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL
        )
    """)

    products = [
        (f"Product {i % 1000}", f"Category {i % 20}",
         (i % 10) + 1, ((i % 500) + 1) * 1.25)
        for i in range(RECORD_COUNT)
    ]

    connection.executemany("""
        INSERT INTO sales_records (product, category, quantity, unit_price)
        VALUES (?, ?, ?, ?)
    """, products)
    connection.commit()

    print(f"Records: {RECORD_COUNT:,}")
    print(f"Average query time over {RUNS} runs (lower is better)\n")

    for name, query in QUERIES.items():
        without_indexes = benchmark(connection, query)

        if name == "Category analytics":
            index_name = "idx_category"
            column = "category"
        else:
            index_name = "idx_product"
            column = "product"

        connection.execute(
            f"CREATE INDEX {index_name} ON sales_records ({column})"
        )

        with_indexes = benchmark(connection, query)

        print(name)
        print(f"  Without index: {without_indexes:.3f} ms")
        print(f"  With index:    {with_indexes:.3f} ms")
        if with_indexes > 0:
            print(f"  Relative change: {(without_indexes - with_indexes) / without_indexes * 100:.1f}%")
        print()

        connection.execute(f"DROP INDEX {index_name}")

    connection.close()

print("Benchmark complete. Your project database was not changed.")
