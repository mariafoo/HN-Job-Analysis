from pyquery import PyQuery as pq
import re
import csv
import sys

csv_file = open(sys.argv[1],'w')
job_links_writer = csv.writer(csv_file, delimiter=',')

job_links_writer.writerow(["Year", "Month", "Job Link"])
base_url = "https://news.ycombinator.com/"
next_link = "https://news.ycombinator.com/submitted?id=whoishiring"

# while there are more links, run this loop 
# when there is no more links, stop this loop 
while (len(next_link)):

    current_page = pq(url=next_link)

    job_posting_links = current_page(".storylink")

    for link in job_posting_links:

        title = link.getparent().text_content() 
        if "ASK HN: WHO IS HIRING?" not in title.upper(): 
            continue
        
        date_match = re.search(r'\(([a-zA-Z]+)\s+(\d{4})\)', title)
        month = date_match.group(1)
        year = date_match.group(2)
        
        job_link = base_url + link.attrib["href"]

        job_links_writer.writerow([year, month, job_link])

        print(year + ' ' + month + ' ' + job_link)


    more_links = current_page(".morelink")
    if (len(more_links)):
        next_link = base_url + more_links[0].attrib["href"]
    else:
        next_link = ""

csv_file.close()

print("All done!")

# 07/08/2016 5:00pm-7:00pm 
# Next step is to obtain the first comment of each job post. This can be done by extracting the width when it equals to 0. 
# Specifically the td node with the class ind, and the child image which has a width attribute. This attribute is 0 when it is a top level post. 
