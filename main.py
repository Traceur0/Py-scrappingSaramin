from types import SimpleNamespace
from get_last_page import check_last_p, requesting_data
from saves import save_to_file

last_page = check_last_p()

jobs_info = requesting_data(last_page)
save_to_file(jobs_info)


# /\/\/\ ORIGINAL VER. /\/\/\

# last_indeed_page = extract_indeed_pages()

# indeed_jons = extract_indeed_jobs(last_indeed_page)

# print(indeed_jobs)