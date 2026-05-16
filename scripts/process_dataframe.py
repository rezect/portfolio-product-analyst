import pandas as pd
import os


def process_dataframe(
    ipath: str,
    date_columns: dict | None,
    type_columns: dict | None,
    output_path: str | None = None
):
    """Читает файл, парсит колонку с датой и сохраняет результат в CSV."""
    df = _read_file(ipath)

    if date_columns:
        df = _process_date_columns(df, date_columns)
    if type_columns:
        df = _process_type_columns(df, type_columns)

    if not output_path:
        output_path = os.path.splitext(ipath)[0] + ".csv"
    df.to_csv(output_path, index=False)


def _read_file(ipath: str) -> pd.DataFrame:
    df = pd.DataFrame()
    match os.path.splitext(ipath)[-1]:
        case ".xlsx":
            df = pd.read_excel(ipath)
        case ".csv":
            df = pd.read_csv(ipath)
    return df


# -----------------------------------------------------------------------
# Обработка дат
# -----------------------------------------------------------------------

def _normalize_date_spec(spec: str | dict) -> dict:
    if isinstance(spec, str):
        return {"format": spec}
    return spec


def _process_date_columns(df: pd.DataFrame, date_columns: dict):
    for col, raw_spec in date_columns.items():
        if col not in df.columns:
            raise KeyError(
                f"Колонки {col} нет в датафрейме. Вот все возможные колонки: {df.columns}")

        spec = _normalize_date_spec(raw_spec)
        fmt = spec.get("format")
        err = spec.get("errors", "raise")
        out_fmt = spec.get("output_format")
        if fmt is None:
            raise ValueError(f"Формат должен быть задан для столбца дат.")

        df[col] = pd.to_datetime(df[col], errors=err, format=fmt)

        if out_fmt:
            df[col].dt.strftime(out_fmt)

        return df


# -----------------------------------------------------------------------
# Обработка типов
# -----------------------------------------------------------------------

def _normalize_type_spec(spec: str | dict) -> dict:
    if isinstance(spec, str):
        return {"type": spec}
    return spec


def _process_type_columns(df: pd.DataFrame, date_columns: dict):
    for col, raw_spec in date_columns.items():
        if col not in df.columns:
            raise KeyError(
                f"Колонки {col} нет в датафрейме. Вот все возможные колонки: {df.columns}")

        spec = _normalize_type_spec(raw_spec)
        target_type = spec.get("type")
        err = spec.get("errors", "raise")

        match target_type:
            case "int64" | "int32" | "int":
                if df[col].isna().sum() > 0:
                    print(
                        f"В колонке {col} найдены пустые значения. Столбец приведён к типу float64")
                df[col] = pd.to_numeric(
                    df[col], errors=err).astype("int64")
            case "float64" | "float32" | "float":
                df[col] = pd.to_numeric(df[col], errors=err).astype("float64")
            case "category":
                df[col] = df[col].astype("category")
            case "str" | "object":
                df[col] = df[col].astype("object")
            case "Int64":
                df[col] = pd.to_numeric(df[col], errors=err).astype("Int64")

    return df


if __name__ == "__main__":
    process_dataframe(
        ipath="C:\\Coding\\portfolio-product-analyst\\intern\\week2-joins\\data\\online-retail\\Online Retail.xlsx",
        date_columns={
            "InvoiceDate": "%d %m %Y %H %M"
        },
        type_columns={
            "CustomerID": "int64",
            "InvoiceNo": "object",
            "StockCode": "object",
            "Description": "object",
            "Quantity": "int64",
            "Country": "category",
        }
    )
