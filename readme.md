# searchVIU Labs: Machine Learning Experiments for SEO

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
- [ ] wait until output says "The Jupyter Notebook is running at:" (first run could take some time until additional dependencies are installed)
- [ ] open your Browser and go to http://localhost:8888/tree/work

After that you can choose the notebook and run an experiment

## Stay up to date
Get infos about new experiments or news about presentations of experiments by signing up to our news: http://labs.searchviu.com

## Experiments
#### 1. Click-through rate prediction for a position with Google Search Console data
In this experiment we predict the CTR for a position of a particular website with Google Search Console data.
Also, we cover some machine learning basics in this notebook.

You will need to get GSC data from your website for this experiment. For this, we use https://searchanalyticsforsheets.com/.
You will find an example file with 3 rows in data/example_ctr_prediction.csv

#### 2. Prediction of positions for optimized landing pages
In this experiment we try to predict the position for the case that we have an optimized landing page for a set of Keywords from SEMrush API.
To run this experiment you need a SEMrush API Key.
[You will find an explanation of this experiment in our blog](https://www.searchviu.com/blog/article)