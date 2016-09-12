import os
import sys
import salt.payload
import salt.config
opts = salt.config.client_config('/etc/salt/master')
cachedir = opts.get('cachedir', '/var/cache/salt/master')
serial = salt.payload.Serial(opts)

search_jid = sys.argv[1] # '20160708102108506802'
search_minion = sys.argv[2] #None #'10.104.107.36'

def read_return(minion, jobs_path, final, job):
    minion_path = os.path.join(jobs_path, final + '/' + minion, 'return.p')
    if not os.path.isfile(minion_path):
        return
    # print minion_path
    return_str = serial.load(salt.utils.fopen(minion_path, 'rb'))
    if (search_jid is not 'None' and job['jid'] == search_jid) or (search_minion is not 'None' and minion == search_minion):
        print('\033[1;32;40mJOB PATH: \033[0m')
        print minion_path
        print('\033[1;32;40mJOB INFO: \033[0m')
        if isinstance(job, dict):
            print_dict(job)
        else:
            print job
        print('\033[1;32;40mJOB RETURN INFO: \033[0m')
        if isinstance(return_str, dict):
            print_dict(return_str)
        else:
            print return_str


def print_dict(o, space=''):
    assert isinstance(o, dict)
    for key, value in o.iteritems():
        if isinstance(value, dict):
            print '%s%s: ' % (space, key)
            print_dict(value, space=space + '  ')
        elif isinstance(value, list):
            print '%s%s: ' % (space, key)
            print_list(value, space=space + '  - ')
        else:
            print '%s%s: %s' % (space, key, value)


def print_list(o, space=''):
    assert isinstance(o, list)
    for v in o:
        print '%s%s' % (space, v)

if __name__ == '__main__':
    for top in os.listdir(cachedir + '/jobs'):
        jobs_path = os.path.join(cachedir + '/jobs', top)
        for final in os.listdir(jobs_path):
            load_path = os.path.join(jobs_path, final, '.load.p')
            jid_path = os.path.join(jobs_path, final, 'jid')

            if not os.path.isfile(load_path):
                continue
            if not os.path.isfile(jid_path):
                continue
            jid = open(jid_path).read()
            if search_jid is not 'None' and jid == search_jid:
                print("This is Jid: %s and the path is %s" % (jid, jid_path))
            job = serial.load(salt.utils.fopen(load_path, 'rb'))
            if job['fun'] == 'saltutil.find_job':
                break
            # print job
            # print load_path
            # 在syndic中读取
            if job.__contains__('tgt'):
                if isinstance(job['tgt'],list):
                    for minion in job['tgt']:
                        read_return(minion, jobs_path, final, job)
                else:
                    read_return(job['tgt'], jobs_path, final, job)
            # 在master中读取的时候，大部分会跑到这里执行
            if job.__contains__('Minions'):
                for minion in job['Minions']:
                    read_return(minion, jobs_path, final, job)
