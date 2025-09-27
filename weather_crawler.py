#!/usr/bin/env python3
"""
Weather Crawler - 天气数据爬虫
获取指定城市的天气信息并保存到文件
"""

import requests
import json
import csv
import time
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Optional


class WeatherCrawler:
    """天气数据爬虫类"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化天气爬虫
        
        Args:
            api_key: OpenWeatherMap API密钥
        """
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.session = requests.Session()
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
    def get_weather_data(self, city: str, country_code: str = "") -> Dict:
        """
        获取指定城市的天气数据
        
        Args:
            city: 城市名称
            country_code: 国家代码（可选）
            
        Returns:
            包含天气数据的字典
        """
        try:
            # 构建查询参数
            location = city
            if country_code:
                location = f"{city},{country_code}"
                
            params = {
                "q": location,
                "appid": self.api_key or "demo_key",
                "units": "metric",  # 使用摄氏度
                "lang": "zh_cn"     # 中文描述
            }
            
            self.logger.info(f"正在获取 {location} 的天气数据...")
            
            # 发送API请求
            response = self.session.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 处理和格式化数据
            weather_info = {
                "city": data.get("name"),
                "country": data.get("sys", {}).get("country"),
                "timestamp": datetime.now().isoformat(),
                "temperature": data.get("main", {}).get("temp"),
                "feels_like": data.get("main", {}).get("feels_like"),
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "weather_main": data.get("weather", [{}])[0].get("main"),
                "weather_description": data.get("weather", [{}])[0].get("description"),
                "wind_speed": data.get("wind", {}).get("speed"),
                "wind_direction": data.get("wind", {}).get("deg"),
                "visibility": data.get("visibility"),
                "sunrise": datetime.fromtimestamp(
                    data.get("sys", {}).get("sunrise", 0)
                ).isoformat() if data.get("sys", {}).get("sunrise") else None,
                "sunset": datetime.fromtimestamp(
                    data.get("sys", {}).get("sunset", 0)
                ).isoformat() if data.get("sys", {}).get("sunset") else None
            }
            
            self.logger.info(f"成功获取 {location} 的天气数据")
            return weather_info
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"网络请求错误: {e}")
            raise
        except KeyError as e:
            self.logger.error(f"数据解析错误: {e}")
            raise
        except Exception as e:
            self.logger.error(f"获取天气数据时发生错误: {e}")
            raise
    
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
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"天气数据已保存到: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"保存JSON文件时发生错误: {e}")
            raise
    
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
            filename = f"weather_data_{timestamp}.csv"
        
        try:
            # 获取所有字段名
            fieldnames = set()
            for data in data_list:
                fieldnames.update(data.keys())
            
            fieldnames = sorted(fieldnames)
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data_list)
            
            self.logger.info(f"天气数据已保存到CSV文件: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"保存CSV文件时发生错误: {e}")
            raise
    
    def crawl_multiple_cities(self, cities: List[str], delay: int = 1) -> List[Dict]:
        """
        爬取多个城市的天气数据
        
        Args:
            cities: 城市名称列表
            delay: 请求间隔时间（秒）
            
        Returns:
            天气数据字典列表
        """
        weather_data_list = []
        
        for city in cities:
            try:
                weather_data = self.get_weather_data(city)
                weather_data_list.append(weather_data)
                
                # 添加延迟避免API限制
                if delay > 0:
                    time.sleep(delay)
                    
            except Exception as e:
                self.logger.error(f"获取城市 {city} 的天气数据失败: {e}")
                continue
        
        return weather_data_list


def main():
    """主函数 - 命令行接口"""
    parser = argparse.ArgumentParser(
        description="天气数据爬虫 - 获取城市天气信息",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python weather_crawler.py --city "北京"
  python weather_crawler.py --city "Shanghai" --country "CN" --format json
  python weather_crawler.py --cities "北京,上海,广州" --format csv
  python weather_crawler.py --city "London" --api-key "your_api_key_here"
        """
    )
    
    parser.add_argument(
        "--city", 
        help="城市名称"
    )
    parser.add_argument(
        "--cities", 
        help="多个城市名称，用逗号分隔"
    )
    parser.add_argument(
        "--country", 
        default="", 
        help="国家代码 (如: CN, US, UK)"
    )
    parser.add_argument(
        "--format", 
        choices=["json", "csv"], 
        default="json",
        help="输出格式 (默认: json)"
    )
    parser.add_argument(
        "--output", 
        help="输出文件名"
    )
    parser.add_argument(
        "--api-key", 
        help="OpenWeatherMap API密钥"
    )
    parser.add_argument(
        "--delay", 
        type=int, 
        default=1,
        help="多城市查询时的延迟时间（秒，默认1秒）"
    )
    
    args = parser.parse_args()
    
    # 检查参数
    if not args.city and not args.cities:
        parser.error("必须指定 --city 或 --cities 参数")
    
    try:
        # 创建爬虫实例
        crawler = WeatherCrawler(api_key=args.api_key)
        
        if args.cities:
            # 多城市模式
            cities = [city.strip() for city in args.cities.split(",")]
            weather_data_list = crawler.crawl_multiple_cities(cities, args.delay)
            
            if not weather_data_list:
                print("未能获取任何天气数据")
                return
            
            # 保存数据
            if args.format == "csv":
                filename = crawler.save_to_csv(weather_data_list, args.output)
            else:
                # 对于多个城市的JSON格式，保存为数组
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = args.output or f"weather_multiple_cities_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(weather_data_list, f, ensure_ascii=False, indent=2)
                print(f"天气数据已保存到: {filename}")
        else:
            # 单城市模式
            weather_data = crawler.get_weather_data(args.city, args.country)
            
            # 显示天气信息
            print(f"\n=== {weather_data['city']} 天气信息 ===")
            print(f"时间: {weather_data['timestamp']}")
            print(f"温度: {weather_data['temperature']}°C")
            print(f"体感温度: {weather_data['feels_like']}°C")
            print(f"天气: {weather_data['weather_description']}")
            print(f"湿度: {weather_data['humidity']}%")
            print(f"气压: {weather_data['pressure']} hPa")
            if weather_data['wind_speed']:
                print(f"风速: {weather_data['wind_speed']} m/s")
            print()
            
            # 保存数据
            if args.format == "csv":
                filename = crawler.save_to_csv([weather_data], args.output)
            else:
                filename = crawler.save_to_json(weather_data, args.output)
                
    except Exception as e:
        logging.error(f"程序执行出错: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())