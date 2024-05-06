import imaplib
import pandas as pd # used for data manipulation and analysis.
import datetime 
from selenium import webdriver # use webdriver
from selenium.webdriver.common.by import By # different methods of locating data
from selenium.webdriver.chrome.options import Options # options for selenium driver
from selenium.webdriver.common.keys import Keys # used for simulating keyboard actions
from functions import remove_dollar_sign, date # import functions 
import time # used for working with time-related operations in Python
from mysql_db import MysqlDB # connect database



def load_product(driver):
    product_count = 0
    while True:
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(5)  # 等待加載更多的產品，您可以根據需要調整等待時間
        result = driver.find_elements(By.XPATH, '//li[@class="column-grid-container__column"]')
        print('\nNumber of products: ', len(result))

        if len(result) == product_count:
            break
        product_count = len(result)


def get_product_info(driver):

    status_list =  []
    product_list = []
    past_prices = []
    price_list = []
    date_list = []
    plat_id = []
    platform = []
    product_url_list = []


    """"
    print out the webElement for result
    """
    # For checking webElement
    # for webElement in result:
    #     print("="*100)
    #     print(webElement.text)


    result = driver.find_elements(By.XPATH, '//li[@class="column-grid-container__column"]')
    for webElement in result:
        product_info_list = webElement.text.split('\n')
        # print("="*100)
        # print(product_info_list)
        product_count = len(result)

        # print('\nNumber of products: ', len(result))
        # Product Column & State Column
        current_time = date(date_list)
        plat_id.append("001")
        platform.append("sasa")

        if product_info_list[0].count("補貨通知") > 0 or product_info_list[0].count("已售完") > 0:
            product_list.append(product_info_list[1])
            status_list.append(product_info_list[0])
        else:
            product_list.append(product_info_list[0])
            status_list.append("現有現貨")
        # Past Price & Current Price
        if len(product_info_list) >= 3:
            if len(product_info_list) == 4 and (product_info_list[0].count("補貨通知") > 0 or product_info_list[0].count("已售完") > 0):
                past_prices.append(product_info_list[-2])
                price_list.append(product_info_list[-1])  # Use the last element as the price
            elif len(product_info_list) == 3 and product_info_list[0].count("補貨通知") > 0 or product_info_list[0].count("已售完") > 0:
                past_prices.append(None)
                price_list.append(product_info_list[-1])  # Use the first element as the price
            else:
                past_prices.append(product_info_list[1])  # Use the second element as the past price
                price_list.append(product_info_list[-1])  # Use the last element as the price
        else:
            past_prices.append(None)
            price_list.append(product_info_list[-1])

    link_path = driver.find_elements(By.XPATH, '//li[@class="column-grid-container__column"]//a[1]')
    for product_link in link_path:
        product_link_url = product_link.get_attribute("href")
        product_url_list.append(product_link_url)



    # for chenking the seam product link url
    seen = set()
    duplicates = []
    for element in product_url_list:
        if element in seen:
            duplicates.append(element)
        else:
            seen.add(element)

    print('Duplicates:', duplicates)



    # call fuction to remove dollar sign
    past_prices, price_list  = remove_dollar_sign(past_prices, price_list)

    return (current_time, plat_id, platform, status_list, product_list, 
                  past_prices, price_list, product_url_list)
    


def checking_list(current_time, plat_id, platform, status_list, product_list, 
                  past_prices, price_list, product_url_list):
# print('\nNumber of products: ', len(result))
# # print out of all this
    # time.sleep(2)
    print("\n", "="*100)
    print("time_list:", len(current_time))
    print("="*100)
    print("plat_id_list:", len(plat_id))
    print("="*100)
    print("platform_list:", len(platform))
    print("="*100)
    print("state_list:", len(status_list))
    print("="*100)
    print("product_list:", len(product_list))
    print("="*100)
    print("past_prices:", len(past_prices))
    print("="*100)
    print("price_list:",len(price_list))
    print("="*100)
    print("product_url_list:",len(product_url_list))
    print("="*100)


    # for i in current_time:
    #     print(type(i))
    #     # exit()
    #     break

def create_dataframe(current_time, plat_id, platform, status_list, product_list, 
                  past_prices, price_list, product_url_list):
    df = pd.DataFrame(
        {'Date' : current_time,
        'Plat_ID' : plat_id,
        'Platform' : platform,
        'Product_State' : status_list, 
        'Product_Title' : product_list, 
        'Original_Price' : past_prices,
        'Discount_Price' : price_list,
        'Product_Link' : product_url_list,
        }
    )

    print(df)
    return df


def export_to_csv(df):
    current_date = datetime.datetime.now().strftime("%d-%m-%Y")
    path= 'C:/JDE8/Github_Online_Retailer_Analysis/csv/'
    file_name = f"SASA({current_date}).csv"
    # # # Export into csv file /
    
    df.to_csv(path + file_name, encoding="utf-8-sig", errors="replace", index=False)



def main():
    driver = webdriver.Chrome()

    result_page_url = "https://www.sasa.com.hk/v2/official/SalePageCategory/5886?sortMode=Sales"
    driver.get(result_page_url)
    time.sleep(5)
    load_product(driver)
    current_time, plat_id, platform, status_list, product_list, past_prices, price_list, product_url_list = get_product_info(driver)
    checking_list(current_time, plat_id, platform, status_list, product_list, 
                    past_prices, price_list, product_url_list)
    df = create_dataframe(current_time, plat_id, platform, status_list, product_list, 
                    past_prices, price_list, product_url_list)
     
    # Storing scrapping data into Mysql Database
    mysql_db = MysqlDB()
    mysql_db.connect()
    mysql_db.create_table()
    for i in range(len(current_time)):
        # print(type(current_time[i]))
        # print(type(plat_id[i]))
        # print(type(platform[i]))
        # print(type(status_list[i]))
        # print(type(product_list[i]))
        # print(type(past_prices[i]))
        # print(type(price_list[i]))
        # print(type(product_url_list[i]))
        # print(current_time[i], plat_id[i], platform[i], status_list[i], product_list[i], past_prices[i], price_list[i], product_url_list[i])
        mysql_db.save_mysql(current_time[i], plat_id[i], platform[i], status_list[i], product_list[i], past_prices[i], price_list[i], product_url_list[i])


    export_to_csv(df)

    driver.quit()
    # time.sleep(30000)

if __name__ == "__main__":
    main()  
