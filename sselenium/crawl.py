<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Similar to soup package, we have define crawl function to
do them automatically using sselenium

Created by Ludi Feng
Date: 2022/05/12
"""
# from cgitb import small
# from operator import index
# from matplotlib.pyplot import title
from selenium import webdriver
import pandas as pd

from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome()

def crawl_subjects_ulr(driver):
    ssubject = {}
    sssubject = {}
    print("*" * 50)
    print("Start crawling subjects_ulr")
    try:
        driver.get("https://arxiv.org/")
    except Exception as e:
        print(e)
        return
    content = driver.find_element(By.ID, "content")
    uls = content.find_elements(By.TAG_NAME, "ul")
    h2s = content.find_elements(By.TAG_NAME, "h2")
    for i in range(1, len(uls) - 1):
        # subject
        print("subject:", h2s[i - 1].text)
        lis = uls[i].find_elements(By.TAG_NAME, "li")
        for li in lis:
            a = li.find_elements(By.TAG_NAME, "a")[0]
            ssubject_url = li.find_elements(By.TAG_NAME, "a")[2].get_attribute("href")
            # ssubject
            print("     ssubject:", a.text, ssubject_url)
            aria = a.get_attribute("aria-labelledby")
            aa = li.find_elements(By.CSS_SELECTOR, "a[aria-labelledby^='" + aria + "']")
            ssubject[a.text] = ssubject_url
            for j in range(1, len(aa)):
                sssubject_url = aa[j].get_attribute("href")
                # sssubject
                print("          sssubject:", aa[j].text, sssubject_url)
                sssubject[aa[j].text] = sssubject_url
    return ssubject, sssubject


def crawl_all(limit=50,
              page_limit = False,
              subject =['Computer Science', 'Physics', 'Mathematics'],
              ssubject = ['Computing Research Repository', 'Physics', 'Mathematics'],
              sssubject = ['Computer Vision and Pattern Recognition', 'Machine Learning', 'Applied Physics',
             'functional analysis']):
    df = pd.DataFrame({'title': [], 'authors': [], 'abstract': [],
                       'comment': []})
    #driver = webdriver.Chrome()
    subjects = subject
    ssubjects = ssubject
    sssubjects = sssubject
    ssubject_url, sssubject_url = crawl_subjects_ulr(driver)
    print("************      crawl papers      ************")

    for sssubject in sssubjects:
        try:
            print("crawl sssubject:", sssubject)

            df = request_url(df,driver, sssubject_url[sssubject], limit,subject,ssubject,sssubject, page_limit)
            if page_limit and len(df) == 100:
                print('Upper limit 100 achieved! Stop!')
                break
        except:
            # crawl the whole ssubject
            pass
            # df = request_url(df,driver, ssubject_url[ssubject], limit,subject,ssubject,"NONE")

    # write_to_csv
    try:
        df.to_csv('./sselenium/data/allinfo.csv', index = False, sep = '#')
    except:
        df.to_csv('./data/allinfo.csv', index=False, sep='#')
    driver.close()

def request_url(df,driver, url, limit,subject,ssubject,sssubject, page_limit):
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return
    dlpage = driver.find_element(By.ID, "dlpage")
    aa = dlpage.find_elements(By.TAG_NAME, "small")[1].find_elements(By.TAG_NAME, "a")
    a = aa[len(aa) - 1]
    # click to show all
    a.click()
    dds = driver.find_elements(By.TAG_NAME, "dd")
    dts = driver.find_elements(By.TAG_NAME, "dt")
    for i in range(0, len(dds)):
        dd = dds[i]
        meta = dd.find_element(By.CLASS_NAME, "meta")
        # title
        title = meta.find_element(
            By.CLASS_NAME, "list-title").text.replace("\n", " ")
        # authors
        author_arr = []
        authors = meta.find_element(By.CLASS_NAME, "list-authors").find_elements(By.TAG_NAME, "a")
        for author in authors:
            author_arr.append(author.text)
        comments = ""
        try:
            # comments
            comments = meta.find_element(By.CLASS_NAME, "list-comments").text[10:]
        except Exception as e:
            print("no comments")
        # abstract
        dts[i].find_elements(By.TAG_NAME, "a")[1].click()
        abstract = driver.find_element(By.CLASS_NAME, "abstract ").text.replace("\n", " ")
        print("--------------------------------------------------------")
        print(i, "title:", title)
        print("   author:", ",".join(author_arr))
        print("   comments:", comments)
        print("   abstract:", abstract)
        df = df.append({"title": title, "authors": ",".join(author_arr), "comment": comments, "abstract": abstract,"sssubject":sssubject},ignore_index=True)
        if page_limit and len(df) == 100:
            print('Upper limit 100 achieved! Stop!')
            return df
        driver.back()
        limit -= 1
        if limit <= 0:
            break
    return df
=======
# -*- coding: utf-8 -*-
"""
Similar to soup package, we have define crawl function to
do them automatically using sselenium

