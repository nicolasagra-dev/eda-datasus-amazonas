from __future__ import annotations

import csv
import json
import urllib.request
from pathlib import Path


OUTPUT_PATH = Path("data/raw/populacao_municipios_am.csv")

ESTIMATIVAS_URL = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/6579/"
    "periodos/2021|2024|2025/variaveis/9324?localidades=N6[N3[13]]"
)
CENSO_2022_URL = (
    "https://servicodados.ibge.gov.br/api/v3/agregados/4714/"
    "periodos/2022/variaveis/93?localidades=N6[N3[13]]"
)


def fetch_json(url: str) -> object:
    with urllib.request.urlopen(url, timeout=90) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_series(payload: object, fonte: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    series = payload[0]["resultados"][0]["series"]
    for item in series:
        codigo_ibge_7 = item["localidade"]["id"]
        municipio = item["localidade"]["nome"].replace(" - AM", "")
        codigo_municipio = codigo_ibge_7[:6]
        for ano, populacao in item["serie"].items():
            rows.append(
                {
                    "codigo_municipio": codigo_municipio,
                    "codigo_ibge_7": codigo_ibge_7,
                    "municipio": municipio,
                    "ano": int(ano),
                    "populacao": int(populacao),
                    "fonte_populacao": fonte,
                }
            )
    return rows


def add_interpolated_2023(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    by_city: dict[str, dict[int, dict[str, object]]] = {}
    for row in rows:
        by_city.setdefault(str(row["codigo_municipio"]), {})[int(row["ano"])] = row

    interpolated: list[dict[str, object]] = []
    for codigo_municipio, years in by_city.items():
        if 2022 not in years or 2024 not in years:
            continue
        pop_2022 = int(years[2022]["populacao"])
        pop_2024 = int(years[2024]["populacao"])
        base = years[2022]
        interpolated.append(
            {
                "codigo_municipio": codigo_municipio,
                "codigo_ibge_7": base["codigo_ibge_7"],
                "municipio": base["municipio"],
                "ano": 2023,
                "populacao": round((pop_2022 + pop_2024) / 2),
                "fonte_populacao": "Interpolacao linear entre Censo 2022 e estimativa 2024",
            }
        )
    return rows + interpolated


def main() -> None:
    estimativas = parse_series(fetch_json(ESTIMATIVAS_URL), "IBGE - Estimativas de populacao")
    censo_2022 = parse_series(fetch_json(CENSO_2022_URL), "IBGE - Censo Demografico 2022")
    rows = add_interpolated_2023(estimativas + censo_2022)
    rows = sorted(rows, key=lambda row: (str(row["municipio"]), int(row["ano"])))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "codigo_municipio",
                "codigo_ibge_7",
                "municipio",
                "ano",
                "populacao",
                "fonte_populacao",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Arquivo salvo em {OUTPUT_PATH} ({len(rows)} linhas).")


if __name__ == "__main__":
    main()
