import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_tr_tags(url, page):
    res = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tr_tags = soup.find_all('tr')
        idx = 1
        # print(tr_tags[idx])
        while idx < len(tr_tags):
            currentCollege = {}
            collegeName = ""
            program = ""
            degree = ""
            decision = ""
            semester = ""
            collegeDiv = tr_tags[idx].find('div', class_='tw-font-medium tw-text-gray-900 tw-text-sm')
            # print(collegeDiv)
            if collegeDiv is None:
                idx += 1
                continue
            collegeName = collegeDiv.get_text(strip = True)
            programDiv = tr_tags[idx].find(lambda tag: tag.name == "div" and tag.get("class") == ["tw-text-gray-900"])
            spans = programDiv.find_all('span')
            program = spans[0].get_text(strip = True)
            degree = spans[1].get_text(strip = True)
            decision_classes = ["tw-inline-flex tw-items-center tw-rounded-md tw-bg-sky-50 tw-text-sky-700 tw-ring-sky-600/20 tw-px-2 tw-py-1 tw-text-sm tw-font-medium tw-ring-1 tw-ring-inset",
                                "tw-inline-flex tw-items-center tw-rounded-md tw-bg-green-50 tw-text-green-700 tw-ring-green-600/20 tw-px-2 tw-py-1 tw-text-sm tw-font-medium tw-ring-1 tw-ring-inset",
                                "tw-inline-flex tw-items-center tw-rounded-md tw-bg-red-50 tw-text-red-700 tw-ring-red-600/20 tw-px-2 tw-py-1 tw-text-sm tw-font-medium tw-ring-1 tw-ring-inset",
                                "tw-inline-flex tw-items-center tw-rounded-md tw-bg-purple-50 tw-text-purple-700 tw-ring-purple-600/20 tw-px-2 tw-py-1 tw-text-sm tw-font-medium tw-ring-1 tw-ring-inset"]
            decisionDivs = tr_tags[idx].find_all('div', class_=lambda x: x and any(cls in x for cls in decision_classes))
            semester_classes=["tw-inline-flex tw-items-center tw-rounded-md tw-bg-orange-400 tw-px-2 tw-py-1 tw-text-xs tw-font-medium tw-text-white tw-ring-1 tw-ring-inset tw-ring-orange-800/20",
                              "tw-inline-flex tw-items-center tw-rounded-md tw-px-2 tw-py-1 tw-text-xs tw-font-medium tw-ring-1 tw-ring-inset tw-ring-green-800/20 tw-bg-green-400 tw-text-white"]
            semRows = tr_tags[idx + 1].find_all('div', class_=lambda x: x and any(cls in x for cls in semester_classes))
            semester = semRows[0].get_text(strip = True).split()[0]
            currentCollege['collegeName'] = collegeName
            currentCollege['program'] = program
            currentCollege['degree'] = degree
            currentCollege['decision'] = decisionDivs[0].get_text(strip = True).split()[0]
            currentCollege['semester'] = semester
            origin = ""
            gpa = ""
            gre = ""
            gre_v = ""
            gre_aw = ""
            profileDivs = tr_tags[idx + 1].find_all('div', class_="tw-inline-flex tw-items-center tw-rounded-md tw-bg-stone-50 tw-px-2 tw-py-1 tw-text-xs tw-font-medium tw-text-stone-700 tw-ring-1 tw-ring-inset tw-ring-stone-600/20")
            for div in profileDivs:
                if "GPA" in div.get_text(strip = True):
                    # print(div.get_text(strip = True))
                    gpa = div.get_text(strip = True).split()[1]
                elif "GRE V" in div.get_text(strip = True):
                    gre_v = div.get_text(strip = True).split()[2]
                elif "GRE AW" in div.get_text(strip = True):
                    gre_aw = div.get_text(strip = True).split()[2]
                elif "GRE" in div.get_text(strip = True):
                    gre = div.get_text(strip = True).split()[1]
                else:
                    origin = div.get_text(strip = True)

            currentCollege['origin'] = origin
            currentCollege['gpa'] = gpa
            currentCollege['gre'] = gre
            currentCollege['gre_v'] = gre_v
            currentCollege['gre_aw'] = gre_aw


            res.append(currentCollege)
            
            idx += 2
        f = open("data/{}.json".format(page), "w")
        json.dump(res, f)
        f.close()


    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    print(res)
    print(len(res))


if __name__ == "__main__":
    os.mkdir("data")
    for page in range(1, 10):
        print("Scraping page: ", page)
        
        url = f"https://www.thegradcafe.com/survey/?q=&sort=newest&institution=&program=Computer+Science&degree=Masters&season=&decision=&decision_start=&decision_end=&added_start=&added_end=&page={page}"
        scrape_tr_tags(url, page)
        print()