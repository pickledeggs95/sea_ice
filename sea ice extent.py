import requests
from PIL import Image, ImageDraw
import csv


## Hardcoded to download arctic sea ice extent data from NOAA in JPEG format.
def download_jpgs():
    url_base="https://masie_web.apps.nsidc.org/pub/DATASETS/NOAA/G02135/north/monthly/images/09_Sep/"
    years=range(1979, 2023)
    image_data_=[]
    for year in years:
        url=url_base + (f"N_{year}09_extn_v3.0.png")
        image_data_=requests.get(url).content
        with open(f"image_data_{year}.jpg", "wb") as f:
            f.write(image_data_)


## Crop images.
def prepare_images():
    for year in range(1979,2023):
        im=Image.open(f"C:\\Users\\Liam\\python\\learning\\sea_ice\\image_data_{year}.jpg")
        box=(16, 29, 319, 476)
        im=im.crop(box)
        im.save(f'C:\\Users\\Liam\\python\\learning\\sea_ice\\cropped_image_data_{year}.png')


## Measure distance from Pole to edge of sea-ice or nearest land mass. N.B. each pixel is 25km^2 per documentation <https://nsidc.org/sites/nsidc.org/files/G02135-V3.0_0.pdf>
def find_extent():
    extent_x=center_x
    extent_y=center_y
    global direction
    if (direction=='SE') or (direction=='NW'):
        extent_x+=2
    else:
        pass
    while px[extent_x,extent_y]!=(9, 60, 112, 255):
        if px[extent_x,extent_y] == (0, 0, 0, 255):
            break
        else:
            extent_x, extent_y=move(extent_x, extent_y)
    return extent_x, extent_y


## Specific instructions to move pixel depending on direction. Need to rename, technically all are south lol
def move(extent_x, extent_y):
    global  direction
    if direction=='N':
        extent_y-=1
        return extent_x, extent_y
    elif direction=='E':
        extent_x+=1
        return extent_x, extent_y
    elif direction=='S':
        extent_y+=1
        return extent_x, extent_y
    elif direction =='W':
        extent_x-=1
        return extent_x, extent_y
    elif direction =='NE':
        extent_x+=1
        extent_y-=1
        return extent_x, extent_y
    elif direction=='SE':
        extent_x+=1
        extent_y+=1
        return extent_x, extent_y
    elif direction=='SW':
        extent_x-=1
        extent_y+=1
        return extent_x, extent_y    
    elif direction=='NW':
        extent_x-=1
        extent_y-=1
        return extent_x, extent_y


download_jpgs()
prepare_images()

# For loop to iterate over each image and extract the extent of the sea-ice in each direction. Writes to CSV file.
filename='sea_ice.csv'
with open(filename, 'w') as csvfile: 
    writer=csv.writer(csvfile, delimiter=',')
    writer.writerow(['YEAR','N','NE','E','SE','S','SW','W','NW'])
    for year in range(1979,2023):
        im=Image.open(f'C:\\Users\\Liam\\python\\learning\\sea_ice\\cropped_image_data_{year}.png')
        px=im.load()
        center_x=154
        center_y=234

        direction='E'
        E_extent_x, E_extent_y=find_extent()
        eastern_length=[(E_extent_x-center_x)*25,(E_extent_y-center_y)*25]
        eastern_length=sum(eastern_length)

        direction='W'
        W_extent_x, W_extent_y = find_extent()
        western_length=[(center_x-W_extent_x)*25,(center_y-W_extent_y)*25]
        western_length=sum(western_length)

        direction='N'
        N_extent_x, N_extent_y=find_extent()
        northern_length=[(N_extent_x-center_x)*25,(center_y-N_extent_y)*25]
        northern_length=sum(northern_length)

        direction='S'
        S_extent_x, S_extent_y=find_extent()
        southern_length=[(S_extent_x-center_x)*25,(S_extent_y-center_y)*25]
        southern_length=sum(southern_length)

        direction='NE'
        NE_extent_x, NE_extent_y=find_extent()
        NE_length=[(NE_extent_x-center_x)*25,(center_y-NE_extent_y)*25]
        NE_length=((NE_length[0]**2)  +  (NE_length[1]**2))**0.5

        direction='SE'
        SE_extent_x, SE_extent_y=find_extent()
        SE_length=[(SE_extent_x-center_x)*25,(SE_extent_y-center_y)*25]
        SE_length=((SE_length[0]**2)  +  (SE_length[1]**2))**0.5

        direction='SW'
        SW_extent_x, SW_extent_y=find_extent()
        SW_LENGTH=[(center_x-SW_extent_x)*25,(SW_extent_y-center_y)*25]
        SW_LENGTH=((SW_LENGTH[0])**2+(SW_LENGTH[1])**2)**0.5

        direction='NW'
        NW_extent_x, NW_extent_y=find_extent()
        NW_LENGTH=[(center_x-NW_extent_x)*25,(center_y-NW_extent_y)*25]
        NW_LENGTH=((NW_LENGTH[0])**2+(NW_LENGTH[1])**2)**0.5


        N= northern_length
        NE= round(NE_length)
        E= eastern_length
        SE= round(SE_length)
        S= southern_length
        SW= round(SW_LENGTH)
        W= western_length
        NW= round(NW_LENGTH)

        span=[N,NE,E,SE,S,SW,W,NW]
        writer.writerow([{year},N,NE,E,SE,S,SW,W,NW])
        print(f'{year}: {span}')