Created by Kunhong Yu
Date: 2022/04/25
"""
from cgitb import small
from operator import index
from matplotlib.pyplot import title
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
def crawl_subjects_ulr(driver):
    ssubject = {}
    sssubject = {}
    print("************begin to crawl_subjects_ulr****************")
    try:
        driver.get("https://arxiv.org/")
    except Exception as e:
        print(e)
        return
    content = driver.find_element(By.ID, "content")
    uls = content.find_elements(By.TAG_NAME, "ul")
    h2s = content.find_elements(By.TAG_NAME, "h2")
    for i in range(1, len(uls) - 1):
        # subject
        print("subject:", h2s[i - 1].text)
        lis = uls[i].find_elements(By.TAG_NAME, "li")
        for li in lis:
            a = li.find_elements(By.TAG_NAME, "a")[0]
            ssubject_url = li.find_elements(By.TAG_NAME, "a")[2].get_attribute("href")
            # ssubject
            print("     ssubject:", a.text, ssubject_url)
            aria = a.get_attribute("aria-labelledby")
            aa = li.find_elements(By.CSS_SELECTOR, "a[aria-labelledby^='" + aria + "']")
            ssubject[a.text] = ssubject_url
            for j in range(1, len(aa)):
                sssubject_url = aa[j].get_attribute("href")
                # sssubject
                print("          sssubject:", aa[j].text, sssubject_url)
                sssubject[aa[j].text] = sssubject_url
    print("************  crawl_subjects_ulr end   ************")
    return ssubject, sssubject


def crawl_all(limit=50,
              subjects=[
                  {"subject": "Physics", "children": [
                      {"ssubject": "Astrophysics", "children": [
                          {"sssubject": "Astrophysics of Galaxies"}]}
                  ]}
              ]):
    papers = []
    #driver = webdriver.Chrome()
    ssubject_url, sssubject_url = crawl_subjects_ulr(driver)
    print("************      crawl papers      ************")
    for subject in subjects:
        print("crawl subject:", subject["subject"])
        for ssubject in subject["children"]:
            print("     crawl ssubject:", ssubject["ssubject"])
            if "children" in ssubject:
                # contain sssubject
                for sssubject in ssubject["children"]:
                    print("          crawl sssubject:", sssubject["sssubject"])
                    paper = request_url(driver, sssubject_url[sssubject["sssubject"]], limit)
                    papers.extend(paper)
                    return
            else:
                # crawl the whole ssubject
                paper = request_url(driver, ssubject_url[ssubject["ssubject"]], limit)
                papers.extend(paper)
    return papers


def request_url(driver, url, limit):
    try:
        driver.get(url)
    except Exception as e:
        print(e)
        return
    paper = []
    dlpage = driver.find_element(By.ID, "dlpage")
    aa = dlpage.find_elements(By.TAG_NAME, "small")[
        1].find_elements(By.TAG_NAME, "a")
    a = aa[len(aa) - 1]
    # click to show all
    a.click()
    dds = driver.find_elements(By.TAG_NAME, "dd")
    dts = driver.find_elements(By.TAG_NAME, "dt")
    for i in range(0, len(dds)):
        dd = dds[i]
        meta = dd.find_element(By.CLASS_NAME, "meta")
        # title
        title = meta.find_element(
            By.CLASS_NAME, "list-title").text.replace("\n", " ")
        # authors
        author_arr = []
        authors = meta.find_element(By.CLASS_NAME, "list-authors").find_elements(By.TAG_NAME, "a")
        for author in authors:
            author_arr.append(author.text)
        # comments
        comments = meta.find_element(By.CLASS_NAME, "list-comments").text[10:]
        # abstract
        dts[i].find_elements(By.TAG_NAME, "a")[1].click()
        abstract = driver.find_element(By.CLASS_NAME, "abstract ").text.replace("\n", " ")
        print("--------------------------------------------------------")
        print(i, "title:", title)
        print("   author:", ",".join(author_arr))
        print("   comments:", comments)
        print("   abstract:", abstract)
        paper.append({"title": title, "authors": ",".join(author_arr), "comments": comments, "abstract": abstract})
        driver.back()
        limit -= 1
        if limit <= 0:
            break
    return paper

# Finally, we combine them together
def crawl_all(limit = 50,
              scrape_each_author = True,
              subject = ['Computer Science', 'Physics', 'Mathematics'],
              ssubject = ['Computing Research Repository', 'Physics', 'Mathematics'],
              sssubject = ['Computer Vision and Pattern Recognition', 'Machine Learning',
                          'Applied Physics', 'functional analysis']):
    """This function is used to combine all together
    Unlike Beautiful Soup, we can not print information SEQUENTIALLY,
    since scrapy runs with multithreads, so we tend to print each item
    after we scrape everything!
    Args :
        --limit: upper limit of scrapy, default is 50
        --subject: main subject
        --ssubject: subsubject
        --sssubject: subsubsubject
    return :
        --author_links
    """
    pass # TODO



# Unit test
if __name__ == '__main__':
    crawl_all(limit = 10,
              scrape_each_author = True)
>>>>>>> e7b8b23db5988ddd218b6275de838a3c7e89c2f8
