import requests
from bs4 import BeautifulSoup


#Getting the url and storing the page contents into a variable to be scraped for data.
headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/"
r = requests.get(base_url, headers=headers)
c=r.content

soup=BeautifulSoup(c,"html.parser")

all=soup.find_all("div",{"class":"propertyRow"})

all[0].find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","")

page_nr=soup.find_all("a",{"class":"Page"})[-1].text

#Empty list to store for loop results
l = []

#For loop that will scrape the web pages to collect the wanted real estate data for each listing.
for page in range(0,int(page_nr)*10,10):
    url = base_url + "t=0&s=" + str(page) + ".html"
    print(url)
    r=requests.get(url, headers=headers)
    c=r.content
    #c=r.json()["list"]
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    for item in all:
        d={}
        d["Address"]=item.find_all("span",{"class","propAddressCollapse"})[0].text
        try:
            d["Locality"]=item.find_all("span",{"class","propAddressCollapse"})[1].text
        except:
            d["Locality"]=None
        d["Price"]=item.find("h4",{"class","propPrice"}).text.replace("\n","").replace(" ","")
        try:
            d["Beds"]=item.find("span",{"class","infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Full Baths"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None
        try:
            d["Half Baths"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
        l.append(d)

#Converting pandas dataframe into a csv file.
import pandas
df=pandas.DataFrame(l)
df
df.to_csv("Output.csv")


    



    
    








