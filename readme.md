# searchVIU Labs: Machine Learning experiments for SEO

## How to Use
- [ ] [Install Docker] (https://www.docker.com/)
- [ ] Download this repository by downloading the zip or running command:
```
git clone https://github.com/searchVIU/Labs.git
```
- [ ] go into Labs folder
- [ ] run
```
docker-compose up
```
- [ ] open your Browser and go to http://localhost:8899

After that you can choose the notebook an run an experiment

## Stay up to date
Get infos about new experiments or news about presentations of experiments by signing up to our news: http://labs.searchviu.com

## Experiments:
#### 1. Click-through rate prediction for a position with Google Search Console data
In this experiment we predict the CTR for a position of a particular Website with Google Search Console data.
Also we cover some machine learning basics in this Notebook.

You will need to get GSC Data from your website for this experiment. For this we have used https://searchanalyticsforsheets.com/.
You find an example file with 3 rows in data/example_ctr_prediction.csv

#### 2. Prediction of positions for optimized landingpages
In this experiment we try to predicting the position for the case that we've an optimized landingpage for a set of Keywords from SEMRUSH API.
To run this experiment you need a SEMRush Api Key.
[You will find an explanation of this experiment in our blog](https://www.searchviu.com/blog/article)