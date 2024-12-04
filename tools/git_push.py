from pathlib import Path
from git import Repo

def upload_to_git(repo_path, file_path, commit_message, branch="main"):
    """
    上传文件到 Git 仓库

    :param repo_path: Git 仓库路径
    :param file_path: 要上传的文件路径
    :param commit_message: 提交的消息
    :param branch: 分支名称，默认是 'main'
    """
    repo = Repo(repo_path)

    if repo.is_dirty(untracked_files=True):
        print("发现未提交的更改，先提交它们...")

    # 检查目标分支是否存在，切换到目标分支
    if branch not in repo.branches:
        print(f"创建分支 {branch} 并切换")
        repo.git.checkout("-b", branch)
    else:
        repo.git.checkout(branch)

    # 确保目标文件在 Git 仓库中
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"文件 {file_path} 不存在！")

    relative_path = file.relative_to(repo.working_tree_dir)
    repo.index.add([str(relative_path)])

    # 提交文件
    print(f"正在提交文件：{relative_path}")
    repo.index.commit(commit_message)

    # 推送到远程仓库
    print(f"推送到远程分支 {branch}...")
    origin = repo.remote(name="origin")
    origin.push(branch)
    print(f"文件 {file_path} 已成功上传到分支 {branch}！")

if __name__ == "__main__":
    # 配置路径和文件
    repo_path = "/path/to/your/local/git/repo"  # 本地 Git 仓库路径
    file_path = "/path/to/your/file.txt"       # 要上传的文件路径
    commit_message = "Add new file"            # 提交消息

    # 调用函数
    try:
        upload_to_git(repo_path, file_path, commit_message)
    except Exception as e:
        print(f"操作失败: {e}")
