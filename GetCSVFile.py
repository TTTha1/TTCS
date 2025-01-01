import requests
import pandas as pd 
import time
from datetime import datetime

def get_weather_data(cities, api_key):
    """
    Lấy dữ liệu thời tiết cho danh sách các thành phố và lưu vào CSV.
    
    Args:
        cities (list): Danh sách tên các thành phố
        api_key (str): API key của OpenWeatherMap
    """
    
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    weather_data = []
    
    for city in cities:
        try:
            # Tạo URL với city name và api key
            url = BASE_URL + f"q={city}&appid={api_key}"
            
            # Gọi API và lấy response
            response = requests.get(url).json()
            
            # Kiểm tra response thành công
            if response["cod"] == 200:
                weather = {
                    'city': city,
                    'country': response['sys']['country'],
                    'temperature': round(response['main']['temp'] - 273.15, 2), # Chuyển từ °K sang °C
                    'humidity': response['main']['humidity'],
                    'pressure': response['main']['pressure'],
                    'wind_speed': round(response['wind']['speed'] * 3.6, 1), # Chuyển từ m/s sang km/h
                    'description': response['weather'][0]['description'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                weather_data.append(weather)
                print(f"Đã lấy dữ liệu thành công cho {city}")
            else:
                print(f"Không thể lấy dữ liệu cho {city}: {response['message']}")
                
            # Delay để tránh hit rate limit
            time.sleep(1)
            
        except Exception as e:
            print(f"Lỗi khi lấy dữ liệu cho {city}: {str(e)}")
            continue
    
    # Chuyển đổi sang DataFrame và lưu vào CSV
    if weather_data:
        df = pd.DataFrame(weather_data)
        filename = f"weather_data_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nĐã lưu dữ liệu vào file {filename}")
        return df
    else:
        print("Không có dữ liệu để lưu")
        return None

# Sử dụng hàm
if __name__ == "__main__":
    # API key của bạn
    API_KEY = "5fa789c022def2ca3417c45d533465e5"
    
    # Danh sách các thành phố muốn lấy dữ liệu
    cities = [
    "Hanoi", "Ho Chi Minh City", "Da Nang", "Hue", "Can Tho", "Nha Trang", "Da Lat", "Vung Tau", "Quy Nhon",
    "Phan Rang-Thap Cham", "Ca Mau", "Tuy Hoa", "New York", "London", "Beijing", "Tokyo", "Seoul", "Oxford",
    "Cambridge", "Las Vegas", "Hawaii", "Phan Thiet", "Paris", "Berlin", "Madrid", "Rome", "Vienna", "Amsterdam",
    "Brussels", "Lisbon", "Stockholm", "Oslo", "Copenhagen", "Helsinki", "Dublin", "Warsaw", "Prague", "Budapest",
    "Athens", "Zurich", "Istanbul", "Moscow", "Saint Petersburg", "Kiev", "Minsk", "Bucharest", "Sofia", "Belgrade",
    "Zagreb", "Sarajevo", "Ljubljana", "Bratislava", "Tallinn", "Riga", "Vilnius", "Skopje", "Podgorica", "Tirana",
    "Valletta", "Reykjavik", "Luxembourg", "Monaco", "San Marino", "Andorra la Vella", "Vaduz", "Manama", "Doha",
    "Abu Dhabi", "Muscat", "Kuwait City", "Riyadh", "Baghdad", "Jakarta", "Singapore", "Bangkok", "Kuala Lumpur", "Manila", "Sydney", "Melbourne", "Perth", "Brisbane", "Cape Town", "Johannesburg", "Nairobi", "Lagos", "Casablanca", "Cairo", "Algiers", "Tunis", "Accra", "Mexico City", "Toronto", "Montreal", "Vancouver", "Buenos Aires", "Santiago", "Lima", "Bogotá", "Caracas", "Brasilia", "Rio de Janeiro", "Sao Paulo"]
    
    # Lấy và lưu dữ liệu
    df = get_weather_data(cities, API_KEY)
    
    if df is not None:
        print("\nDữ liệu đã lấy được:")
        print(df)