import json
import pprint
import subprocess

class Config():
    def __init__(self, jsonConfigFile):
        with open(jsonConfigFile) as f:
            __configs = json.load(f) 

        cfg = {}        

        ### Repos

        # name, org_or_user, rel_data_dir
        cfg['vater_repo'] = __configs['repos'][0]['vater_repo']

        # name, org_or_user, terraform_dir, ansible_dir
        cfg['content_repo'] = __configs['repos'][0]['content_repo']

        ### Host variables
 
        # hostname, project_path
        cfg['host'] = __configs['host']

        ps = subprocess.Popen(('hostname', '-I'), stdout=subprocess.PIPE)
        output = subprocess.check_output(('cut', '-d', ' ', '-f1'), stdin=ps.stdout)
        cfg['host']['ip'] = (output.decode('utf-8').strip())

        cfg['host']['content_dir_path'] =                                                   \
            cfg['host']['project_path'] + cfg['content_repo']['name'] + '/'                 

        cfg['host']['content_git_dir_path'] =                                               \
            cfg['host']['content_dir_path'] + '.git/'

        cfg['host']['terraform_path'] =                                                     \
            cfg['host']['content_dir_path'] + cfg['content_repo']['terraform_dir'] + '/'


        ### Development variables

        # enable
        cfg['dev'] = __configs['dev']

        if cfg['dev']['enable'] == True:
            cfg['dev']['ssh_path'] =                                                        \
                cfg['host']['project_path'] + '.ssh/' 

            cfg['dev']['ssh_auth_key_path'] =                                               \
                cfg['dev']['ssh_path'] + 'authorized_keys'

            cfg['dev']['vater_key_path'] =                                                  \
                cfg['dev']['ssh_path'] + cfg['vater_repo']['name']

            cfg['dev']['content_key_path'] =                                                \
                cfg['dev']['ssh_path'] + cfg['content_repo']['name']

        ### Services

        # Gitea

        # config_password, config_user, org_or_user, port
        cfg['gitea'] = __configs['services'][0]['gitea']


        cfg['gitea']['url'] =                                                               \
            'http://' + cfg['host']['ip'] + ':' + cfg['gitea']['port'] + '/'

        cfg['gitea']['api_url'] =                                                           \
            cfg['gitea']['url'] + 'api/v1/'

        cfg['gitea']['gitea_content_repo_path'] =                                           \
            cfg['host']['project_path'] + cfg['vater_repo']['name'] + '/' +                 \
            cfg['vater_repo']['rel_data_dir'] + 'gitea/git/' +                              \
            cfg['content_repo']['name']

        cfg['gitea']['gitea_content_repo_git_dir_path'] =                                   \
            cfg['gitea']['gitea_content_repo_path'] + '/.git/'

        cfg['gitea']['gitea_container_content_repo'] =                                      \
            '/data/git/' + cfg['content_repo']['name']

        cfg['gitea']['gitea_config_repo_url'] =                                             \
            cfg['gitea']['url'] + cfg['gitea']['org_or_user'] + '/' +                       \
            cfg['content_repo']['name']

        # Gitea Database

        # db_password, db_user, port
        cfg['gitea_db'] = __configs['services'][0]['gitea_db']

        # Semaphore

        # password, port, user
        cfg['semaphore'] = __configs['services'][0]['semaphore']

        # Semaphore Database

        # db_password, db_user, port
        cfg['semaphore_db'] = __configs['services'][0]['semaphore_db']

        self.cfg = cfg

    def __str__(self):
        return json.dumps(self.cfg, indent=4)
        
c = Config('../config.json')
print(c)