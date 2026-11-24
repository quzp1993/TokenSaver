# Q1
## S1
401 和 403 是两个含义不同的 HTTP 状态码，经常被混淆。401 Unauthorized 表示请求没有携带有效的身份认证凭据，也就是服务器还不知道你是谁，或者你提供的密码、token 等凭据已经失效，此时你需要先登录或重新认证。403 Forbidden 则表示服务器已经认出了你的身份，你确实是一个已经认证过的用户，但你没有权限访问当前请求的这个资源，即使重新登录也无法解决，需要由管理员为你授予相应的权限。因此两者的核心区别在于：401 是认证（authentication）层面的问题，403 是授权（authorization）层面的问题。
## S2
401 = 未认证。缺有效凭据，服务器不知道你是谁。需登录。
403 = 已认证但无权限。服务器认识你，但不许访问。
区别：认证 authn vs 授权 authz。
## S3
401 未认证：缺有效凭据 → 登录
403 无权限：已认证但不许访问 → 授权
区别：authn vs authz

# Q2
## S1
下面是一个完整可用的 Python 函数，使用标准库的 csv 模块实现。它会读取 CSV 文件，遍历每一行，提取指定列的数值，忽略空单元格和无法转换成数字的内容，最后返回这些数值的平均值。如果这一列没有任何有效数字，函数会返回 None，从而避免除以零的错误。

```python
import csv

def col_mean(path, col):
    values = []
    with open(path, newline='') as f:
        for row in csv.reader(f):
            if col >= len(row):
                continue
            cell = row[col].strip()
            if not cell:
                continue
            try:
                values.append(float(cell))
            except ValueError:
                continue
    return sum(values) / len(values) if values else None
```
## S2
用 csv 模块。遍历行，取目标列，空值跳过，float() 转换，ValueError 跳过非数字，空列返回 None 防除零。

```python
import csv

def col_mean(path, col):
    vals = []
    with open(path, newline='') as f:
        for row in csv.reader(f):
            if col >= len(row):
                continue
            cell = row[col].strip()
            if not cell:
                continue
            try:
                vals.append(float(cell))
            except ValueError:
                continue
    return sum(vals) / len(vals) if vals else None
```
## S3
```python
import csv

def col_mean(path, col):
    vals = []
    with open(path, newline='') as f:
        for row in csv.reader(f):
            if col >= len(row):
                continue
            cell = row[col].strip()
            if not cell:
                continue
            try:
                vals.append(float(cell))
            except ValueError:
                continue
    return sum(vals) / len(vals) if vals else None
```

# Q3
## S1
要撤销最近一次 commit 并且保留所有改动，可以使用 git reset --soft HEAD~1。这个命令会把 HEAD 指针回退到上一次提交，但不会改动你的工作区和暂存区，所以你的所有代码改动都还在。如果你想让改动退回到未暂存状态，就用 git reset --mixed HEAD~1（这也是默认行为）。需要注意的是，如果这次 commit 已经推送到远端仓库，就不要再用 reset 改写历史，否则会导致其他人拉取时出现冲突。
## S2
git reset --soft HEAD~1。工作区改动保留，暂存区也保留。--mixed 回退暂存。已推送勿 reset。
## S3
`git reset --soft HEAD~1`（改动+暂存保留）
`--mixed`：回退暂存
已推送勿 reset

# Q4
## S1
TCP 三次握手是建立 TCP 连接的过程，分三步。第一步，客户端向服务器发送一个 SYN 报文，表示请求建立连接，并携带一个初始序号。第二步，服务器收到后回复一个 SYN-ACK 报文，表示同意连接，同时带上自己的初始序号并确认客户端的序号。第三步，客户端再发送一个 ACK 报文进行确认。经过这三步，双方就同步了各自的序号，连接正式建立，之后就可以开始传输数据了。
## S2
三步建连接：
1 客户端发 SYN
2 服务端回 SYN-ACK
3 客户端发 ACK
目的：同步序号，建立连接。
## S3
1 客户端 → SYN
2 服务端 → SYN-ACK
3 客户端 → ACK
目的：同步序号，建立连接

# Q5
## S1
这个需求可以用 GROUP BY 加 HAVING 来实现。GROUP BY 把数据按部门分组，AVG(salary) 计算每个部门的平均工资，HAVING 在分组之后过滤出平均工资大于 5000 的部门。SQL 如下：

