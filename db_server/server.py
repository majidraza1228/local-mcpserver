from fastmcp import FastMCP
from sqlalchemy import create_engine, text
import os
DSN = os.environ.get("DB_DSN", "sqlite+pysqlite:///./app.db")
READ_ONLY = os.environ.get("DB_READONLY", "1") == "1"
MAX_ROWS = int(os.environ.get("DB_MAX_ROWS", "1000"))
app = FastMCP(name="db-tools", instructions="Safe SQLite access for previews and queries")
engine = create_engine(DSN, future=True)
@app.resource(uri="resource://db/schema", mime_type="text/markdown")
def schema_resource():
    with engine.connect() as c:
        lines = ["| schema | table | column | type |", "|---|---|---|---|"]
        for (t,) in c.exec_driver_sql("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            for col in c.exec_driver_sql(f"PRAGMA table_info('{t}')").fetchall():
                lines.append(f"| main | {t} | {col[1]} | {col[2]} |")
        return "\n".join(lines)
@app.tool(description="List tables")
def db_tables():
    with engine.connect() as c:
        return {"tables": [r[0] for r in c.exec_driver_sql("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]}
@app.tool(description="Preview first N rows from a table")
def db_preview(table: str, limit: int = 20):
    limit = max(1, min(limit, 200))
    with engine.connect() as c:
        res = c.exec_driver_sql(f"SELECT * FROM {table} LIMIT {limit}").fetchmany(limit)
        cols = res[0].keys() if res else []
        return {"columns": list(cols), "rows": [list(r) for r in res]}
@app.tool(description="Run parameterized SQL; caps rows; blocks writes when READ_ONLY")
def db_query(sql: str, params: dict | None = None, max_rows: int = 200):
    if READ_ONLY and any(k in sql.lower() for k in ["insert ","update ","delete ","alter ","drop ","truncate ","create "]):
        return {"error": "write operations are disabled"}
    cap = min(max_rows, MAX_ROWS)
    rows = []
    with engine.connect() as c:
        cur = c.execute(text(sql).execution_options(stream_results=True), params or {})
        cols = cur.keys()
        for i, r in enumerate(cur):
            if i >= cap: break
            rows.append(list(r))
    return {"columns": list(cols), "rows": rows, "rowCount": len(rows)}

if __name__ == "__main__":
    app.run()
