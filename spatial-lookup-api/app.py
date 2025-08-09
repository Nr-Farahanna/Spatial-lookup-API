from flask import Flask, request, jsonify
import geopandas as gpd
from shapely.geometry import Point

app = Flask(__name__)

# Load GeoJSON files
parliament = gpd.read_file(r"C:\Users\farahanna.suid\OneDrive - Malaysian Communications and Multimedia Commission\Documents\QMoD\geodata\spatial-lookup-api\parliament.geojson")
dun = gpd.read_file(r"C:\Users\farahanna.suid\OneDrive - Malaysian Communications and Multimedia Commission\Documents\QMoD\geodata\spatial-lookup-api\dun.geojson")
district = gpd.read_file(r"C:\Users\farahanna.suid\OneDrive - Malaysian Communications and Multimedia Commission\Documents\QMoD\geodata\spatial-lookup-api\district.geojson")

@app.route('/lookup')
def lookup():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not lat or not lon:
        return jsonify({"error": "Missing lat or lon"}), 400

    try:
        point = Point(float(lon), float(lat))

        # Parliament match
        match_parliament = parliament[parliament.contains(point)]
        parliament_name = match_parliament.iloc[0]["parliament"] if not match_parliament.empty else None

        # DUN match
        match_dun = dun[dun.contains(point)]
        dun_name = match_dun.iloc[0]["dun"] if not match_dun.empty else None

        # District match
        match_district = district[district.contains(point)]
        district_name = match_district.iloc[0]["district"] if not match_district.empty else None

        return jsonify({
            "match": any([parliament_name, dun_name, district_name]),
            "district": district_name,
            "parliament": parliament_name,
            "dun": dun_name
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
