# Weather Crawler - 天气数据爬虫

这是一个功能完整的天气数据爬虫，可以获取全球各个城市的实时天气信息并保存为多种格式。

## 功能特性

- 🌍 支持全球城市天气查询
- 📊 支持JSON和CSV格式输出
- 🏙️ 支持单个或多个城市批量查询
- 🔧 灵活的命令行接口
- 📝 详细的日志记录
- 🌡️ 完整的天气数据（温度、湿度、气压、风速等）
- 🕒 自动添加时间戳
- ⚡ 内置请求限制和错误处理

## 安装依赖

```bash
pip install -r requirements.txt
```

## API密钥设置

本爬虫使用OpenWeatherMap API，需要获取免费API密钥：

1. 访问 [OpenWeatherMap API](https://openweathermap.org/api)
2. 注册账户并获取API密钥
3. 将API密钥添加到 `config.env` 文件或通过命令行参数传入

## 使用方法

### 命令行使用

#### 查询单个城市
```bash
# 基本查询
python weather_crawler.py --city "北京"

# 指定国家代码
python weather_crawler.py --city "Beijing" --country "CN"

# 使用API密钥
python weather_crawler.py --city "London" --api-key "your_api_key_here"

# 保存为CSV格式
python weather_crawler.py --city "Shanghai" --format csv
```

#### 查询多个城市
```bash
# 批量查询多个城市
python weather_crawler.py --cities "北京,上海,广州,深圳"

# 保存为CSV格式
python weather_crawler.py --cities "Beijing,Shanghai,Guangzhou" --format csv

# 自定义输出文件名
python weather_crawler.py --cities "北京,上海" --output "china_weather.json"
```

### Python脚本使用

```python
from weather_crawler import WeatherCrawler

# 创建爬虫实例
crawler = WeatherCrawler(api_key="your_api_key")

# 查询单个城市
weather_data = crawler.get_weather_data("北京", "CN")
print(f"温度: {weather_data['temperature']}°C")

# 批量查询
cities = ["北京", "上海", "广州"]
weather_list = crawler.crawl_multiple_cities(cities)

# 保存数据
crawler.save_to_json(weather_data, "beijing_weather.json")
crawler.save_to_csv(weather_list, "cities_weather.csv")
```

## 输出数据格式

天气数据包含以下字段：

```json
{
  "city": "北京",
  "country": "CN",
  "timestamp": "2024-01-01T12:00:00.000000",
  "temperature": 15.5,
  "feels_like": 14.2,
  "humidity": 65,
  "pressure": 1013,
  "weather_main": "Clear",
  "weather_description": "晴",
  "wind_speed": 3.5,
  "wind_direction": 180,
  "visibility": 10000,
  "sunrise": "2024-01-01T06:30:00.000000",
  "sunset": "2024-01-01T18:30:00.000000"
}
```

## 命令行参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--city` | 单个城市名称 | `--city "北京"` |
| `--cities` | 多个城市，逗号分隔 | `--cities "北京,上海,广州"` |
| `--country` | 国家代码 | `--country "CN"` |
| `--format` | 输出格式 (json/csv) | `--format csv` |
| `--output` | 输出文件名 | `--output "weather.json"` |
| `--api-key` | API密钥 | `--api-key "your_key"` |
| `--delay` | 多城市查询延迟（秒） | `--delay 2` |

## 示例运行

运行示例脚本查看不同使用方法：

```bash
python examples.py
```

## 文件说明

- `weather_crawler.py` - 主程序文件
- `examples.py` - 使用示例
- `requirements.txt` - 依赖包列表
- `config.env` - 配置文件模板
- `README.md` - 项目文档

## 注意事项

1. **API限制**: 免费API密钥有请求限制，建议在批量查询时设置适当的延迟
2. **网络连接**: 需要稳定的网络连接访问OpenWeatherMap API
3. **城市名称**: 支持中英文城市名称，建议使用英文获得更准确的结果
4. **数据精度**: 温度精确到小数点后一位，其他数据按API返回精度

## 错误处理

程序包含完善的错误处理机制：

- 网络连接错误
- API密钥无效
- 城市名称不存在
- 数据解析错误
- 文件保存错误

所有错误都会记录到日志中，方便调试和监控。

## 许可证

此项目为开源项目，可自由使用和修改。
