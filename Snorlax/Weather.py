import requests

def get_weather(location):
    # API URL
    url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-077'
    params = {
        'Authorization': 'CWA-1DE85918-40F9-4484-ACB1-C5BF36B7CF31',
        'limit': 1,  # 限制回應數據只有最近的一筆
        'format': 'JSON',
        'locationName': location  # 使用參數化的地區名
    }

    # 發送GET請求
    response = requests.get(url, params=params)

    # 檢查回應狀態碼
    if response.status_code == 200:
        data = response.json()
        # 解析JSON以提取溫度數據
        try:
            temperature_info = data['records']['locations'][0]['location'][0]['weatherElement'][3]['time'][0]['elementValue'][0]['value']
            #print(f"現在的溫度：{temperature_info}°C")
        except (IndexError, KeyError):
            print("溫度數據無法提取，請檢查JSON結構是否有改變。")
    else:
        print("Error:", response.status_code)

# 調用函數，並傳入地區名稱
get_weather('永康區')
