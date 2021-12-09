from invoke import task


@task
def start(ctx):
    ctx.run('flask run --host=0.0.0.0')


@task
def pylint(ctx):
    ctx.run('pylint src')


@task
def test(ctx):
    ctx.run('pytest src')


@task
def coverage(ctx):
    ctx.run('coverage run -m pytest src')


@task(coverage)
def covreport(ctx):
    ctx.run("coverage html -d documentation/test_reports/unittests")


@task(covreport)
def coverage_report(ctx):
    ctx.run("rm documentation/test_reports/unittests/.gitignore")
