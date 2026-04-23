from __future__ import annotations

import argparse
import csv
import re
import urllib.parse
import urllib.request
from pathlib import Path


TABNET_URL = "http://tabnet.datasus.gov.br/cgi/tabcgi.exe?sih/cnv/nram.def"
FORM_URL = "http://tabnet.datasus.gov.br/cgi/deftohtm.exe?sih/cnv/nram.def"


MONTH_LABELS = {
    1: "Jan",
    2: "Fev",
    3: "Mar",
    4: "Abr",
    5: "Mai",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Set",
    10: "Out",
    11: "Nov",
    12: "Dez",
}


def month_files(start_year: int, end_year: int, end_month: int = 12) -> list[str]:
    files: list[str] = []
    for year in range(start_year, end_year + 1):
        last_month = end_month if year == end_year else 12
        for month in range(1, last_month + 1):
            files.append(f"nram{year % 100:02d}{month:02d}.dbf")
    return files


def period_label(start_year: int, end_year: int, end_month: int) -> str:
    return f"Jan/{start_year} a {MONTH_LABELS[end_month]}/{end_year}"


def fetch_tabnet(linha: str, coluna: str, incremento: str, arquivos: list[str]) -> str:
    payload = {
        "Linha": linha,
        "Coluna": coluna,
        "Incremento": incremento,
        "Arquivos": arquivos,
        "formato": "prn",
        "mostre": "Mostra",
    }
    data = urllib.parse.urlencode(payload, doseq=True, encoding="latin-1").encode("latin-1")
    request = urllib.request.Request(
        TABNET_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read().decode("latin-1")


def clean_prn(text: str) -> list[list[str]]:
    if "<PRE>" in text:
        text = text.split("<PRE>", 1)[1]
    if "</PRE>" in text:
        text = text.split("</PRE>", 1)[0]

    rows: list[list[str]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or ";" not in line:
            continue
        line = re.sub(r"<[^>]+>", "", line)
        if line.startswith("Fonte:") or line.startswith("Notas:"):
            continue
        rows.append(next(csv.reader([line], delimiter=";")))
    return rows


def write_csv(rows: list[list[str]], output_path: Path, metadata: dict[str, str]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as file:
        for key, value in metadata.items():
            file.write(f"# {key}: {value}\n")
        file.write("\n")
        writer = csv.writer(file)
        writer.writerows(rows)


def query_and_save(
    output_path: Path,
    linha: str,
    coluna: str,
    incremento: str,
    arquivos: list[str],
    label: str,
    period: str,
) -> None:
    text = fetch_tabnet(linha=linha, coluna=coluna, incremento=incremento, arquivos=arquivos)
    rows = clean_prn(text)
    if not rows:
        output_path.write_text(text, encoding="latin-1")
        raise RuntimeError(f"TABNET did not return delimited rows for {label}. Raw response saved.")

    metadata = {
        "fonte": "DATASUS TABNET - SIH/SUS, Morbidade Hospitalar por local de residencia - Amazonas",
        "url_formulario": FORM_URL,
        "consulta": label,
        "periodo": period,
        "linha": linha,
        "coluna": coluna,
        "conteudo": incremento,
        "observacao": "Retorno TABNET em formato prn separado por ponto e virgula; arquivo salvo como CSV UTF-8.",
    }
    write_csv(rows=rows, output_path=output_path, metadata=metadata)


def parse_latest_period_from_form(default_year: int, default_month: int) -> tuple[int, int]:
    try:
        with urllib.request.urlopen(FORM_URL, timeout=60) as response:
            html = response.read().decode("latin-1")
    except Exception:
        return default_year, default_month

    match = re.search(r'VALUE="nram(\d{2})(\d{2})\.dbf"\s+SELECTED', html)
    if not match:
        return default_year, default_month

    year = 2000 + int(match.group(1))
    month = int(match.group(2))
    return year, month


def main() -> None:
    parser = argparse.ArgumentParser(description="Baixa CSVs do TABNET/SIH-SUS para Amazonas.")
    parser.add_argument("--start-year", type=int, default=2021)
    parser.add_argument("--end-year", type=int)
    parser.add_argument("--end-month", type=int)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw"))
    args = parser.parse_args()

    latest_year, latest_month = parse_latest_period_from_form(default_year=2026, default_month=2)
    end_year = args.end_year or latest_year
    end_month = args.end_month or (latest_month if end_year == latest_year else 12)
    arquivos = month_files(args.start_year, end_year, end_month)
    period = period_label(args.start_year, end_year, end_month)

    queries = [
        (
            "internacoes_municipio_ano_am.csv",
            "Município",
            "Ano_atendimento",
            "Internações",
            "Internacoes por municipio e ano de atendimento",
        ),
        (
            "internacoes_faixa_etaria_ano_am.csv",
            "Faixa_Etária_1",
            "Ano_atendimento",
            "Internações",
            "Internacoes por faixa etaria e ano de atendimento",
        ),
        (
            "obitos_municipio_ano_am.csv",
            "Município",
            "Ano_atendimento",
            "Óbitos",
            "Obitos por municipio e ano de atendimento",
        ),
        (
            "taxa_mortalidade_faixa_etaria_ano_am.csv",
            "Faixa_Etária_1",
            "Ano_atendimento",
            "Taxa_mortalidade",
            "Taxa de mortalidade por faixa etaria e ano de atendimento",
        ),
    ]

    for filename, linha, coluna, incremento, label in queries:
        output_path = args.output_dir / filename
        print(f"Baixando: {label}")
        query_and_save(
            output_path=output_path,
            linha=linha,
            coluna=coluna,
            incremento=incremento,
            arquivos=arquivos,
            label=label,
            period=period,
        )
        print(f"Salvo em: {output_path}")


if __name__ == "__main__":
    main()
