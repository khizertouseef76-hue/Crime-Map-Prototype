from typing import Dict, Any, Tuple
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import st_folium
from shapely.geometry import Point
from shapely.ops import transform as shp_transform
import pyproj

from utils.colors import rate_to_color

def _circle_points(lat: float, lon: float, miles: float, n: int = 64):
    """
    Create a lat/lon circle polygon as list of (lat, lon) points.
    """
    # Project to local metric, buffer, then project back
    proj_wgs84 = pyproj.CRS("EPSG:4326")
    proj_m = pyproj.CRS("EPSG:3857")

    project = pyproj.Transformer.from_crs(proj_wgs84, proj_m, always_xy=True).transform
    unproject = pyproj.Transformer.from_crs(proj_m, proj_wgs84, always_xy=True).transform

    p = Point(lon, lat)
    meters = miles * 1609.34
    p_buf = shp_transform(unproject, shp_transform(project, p).buffer(meters, resolution=n))
    return [(y, x) for x, y in p_buf.exterior.coords]

def render_map(
    geojson: Dict[str, Any],
    center: Tuple[float, float],
    selected_metric: str,
    radius_miles: float,
    height: int = 620,
):
    """
    Draws a Folium map with tract polygons colored by 'rate'.
    """
    fmap = folium.Map(location=center, zoom_start=12, tiles="cartodbpositron")

    # Style function for GeoJSON
    def style_fn(feature):
        rate = feature.get("properties", {}).get("rate")
        color, _ = rate_to_color(rate)
        return {
            "fillColor": color,
            "color": "#334155",
            "weight": 1,
            "fillOpacity": 0.55,
        }

    tooltip = GeoJsonTooltip(
        fields=["tract_id", "rate"],
        aliases=["Tract", "Rate/100k"],
        localize=True,
        sticky=True,
        labels=True,
    )

    gj = folium.GeoJson(
        geojson,
        name="Tracts",
        style_function=style_fn,
        tooltip=tooltip,
    )
    gj.add_to(fmap)

    # Legend
    legend_html = """
    <div style="
      position: fixed; 
      bottom: 35px; left: 15px; z-index: 9999;
      background: white; border: 1px solid #CBD5E1; padding: 10px 12px; border-radius: 10px;
      box-shadow: 0 4px 8px rgba(0,0,0,.08); font-size: 13px;">
      <b>Rate per 100k</b><br>
      <div style="margin-top:6px">
        <div><span style="display:inline-block;width:14px;height:14px;background:#7F1D1D;margin-right:6px;border-radius:3px;border:1px solid #0001"></span> > 1000</div>
        <div><span style="display:inline-block;width:14px;height:14px;background:#DC2626;margin-right:6px;border-radius:3px;border:1px solid #0001"></span> 500–999</div>
        <div><span style="display:inline-block;width:14px;height:14px;background:#F87171;margin-right:6px;border-radius:3px;border:1px solid #0001"></span> 200–499</div>
        <div><span style="display:inline-block;width:14px;height:14px;background:#FBCFE8;margin-right:6px;border-radius:3px;border:1px solid #0001"></span> &lt; 200</div>
        <div><span style="display:inline-block;width:14px;height:14px;background:#9CA3AF;margin-right:6px;border-radius:3px;border:1px solid #0001"></span> No data</div>
      </div>
    </div>
    """
    fmap.get_root().html.add_child(folium.Element(legend_html))

    # Pin and 1-mile circle
    lat, lon = center
    folium.Marker(location=(lat, lon), tooltip="Search location").add_to(fmap)
    circle_pts = _circle_points(lat, lon, radius_miles)
    folium.Polygon(circle_pts, color="#0EA5E9", weight=2, fill=False, opacity=0.8).add_to(fmap)

    return st_folium(fmap, height=height, returned_objects=[])
