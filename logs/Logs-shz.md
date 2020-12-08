# Logs-shz

## Problems&Solutions

### How to send Get/Post requests

requests.get(URL)
requests.post(URL, DATA)

>HTTP GET 方法请求指定的资源。使用 GET 的请求应该只用于获取数据。
>
>| 请求是否有主体       | 否  |
>| -------------------- | --- |
>| 成功的响应是否有主体 | 是  |
>| 安全                 | 是  |
>| 幂等                 | 是  |
>| 可缓存               | 是  |
>| HTML 表单是否支持    | 是  |

### 不同的HTTP 请求类型

> HTTP 协议中共定义了八种方法或者叫“动作”来表明对 Request-URI 指定的资源的不同操作方式，具体介绍如下：
>
>OPTIONS：返回服务器针对特定资源所支持的HTTP请求方法。也可以利用向Web服务器发送'*'的请求来测试服务器的功能性。
>HEAD：向服务器索要与GET请求相一致的响应，只不过响应体将不会被返回。这一方法可以在不必传输整个响应内容的情况下，就可以获取包含在响应消息头中的元信息。
>GET：向特定的资源发出请求。
>POST：向指定资源提交数据进行处理请求（例如提交表单或者上传文件）。数据被包含在请求体中。POST请求可能会导致新的资源的创建和/或已有资源的修改。
>PUT：向指定资源位置上传其最新内容。
>DELETE：请求服务器删除 Request-URI 所标识的资源。
>TRACE：回显服务器收到的请求，主要用于测试或诊断。
>CONNECT：HTTP/1.1 协议中预留给能够将连接改为管道方式的代理服务器。
>虽然 HTTP 的请求方式有 8 种，但是我们在实际应用中常用的也就是 get 和 post，其他请求方式也都可以通过这两种方式间接的来实现。

### 不同HTTP状态码

>下面是常见的HTTP状态码：
>
>200 - 请求成功
>301 - 资源（网页等）被永久转移到其它URL
>404 - 请求的资源（网页等）不存在
>500 - 内部服务器错误

204 - 服务器处理成功，但无访问内容
304 - 访问内容没有修改，使用缓存资源。

>HTTP 304 未改变说明无需再次传输请求的内容，也就是说可以使用缓存的内容。这通常是在一些安全的方法（safe），例如GET 或HEAD 或在请求中附带了头部信息： If-None-Match 或If-Modified-Since。
>如果是 200 OK ，响应会带有头部 Cache-Control, Content-Location, Date, ETag, Expires，和 Vary.

### HTTP Headers

>HTTP 消息头允许客户端和服务器通过 request和 response传递附加信息。一个请求头由名称（不区分大小写）后跟一个冒号“：”，冒号后跟具体的值（不带换行符）组成。该值前面的引导空白会被忽略。
>据不同上下文，可将消息头分为：
>General headers: 同时适用于请求和响应消息，但与最终消息主体中传输的数据无关的消息头。
>Request headers: 包含更多有关要获取的资源或客户端本身信息的消息头。
>Response headers: 包含有关响应的补充信息，如其位置或服务器本身（名称和版本等）的消息头。
>Entity headers: 包含有关实体主体的更多信息，比如主体长(Content-Length)度或其MIME类型。

通用头部

>通用首部指的是可以应用于请求和响应中，但是不能应用于消息内容自身的 HTTP 首部 。 取决于应用的上下文环境，通用首部可以是响应头部或者请求头部。但是不可以是实体头部。

实体头部

>An entity header is an HTTP header that describes the payload of an HTTP message (i.e. metadata about the message body). Entity headers include: Content-Length, Content-Language, Content-Encoding, Content-Type, Expires, etc. Entity headers may be present in both HTTP request and response messages.

请求头部

>请求头是 HTTP 头的一种，它可在 HTTP 请求中使用，并且和请求主体无关 。某些请求头如 Accept、Accept-*、 If-* 允许执行条件请求。某些请求头如：Cookie, User-Agent 和 Referer 描述了请求本身以确保服务端能返回正确的响应。
>并非所有出现在请求中的 HTTP 首部都属于请求头，例如在 POST 请求中经常出现的 Content-Length 实际上是一个代表请求主体大小的 entity header，虽然你也可以把它叫做请求头。

