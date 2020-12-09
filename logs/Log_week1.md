# Project Report - Week 1

## SI100B Project Report - Crawler

### Workload Division

- 颜毅恒（yanyh1@shanghaitech.edu.cn）& 彭琬迪（pengwd@shanghaitech.edu.cn)：

  探究如何向网页发送请求，参数的意义，如何获取网页响应的内容等问题。

- 苏慧哲（suhzh@shanghaitech.edu.cn or ):

  python程序的实现等相关问题。

### Answers to the document

#### ##The Data Source

- **How to send an HTTP GET request to a URL?**

  ```python
  import requests as rq
  r1 = rq.get("https://www.shanghaitech.edu.cn/", timeout=5)
  r2 = rq.get("https://man7.org/linux/man-pages/man1/pwd.1.html", timeout=5)
  ```

- **Which format of URL does the package accept?**

  >大多数 URL 方案的 URL 语法都建立在这个由 9 部分构成的通用格式上：

  ```<scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<frag>```

  >几乎没有哪个 URL 中包含了所有这些组件。URL 最重要的 3 个部分是方案（scheme）、主机（host）和路径（path）。表 2-1 对各种组件进行了总结。
  >表2-1　通用URL组件
  >
  >| 组　　件                                                     | 描　　述                                                     | 默　认　值     |
  >| ------------------------------------------------------------ | ------------------------------------------------------------ | -------------- |
  >| 方案                                                         | 访问服务器以获取资源时要使用哪种协议                         | 无             |
  >| 用户                                                         | 某些方案访问资源时需要的用户名                               | 匿名           |
  >| 密码                                                         | 用户名后面可能要包含的密码，中间由冒号（:）分隔              | \<E-mail地址\> |
  >| 主机                                                         | 资源宿主服务器的主机名或点分IP地址                           | 无             |
  >| 端口                                                         | 资源宿主服务器正在监听的端口号。很多方案都有默认端口号（HTTP的默认端口号为80） | 每个方案特有   |
  >| 路径                                                         | 服务器上资源的本地名，由一个斜杠（/）将其与前面的URL组件分隔开来。路径组件的语法是与服务器和方案有关的（本章稍后会讲到URL路径可以分为若干个段，每段都可以有其特有的组件。） | 无             |
  >| 参数                                                         | 某些方案会用这个组件来指定输入参数。参数为名/值对。URL中可以包含多个参数字段，它们相互之间以及与路径的其余部分之间用分号（;）分隔 | 无             |
  >| 查询                                                         | 某些方案会用这个组件传递参数以激活应用程序（比如数据库、公告板、搜索引擎以及其他因特网网关）。查询组件的内容没有通用格式。用字符“?”将其与URL的其余部分分隔开来 | 无             |
  >| 片段 一小片或一部分资源的名字。引用对象时，不会将frag字段传送给服务器；这个字段是在客户端内部使用的。通过字符“#”将其与URL的其余部分分隔开来 | 无                                                           |                |

  语法:

  - 不为空的协议名 + ```:```
  - ```//``` + 主体名（可选）
    - 用户信息 + ```@``` （可选）
      - 用户名
      - ```:``` + 密码（可选）
    - 主机
    - ```:``` + 端口号（可选）
  - 路径
  - ```?``` + 查询（可选）
  - ```#``` + 片段

- **How to determine if the request is successful?** 

  >下面是常见的HTTP状态码：
  >
  >200 - 请求成功
  >
  >204 - 服务器处理成功，但无访问内容301 - 资源（网页等）被永久转移到其它URL
  >
  >304 - 访问内容没有修改，使用缓存资源。
  >
  >404 - 请求的资源（网页等）不存在
  >500 - 内部服务器错误
  >如果是 200 OK ，响应会带有头部 Cache-Control, Content-Location, Date, ETag, Expires，和 Vary.

  成功：

  >1. ▪ 200 OK
  >2. ▪ 201 Created
  >3. ▪ 202 Accepted
  >4. ▪ 203 Non-Authoritative Information
  >5. ▪ 204 No Content
  >6. ▪ 205 Reset Content
  >7. ▪ 206 Partial Content
  >8. ▪ 207 Multi-Status

  

- **How to get the response body for a request?** 

```python
import requests as rq
r3 = rq.get("https://tools.ietf.org/rfc/rfc2616.txt")
print(r3.text)
```



#### ### FlightAware

- **Write down the URL of the requests and take a guess of what each part of the parameters means.**

  URL:<https://flightaware.com/ajax/vicinity_aircraft.rvt>

  | Params | Meaning                 |
  | ------ | ----------------------- |
  | minLon | 最小的经度（Longitude） |
  | minLat | 最小的纬度（Latitude）  |
  | maxLon | 最大经度                |
  | maxLat | 最大纬度                |
  | token  | 验证码                  |

- **Determine what method is used for each request.**

  用get请求方式。

- **Determine the format of the response and find a way to parse it to a structured one that Python could understand.**

  【苏慧哲重新编辑】

  通过requests 的 text属性观察到是json的格式
  使用requests的自带json()方法转换成dict。
  用key()看到dict一共有两个keys:feature 和 type.
  feature中的信息是需要的。其中一个数据示例：

  ```python
  {'type': 'Feature',
    'geometry': {'type': 'Point', 'coordinates': [113.01264, 24.36804]},
    'properties': {'flight_id': 'GCR6468-1607228100-schedule-0273:0',
     'prefix': 'GCR',
     'direction': 282,
     'type': 'A320',
     'ident': 'GCR6468',
     'icon': 'airliner',
     'ga': False,
     'landingTimes': {'estimated': '1607409960'},
     'origin': {'icao': 'ZSQZ', 'iata': 'JJN', 'isUSAirport': False},
     'destination': {'icao': 'ZUGY',
      'iata': 'KWE',
      'TZ': ':Asia/Shanghai',
      'isUSAirport': False},
     'prominence': 25916,
     'flightType': 'airline',
     'projected': 0,
     'altitude': 341,
     'altitudeChange': '-',
     'groundspeed': 394}}
  ```

  keys有着良好的命名规范，可以直接看出来是什么意思。
  不明白的：prominece，projected
  时间应该都是时间戳。

- **Determine the meaning of each field of the response.**

  【苏慧哲重新编辑】