# Project Report - Week 1

## SI100B Project Report - Crawler

### Workload Division

- 颜毅恒（yanyh1@shanghaitech.edu.cn）& 彭琬迪（pengwd@shanghaitech.edu.cn)：

  Find how to send requests to the web, understand the meaning of the data crawled form the web.

- 苏慧哲（suhzh@shanghaitech.edu.cn or vhtmscyo@gmail.com):

  Write python program and the report.

### Preliminary Comments

#### Solution

We want to write a crawler to get the data from the website. First, we should understand how normal people or the browser get the information from the website.

##### Understand How Browser Get the information

After searching the web, we find that browsers send HTTP messages to communicate with the server. HTTP is the abbriviation of Hypertext Transfer Protocol. We can find the definition of HTTP messages in MDN[<sup>[1]</sup>](#ref-1):

> HTTP messages are how data is exchanged between a server and a client. There are two types of messages: requests sent by the client to trigger an action on the server, and responses, the answer from the server.

Since we want to sent requests to the server to ask for information, we should understand the requests message.

A request message is compose of three parts: start line, headers and body. 

In the status line, an HTTP method, the request target and the HTTP version should be given.

Headers contains some useful information to be used by the server. Headers should follow the same basic structure:

> a case-insensitive string followed by a colon (`':'`) and a value whose structure depends upon the header.

Some requests need to fetch data from or send data to the server. These data are in body part. Not all requests have a body.

There're eight types of requests in total[<sup>[2]</sup>](#ref-2):

> - `GET`
>
>   The `GET` method requests a representation of the specified resource. Requests using `GET` should only retrieve data.
>
> - `HEAD`
>
>   The `HEAD` method asks for a response identical to that of a `GET` request, but without the response body.
>
> - `POST`
>
>   The `POST` method is used to submit an entity to the specified resource, often causing a change in state or side effects on the server.
>
> - `PUT`
>
>   The `PUT` method replaces all current representations of the target resource with the request payload.
>
> - `DELETE`
>
>   The `DELETE` method deletes the specified resource.
>
> - `CONNECT`
>
>   The `CONNECT` method establishes a tunnel to the server identified by the target resource.
>
> - `OPTIONS`
>
>   The `OPTIONS` method is used to describe the communication options for the target resource.
>
> - `TRACE`
>
>   The `TRACE` method performs a message loop-back test along the path to the target resource.
>
> - `PATCH`
>
>   The `PATCH` method is used to apply partial modifications to a resource.

`GET` and `POST` are the most commenly use two requests. In this project, we only need to understand `get` method so that we can get resources from the server.

After the requests accepted by the server, it will give back an HTTP response. It is also composed of three parts: status line, headers and body.

The status line contains the the protocol version, a status code and status text. The status code and the status text indicates whether the request is successed or failed. According to MDN[<sup>[4]</sup>](#ref-4):

>Responses are grouped in five classes:
>
>1. Informational responses (`100`–`199`)
>2. Successful responses (`200`–`299`)
>3. Redirects (`300`–`399`)
>4. Client errors (`400`–`499`)
>5. Server errors (`500`–`599`)

And following are some commonly seen status[<sup>[5]</sup>](#ref-5):

> 200  OK - The request has succeeded. 
>
> 204 No Content - There is no content to send for this request, but the headers may be useful.
>
> 301 Moved Permanently - The URL of the requested resource has been changed permanently. The new URL is given in the response.
>
> 304 Not Modified - This is used for caching purposes. It tells the client that the response has not been modified, so the client can continue to use the same cached version of the response.
>
> 404 Not Found - The server can not find the requested resource.
>
> 500 Internal Server Error- The server has encountered a situation it doesn't know how to handle.

The headers are similar to the headers of the HTTP requests. The structure are strictly the same, but the type of the headers may be different.

The body contains the data given by the server. The information we want should be in the body.



It not enough to understand the HTTP messages only if we want to actually send the massege. We should also understand the URLs.

##### Design a Valid URL

We search the wikipedia and find the syntax of a valid URL (Since a URL is a URI points to the resources on a network, it's syntax is the same as the URI). It should be composed of[<sup>[6]</sup>](#ref-6):

- A non-empty **scheme** + ```:```

- ```//``` + an **authority** component (optional)
  - A **userinfo** subcomponent + ```@``` (optional)
    - username
    - ```:``` + password (optional)
  - A **host** subcomponent
  - ```:``` + A **port** subcomponent (optional)

- A **path** component

- ```?``` + A **query** component (optional)

- ```#``` + A **fragment** component (optional)

There is also a more clear picture:

![URI syntax diagram](https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/URI_syntax_diagram.svg/1068px-URI_syntax_diagram.svg.png "URL Syntax")

<center>Fig.1 URI Syntanx<a href="#ref-6"><sup>[6]</sup></a></center>

##### Get the Information Using Python

In order to use python to send HTTP requests and parse HTTP responses, we decide to use requests library. Two of our team member failed to connect to flightradar24, so we decided to set fliaghtaware as our target website.

According to the first week's document of the project, before we sent the requests, we should first find the tocken on on the website. Through some simple searching, we can find that the token is written in the html file.

![截屏2020-12-10 下午3.33.06](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午3.33.06.png)

<center>Fig.2 How to find the token - first step</center>

![截屏2020-12-10 下午3.34.01](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午3.34.01.png)

<center>Fig.3 How to find the token - second step</center>

We can first request the html file and find the token use regex[<sup>[8]</sup>](#ref-8).

```python
import requests as rq
import re #regex pakage of python

tokenregx = '\"VICINITY_TOKEN\":\"([A-Za-z0-9]*)\"'

html = rq.get("https://flightaware.com/live/", timeout=5)

testurl = "https://flightaware.com/ajax/vicinity_aircraft.rvt"

token = re.search(tokenregx,html.text)
print(token.group(1))
```

![截屏2020-12-10 下午3.39.27](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午3.39.27.png)

<center>Fig.4 Find token</center>

Once we got the token we can send HTTP requests using requests:

```python
estparam = {"minLon":100,"minLat":11,"maxLon":143,"maxLat":51,"token":token.group(1)}

testquery = rq.get(testurl,params = testparam)

print(testquery)
t = testquery.json()
print(type(t))
print(t.keys())
```

![截屏2020-12-10 下午4.14.13](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午4.14.13.png)

<center>Fig.5 Get data</center>

`minLon` means the minimal longitude, `maxLon` is maximal longitude. Likewise, `minLat` is minimal Latitude and `maxLat` is maximal Latitude.

The whole data is too large, so we won't write it in this report, nor will we show it directly to the user. In this case, we should parse the data and display them in a human-friendly way.

##### Display the Information

First, take a look at the raw data:

![截屏2020-12-10 下午4.21.42](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午4.21.42.png)

<center>Fig.6 What's inside</center>

We can easily find that the useful information is in the "feature". ![截屏2020-12-10 下午4.24.45](/Users/sorano_akia/Library/Application Support/typora-user-images/截屏2020-12-10 下午4.24.45.png)

The information are stored in a list of dictionaries. Here's an examplar of the data:

```python
{'type': 'Feature', 
 'geometry': {'type': 'Point', 
              'coordinates': [121.33802, 31.16602]}, 
 'properties': {'flight_id': 'CSN3557-1607409360-schedule-0316:0', 
                'prefix': 'CSN', 
                'direction': 358, 
                'type': 'A321', 
                'ident': 'CSN3557', 
                'icon': 'airliner', 
                'ga': False, 
                'landingTimes': {'estimated': '1607588305'}, 
                'origin': {'icao': 'ZGSZ', 
                           'iata': 'SZX', 
                           'isUSAirport': False}, 
                'destination': {'icao': 'ZSSS', 
                                'iata': 'SHA', 
                                'TZ': ':Asia/Shanghai', 
                                'isUSAirport': False}, 
                'prominence': 118, 
                'flightType': 'airline', 
                'projected': 0, 'altitude': 2, 
                'altitudeChange': 'D', 
                'groundspeed': 125}
}
```

We can guess the meaning of the data based on the keys of the dictionary.

The `coordinates`(longitude and latitude), `direction` (heading), `altitude`, `ident`, `groundspeed` (flight number), `iata` of `origin` and `iata` of `destination` are informations we need.

`altitude` and `groundspeed` may not appear in some pieces of data.

However, the squawk number and the registration number are missing.

Note that the 'filight_id' is composed of flight number of the airline and a unix timestamp, so it should be distinct and can be used  to get rid of the duplicated data.

We create a dictionary to store the data. The key is the 'flight_id' and the value is a list of dictionaries contains the selected data.

However when we implment the data-selection part, we find that one query per time may not enough.

##### Cross Antimeridian

The website can only accept the query when minLat and minLon are smaller than maxLat and maxLon respectively (if not, the result would be the same as that case). So if the square area we ask has cross the antimeridian, we should seperate the query into two parts and merge the two query  results.

#### References

[1] <a id="ref-1" href="N (https://developer.mozilla.org/en-US/docs/Web/HTTP/Messages">HTTP messages-HTTP|MDN</a>

[2] <a id="ref-2" href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods">HTTP request methods-HTTP|MDN</a>

[3] [Get-HTTP|MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/GET)

[4] <a id="ref-4" href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Status">HTTP response status codes-HTTP|MDN</a>

[5] <a id="ref-5" href="https://www.runoob.com/http/http-status-codes.html">HTTP状态码｜菜鸟教程</a>

[6] <a id="ref-6" href="https://en.wikipedia.org/wiki/Uniform_Resource_Identifier">Uniform Resources Identifier - Wikipedia</a>

[7] <a id="ref-7" href="https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html">快速上手 - Requests 2.18.1 文档</a>

[8] <a id="ref-8" href="https://tool.oschina.net/uploads/apidocs/jquery/regexp.html">正则表达式手册</a>

### Data Source

### Implementation

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

FlightAware

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