from invoke import task


@task
def start(ctx):
    ctx.run('flask run --host=0.0.0.0')


@task
def pylint(ctx):
    ctx.run('pylint src')
