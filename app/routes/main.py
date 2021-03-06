from flask import render_template

from app import app
from app.models import Score, Chart, Player
from app.ranking import get_scores_query
from . import build_pager


@app.route('/index')
@app.route('/')
def index():
    latest_scores = (Score.query
        .order_by(Score.achieved_at.desc())
    )
    return render_template(
        'home.html',
        **build_pager('index', latest_scores, per_page=20)
    )


@app.route('/scores')
def scores():
    return 'TODO'


@app.route('/share/<id>')
def share(id):
    score = Score.query.get_or_404(id)
    title = '{} {}⭐: {} [{}]'.format(
        score.chart.mode,
        score.chart.display_difficulty(),
        score.chart.display_name(prefer_romanzied=True),
        score.chart.difficulty_name,
    )
    description = '\n'.join(filter(lambda x: x, [
        'Original title: {}'.format(score.chart.name) if score.chart.name != None and score.chart.name != score.chart.name_romanized else None,
        'Artist: {}'.format(score.chart.display_artist()),
        'Mapset by: {}\n'.format(score.chart.creator_name),
        'Played by {}\non {} UTC\n'.format(score.player.username, score.display_time()),
        'Accuracy: {} ({})'.format(score.display_accuracy(), score.display_rank()),
        'Judges: {}'.format(score.display_judges()),
        ' | '.join(['+{}'.format(mod['acronym']) for mod in score.get_mods()]) or None,
        ' | '.join(score.flairs) or None,
    ]))
    meta = {
        'title': title,
        'description': description,
    }
    return chart(score.chart.id, highlight=score, meta_bypass=meta)


@app.route('/players')
def players():
    players = Player.query.order_by(Player.osmos.desc())
    return render_template(
        'players.html',
        title='Players list',
        **build_pager('players', players, per_page=50)
    )


@app.route('/charts')
def charts():
    rankeds = Chart.query.filter(Chart.ranked == True).order_by(
        Chart.ssr.desc(),
        Chart.name_romanized.asc(),
        Chart.difficulty_name.asc(),
    )
    return render_template(
        'charts.html',
        title='Ranked charts',
        **build_pager('charts', rankeds, per_page=50)
    )


@app.route('/charts/<id>')
def chart(id, highlight=None, meta_bypass=None):
    chart = Chart.query.get_or_404(id)
    scores_query = get_scores_query(chart, only_best=True)
    scores = (scores_query
        .order_by(Score.accuracy.desc())
    )
    meta = {}
    if meta_bypass:
        meta = meta_bypass
    if meta.get('description') is None:
        meta['description'] = '\n'.join(filter(lambda x: x, [
            'Mode: {}'.format(chart.mode),
            'AR: {0.ar}  CS: {0.cs}  HP: {0.hp}  OD: {0.od}'.format(chart),
            'Creator: {}'.format(chart.creator_name),
        ]))
    if meta.get('title') is None:
        meta['title'] = chart.display_short() + ' {}⭐'.format(chart.display_difficulty())
    if meta.get('image') is None:
        meta['image'] = chart.get_osu_thumbnail_url()
    return render_template(
        'chart.html',
        title=meta['title'],
        chart=chart,
        meta=meta,
        score=highlight,
        **build_pager('chart', scores, per_page=50, id=id)
    )


@app.route('/players/<id>')
def player(id):
    player = Player.query.get_or_404(id)
    top = Score.query.filter(Score.player == player, Score.osmos > 0).order_by(Score.osmos.desc()).limit(20)
    scores = Score.query.filter_by(player=player).order_by(Score.achieved_at.desc())
    return render_template(
        'player.html',
        player=player,
        top=top,
        **build_pager('player', scores, per_page=20, id=id)
    )
