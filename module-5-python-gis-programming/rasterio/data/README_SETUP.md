# GIST 604B - Real Geospatial Data Setup Guide

Welcome to authentic geospatial learning! This setup downloads **real satellite imagery and elevation data** from NASA, USGS, and NOAA for your rasterio assignments.

## 🌍 What You'll Get

Instead of synthetic data, you'll work with:

- **Real NASA SRTM Digital Elevation Model** (30m resolution)
- **Real Landsat 8 Surface Reflectance imagery** (6-band multispectral)
- **Real MODIS Land Surface Temperature** (1km daily data)
- **Professional metadata** (STAC-compliant)
- **Supporting vector datasets**

All focused on **Phoenix, Arizona** - an ideal study area with diverse terrain, clear imagery, and interesting urban heat island effects.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to this directory
cd rasterio/data

# Run the automated setup
python setup_rasterio_data.py
```

This will:
✅ Check your Python environment  
✅ Install missing packages  
✅ Download real geospatial data  
✅ Create fallback synthetic data if needed  
✅ Validate your setup  

### Option 2: Manual Setup

```bash
# Install required packages
pip install -r requirements.txt

# Download the data
python create_sample_data.py
```

## 📊 Expected Data

After successful setup, you'll have:

```
data/
├── raster/
│   ├── phoenix_dem_30m.tif           # Digital Elevation Model
│   ├── landsat8_phoenix_2024.tif     # Satellite imagery (6 bands)
│   └── modis_lst_phoenix.tif         # Land surface temperature
├── vector/
│   ├── phoenix_study_area.geojson    # Study area boundary
│   └── sample_points.geojson         # Validation points
├── downloads/                        # Raw downloads (temporary)
├── processed/                        # Your analysis outputs
├── data_inventory.json               # Dataset catalog
├── phoenix_stac_metadata.json        # STAC metadata
└── README.md                         # Dataset documentation
```

**Total size:** ~50-200 MB (manageable for coursework)

## 🔧 System Requirements

**Python:** 3.8 or higher  
**Key packages:** rasterio, geopandas, numpy, requests  
**Internet:** Required for initial data download  
**Storage:** ~500 MB free space recommended  

### Installation Issues?

If package installation fails:

```bash
# Try with conda instead
conda install -c conda-forge rasterio geopandas numpy pandas matplotlib

# Or install specific packages individually
pip install rasterio
pip install geopandas
```

## 📡 How Data Download Works

1. **Real Data First:** Attempts to download from NASA/USGS servers
   - SRTM DEM from NASA OpenTopography
   - Landsat from USGS/AWS Open Data Registry
   - MODIS LST from NASA LAADS DAAC

2. **Smart Fallbacks:** If downloads fail, creates high-quality synthetic data
   - Based on real geographic patterns
   - Maintains authentic data characteristics
   - Still suitable for professional learning

3. **Quality Validation:** Ensures all data is properly georeferenced

## 🎓 Learning Benefits

Working with real data means:

✅ **Authentic experience** - same data scientists use  
✅ **Real-world challenges** - handling actual data quality issues  
✅ **Professional skills** - industry-standard formats and metadata  
✅ **Practical knowledge** - understanding satellite data characteristics  

## 🧪 Quick Test

Verify your setup works:

```python
import rasterio
import geopandas as gpd
import numpy as np

# Test DEM loading
with rasterio.open('data/raster/phoenix_dem_30m.tif') as src:
    dem = src.read(1)
    print(f"DEM shape: {dem.shape}")
    print(f"Elevation range: {np.nanmin(dem):.0f} to {np.nanmax(dem):.0f} meters")
    print(f"CRS: {src.crs}")

# Test multispectral imagery
with rasterio.open('data/raster/landsat8_phoenix_2024.tif') as src:
    print(f"Landsat bands: {src.count}")
    print(f"Image size: {src.width} x {src.height}")

print("✅ All tests passed! Ready for rasterio learning.")
```

## 🛠️ Troubleshooting

### "Package installation failed"
```bash
# Try upgrading pip first
python -m pip install --upgrade pip

# Then install packages
pip install -r requirements.txt
```

### "Data download failed"
- **Check internet connection**
- **Try running again** (servers sometimes busy)
- **Still works!** - script creates synthetic fallbacks automatically

### "No raster files found"
```bash
# Re-run data creation
python create_sample_data.py

# Check what was created
ls -la data/raster/
```

### "Import errors"
```bash
# Restart your Python environment/Jupyter kernel
# Re-run the setup
python setup_rasterio_data.py
```

## 📚 Next Steps

Once setup is complete:

1. **Start learning:** Open `01_function_load_and_explore_raster.ipynb`
2. **Read overview:** Check `00_start_here_overview.ipynb` 
3. **Explore data:** Review `data/README.md` for detailed dataset info
4. **Try examples:** Test the code snippets in the dataset documentation

## 🔄 Updates & Maintenance

This system can:
- **Re-download data** if files are corrupted
- **Update datasets** when new versions are available  
- **Add new data sources** as the course evolves

To refresh your data:
```bash
rm -rf data/raster/*  # Clear old data
python create_sample_data.py  # Download fresh data
```

## 🆘 Getting Help

1. **Check logs:** Setup scripts show detailed error messages
2. **Read documentation:** `data/README.md` has usage examples
3. **Ask for help:** Contact your instructor or TA
4. **Verify environment:** Run `python setup_rasterio_data.py` again

## 🎯 Why Real Data Matters

In professional GIS work, you'll encounter:
- **Data download challenges** - servers, authentication, formats
- **Quality issues** - missing data, coordinate problems, large files
- **Processing workflows** - metadata, projections, optimization

This setup gives you authentic practice with these real-world skills while learning rasterio fundamentals.

---

**Ready to start?** Run `python setup_rasterio_data.py` and begin your journey with real geospatial data! 🚀

*Questions? Check with your GIST 604B instructor or TA.*