相应头部

>响应头（Response header） 可以定义为：被用于http响应中并且和响应消息主体无关的那一类 HTTP header。像Age, Location 和 Server都属于响应头，他们被用于描述响应。
>并非所有出现在响应中的http header都属于响应头，例如Content-Length就是一个代表响应体消息大小的entity header，虽然你也可以把它叫做响应头。

### 合法的URL

这个问题可复杂了。。

>大多数 URL 方案的 URL 语法都建立在这个由 9 部分构成的通用格式上：

```<scheme>://<user>:<password>@<host>:<port>/<path>;<params>?<query>#<frag>```
>几乎没有哪个 URL 中包含了所有这些组件。URL 最重要的 3 个部分是方案（scheme）、主机（host）和路径（path）。表 2-1 对各种组件进行了总结。
>表2-1　通用URL组件
>
>|组　　件 |描　　述 |默　认　值|
>|---|---|---|
>|方案 |访问服务器以获取资源时要使用哪种协议 |无|
>|用户| 某些方案访问资源时需要的用户名| 匿名|
>|密码| 用户名后面可能要包含的密码，中间由冒号（:）分隔| \<E-mail地址\>|
>|主机 |资源宿主服务器的主机名或点分IP地址 |无|
>|端口| 资源宿主服务器正在监听的端口号。很多方案都有默认端口号（HTTP的默认端口号为80）| 每个方案特有|
>|路径 |服务器上资源的本地名，由一个斜杠（/）将其与前面的URL组件分隔开来。路径组件的语法是与服务器和方案有关的（本章稍后会讲到URL路径可以分为若干个段，每段都可以有其特有的组件。）| 无|
>|参数 |某些方案会用这个组件来指定输入参数。参数为名/值对。URL中可以包含多个参数字段，它们相互之间以及与路径的其余部分之间用分号（;）分隔 |无|
>|查询| 某些方案会用这个组件传递参数以激活应用程序（比如数据库、公告板、搜索引擎以及其他因特网网关）。查询组件的内容没有通用格式。用字符“?”将其与URL的其余部分分隔开来 |无|
>|片段 一小片或一部分资源的名字。引用对象时，不会将frag字段传送给服务器；这个字段是在客户端内部使用的。通过字符“#”将其与URL的其余部分分隔开来| 无|

#### 语法

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

### Answer to the doc

#### How to send an HTTP GET request to a URL

```python
import requests as rq
r1 = rq.get("https://www.shanghaitech.edu.cn/", timeout=5)
print(r1)
r2 = rq.get("https://man7.org/linux/man-pages/man1/pwd.1.html", timeout=5)
print(r2)
```

#### Which format of URL does the package accept

参见合法的URL

#### How to determine if the request is successful

参见 HTTP 状态码

#### How to get the response body for a request

```python
import requests as rq
r3 = rq.get("https://tools.ietf.org/rfc/rfc2616.txt")
print(r3.text)
```

## References

<https://2.python-requests.org/zh_CN/latest/index.html>

<https://www.runoob.com/note/35442>

<https://www.runoob.com/http/http-status-codes.html>

<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status>

<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/304>

<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods>

<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers>

<https://developer.mozilla.org/zh-CN/docs/Glossary/%E9%80%9A%E7%94%A8%E9%A6%96%E9%83%A8>

<https://developer.mozilla.org/en-US/docs/Glossary/entity_header>

<https://developer.mozilla.org/zh-CN/docs/Glossary/%E8%AF%B7%E6%B1%82%E5%A4%B4>

<https://developer.mozilla.org/zh-CN/docs/Glossary/Response_header>

<https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods/GET>

<https://zh.wikipedia.org/wiki/%E7%BB%9F%E4%B8%80%E8%B5%84%E6%BA%90%E6%A0%87%E5%BF%97%E7%AC%A6#.E4.B8.8EURL.E5.92.8CURN.E7.9A.84.E5.85.B3.E7.B3.BB>

<https://blog.csdn.net/Godric42/article/details/26083303>

<https://www.ituring.com.cn/book/miniarticle/44588>

<https://developer.mozilla.org/zh-CN/docs/Learn/Common_questions/What_is_a_URL>

<https://en.wikipedia.org/wiki/URL#Syntax>

## Package Used

requests
