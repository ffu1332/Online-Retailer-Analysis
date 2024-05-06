import datetime



def date(date_list):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d")
    # date_time = datetime.strptime(date_time, "%Y-%m-%d")
    date_list.append(date_time)
    return date_list


def remove_dollar_sign(past_prices, price_list):
    # for transform_price in price_list:
    for i in range(len(past_prices)):
        if past_prices[i] == None:
            pass
        else:
            past_prices[i] = float(past_prices[i].replace(',', '').replace('HK$', ''))
    for i in range(len(price_list)):
        if price_list[i] == None:
            pass
        else:
            price_list[i] = float(price_list[i].replace('HK$', '').replace(',', ''))

    return past_prices, price_list  # 返回處理後的 past_prices 和 price_list


def remove_dollar_sign_hktv(price_list):
    for i in range(len(price_list)):
        price_list[i] = float(price_list[i].replace(',', '').replace('$', ''))

    return price_list


# def remove_dollar_sign(past_prices, price_list):
#     for i in range(len(past_prices)):
#         past_price = past_prices[i]
#         price = price_list[i]

#         remove_dollar = past_price.replace('HK$', '').replace(',', '')
#         past_prices[i] = remove_dollar

#         remove_dollar = price.replace('HK$', '').replace(',', '')
#         price_list[i] = remove_dollar

#     return past_prices, price_list