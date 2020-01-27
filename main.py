import folium
import pandas

#function to give color regarding the elevation
def give_me_color(elev):
    if elev < 1000:
        return 'green'
    elif elev>= 1000 and elev <3000:
        return 'orange'
    elif elev>= 3000:
        return 'red'
    else:
        return 'black'

#read data from csv file
data = pandas.read_csv('Volcanoes.txt')

#save data in lists
lat= list(data['LAT'])
lon= list(data['LON'])
elev= list(data['ELEV'])


#html version to transform a bit

html = """<h4>Volcano information:</h4>
Height: %s m
"""

#starting point of our map
map = folium.Map(location=[38.58, -99.09],zoom_start=5, tiles="Stamen Terrain")

fgv = folium.FeatureGroup(name = "Volcanoes")

#iterate through the values and assign those values to the map
for lt, ln, el in zip(lat, lon, elev):
    iframe = folium.IFrame(html=html % str(el), width=200, height=100)
    fgv.add_child(
        folium.CircleMarker(location=[lt, ln],
                            radius=6,
                            popup=folium.Popup(iframe),
                            fill=True,
                            fill_color = give_me_color(el),
                            color = 'grey',
                            fill_opacity=0.7
                            ))

fgp = folium.FeatureGroup(name = "Population")

#add_child means add layers of points
fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding='utf-8-sig').read(),
             style_function= lambda x: {'fillColor': 'yellow' if x['properties']['POP2005']< 1000000
             else 'orange' if 1000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))



map.add_child(fgv)

map.add_child(fgp)

map.add_child(folium.LayerControl())

map.save("Circle_Volcanoes_elevation_v4.html")
