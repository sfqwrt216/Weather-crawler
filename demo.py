#!/usr/bin/env python3
"""
Weather Crawler Demo - 天气爬虫演示版本
此版本使用模拟数据进行演示，不需要API密钥
"""

import json
import csv
import time
import random
from datetime import datetime
from typing import Dict, List


class WeatherCrawlerDemo:
    """天气数据爬虫演示类 - 使用模拟数据"""
    
    def __init__(self):
        """初始化演示版天气爬虫"""
        self.demo_cities = {
            "Beijing": {"country": "CN", "temp_range": (10, 25)},
            "Shanghai": {"country": "CN", "temp_range": (15, 28)},
            "Guangzhou": {"country": "CN", "temp_range": (20, 32)},
            "London": {"country": "UK", "temp_range": (5, 18)},
            "New York": {"country": "US", "temp_range": (8, 22)},
            "Tokyo": {"country": "JP", "temp_range": (12, 26)},
            "Paris": {"country": "FR", "temp_range": (7, 20)},
        }
        
        self.weather_conditions = [
            {"main": "Clear", "description": "晴朗"},
            {"main": "Clouds", "description": "多云"},
            {"main": "Rain", "description": "小雨"},
            {"main": "Snow", "description": "下雪"},
            {"main": "Mist", "description": "薄雾"},
        ]
    
    def generate_demo_data(self, city: str) -> Dict:
        """
        生成模拟天气数据
        
        Args:
            city: 城市名称
            
        Returns:
            模拟的天气数据字典
        """
        # 获取城市信息或使用默认值
        city_info = self.demo_cities.get(city, {
            "country": "XX", 
            "temp_range": (10, 25)
        })
        
        # 随机生成天气数据
        temp_min, temp_max = city_info["temp_range"]
        temperature = round(random.uniform(temp_min, temp_max), 1)
        feels_like = round(temperature + random.uniform(-2, 2), 1)
        humidity = random.randint(30, 90)
        pressure = random.randint(980, 1030)
        wind_speed = round(random.uniform(0, 10), 1)
        wind_direction = random.randint(0, 360)
        visibility = random.randint(5000, 15000)
        
        # 随机选择天气状况
        weather = random.choice(self.weather_conditions)
        
        # 模拟日出日落时间
        now = datetime.now()
        sunrise_hour = random.randint(5, 7)
        sunset_hour = random.randint(17, 19)
        
        return {
            "city": city,
            "country": city_info["country"],
            "timestamp": now.isoformat(),
            "temperature": temperature,
            "feels_like": feels_like,
            "humidity": humidity,
            "pressure": pressure,
            "weather_main": weather["main"],
            "weather_description": weather["description"],
            "wind_speed": wind_speed,
            "wind_direction": wind_direction,
            "visibility": visibility,
            "sunrise": now.replace(hour=sunrise_hour, minute=random.randint(0, 59)).isoformat(),
            "sunset": now.replace(hour=sunset_hour, minute=random.randint(0, 59)).isoformat()
        }
    
    def get_weather_data(self, city: str, country_code: str = "") -> Dict:
        """
        获取天气数据（演示版）
        
        Args:
            city: 城市名称
            country_code: 国家代码（在演示版中忽略）
            
        Returns:
            模拟的天气数据字典
        """
        print(f"[演示模式] 正在获取 {city} 的天气数据...")
        
        # 模拟网络延迟
        time.sleep(0.5)
        
        # 生成模拟数据
        weather_data = self.generate_demo_data(city)
        
        print(f"[演示模式] 成功获取 {city} 的天气数据")
        return weather_data
    
    def save_to_json(self, data: Dict, filename: str = None) -> str:
        """
        将天气数据保存为JSON文件
        
        Args:
            data: 天气数据字典
            filename: 输出文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            city_name = data.get("city", "unknown").replace(" ", "_")
            filename = f"weather_{city_name}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"天气数据已保存到: {filename}")
        return filename
    
    def save_to_csv(self, data_list: List[Dict], filename: str = None) -> str:
        """
        将天气数据保存为CSV文件
        
        Args:
            data_list: 天气数据字典列表
            filename: 输出文件名（可选）
            
        Returns:
            保存的文件路径
        """
        if not data_list:
            raise ValueError("数据列表不能为空")
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weather_data_demo_{timestamp}.csv"
        
        # 获取所有字段名
        fieldnames = set()
        for data in data_list:
            fieldnames.update(data.keys())
        fieldnames = sorted(fieldnames)
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_list)
        
        print(f"天气数据已保存到CSV文件: {filename}")
        return filename
    
    def crawl_multiple_cities(self, cities: List[str], delay: int = 1) -> List[Dict]:
        """
        爬取多个城市的天气数据（演示版）
        
        Args:
            cities: 城市名称列表
            delay: 请求间隔时间（秒）
            
        Returns:
            天气数据字典列表
        """
        weather_data_list = []
        
        for city in cities:
            weather_data = self.get_weather_data(city)
            weather_data_list.append(weather_data)
            
            # 添加延迟
            if delay > 0 and city != cities[-1]:  # 最后一个城市不需要延迟
                time.sleep(delay)
        
        return weather_data_list


def demo_single_city():
    """演示单个城市查询"""
    print("=== 天气爬虫演示 - 单个城市查询 ===")
    
    crawler = WeatherCrawlerDemo()
    
    # 查询北京天气
    weather_data = crawler.get_weather_data("Beijing")
    
    # 显示结果
    print(f"\n城市: {weather_data['city']}")
    print(f"国家: {weather_data['country']}")
    print(f"温度: {weather_data['temperature']}°C")
    print(f"体感温度: {weather_data['feels_like']}°C")
    print(f"天气: {weather_data['weather_description']}")
    print(f"湿度: {weather_data['humidity']}%")
    print(f"气压: {weather_data['pressure']} hPa")
    print(f"风速: {weather_data['wind_speed']} m/s")
    print()
    
    # 保存数据
    json_file = crawler.save_to_json(weather_data)
    csv_file = crawler.save_to_csv([weather_data])
    
    return weather_data


def demo_multiple_cities():
    """演示多个城市查询"""
    print("=== 天气爬虫演示 - 多个城市查询 ===")
    
    crawler = WeatherCrawlerDemo()
    cities = ["Beijing", "Shanghai", "Guangzhou", "London", "New York"]
    
    # 批量查询
    print(f"正在查询 {len(cities)} 个城市的天气数据...")
    weather_data_list = crawler.crawl_multiple_cities(cities, delay=0.3)
    
    # 显示结果摘要
    print(f"\n成功获取 {len(weather_data_list)} 个城市的天气数据:")
    for data in weather_data_list:
        print(f"- {data['city']}: {data['temperature']}°C, {data['weather_description']}")
    
    # 保存数据
    csv_file = crawler.save_to_csv(weather_data_list)
    
    return weather_data_list


def main():
    """主演示函数"""
    print("Weather Crawler 演示版本")
    print("=" * 60)
    print("注意: 这是演示版本，使用模拟数据，不需要API密钥")
    print("=" * 60)
    print()
    
    try:
        # 单城市演示
        demo_single_city()
        
        print("-" * 40)
        
        # 多城市演示
        demo_multiple_cities()
        
        print("\n" + "=" * 60)
        print("演示完成！")
        print("生成的文件可以查看具体的天气数据格式。")
        print("要使用真实数据，请使用 weather_crawler.py 并提供API密钥。")
        print("=" * 60)
        
    except Exception as e:
        print(f"演示过程中发生错误: {e}")


if __name__ == "__main__":
    main()