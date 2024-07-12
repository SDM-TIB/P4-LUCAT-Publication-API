

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
# P4-LUCAT-Publication-API

Retrieve list of publication based on the input variables

## License
This work is licensed under the MIT license.

## Authors
P4-LUCAT_APIs have been developed by members of the Scientific Data Management Group at TIB, as an ongoing research effort.
The development is co-ordinated and supervised by Maria-Esther Vidal.
This API has been developed by Ahmad Sakor.

## Input Example

POST:
https://labs.tib.eu/sdm/p4lucat_publication_api/get_publications?limit=10&page=0&sort=hindex&topic=lc
```
{
	"data":{
   "comorbidities":[
  	"C0242339",
  	"C0020538",
  	"C0149871"
   ],
   "biomarkers":[
  	"C0034802",
  	"C1332080",
  	"C0812281"
   ],
   "histology":[
  	"C0152013"
   ],
   "LCdrugs":[
  	"C0000979",
  	"C0028978"
   ],
   "oncologicalTreatments":[
  	"C0021083",
  	"C3665472",
  	"C3899317",
  	"C0596087",
  	"C0034619",
  	"C0543467"
   ]
},
	"filter":{
		"journals":[],
		"publication_types":[],
         "authors":[]
	}
}
```

## Output Example

```
{
    "resultsTotal": "36352",
    "publications": [
        {
            "title": "Low-molecular-weight heparin and survival in lung cancer.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/22682120",
            "authors": "http://research.tib.eu/p4-lucat/entity/Noble_Simon",
            "journal": "Thrombosis research",
            "year": 2012,
            "score": 1.4285714285714286,
            "sjr": 1.096,
            "type": "Journal Article",
            "hindex": 99,
            "citations": 0.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/de_Vries_Rory_D",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Hoogendijk_Arie_J",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Kreft_Iris_C",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Moscona_Anne",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Porotto_Matteo",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Salvatori_Daniela_C_F",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Schmitz_Katharina_S",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Tanis_Fric_J",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        },
        {
            "title": "Absence of COVID-19-associated changes in plasma coagulation proteins and pulmonary thrombosis in the ferret model.",
            "url": "https://www.ncbi.nlm.nih.gov/pubmed/34954402",
            "authors": "http://research.tib.eu/p4-lucat/entity/Winiarczyk_Roy_R_A",
            "journal": "Thrombosis research",
            "year": 2022,
            "score": 2.857142857142857,
            "sjr": 1.096,
            "type": "Journal Article, Comment",
            "hindex": 99,
            "citations": -1.0,
            "group": "comorbidities"
        }
    ],
    "filter": {
        "journals": [
            {
                "name": "Journal of hepato-biliary-pancreatic surgery",
                "results": "1"
            },
            {
                "name": "BMJ open gastroenterology",
                "results": "4"
            },
            {
                "name": "Electromagnetic biology and medicine",
                "results": "1"
                
                }
             ],   
           "publication_types": [
            {
                "name": "Historical_Article",
                "results": "13"
            },
            {
                "name": "Practice_Guideline",
                "results": "44"
            },
            {
                "name": "Introductory_Journal_Article",
                "results": "2"
                
               }
                ]

```

