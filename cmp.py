from itertools import combinations
from selenium import webdriver
import pandas as pd

df = pd.DataFrame(columns=["MF_1",
                           "MF_2",
                           "Base Comparison Link",
                           "Detailed Comparison Link"])

with open('mf_cmp.txt', 'r') as fp:
    lines = fp.readlines()
    fp.close()
lines = [x.replace('\n', '') for x in lines]

combos = list(combinations(lines, 2))

url = "https://www.advisorkhoj.com/mutual-funds-research/mutual-fund-portfolio-overlap"
xp1 = "/html/body/div[1]/section[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/select/option[1]"
xp2 = "/html/body/div[1]/section[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/input"
xp3 = "/html/body/div[1]/section[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/input"
xp4 = "/html/body/div[1]/section[2]/div/div/div[2]/div[2]/div[2]/div[3]/div/div/a"
xp5 = "/html/body/div[1]/section[2]/div/div/div[2]/div[4]/div[3]/div/a"

driver = webdriver.Chrome()
try:
    for _ in combos:
        driver.get(url)
        driver.find_element_by_xpath(xp1).click()
        mf1 = driver.find_element_by_xpath(xp2)
        mf1.send_keys(_[0])
        mf2 = driver.find_element_by_xpath(xp3)
        mf2.send_keys(_[1])
        sub = driver.find_element_by_xpath(xp4).click()
        comp_base = driver.current_url
        tab = driver.find_element_by_xpath(xp5).click()
        comp_final = driver.current_url
        df = df.append(
            {
                "MF_1": _[0],
                "MF_2": _[1],
                "Base Comparison Link": comp_base,
                "Detailed Comparison Link": comp_final
            },
            ignore_index=True
        )

except Exception as e:
    print(e)
    driver.close()


print(df)
df.to_excel('data.xlsx')
driver.close()