```sql
SELECT dept, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
HAVING AVG(salary) > 5000;
```
## S2
分组后过滤，用 HAVING：

```sql
SELECT dept, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
HAVING AVG(salary) > 5000;
```
## S3
```sql
SELECT dept, AVG(salary) AS avg_salary
FROM employees
GROUP BY dept
HAVING AVG(salary) > 5000;
```

# Q6
## S1
这个报错的意思是 Python 找不到 pandas 这个第三方库，通常是因为你还没有安装它。解决方法是先确认你当前用的是哪个 Python 环境（可以用 which python 或 python --version 查看），然后在这个环境里执行 pip install pandas 安装。如果安装后仍然报错，很可能是你运行脚本时用了另一个虚拟环境或解释器，需要检查你的 IDE 或终端配置的 Python 解释器是否和你安装 pandas 的环境一致。安装完成后可以运行 python -c "import pandas" 来验证。
## S2
pandas 没装。装：pip install pandas。若仍报错，检查解释器/虚拟环境（which python）。验证：python -c "import pandas"。
## S3
· 未装 pandas
· 装：`pip install pandas`
· 检查解释器：`which python`（可能环境不对）
· 验证：`python -c "import pandas"`

# Q7
## S1
这个正则表达式用来精确匹配一个 YYYY-MM-DD 格式的日期。开头的 ^ 和结尾的 $ 表示锚定整个字符串，也就是必须从头到尾完全匹配。\d{4} 匹配四个数字，代表年份；中间的 - 是字面连字符；两个 \d{2} 分别匹配两个数字，代表月份和日期。整条表达式里有三组圆括号，形成三个捕获组，分别捕获年、月、日三部分。
## S2
匹配 YYYY-MM-DD 日期。^ 和 $ 锚定整串。\d{4}=4位年。两个 \d{2}=月、日各2位。3 个捕获组。
## S3
匹配 YYYY-MM-DD 日期
· ^…$：锚定整串
· \d{4}：4 位（年）
· \d{2} ×2：各 2 位（月、日）
· 捕获组：3

# Q8
## S1
git merge 和 git rebase 是两种整合分支的方式，主要区别在于产生的历史。git merge 会把两个分支合并在一起，保留各自的分叉历史，并生成一个新的 merge commit。git rebase 则是把当前分支的提交逐个重放到目标分支的最新提交之上，使历史变成一条直线，看起来更干净。但 rebase 会改写提交历史，如果这些提交已经推送到公共分支，改写会导致别人基于旧历史的工作产生冲突，所以公共分支不要 rebase。一般建议：公共分支用 merge 保留真实历史，自己本地未推送的分支可以用 rebase 整理。
## S2
merge：保留分叉历史 + merge commit。
rebase：重放提交，线性历史，改写历史。
rebase 公共分支慎用。
建议：公共 merge，本地整理 rebase。
## S3
merge：保留分叉 + merge commit
rebase：线性历史，改写提交
rebase 勿用于已推送/公共分支
用：公共 merge，本地 rebase

# Q9
## S1
这段话的核心要点是：过拟合指的是模型在训练数据上表现很好，但到了没见过的数据上准确率大幅下降的现象。解决过拟合的办法有：增加训练数据、降低模型复杂度、使用正则化、以及使用交叉验证。另外，在训练过程中采用早停（early stopping），也能防止模型过度记忆训练数据中的噪声。
## S2
过拟合：训练好、新数据差。
解法：加数据、降复杂度、正则化、交叉验证。
早停 early stopping。
## S3
过拟合：训练好 / 新数据差
解法：加数据 · 降复杂度 · 正则化 · 交叉验证 · 早停(early stopping)

# Q10
## S1
要列出当前目录及所有子目录下的 .log 文件并按大小降序排列，可以用 find 查找文件，再用 du 或 ls 配合 sort 排序。下面这条命令可以完成这个需求：先用 find 找到所有 .log 文件，然后用 du -b 得到每个文件的字节大小，最后用 sort -rn 按数值降序排列。

```bash
find . -name '*.log' -type f -exec du -b {} + | sort -rn
```
## S2
find 找 .log，du 取大小，sort 降序：

```bash
find . -name '*.log' -type f -exec du -b {} + | sort -rn
```
## S3
```bash
find . -name '*.log' -type f -exec du -b {} + | sort -rn
```
