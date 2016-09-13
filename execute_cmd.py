import salt.client
import salt.config

opts = salt.config.client_config('/etc/salt/master')
client = salt.client.get_local_client(opts.get('conf_file'))

array = ['1.1.1.1']
for fun_ret in client.cmd_cli(array, 'saltutil.running', expr_form='list', verbose=True):
    print fun_ret
