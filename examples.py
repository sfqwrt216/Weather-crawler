#!/usr/bin/env python3
"""
Weather Crawler Example Usage - 天气爬虫使用示例
演示天气爬虫的各种使用方法
"""

from weather_crawler import WeatherCrawler
import json

def example_single_city():
    """示例: 单个城市天气查询"""
    print("=== 单个城市天气查询示例 ===")
    
    # 创建爬虫实例（使用演示模式，实际使用需要API key）
    crawler = WeatherCrawler()
    
    try:
        # 查询北京天气
        weather_data = crawler.get_weather_data("Beijing", "CN")
        
        # 显示结果
        print(f"城市: {weather_data['city']}")
        print(f"温度: {weather_data['temperature']}°C")
        print(f"天气: {weather_data['weather_description']}")
        print(f"湿度: {weather_data['humidity']}%")
        
        # 保存为JSON
        json_file = crawler.save_to_json(weather_data)
        print(f"数据已保存到: {json_file}")
        
    except Exception as e:
        print(f"查询失败: {e}")

def example_multiple_cities():
    """示例: 多个城市天气查询"""
    print("\n=== 多个城市天气查询示例 ===")
    
    crawler = WeatherCrawler()
    cities = ["Beijing", "Shanghai", "Guangzhou", "Shenzhen"]
    
    try:
        # 批量查询
        weather_data_list = crawler.crawl_multiple_cities(cities, delay=1)
        
        # 显示结果摘要
        print(f"成功获取 {len(weather_data_list)} 个城市的天气数据:")
        for data in weather_data_list:
            print(f"- {data['city']}: {data['temperature']}°C, {data['weather_description']}")
        
        # 保存为CSV
        csv_file = crawler.save_to_csv(weather_data_list)
        print(f"数据已保存到CSV文件: {csv_file}")
        
    except Exception as e:
        print(f"批量查询失败: {e}")

def example_with_api_key():
    """示例: 使用API key查询（实际应用）"""
    print("\n=== 使用API Key查询示例 ===")
    
    # 注意: 实际使用时请替换为真实的API key
    api_key = "your_real_api_key_here"  
    crawler = WeatherCrawler(api_key=api_key)
    
    print("请注意: 此示例需要真实的OpenWeatherMap API密钥")
    print("访问 https://openweathermap.org/api 获取免费API密钥")

def main():
    """运行所有示例"""
    print("Weather Crawler 使用示例")
    print("=" * 50)
    
    # 运行示例（注意：没有真实API key时会失败）
    try:
        example_single_city()
    except Exception as e:
        print(f"单城市示例执行失败: {e}")
        print("提示: 需要有效的OpenWeatherMap API密钥")
    
    try:
        example_multiple_cities()
    except Exception as e:
        print(f"多城市示例执行失败: {e}")
        print("提示: 需要有效的OpenWeatherMap API密钥")
    
    example_with_api_key()
    
    print("\n" + "=" * 50)
    print("获取OpenWeatherMap免费API密钥:")
    print("1. 访问 https://openweathermap.org/api")
    print("2. 注册账户")
    print("3. 获取API密钥")
    print("4. 将密钥添加到config.env文件或作为命令行参数")

if __name__ == "__main__":
    main()