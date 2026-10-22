# Open (Esri-free) imagery pipeline (22.10.2026)

Decision: no Esri World Imagery in any video (static-map terms need permission for monetised use).
- `open_imagery.py lon lat d w h out.jpg`: NASA GIBS Blue Marble (500 m, shaded relief + bathymetry) + Sentinel-2 L2A (10 m, AWS earth-search, SCL cloud mask, summer scenes, water tone matching, smooth sea).
- `engine66o.py`: engine66 reading `satO/` + credit line "NASA Blue Marble · Contains modified Copernicus Sentinel data 2023-2025 · Natural Earth".
- `render66o.sh <short>`: render with existing voice/mix/timing.
Known limit: at town/rooftop zoom Sentinel-2 is soft (Monaco, Llívia, Point Roberts): keep those moments short or stylised.
