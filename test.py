import os
import numpy as np
from astropy.io import fits
from astropy.table import Table

def dump_all_fits_info(file_path):
    if not os.path.exists(file_path):
        print(f"[!] ไม่พบไฟล์: {file_path}")
        return

    print(f"\n{'='*80}")
    print(f"📂 FULL DATA DUMP: {os.path.basename(file_path)}")
    print(f"{'='*80}")

    with fits.open(file_path) as hdul:
        # 1. วนลูปดูทุก HDU (Extension)
        for i, hdu in enumerate(hdul):
            print(f"\n[EXTENSION {i}: {hdu.name}]")
            print("-" * 40)
            
            # 2. พ่น Header ทั้งหมดออกมา (Metadata ทุกบรรทัด)
            print("--- ALL HEADER KEYWORDS ---")
            for key, value in hdu.header.items():
                # กรองพวกพารามิเตอร์ทางเทคนิคที่ซ้ำซ้อนออกบ้างเพื่อให้ไม่งง
                if key and key.strip():
                    print(f"{key:<12} : {value}")

            # 3. ถ้ามีตารางข้อมูล (Binary Table) ให้พ่นรายละเอียดคอลัมน์และตัวอย่าง
            if hdu.data is not None:
                print(f"\n--- DATA CONTENT (Shape: {hdu.data.shape}) ---")
                try:
                    # ใช้ Table จาก astropy เพื่อการแสดงผลที่อ่านง่าย
                    tab = Table.read(file_path, hdu=i)
                    print(f"Columns: {tab.colnames}")
                    print(tab)
                    
                    # สรุปสถิติเบื้องต้นของแต่ละคอลัมน์ (ถ้าเป็นตัวเลข)
                    print("\n--- COLUMN STATISTICS ---")
                    for col in tab.colnames:
                        if np.issubdtype(tab[col].dtype, np.number):
                            print(f"{col} | Min: {np.min(tab[col]):.2e} | Max: {np.max(tab[col]):.2e} | Mean: {np.mean(tab[col]):.2e}")
                except Exception as e:
                    print(f"Could not parse table data: {e}")
            else:
                print("--- NO DATA CONTENT IN THIS EXTENSION ---")

    print(f"\n{'='*80}")
    print("FINISHED DUMPING ALL DATA")

if __name__ == "__main__":
    # เปลี่ยน Path ให้ตรงกับไฟล์ในเครื่องคุณ
    path = "./skymaps/S251117dq_bayestar.multiorder.fits" 
    dump_all_fits_info(path)