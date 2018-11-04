"""
This program is a web map showing the world population(2005 data) based on colors.
Also, all the volcanic spots with PEI>7 (Population Exposed Index) as well as
all volcanic spots with VEI>6 (Volcanic Explosive Index) have been added to this web map.

Developed by: Behzad Farhangirad
"""
import folium
import pandas
data=pandas.read_json("world volcanoes.json")
features=list(data["features"])

map=folium.Map(location=[38,-99],zoom_start=2,tiles="mapbox bright")
fgv_vei=folium.FeatureGroup(name="All Volcanoes with vei>5")
fgv=folium.FeatureGroup(name="All Volcanoes with pei>6")
fgp=folium.FeatureGroup(name="Population")
fgv_r1=folium.FeatureGroup(name="Volcanoes in Mexico and Central America with pei>6")
fgv_r2=folium.FeatureGroup(name="Volcanoes in Indonesia with pei>6")

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
    vei=properties['VEI_Holoce']
    if pei>=6:
        popup=folium.Popup("PEI:"+str(pei), parse_html=True)
        fgv.add_child(folium.CircleMarker(location=[lt,ln], radius=7,
        popup=popup,fill_color="red", color="gray", fill_opacity=0.7))
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

    if vei!="Unknown VEI" or "No confirmed eruptions":
        if vei=="5" or vei=="6" or vei=="7":
            popup=folium.Popup("VEI:"+vei, parse_html=True)
            fgv_vei.add_child(folium.CircleMarker(location=[lt,ln], radius=7,
            popup=popup,fill_color="green", color="gray", fill_opacity=0.7))

    i=i+1

map.add_child(fgv)
map.add_child(fgv_vei)
map.add_child(fgv_r1)
map.add_child(fgv_r2)
map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("map_pop_vol2.html")
