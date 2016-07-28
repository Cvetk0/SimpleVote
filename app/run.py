import random
from flask import Flask, request, render_template
import voteredis as vr


app = Flask(__name__)

POLL = 'animals'
POLL_OPTIONS = {'dog', 'cat', 'lion', 'goat', 'chupacabra', 'colibry', 'shark', 'buffalo', 'otter', 'eagle', 'giraffe',
                'rabbit', 'mouse', 'squid'}


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
    pv = None
    pv_num = 0

    if request.method == 'POST':
        vote = request.form['vote_option'].lower()
        vr.cast_vote(POLL, vote)
        pv = vote
        pv_num = vr.get_votes(POLL, vote)

    return render_template('index.html', vote_opts=get_vote_options(POLL_OPTIONS), previous_vote=pv,
                           previous_vote_num=pv_num)


if __name__ == '__main__':
    vr.vote_init(POLL, POLL_OPTIONS)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
