-----------------------------------
Overview:
-----------------------------------

A three month service learning project for the Idaho Policy Institute(IPI); this is a project I completed for my graduate data science course at Boise State. This Project successfully makes use of Idaho's municipal government financial data by providing insightful models to augment the decision making process. This specifically correlates government expenditure and crime allowing for the optimization of all future investments. 

-----------------------------------
Summary:
-----------------------------------

I was provided a database comprised of financial expenditure/revenue and crime for various cities in Idaho. My client, the Idaho Policy Institute, desired to know how better to allocate resources to better reduce crime. Throughout my analysis I found the data to contain missing values, was unbalance along the temporal axis and was overall sparse. However, after some data scrapping, dimensionality reduction and minimal interpolation; I was successful in cleaning the data having greatly reduced the noise.

I then used a non biased OLS time fixed effects regression model to further understand the data. Having made a statistically significant and reliable model I was able to draw a clear insight. Many of the features were that of general/overall expenditure and revenue, thus were not only largely correlated to crime but also population. This is difficult because logically, more people means more total crime even if the rates are identical.

Taking another look at the model I then noticed that the most statistically significant feature (by a large margin) was that of "long term outstanding debt." The correlation between long term debt of a city and the associated crime provided invaluable insight towards the client's desired objective, reducing crime. Using this information government bodies are better able to allocate resources; by removing the "pigeon superstition" associated to investing funds, my analysis saved local governments thousands of dollars.




-----------------------------------
Data Manual:
-----------------------------------

GeoNames Postal Code files :

allCountries.zip: all countries, for the UK only the outwards codes, the UK total codes are in GB_full.csv.zip 
GB_full.csv.zip the full codes for the UK, ca 1.7 mio rows
<iso countrycode>: country specific subset also included in allCountries.zip
This work is licensed under a Creative Commons Attribution 3.0 License.
This means you can use the dump as long as you give credit to geonames (a link on your website to www.geonames.org is ok)
see http://creativecommons.org/licenses/by/3.0/
UK (GB_full.csv.zip): Contains Royal Mail data Royal Mail copyright and database right 2017.
The Data is provided "as is" without warranty or any representation of accuracy, timeliness or completeness.

This readme describes the GeoNames Postal Code dataset.
The main GeoNames gazetteer data extract is here: http://download.geonames.org/export/dump/


For many countries lat/lng are determined with an algorithm that searches the place names in the main geonames database 
using administrative divisions and numerical vicinity of the postal codes as factors in the disambiguation of place names. 
For postal codes and place name for which no corresponding toponym in the main geonames database could be found an average 
lat/lng of 'neighbouring' postal codes is calculated.
Please let us know if you find any errors in the data set. Thanks

For Canada we have only the first letters of the full postal codes (for copyright reasons)

For Chile we have only the first digits of the full postal codes (for copyright reasons)

For Ireland we have only the first letters of the full postal codes (for copyright reasons)

For Malta we have only the first letters of the full postal codes (for copyright reasons)

The Argentina data file contains the first 5 positions of the postal code.

For Brazil only major postal codes are available (only the codes ending with -000 and the major code per municipality).

The data format is tab-delimited text in utf8 encoding, with the following fields :

country code      : iso country code, 2 characters
postal code       : varchar(20)
place name        : varchar(180)
admin name1       : 1. order subdivision (state) varchar(100)
admin code1       : 1. order subdivision (state) varchar(20)
admin name2       : 2. order subdivision (county/province) varchar(100)
admin code2       : 2. order subdivision (county/province) varchar(20)
admin name3       : 3. order subdivision (community) varchar(100)
admin code3       : 3. order subdivision (community) varchar(20)
latitude          : estimated latitude (wgs84)
longitude         : estimated longitude (wgs84)
accuracy          : accuracy of lat/lng from 1=estimated, 4=geonameid, 6=centroid of addresses or shape
