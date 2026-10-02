from flask import Flask, render_template, request, redirect, send_file
from scraper.bsj_scraper import Scrape_Skills
from scraper.wwr_scraper import Scrape_wwr
from my_file_utils import save_to_file
import os

app = Flask("JobScrapper")
db = {}

@app.route("/")
def home():
    return render_template("home.html", name="george")

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else: 
        scraper_bsj = Scrape_Skills(keyword)
        scraper_bsj.scrape_page()
        jobs_bsj = scraper_bsj.keyword_jobs()

        scraper_wwr = Scrape_wwr(keyword)
        scraper_wwr.scrape_page()
        jobs_wwr = scraper_wwr.keyword_jobs()

        jobs = jobs_bsj + jobs_wwr
        db[keyword] = jobs
    return render_template("search.html", keyword = keyword, jobs = jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in db:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, db[keyword])
    return send_file(os.path.join('dynamic_scraper/csv', f"{keyword}.csv"), as_attachment=True)

app.run("0.0.0.0")