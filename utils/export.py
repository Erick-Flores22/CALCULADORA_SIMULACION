import csv
import pandas as pd

def export_csv(path, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['i','y','x','r'])
        for r in rows:
            w.writerow(r)

def export_xlsx(path, rows):
    df = pd.DataFrame(rows, columns=['i','y','x','r'])
    df.to_excel(path, index=False)
