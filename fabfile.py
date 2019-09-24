from fabric import task
from invoke import Responder
from ._credentials import github_username, github_password


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
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'hellodjango-blog-tutorial'

    project_root_path = '~/sites/www.lingxt.online/homepage/'

    # 切换的相应用户
    cmd = 'echo "password\n" | su - lingxt'
    c.run(cmd)

    # 停止应用
    cmd = 'echo "password\n" | sudo systemctl stop gunicorn-www.lingxt.online'
    c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        workon = 'workon homepage &&'
        c.run(workon + 'pip install -r requirements.txt')
        c.run(workon + 'python manage.py migrate')
        c.run(workon + 'python manage.py collectstatic --noinput')

    # 重新启动应用
    c.run('sudo systemctl start gunicorn-www.lingxt.online')
