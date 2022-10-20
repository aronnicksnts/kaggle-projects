# Abstract - Iowa Liquor Sales
Data visualization applied to the liquor sales in Iowa from 2012 to 2017. It appears that significant data is missing from the year 2017 as it does not match the [annual liquor sales](https://abd.iowa.gov/sites/default/files/media/file/2020-09/annual_report_fy17.pdf) from the Alcoholic Beverages Division in the State of Iowa. Significant data from the year 2016 also appears to be missing as it does not match the data in the dataset. 

This notebook visualizes the following: 
- the total number of bottles sold per year and per month (in totality of that particular month), 
- the city with the highest bottles sold, 
- liquor with the highest revenue and the liquor that is most sold, 
- and stores that sold the most.

## Dataset Link
Download the dataset and extract it to the folder in order to use the code.

[Kaggle Link](https://www.kaggle.com/datasets/residentmario/iowa-liquor-sales)

## Report
![Bottles Sold per Year](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/BottlesSoldPerYear.jpg)

The figure shows the total number of bottles sold per year. From the data it shows that the number of bottles sold significantly dropped from 2016 to 2017. However, from the [report](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/BottlesSoldPerYear.jpg) of the Alcoholic Beverages Division in the State of Iowa, it appears that the annual liquor sales from 2006-2017 increased at around a steady rate where-in the annual liquor sales in 2016 was actually 288.9 million dollars and in 2017 it was 305.6 million dollars which highly contradicts the data given in the kaggle dataset.

The figure below is highly correlated to the number of bottles sold per year, where-in it shows the annual liquor sales
![Annual Liquor Sales](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/TotalSalesPerYear.jpg)

Moving on, looking at the total bottles sold per month chart, where-in the total sales of each month is aggregated, it appears that the bottles sold has seasonality. The bottles sold appears to peak at June, October, and December with the lowest being at November. The number of bottles sold slowly increases from January to June and declines slowly until September.

![Total Bottles Sold Per Month](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/TotalBottlesMonth.jpg)

The store with the highest sales is Hy-Vee #3 / BDI / Des Moines with more than 47 million dollars in total sales, and the next store with the highest sales would be Central City 2 with about 34 million dollars in sales, and the next three would be Hy-Vee Wine and Spirits, and Sam's Club 8162 and 6344 with around 19 million dollars in sales
![Highest Establishment Sales](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/StoreHighSales.jpg)

The most bought liquor is the Black Velvet, Captain Morgan Spiced Rum, Hawkeye Vodka, Mccormick Vodka Pet, and Barton Vodka. The Black Velvet has a significant lead amongst the most sought after liquors with around 2.5 million bottles sold, and the rest of the liquors ranging from around 900 thousand up to 1.6 million bottles sold.
![Liquor Bottles Sold](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/LiquorMostSold.jpg)

The city with the highest bottles sold would go to Des Moines with around 42 million bottles sold from 2012-2017 (2016-2017 data is incomplete). The 4 following cities are Cedar Rapids, Iowa City, and Ames.
![City Bottles Sold](https://github.com/aronnicksnts/kaggle-projects/blob/main/Iowa%20Liquor%20Sales/Images/CityBottleSold.jpg)
