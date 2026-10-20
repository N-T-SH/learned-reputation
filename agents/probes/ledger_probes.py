    summary = out / f"summary-{slug}.csv"
    with summary.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "cell", "n", "p_named_x", "p_named_y", "p_named_target", "p_named_d", "repair_failures"])
        by = {}
        for row in rows:
            by.setdefault(row["cell"], []).append(row)
        for cell, chunk in by.items():
            n = len(chunk)
            fails = sum(1 for row in chunk if row["repair"] != "ok")
            def rate(key):
                if key not in chunk[0]["targets"]:
                    return ""
                hits = sum(row["targets"][key] in row["partners"] for row in chunk)
                return round(hits / n, 3)
            writer.writerow([slug, cell, n, rate("x"), rate("y"), rate("target"), rate("d"), fails])
