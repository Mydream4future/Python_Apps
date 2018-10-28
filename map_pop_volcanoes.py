import folium
import pandas
data=pandas.read_json("world volcanoes.json")
features=list(data["features"])

map=folium.Map(location=[38,-99],zoom_start=2,tiles="mapbox bright")
fgv=folium.FeatureGroup(name="All Volcanoes with pei>7")
fgp=folium.FeatureGroup(name="Population")
fgv_r1=folium.FeatureGroup(name="Volcanoes in Mexico and Central America with pei>7")
fgv_r2=folium.FeatureGroup(name="Volcanoes in Indonesia with pei>7")

fgp.add_child(folium.GeoJson(data=open("world.json",'r',encoding="utf-8-sig").read(),
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000<= x['properties']['POP2005'] <25000000 else 'red'}))

i=0
while i<1546:
    properties=features[i]["properties"]
    lt=properties['Latitude']
    ln=properties['Longitude']
    pei=properties['PEI']
    reg=properties['Region']
    if pei>=7:
        fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=7,
        fill_color="red", color="gray", fill_opacity=0.7))
        if reg=="M?xico and Central America":
            fgv_r1.add_child(folium.CircleMarker(location=[lt,ln], radius=7,
            fill_color="red", color="gray", fill_opacity=0.7))
        elif reg=="Indonesia":
            fgv_r2.add_child(folium.CircleMarker(location=[lt,ln], radius=7,
            fill_color="red", color="gray", fill_opacity=0.7))
        else:
            pass
    else:
        pass
    i=i+1

map.add_child(fgv)
map.add_child(fgv_r1)
map.add_child(fgv_r2)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("map_pop_vol.html")
