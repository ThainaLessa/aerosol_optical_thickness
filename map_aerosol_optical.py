import numpy as np
#Para ignorar warning da biblioteca h5py versão 2.7.1 (https://github.com/quantumlib/OpenFermion/issues/175):
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import h5py
warnings.resetwarnings()

import plotly
import plotly.graph_objs as go
import plotly.tools as tls


#Arquivo .hdf5:
file_name = 'DeepBlue-SeaWiFS-1.0_L3_20100101_v004-20130604T131317Z.h5'

#Fazer leitura do arquivo com a biblioteca h5py:
with h5py.File(file_name, mode='r') as f:
    #Para saber os conjuntos de dados disponíveis no arquivo:
    #print(list(f.keys())

    #Arrays com dados da espessura óptica do aerossol estimada em 550 nm acima do oceano, e longitude e latitude dos dados:
    data = f['aerosol_optical_thickness_550_ocean'][:]
    latitude = f['latitude'][:]
    longitude = f['longitude'][:]

    #Para saber os atributos do conjunto de dados:
    #print(list(f['aerosol_optical_thickness_550_ocean'].attrs.keys()))

    #Nome do conjunto de dados - Atributos do tipo string precisam ser decodificadas para UTF-8 (python3):
    long_name = f['aerosol_optical_thickness_550_ocean'].attrs['long_name'].decode()
    
    #Alterar valores indefinidos no conjunto de dados para serem do tipo NaN
    _FillValue = f['aerosol_optical_thickness_550_ocean'].attrs['_FillValue']
    data[data == _FillValue] = np.nan
    data = np.ma.masked_array(data, np.isnan(data))
    data_ = []
    for i in range(len(data)):
        data_.append(np.mean(data[i]))
    
    scl = [[0,"rgb(150,0,90)"],[0.125,"rgb(0, 0, 200)"],[0.25,"rgb(0, 25, 255)"],[0.375,"rgb(0, 152, 255)"],[0.5,"rgb(44, 255, 150)"],[0.625,"rgb(151, 255, 0)"],[0.75,"rgb(255, 234, 0)"],[0.875,"rgb(255, 111, 0)"],[1,"rgb(255, 0, 0)"]]
    
    trace = [ dict(
        lat = latitude,
        lon = longitude,
        text = data_,
        marker = dict(
            color = data_,
            colorscale = scl,
            reversescale = True,
            opacity = 0.7,
            size = 3,
            colorbar = dict(
                thickness = 10,
                titleside = "right",
                outlinecolor = "rgba(68, 68, 68, 0)",
                ticks = "outside",
                ticklen = 3,
                showticksuffix = "last",
                dtick = 0.1
            ),
        ),
        type = 'scattergeo'
    ) ]

    layout = dict(
        geo = dict(
            showland = True,
            landcolor = "rgb(212, 212, 212)",
            subunitcolor = "rgb(255, 255, 255)",
            countrycolor = "rgb(255, 255, 255)",
            showlakes = True,
            lakecolor = "rgb(255, 255, 255)",
            showsubunits = True,
            showcountries = True,
            resolution = 50,
        ),
        title = long_name,
    )
  
    fig = {'data':trace, 'layout':layout }
    plotly.offline.plot(fig, filename="maps.html")
