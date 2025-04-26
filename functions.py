import json
from bs4 import BeautifulSoup
import requests as rq
import time


def login(user_pass, session: rq.Session):
    for i in user_pass:
        if user_pass[i] == "":
            return False

    global t
    attempts = 0
    print("Logging in...")
    while attempts < 5:
        try:
            url = "https://sis.squ.edu.om/sis/webreg/3s/login.jsp"
            time.sleep(1)
            t = session.post(url, data=user_pass)
            break
        except Exception as e:
            print(f"ERROR: {e}")
            attempts += 1
    if "Authentication failed; invalid user name or password" in str(t.content):
        return False
    return True


def add_course(course, session: rq.Session):
    # to avoid error "enternal error 500".
    session.get('https://sis.squ.edu.om/sis/webreg/reg.jsp')

    if "Access to Online Registration is disabled" in session.get("https://sis.squ.edu.om/sis/webreg/addSect.jsp").text:
        print("Online Registration is disabled, please try when registration is open")
        return "disabled"
    regpage2 = session.get(
        f'https://sis.squ.edu.om/sis/webreg/addSect2.jsp?crsno={course[0]}&sectno={course[1]}')

    regcodepage = str(regpage2.content)
    regcodepage = regcodepage[regcodepage.find(
        "name=\"regcode\"", len(regcodepage) // 4 * 3) + 32:]
    regcode = regcodepage[:regcodepage.find("\"")]

    regi = ""
    if len(course) == 2:
        regi = session.get(
            f"https://sis.squ.edu.om/sis/webreg/saveSect.jsp?crsno={course[0]}&noOfSections=1&sectno1={course[1]}&regcode={regcode}")
    elif len(course) == 3:
        regi = session.get(
            f"https://sis.squ.edu.om/sis/webreg/saveSect.jsp?crsno={course[0]}&noOfSections=2&sectno1={course[1]}&sectno2={course[2]}&regcode={regcode}")
    if "Course/Section has been added successfully." in str(regi.content):
        return True
    return False


def extract_seating_data():
    global n
    attempts = 0
    while attempts < 5:
        try:
            url = "https://portal.squ.edu.om/web/guest/sectioncounts?p_p_id" \
                  "=sectioncount_WAR_prjSectionCount_INSTANCE_MBwsbhYD3YWj&p_p_lifecycle=2&p_p_state=normal&p_p_mode" \
                  "=view&p_p_resource_id=getAllCourseInfo&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1" \
                  "&p_p_col_count=1"
            n = rq.get(url)
            break
        except Exception as e:
            print(f"ERROR: {e}")
            attempts += 1

    result = json.loads(n.text)
    return result


def drop_course(course, session: rq.Session):
    reg_page = session.get("https://sis.squ.edu.om/sis/webreg/reg.jsp")
    
    doc = BeautifulSoup(reg_page.text, 'lxml')
        
    trs = doc.find_all("tr")
    code = ''
    for i in trs:
        x = i.find("b")
        if x is not None:
            if x.string == course:
                code = (i.find('input')['value'])
                break
    code = code.split("&")
    res = session.get(f"https://sis.squ.edu.om/sis/webreg/confirmDrop.jsp?{code[0]}&abrcrsno={course}&confirm=Confirm")
    if "Course/Section has been dropped successfully." in str(res.text):
        return True
    return False
    