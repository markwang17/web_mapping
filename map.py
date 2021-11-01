import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
name = list(data['NAME'])
type = list(data['TYPE'])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%s%%20volcano" target="_blank">%s</a><br>
Height: %s m<br>
Type: <a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
"""


def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[48, -120], zoom_start=6, tiles="Stamen Terrain")

featuregroup_v = folium.FeatureGroup(name='Volcano')
for la, lo, ele, nam, typ in zip(lat, lon, elev, name, type):
    iframe = folium.IFrame(html=html % (nam, nam, str(ele), typ, typ), width=200, height=100)
    featuregroup_v.add_child(folium.CircleMarker(location=[la,lo], radius = 6,
    popup=folium.Popup(iframe), fill_color = color_producer(ele),
    color = 'grey', fill_opacity = 0.7))

featuregroup_p = folium.FeatureGroup(name='Population')
featuregroup_p.add_child(folium.GeoJson(data=open('world.json', 'r', encoding= 'utf-8-sig ').read(),
style_function= lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000<=x['properties']['POP2005']<20000000 else 'red'}))


map.add_child(featuregroup_p)
map.add_child(featuregroup_v)
map.add_child(folium.LayerControl())
map.save("Map1.html")
