import random
from flask import Flask, request, render_template
import voteredis as vr
import os
import json


app = Flask(__name__)

POLL = os.getenv('POLL_NAME', 'animals')
if os.getenv('POLL_OPTS'):
    POLL_OPTIONS = os.getenv('POLL_OPTS').split(',')
else:
    POLL_OPTIONS = {'dog', 'cat', 'lion', 'goat', 'chupacabra', 'colibry', 'shark', 'buffalo', 'otter', 'eagle',
                    'giraffe', 'rabbit', 'mouse', 'squid'}

HOSTNAME = os.getenv('HOSTNAME', 'Unknown')


def get_random_set_item(options_set):
    return random.choice(tuple(options_set))


def get_vote_options(options_set):
    opts_set = set(options_set)
    opt_a = get_random_set_item(opts_set)
    opts_set.remove(opt_a)
    opt_b = get_random_set_item(opts_set)

    options = {'A': opt_a,
               'B': opt_b}

    return options


def get_redis():
    pass


@app.route("/", methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote_for = request.form['vote_option'].lower()
        vr.cast_vote(POLL, vote_for)

    pv = vr.last_vote(POLL)
    pv_num = 0

    if pv:
        pv_num = vr.get_votes(POLL, pv)

    poll_opts = sorted(vr.get_poll_options(POLL))

    poll_values = [vr.get_votes(POLL, option) for option in poll_opts]

    print poll_opts, poll_values

    return render_template('index.html', hostname=HOSTNAME, poll_name=POLL, vote_opts=get_vote_options(POLL_OPTIONS),
                           previous_vote=pv, previous_vote_num=pv_num,
                           poll_opts=json.dumps(poll_opts),
                           poll_values=json.dumps(poll_values))

@app.route("/flushdb", methods=['GET'])
def flush():
    vr.flush_redis_db()

    return "Flushed redis DB"


if __name__ == '__main__':
    vr.vote_init(POLL, POLL_OPTIONS)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
