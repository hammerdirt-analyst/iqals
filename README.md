## Identification, quantififcation and analysis of observable anthropogenic debris along swiss freshwater systems.
![map of bielersee and neuch](https://github.com/hammerdirt-analyst/iqals/blob/main/resources/maps/aare_scaled.jpeg)

### <span style="color:#008891">Purpose</span>

Produce decision support packages using the data from beach litter surveys conducted in Switzerland.

### <span style="color:#008891">Recent changes</span>

#### Developing the class and methods for the application

We removed the summary notebooks and replace them with reports for each aggregation level. We are defining the methods for the backend of the application based on the comments and needs recieved from stakeholders over the past year.

Notebooks project indicaotrs:

1. The project_scope notebook provides summary statistics on effected populations, time to survey, number of municipalities, geographic and administrative scope
2. The key_indicator notebook is an explanantion of the key indicators and an example of how you could use them to find specific objects or groups of objects
3. The code_groups notebook sets grouping levels for objects

Notebooks aggregated results:

1. The sitereport notebook gives a summary and analysis of the results for one municipality and compares those results to the water feature, the river bassin and the national results
2. The feature report notebook is for generating reports at the lake or river level
3. The bassin_report notebook is for generating a report for a survey area

### About the data

The data was collected by a variety of organisations and indivdiduals. The earliest records are November 2015 on Lac Léman. All the surveys follow a modified Marine Litter Watch or OSPAR method.

#### A propos des données

Les données ont été recueillies par diverses organisations et personnes. Les premiers enregistrements datent de novembre 2015 sur le lac Léman. Toutes les enquêtes suivent une méthode modifiée de surveillance des déchets marins ou OSPAR.

### How to use this repo:

Clone the repo, Jupyter lab or JupyterNotebooks are required . The workbook 'getdataforrepo' will preprocess the data for you and attach BFS numbers. All other modules draw from the data provided by 'getdataforrepo'.

Make sure to use the requirements.txt or .yml file to set your environment.

!! Make sure to read the use case for each template or notebook !!

#### The atemplate notebook:

This notebook should produce the following output (after you run getdataforrepo and infrastructurerankings):

![wheres the sample](https://github.com/hammerdirt-analyst/iqals/blob/main/output/test_directory/atestchart.svg)

If this doesn't work check the requirements.txt file. You probably need a more updated version of jupyterlab or python. Geopandas is absent from many prepackaged environments. Contact analyst@hammerdirt if you need assistance.

**Syncing of geo data and economic data** as new survey locations get added, there is a delay between when the explanatory vairiables are extracted. For now this gets updated weekly.

#### Comment utiliser ce reposioire :

Il faut cloner le repo, le JupyterLab ou les JupyterNotebooks est requis. Le notebook "getdataforrepo" prétraitera les données pour vous et joindra les numéros BFS. Tous les autres modules s'appuient sur les données fournies par "getdataforrepo".

Veillez à utiliser le fichier requirements.txt ou .yml pour définir votre environnement de travail.

! ! Assurez-vous de lire le cas d'utilisation pour chaque modèle ou cahier ! !


**Synchronisation des données géographiques et des données économiques** à mesure que de nouveaux lieux d'enquête sont ajoutés, il y a un délai entre le moment où les vairiables explicatifs sont extraits. Pour l'instant, cette information est mise à jour chaque semaine.

### Copyright

This repo is for public use: GNU General Public License v2.0. The current project was sponsored by the Swiss federal office for the environment.

#### Droit d'auteur

Ce repostiore est destinée à l'usage du public : Licence publique générale GNU v2.0. Le projet actuel a été mandaté par l'Office fédéral suisse de l'environnement.


### Contributing

If you want to author an article for peer review on the subject of municipal waste, the environment, urbanization or probability and statistics we would love to hear from you.

Have an analysis method to propose ? Clone the repo and send us a pull request.

#### Contribuer

Si vous souhaitez rédiger un article sur le thème des déchets municipaux, de l'environnement, de l'urbanisation ou des probabilités et des statistiques, nous aimerions beaucoup vous entendre.

Vous avez une méthode d'analyse à proposer ? Clonez le repo et envoyez-nous un pull-request.

Contact analyst@hammerdirt.ch
