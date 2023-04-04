from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import string
import numpy as np

# Create the object 'driver' to control the Chrome
dx = []
driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# input url need to craw data
url = "https://diemthi.vnexpress.net/diem-thi-nam-2018?fbclid=IwAR3XoIBjtG9dPF-tgViTp47seURfwRjRQSOugsiHqz68yRoDZCIifTDRdfE#area=2&college=05&q="
driver.get(url)

# Craw data and save in csv file
for i in range(5000001, 5005500):
    try:
        x = f"{i:08d}"
        run = driver.find_element(By.ID, 'keyword')
        run.clear()
        run = driver.find_element(By.ID, 'keyword')
        run.send_keys(x)
        search = driver.find_element(By.XPATH, '//*[@id="seach_diemthi"]/div[3]/input')
        search.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="result"]/div[2]/div/div/div[1]/div/table')))
        sleep(1)

        page_source = BeautifulSoup(driver.page_source, 'html.parser')
        info_div = page_source.find('tbody')
        info_tr = info_div.find_all('td', class_= 'width_sbd')

        sbd = info_tr[3].get_text().strip()
        if not sbd:
            sbd = np.nan

        toan = info_tr[4].get_text().strip()
        if not toan:
            toan = np.nan

        ngu_van = info_tr[5].get_text().strip()
        if not ngu_van:
            ngu_van = np.nan

        ngoai_ngu = info_tr[6].get_text().strip()
        if not ngoai_ngu:
            ngoai_ngu = np.nan

        vat_li = info_tr[7].get_text().strip()
        if not vat_li:
            vat_li = np.nan

        hoa_hoc = info_tr[8].get_text().strip()
        if not hoa_hoc:
            hoa_hoc = np.nan

        sinh_hoc = info_tr[9].get_text().strip()
        if not sinh_hoc:
            sinh_hoc = np.nan

        lich_su = info_tr[11].get_text().strip()
        if not lich_su:
            lich_su = np.nan

        dia_li = info_tr[12].get_text().strip()
        if not dia_li:
            dia_li = np.nan

        gdcd = info_tr[13].get_text().strip()
        if not gdcd:
            gdcd = np.nan

        # sleep(2)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "keyword")))

        dx.append({
            "Số báo danh": sbd,
            "Toán": toan,
            "Ngữ văn": ngu_van,
            "Ngoại Ngữ": ngoai_ngu,
            "Vật lý": vat_li,
            "Hóa học": hoa_hoc,
            "Sinh học": sinh_hoc,
            "Lịch sử": lich_su,
            "Địa lý": dia_li,
            "GDCD": gdcd
        })

        df = pd.DataFrame(dx)
        df.to_csv('diem1.csv', index=False)
    except:
        continue