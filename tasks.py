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
def coverage_report(ctx):
    ctx.run("coverage html -d documentation/test_reports/unittests")
