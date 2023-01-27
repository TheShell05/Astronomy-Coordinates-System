import streamlit as st
from astropy.coordinates import SkyCoord, Distance
from astropy import units as u
from astropy.io import fits
from astropy.table import QTable
from astropy.table import Table
from astroquery.gaia import Gaia
Gaia.ROW_LIMIT = 10000

import matplotlib.pyplot as plt
import os 


with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    choice = st.radio("Navigation", ["Co-ordinates","FITS File Viewing"])
    st.info("This project application helps you build and explore the universe and the FITS File.")

if choice == "Co-ordinates":
    st.title("Input the Celestial body for which you want the Co-ordinates")
    Celest_name = st.text_input("Input the Celestial body for which you want the Co-ordinates")
    ra_dec = SkyCoord.from_name(Celest_name)
    st.write('The Right Ascention is', ra_dec.ra)
    st.write('The Declination is', ra_dec.dec)

    #st.title("Input the Radius (in Radians) that you want to look for stars that might be members")
    #radii = st.text_input("Input the Radius (in Radians) that you want to look for stars that might be members")
    job = Gaia.cone_search_async(Celest_name, radius = 0.5*u.deg)
    celest_table = job.get_results()

    cols = [
    'source_id',
    'ra',
    'dec',
    'parallax',
    'parallax_error',
    'pmra',
    'pmdec',
    'radial_velocity',
    'phot_g_mean_mag',
    'phot_bp_mean_mag',
    'phot_rp_mean_mag'
    ]

    celest_table[cols].write('gaia_results.fits', overwrite=True)
    # only keep stars brighter than G=19 magnitude
    celest_table = QTable.read('gaia_results.fits')
    celest_table_df = Table.to_pandas(celest_table)
    st.dataframe(celest_table_df)


if choice == "FITS Image Viewing": 
    image_file = st.file_uploader("Upload the FITS file")
    hdu_list = fits.open(image_file)
    #hdu_list_df = Table.to_pandas(hdu_list)
    dat = Table.read(image_file)
    df = dat.to_pandas()
    st.dataframe(df)
    
