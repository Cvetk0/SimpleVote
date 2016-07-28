import redis
import os

R_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
R_PORT = os.getenv('REDIS_PORT', 6379)
R_DB_NUM = os.getenv('REDIS_DB', 0)
R_FLUSH_DB = os.getenv('REDIS_FLUSH', False)


def get_redis():
    r = redis.StrictRedis(host=R_HOST, port=R_PORT, db=R_DB_NUM)
    return r


def flush_redis_db():
    r = get_redis()

    r.flushdb()


def vote_init(poll_name, poll_options):
    r = get_redis()

    if R_FLUSH_DB:
        flush_redis_db()
    
    polls = r.smembers('vote:polls')

    if poll_name not in polls:
        print "Poll " + poll_name + " does not exist yet, adding it to vote:polls"
        r.sadd('vote:polls', poll_name)
        for option in poll_options:
            print "Adding poll option " + option + " to vote:" + poll_name + ":options"
            r.sadd('vote:' + poll_name + ':options', option)
            print "Setting value of vote:" + poll_name + ":option:" + option + " to 0"
            r.set('vote:' + poll_name + ':option:' + option, 0)
    else:
        opts = r.smembers('vote:' + poll_name + ':options')
        for option in poll_options:
            if option not in opts:
                print "Adding poll option " + option + " to vote:" + poll_name + ":options"
                r.sadd('vote:' + poll_name + ':options', option)
                print "Setting value of vote:" + poll_name + ":option:" + option + " to 0"
                r.set('vote:' + poll_name + ':option:' + option, 0)


def cast_vote(poll_name, poll_option):
    r = get_redis()

    print "Incrementing value of vote:" + poll_name + ":option:" + poll_option + " by 1"
    r.incr('vote:' + poll_name + ':option:' + poll_option)

def set_last_vote(poll_name, poll_option):
    r = get_redis()

    print "Setting value of vote:" + poll_name + ':lastvote to ' + poll_option
    r.set('vote:' + poll_name + ':lastvote', poll_option)


def get_polls():
    r = get_redis()

    return r.smembers('vote:polls')


def get_poll_options(poll_name):
    r = get_redis()

    return r.smembers('vote:' + poll_name + ':options')


def get_votes(poll_name, poll_option):
    r = get_redis()

    return r.get('vote:' + poll_name + ':option:' + poll_option)


if __name__ == '__main__':
    animals = {'mouse', 'lion', 'elephant', 'snake'}
    vote_init('animals', animals)

    cast_vote('animals', 'mouse')

    print "All polls:", get_polls()
    print "Poll options for animals:", get_poll_options('animals')
    print "Votes for mouse:", get_votes('animals', 'mouse')
