import json
#import time
import re
import requests as req
from bs4 import BeautifulSoup as bs

class Course:
  def __init__(self, AwardLevel, ProgrammeCode, ProgrammeName, ModeOfStudy, DurationOfStudy, OfferingCampusOrVenue, StudyPlaces, AdmissionScore, ProfessionalRecognition, EntranceRequirements, Articulation, CareerProspects, Curriculum, TuitionFees, StudentSharing):
    self.AwardLevel = AwardLevel
    self.ProgrammeCode = ProgrammeCode
    self.ProgrammeName = ProgrammeName
    self.ModeOfStudy = ModeOfStudy
    self.DurationOfStudy = DurationOfStudy
    self.OfferingCampusOrVenue = OfferingCampusOrVenue
    self.StudyPlaces = StudyPlaces
    self.AdmissionScore = AdmissionScore
    self.ProfessionalRecognition = ProfessionalRecognition
    self.EntranceRequirements = EntranceRequirements
    self.Articulation = Articulation
    self.CareerProspects = CareerProspects
    self.Curriculum = Curriculum
    self.TuitionFees = TuitionFees
    self.StudentSharing = StudentSharing

def findCourse(url):
  foundCourse = []
  baseUrl = "https://www.vtc.edu.hk"
  resp = req.get(baseUrl + url)
  soup = bs(resp.text, "html.parser")
  courseItems = soup.find_all("div", class_="course-item")

  for item in courseItems:
    progCode = item.find("div", class_="course-no").text.strip() if item.find("div", class_="course-no") else "N/A"
    progName = item.find("div", class_="course-name").text.strip() if item.find("div", class_="course-name") else "N/A"
    if not (urlDiv := item.find("div", class_="course-url")) or not urlDiv.find("a"):
        continue

    detailUrl = baseUrl + urlDiv.find("a").get("href")
    detalResp = req.get(detailUrl)
    detailSoup = bs(detalResp.text, "html.parser")

    awardLv = detailSoup.find("span", class_="tag tag-secondary").text.strip() if detailSoup.find("span", class_="tag tag-secondary") else "N/A"

    if infoContentRight := detailSoup.find("div", class_="basic-info-content-right"):
        span = infoContentRight.find_all(True, class_="value")
        spanLength = len(span)
        modeStu = span[0].text.strip() if span else "N/A"
        durStu = span[1].text.strip() if span else "N/A"
        offerCamOrVen = "N/A"
        stuPlaces = "N/A"
        admSco = "N/A"
        if spanLength > 2:
            content = [c.strip() for c in span[2].contents if isinstance(c, str) and c.strip()]
            offerCamOrVen = " , ".join(content) if content else "N/A"
        if spanLength > 3:
            content = [c.strip() for c in span[3].contents if isinstance(c, str) and c.strip()]
            stuPlaces = " , ".join(content) if content else "N/A"
        if spanLength > 4:
            content = [c.strip() for c in span[4].contents if isinstance(c, str) and c.strip()]
            admSco = " , ".join(content) if content else "N/A"
    
    proRec = "N/A"
    if proRecDesc := detailSoup.find("div", class_="career-prospects-desc"):
        if richtext := proRecDesc.find("div", class_="richtext"):
            proRec = richtext.text.strip()

    entReq  = []
    if admConDetail := detailSoup.find("div", class_="admission-content-detail"):
        if subjectGroup := admConDetail.find("div", class_="subject-group"):
            subjectItem = subjectGroup.find_all("div", class_="subject-item")

            chiReq = subjectItem[0].find("span", class_="subject-score").text.strip() if subjectItem else "N/A"
            engReq = subjectItem[1].find("span", class_="subject-score").text.strip() if subjectItem else "N/A"
            otherReq1 = subjectItem[2].find("span", class_="subject-score").text.strip() if subjectItem else "N/A"
            otherReq2 = subjectItem[3].find("span", class_="subject-score").text.strip() if subjectItem else "N/A"
            otherReq3 = subjectItem[4].find("span", class_="subject-score").text.strip() if subjectItem else "N/A"

            HKDSE_req = {"Chinese Language" : chiReq,"English Language" : engReq, "Core/Elective Subject1" : otherReq1, "Core/Elective Subject2" : otherReq2, "Core/Elective Subject3" : otherReq3}
            entReq.append(f'HKDSE: {HKDSE_req}')

        richtext = admConDetail.find_all("div", class_="richtext")
        for rt in richtext:
            if liItems := [li.text.strip().replace("\"", "") for li in rt.find_all("li")]:
                entReq.extend(liItems)
        if "HKDSE" in entReq:
            entReq.remove("HKDSE")

    art, carPro = "N/A", "N/A"
    if furtherEduContentDetail := detailSoup.find("div", class_="further-education-content-detail"):
        groups = furtherEduContentDetail.find_all("div", class_="section-group")
        for g in groups:
            h3_tags = g.find_all("div", class_="h3")
            desc_tags = g.find_all("div", class_="desc")

            for h3, desc in zip(h3_tags, desc_tags):
                title = h3.text.strip()
                desc_text = " ".join([c.strip() for c in desc.stripped_strings if c.strip()])
                
                if "Articulation" in title or "銜接" in title or "升學" in title:
                    art = desc_text
                elif "Career Prospects" in title or "就業" in title or "前景" in title or "發展" in title:
                    carPro = desc_text

    curr = {}
    if courseContent := detailSoup.find("div", class_="course-content-main"):
        accItem = courseContent.find_all("div", class_="accordion-item")
        for acc in accItem:
            hdr = acc.find("button", class_="accordion-header")
            if hdr:
                semName = hdr.text.strip()
                richtext = acc.find("div", class_="richtext")
                if richtext:
                    subjects = [li.text.strip() for li in richtext.find_all("li")]
                    curr[semName] = " , ".join(subjects) if subjects else "N/A"

    tuFee = detailSoup.find("div", class_="fee-amount").text.strip()

    stuShare = []
    sharing_blocks = detailSoup.find_all("div", class_="sharing-content")

    seen_descriptions = set()

    for block in sharing_blocks:
        des_tag = block.find("div", class_="description")
        if des_tag:
            des = des_tag.text.strip()
            clean_des = des.replace('"', '').replace('\n', ' ').strip()
            
            if clean_des and clean_des not in seen_descriptions and clean_des != "N/A":
                seen_descriptions.add(clean_des)
                stuShare.append(clean_des)
                
        sharerDetail = block.find("div", class_="sharer") or block.find("div", class_="sharer desktop-sharer")
        if sharerDetail:
            name_tag = sharerDetail.find("div", class_="sharer-name")
            title_tag = sharerDetail.find("div", class_="sharer-title")
            if name_tag and title_tag:
                name = name_tag.text.strip()
                title = title_tag.text.strip()
                # 封裝為鍵值對
                sharer_info = {name: title}
                if sharer_info not in stuShare:
                    stuShare.append(sharer_info)

    newCourse = Course(awardLv, progCode, progName, modeStu, durStu, offerCamOrVen, stuPlaces, admSco, proRec, entReq, art, carPro, curr, tuFee, stuShare)
    foundCourse.append(newCourse)

  return foundCourse

