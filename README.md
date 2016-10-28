# torgit  

基于tornado的git服务器实现  

## 处理的问题  

git-http-protocol 中smart http使用了chunked的传输方式，这里主要借用tornado的chunked能力，实际的服务和orm可以直接挂载在tornado上运行。
演示为无db版本，直接将用户认证和仓库权限使用json存储。

## 如何使用demo  


- 将代码clone到本地  
>   git clone https://github.com/jcteng/torgit.git

- 安装依赖项  
>   pip install -r requirements.txt

- 运行演示  

>   python main.py 

- 访问http://127.0.0.1:8000  可看到如下内容

<h1>Hello ,Torgit!</h1>
<hr>
<h3>User List</h3>
<table border="1">
<thead>
<th>user</th>
<th>password</th>
</thead>
<tbody>

<tr>
<td>user2</td>
<td>2</td>
</tr>

<tr>
<td>user3</td>
<td>3</td>
</tr>

<tr>
<td>user1</td>
<td>1</td>
</tr>

</tbody>
</table>
<h3>Repo List</h3>
<table border="1">
<thead>
<th>prefix</th>
<th>repos</th>
<th>permission</th>
<th>access_url</th>
</thead>
<tbody>


<tr>
<td>user1p</td>
<td>repo1</td>
<td>{u&#39;anonymous_write&#39;: False, u&#39;write_users&#39;: [u&#39;user1&#39;], u&#39;anonymous_read&#39;: True, u&#39;read_users&#39;: []}</td>
<td>http://127.0.0.1:8000/git/user1p/repo1.git</td>
</tr>



<tr>
<td>user2p</td>
<td>repo2</td>
<td>{u&#39;anonymous_write&#39;: False, u&#39;write_users&#39;: [u&#39;user1&#39;], u&#39;anonymous_read&#39;: False, u&#39;read_users&#39;: [u&#39;user1&#39;, u&#39;user2&#39;]}</td>
<td>http://127.0.0.1:8000/git/user2p/repo2.git</td>
</tr>


</tbody>
</table>


- 此时可使用access_url访问torgit提供的git服务  
>   git clone http://127.0.0.1:8000/git/user2p/repo2.git

## 如何使用-code  

通过重载 BaseRepoManager 完成repo的权限控制/存储访问/DB认证，参考demo_repo_mgr.BaseRepoManager


