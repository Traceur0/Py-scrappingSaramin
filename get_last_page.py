import requests
from bs4 import BeautifulSoup


URL_p_null = """https://www.saramin.co.kr/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n
            &searchType=search&searchword=python&recruitSort=relation&recruitPageCount=50&mainSearch=y
            &company_cd=0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C9%2C10"""

def check_last_p(): # 11, 21, 31, 41, 51
    p_num = 11
    err = False
    while err == False: 
        try:
            p_check = requests.get(f"{URL_p_null}&recruitPage={p_num}")
            soup = BeautifulSoup(p_check.text,"html.parser")
            err_no_result = soup.find("span", {"class": "foc"}).string
            err_no_result == "'python'"
        except: #에러가 발생하는 경우 - x1번째 페이지가 존재
            print("Extracting...", p_num, "exists")
            err = False
            p_num += 10
        else:
            print("Error!", p_num, "doesn't exist.")
            err = True
    # 1 ~10, 11 ~21, ...51 ~55
    result = requests.get(f"{URL_p_null}&recruitPage={p_num - 10}")
    soup = BeautifulSoup(result.text,"html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    span_list = pagination.select("span")
    p_num_listize = list(span_list) # invert ResultSet to list
    p_num_list = [] 
    for num in p_num_listize:
        stringizing = num.string # stringizing one by one
        p_num_list.append(stringizing) # adding numbers to list
    last_p = p_num_list[-1] # naviable string, transform required.
    print("Extraction complete. last number :", last_p)
    return int(last_p)


def extract_jobs(html):
    title = html.select_one('div.area_job > h2 > a > span').text 
    location = html.select_one('div.job_condition > span').text
    company = html.select_one('strong.corp_name > a > span').text
    href = html.find("a")["href"]
    return {
        'title' : title,
        'location' : location,
        'company' : company,
        'link' : f"https://www.saramin.co.kr{href}"
    }

def requesting_data(last_page):
    jobs = []
    for page in range(last_page): # 21.12.31 현재기준 54회 반복
        print(f"Scrapping page {page+1}")
        request = requests.get(f"{URL_p_null}&recruitPage={page}")
        page = BeautifulSoup(request.text,"html.parser")
        item_recruit = page.find_all("div", {"class": "item_recruit"})
        for request in item_recruit: # request -> one_page
            job = extract_jobs(request)
            jobs.append(job)
            print(job)
    return jobs