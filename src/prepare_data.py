from pathlib import Path

import pandas as pd

DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "datasets"

ORDER_COLS = [
    "order_id",
    "user_id",
    "order_number",
    "order_dow",
    "order_hour_of_day",
    "days_since_prior_order",
]
PRODUCT_COLS = ["product_id", "product_name", "aisle_id", "department_id"]


def load_raw_tables(data_dir: str | Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    data_dir = Path(data_dir) if data_dir is not None else DEFAULT_DATA_DIR

    orders = pd.read_csv(data_dir / "orders.csv")
    products = pd.read_csv(data_dir / "products.csv")
    order_products = pd.read_csv(data_dir / "order_products.csv")
    return orders, products, order_products


def merge_tables(
    orders: pd.DataFrame,
    products: pd.DataFrame,
    order_products: pd.DataFrame,
) -> pd.DataFrame:

    merged = pd.merge(
        order_products,
        orders[ORDER_COLS],
        on="order_id",
        how="left",
    )
    return pd.merge(
        merged,
        products[PRODUCT_COLS],
        on="product_id",
        how="left",
    )


def clean_analysis_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.drop_duplicates(subset=["order_id", "product_id"]).copy()

    valid_rows = (
        cleaned["order_number"].ge(1)
        & cleaned["order_dow"].between(0, 6)
        & cleaned["order_hour_of_day"].between(0, 23)
        & (
            cleaned["days_since_prior_order"].isna()
            | cleaned["days_since_prior_order"].between(0, 30)
        )
    )
    return cleaned.loc[valid_rows].copy()


def load_cleaned_data(data_dir: str | Path | None = None) -> pd.DataFrame:
    orders, products, order_products = load_raw_tables(data_dir)
    merged = merge_tables(orders, products, order_products)
    return clean_analysis_dataframe(merged)


def build_order_level_view(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("order_id")
        .agg(
            user_id=("user_id", "first"),
            order_number=("order_number", "first"),
            order_dow=("order_dow", "first"),
            order_hour_of_day=("order_hour_of_day", "first"),
            days_since_prior_order=("days_since_prior_order", "first"),
            basket_size=("product_id", "count"),
            reorder_share=("reordered", "mean"),
        )
        .reset_index()
    )
