import pandas as pd
import geopandas as gpd

coordinates = [
    "40 42 54 N;0 36 41 W",
    "40 42 41 N;0 36 46 W",
    "40 42 33 N;0 36 33 W",
    "40 42 35 N;0 36 24 W",
    "40 44 01 N;0 35 10 W",
    "40 43 55 N;0 36 14 W",
    "40 42 47 N;0 36 45 W"
]

# add array to dataframe
df = pd.DataFrame(coordinates, columns=['coordinates'])
# separate lat lon
df['lat'] = df['coordinates'].apply(lambda x: x.split(';')[0])
df['lon'] = df['coordinates'].apply(lambda x: x.split(';')[1])

# convert to decimal degrees
df['lat'] = (df['lat'].apply(lambda x: x.split(' ')[0]).astype(float) + \
    df['lat'].apply(lambda x: x.split(' ')[1]).astype(float)/60 + \
    df['lat'].apply(lambda x: x.split(' ')[2]).astype(float)/3600) * \
    df['lat'].apply(lambda x: -1 if 'S' in x else 1)

# we need to know if it is possitive or negative, lon if has W is negative
df['lon'] = (df['lon'].apply(lambda x: x.split(' ')[0]).astype(float) + \
    df['lon'].apply(lambda x: x.split(' ')[1]).astype(float)/60 + \
    df['lon'].apply(lambda x: x.split(' ')[2]).astype(float)/3600) * \
    df['lon'].apply(lambda x: -1 if 'W' in x else 1)

# remove coordinates
df.drop('coordinates', axis=1, inplace=True)    

# convert to geodataframe
gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.lon, df.lat))

# convert coordinates to WGS8430N
gdf.crs = {'init': 'epsg:4326'}
gdf = gdf.to_crs(epsg=32630)
gdf['x'] = gdf.geometry.x -694521.83
gdf['y'] = gdf.geometry.y -4505806.89

gdf.to_csv('WGS8430N.csv', index=False)