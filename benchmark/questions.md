# 基准测试：10 个问题 + 关键信息清单

每题列出必须命中的关键信息（评分依据）。答案文件：`answers.md`。

1. **概念** HTTP 401 和 403 状态码的区别？
   - 401 = 未认证 / 缺少有效凭据
   - 403 = 已认证但无权限访问
   - 区别 = 认证(authn) vs 授权(authz)

2. **代码** 写一个 Python 函数：读 CSV 文件，返回指定列的平均值（忽略空值和非数字）。
   - 用 csv 模块或 pandas 读取
   - 定位目标列并遍历
   - float() 转换，异常跳过非数字
   - 跳过空值
   - 返回均值，空列时避免除零

3. **代码** Git 撤销最近一次 commit，但保留所有改动（未推送到远端）。
   - git reset --soft HEAD~1（或 --mixed）
   - 工作区改动保留
   - 说明 soft 保留暂存 / mixed 回退暂存
   - 已推送历史勿 reset

4. **概念** 简述 TCP 三次握手。
   - 客户端发 SYN
   - 服务端回 SYN-ACK
   - 客户端发 ACK
   - 目的 = 同步序号 / 建立连接

5. **SQL** 查询每个部门平均工资，只显示平均工资 > 5000 的部门。
   - SELECT dept, AVG(salary)
   - GROUP BY dept
   - HAVING AVG(salary) > 5000

6. **排查** 报错 `ModuleNotFoundError: No module named 'pandas'` 怎么解决？
   - pandas 未安装
   - 安装：pip install pandas
   - 检查是否用错解释器/虚拟环境（which python）
   - 验证安装成功

7. **正则** 解释 `^(\d{4})-(\d{2})-(\d{2})$` 匹配什么。
   - ^ 和 $ 锚定整串
   - \d{4} = 4 位数字
   - 两个 \d{2} = 各 2 位数字
   - 3 个捕获组
   - 整体匹配 YYYY-MM-DD 日期

8. **对比** git merge 和 git rebase 的区别，何时用哪个？
   - merge 保留分支历史 + 产生 merge commit
   - rebase 重放提交，产生线性历史
   - rebase 改写历史，公共分支慎用
   - 建议：公共分支 merge、本地整理 rebase

9. **总结** 总结这段话的核心要点：
   「机器学习模型在训练数据上表现很好，但在未见过的数据上准确率骤降，这是过拟合。解决办法包括增加训练数据、降低模型复杂度、使用正则化和交叉验证。早期停止训练也能防止模型记住噪声。」
   - 过拟合 = 训练好、新数据差
   - 解法：增加数据 / 降复杂度 / 正则化 / 交叉验证
   - 早停（early stopping）

10. **Bash** 列出当前目录及子目录所有 .log 文件，按文件大小降序。
    - find . -name '*.log' -type f
    - 按大小排序（du / ls -S）
    - 降序
    - 命令可直接运行
