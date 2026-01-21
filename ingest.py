from ligo.gracedb.rest import GraceDb
import os
from astropy.io import fits
import numpy as np

def fetch_event():
    client = GraceDb()
    events = client.superevents(query = "category: Production", max_results = 500)
    results = []
    for event in events:
        results.append(event)
    print(f"Fetched {len(results)} events from GraceDB.")
    return results

def download_skymap(superevent_id, output_dir="./skymaps"):
    client = GraceDb()
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = client.files(superevent_id).json
    skymap_filename = None
    for file_info in files.keys():
        if "bayestar.multiorder.fits" in file_info:
            skymap_filename = file_info
            break
    if skymap_filename is None:
        # print(f"No skymap found for superevent {superevent_id}.")
        return None
    
    filepath = os.path.join(output_dir, f"{superevent_id}_{skymap_filename}")
    if os.path.exists(filepath):
        # print(f"Skymap for superevent {superevent_id} already exists at {filepath}.")
        return filepath
    
    response = client.get_file(superevent_id, skymap_filename)
    return filepath

def get_skymap_stats(fits_path):
    with fits.open(fits_path) as files:
        header = files[1].header
        dist_mean = header.get('DISTMU', 0)
        dist_std = header.get('DISTSIGMA', 0)
        area_90 = header.get('AREA_90', "N/A")
        
        return {
            "dist_mean": dist_mean,
            "dist_std": dist_std,
            "area_90": area_90
        }


    
