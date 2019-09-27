from fabric import task
from invoke import Responder
from _credentials import github_username, github_password


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(
            github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    project_root_path = '/home/lingxt/sites/www.lingxt.online/homepage/'

    # 停止应用
    cmd = 'sudo systemctl stop gunicorn-www.lingxt.online'
    c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'sudo git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        # 指定虚拟环境
        with c.prefix(". /home/ubuntu/.local/bin/virtualenvwrapper.sh; workon homepage"):
            c.run('pip install -r requirements.txt')
            c.run('python manage.py migrate -auth')
            c.run('python manage.py migrate --run-syncdb')
            c.run("python manage.py collectstatic --noinput")

    # 重新启动应用
    c.run('sudo systemctl start gunicorn-www.lingxt.online')
