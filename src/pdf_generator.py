from pathlib import Path
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

OUTPUT_PDF = Path(__file__).resolve().parent.parent / "Global_Exchanges_Master_Report.pdf"

def generate_pdf_report(df: pd.DataFrame) -> Path:
    export_df = df.copy()

    # Ensure calculated columns exist
    if "Last_Price" in export_df.columns and "Prev_Close" in export_df.columns:
        export_df["Last Closing Price"] = export_df["Last_Price"]
        export_df["Price Difference"] = (export_df["Last_Price"] - export_df["Prev_Close"]).round(2)
        export_df["% Difference"] = ((export_df["Price Difference"] / export_df["Prev_Close"]) * 100).round(2)

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=landscape(A4),
        rightMargin=28,
        leftMargin=28,
        topMargin=24,
        bottomMargin=24,
    )
    styles = getSampleStyleSheet()
    elements = []

    updated_str = (
        str(export_df["Updated_At"].dropna().iloc[0])
        if "Updated_At" in export_df.columns and not export_df["Updated_At"].dropna().empty
        else "Verification Standby"
    )
    elements.append(Paragraph("Global Stock Exchanges & Indices Filtered Ledger", styles["Title"]))
    elements.append(Paragraph(f"Exported Indices: {len(export_df)} | Last Sync: {updated_str}", styles["Normal"]))
    elements.append(Spacer(1, 14))

    # Strict 5-column PDF layout
    desired_cols = [
        "Index / Benchmark Name",
        "yfinance Ticker",
        "Last Closing Price",
        "Price Difference",
        "% Difference",
    ]
    cols = [c for c in desired_cols if c in export_df.columns]
    table_data = [cols] + export_df[cols].fillna("-").astype(str).values.tolist()

    table = Table(table_data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(table)
    doc.build(elements)
    return OUTPUT_PDF
