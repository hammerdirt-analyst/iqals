## Regional assessement package --- draft

### Purpose: Help identify litter hotspots on a national and regional scale using the results from beach litter inventories.

#### The data: Beach litter survey results conducted in four watersheds of Switzerland.

February 24, 2021

As part of a national strategy to increase quality of life and biodiversity the Swiss Federal Office of the Environment mandated that a national survey of litter density and compostion be conducted.

The data is aggregated by survey date and location. Preprocessing is done by the module \<getdataforrepo\> this includes:

1. adding popualtion data for each survey location
2. adding topographic data to results
3. accounting for zero values

The full description of the preprocessing method is available in the \<getdataforrepo\> notebook.

#### Method

A dril down from the national level with an emphasis on defining a 'significant event'. In the default setting significance is defined as the 90th percentile. This can be changed in the second block.

The surveys are grouped initially by location and date and then further divided in to code groups. The code groups are defined by the \<code_groups\> notebook and stored under the output directory.

curently you can designate up to nine groups. This is not automateed and requires a bit of copy pasting if youi want to adjust that number. In future editions the number of code groups will be defined by the leingth of the array supplying the groups.

The note book defines, caluculates and displays the number of times a location exceeds the 90th percentile for each of code groups. Those results are summarized in heatmaps (nationally and regionally) and topographic maps.

#### output

1. All figures labeled in order of appearance in .jpeg format(300dpi)
2. A .html version of the notebook (code is hidden)
3. all survey data
4. beach data

#### included

1. map of geographic scope
2. regional map of significant events

#### intended use

Provide reliable, observation based data to organizations intreseted in improving quality of life and biodiversity by reducing the amont of trash in the natural envrionment.

Document in draft