# ==================== 新增：維基百科學校背景爬蟲 ====================
def findSchoolIntrodce(url):
    info = {}
    # 偽裝成瀏覽器，防止維基百科阻擋
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    resp = req.get(url, headers=headers)
    soup = bs(resp.text, "html.parser")
    
    # 1. 抓取學校標題
    title = soup.find("h1", id="firstHeading")
    info["SchoolName"] = title.text.strip() if title else "Unknown"
    
    # 2. 抓取右側資訊卡 (Infobox) 提取成立年份、校長等數據
    infobox = soup.find("table", class_="infobox")
    if infobox:
        for row in infobox.find_all("tr"):
            th = row.find("th")
            td = row.find("td")
            if th and td:
                key = th.text.strip()
                # 使用 Regex 移除 [1], [2] 等文獻標籤，並清理換行
                val = re.sub(r'\[\d+\]', '', td.text.strip())
                val = val.replace('\n', ' ')
                info[key] = val
                
    # 3. 抓取第一段核心簡介 (Introduction)
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        text = p.text.strip()
        # 找到第一段有實質內容的文字
        if text and len(text) > 30: 
            info["Introduction"] = re.sub(r'\[\d+\]', '', text)
            break
            
    return info

#allCoursesENG = []
#allCoursesCHI = []

#newCourses = findCourse("/admission/en/s6/?tab=higher-diploma")
#allCoursesENG.extend(newCourses)

#newCourses = findCourse("/admission/tc/s6/?tab=higher-diploma")
#allCoursesCHI.extend(newCourses)

ive_url = "https://zh.wikipedia.org/wiki/香港專業教育學院"
hkiit_url = "https://zh.wikipedia.org/wiki/香港資訊科技學院"

ive_info = findSchoolIntrodce(ive_url)
hkiit_info = findSchoolIntrodce(hkiit_url)



#jsonCompatibleData = [course.__dict__ for course in allCoursesENG]
#jsonCompatibleData2 = [course.__dict__ for course in allCoursesCHI]

"""
with open("./IVE_courses_ENG.json", "w", encoding="utf-8") as f:
    json.dump(jsonCompatibleData, f, ensure_ascii=False, indent=2)

with open("./IVE_courses_CHI.json", "w", encoding="utf-8") as f:
    json.dump(jsonCompatibleData2, f, ensure_ascii=False, indent=2)
"""

with open("./IVE_introduce.json", "w", encoding="utf-8") as f:
    json.dump(ive_info, f, ensure_ascii=False, indent=2)

with open("./HKIIT_introduce.json", "w", encoding="utf-8") as f:
    json.dump(hkiit_info, f, ensure_ascii=False, indent=2)