import click
import modrinth_analytics.collection
import modrinth_analytics.graphing


@click.group()
@click.option('--token', required=True, help='Labrinth API Token')
@click.pass_context
def cli(ctx, token):
    ctx.ensure_object(dict)
    ctx.obj['TOKEN'] = token


@cli.command()
@click.option('--user', 'users', required=True, multiple=True, help='Username or id to collect analytics for.')
@click.option('--db', default='./analytics.json', help='JSON file to put analytics data.')
@click.pass_context
def collect(ctx, users, db):
    token = ctx.obj['TOKEN']

    modrinth_analytics.collection.collect(list(users), token, db)

@cli.command()
@click.argument('analytic', default=None, type=click.Choice(['individual', 'total']))
@click.option('--time', default='daily', type=click.Choice(['hourly', 'daily', 'weekly', 'monthly', 'annually']))
@click.option('--user', required=True, help='User to create analytic graphs for.')
@click.option('--db', default='./analytics.json', help='JSON file to get analytics data.')
@click.pass_context
def graph(ctx, analytic, time, user, db):
    token = ctx.obj['TOKEN']

    modrinth_analytics.graphing.downloads(analytic, time, user, db, token)
