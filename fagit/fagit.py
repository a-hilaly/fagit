import os
import configparser
import subprocess

HOME = os.environ["HOME"]
conf_file_path = ''.join(
    os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]
)

configuration = configparser.ConfigParser().read(conf_file_path)

##@@ SUBPROCESS UTILS

cbts = lambda x : x.decode('utf-8')

def _cbtr(ln):
    r = []
    for i in ln.split(b'\n'):
        if i:
            r += [cbts(i)]
    return r

def _subprocess_call_with_communicate(cmd):
    c = cmd.split(' ')
    p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return _cbtr(stdout), _cbtr(stderr)

##@@

##@@ EXCEPTIONS

class GitCliMissing(Exception):
    pass

class GitHubLogsMissing(Exception):
    pass

class CloneError(Exception):
    pass

class UnknownConfiguration(Exception):
    pass


class FaGit(object):

    @staticmethod
    def __assert_git():
        out, err = _subprocess_call_with_communicate('git --version')
        if err:
            raise GitCliMissing(err)
        print('[ OK ] ... Git checked')
        return True

    @staticmethod
    def __git_clone(url, at_dir=None):
        cmd = "git clone {0}".format(url)
        if at_dir:
            cmd += " {0}".format(at_dir)
        out, err = _subprocess_call_with_communicate(cmd)
        if err:
            raise CloneError(err)
        else:
            print('[ OK ] ... Git clone finished successfully ')

    @staticmethod
    def __reconfigure(**kwargs):
        for k in list(kwargs.keys()):
            if not k in ['source', 'dir', 'user', 'password']:
                raise UnknownConfiguration("Conf : {0}".format(k))
        import configparser
        conf = configparser.ConfigParser()
        conf['DEFAULT'] = kwargs
        f = open(conf_file_path, 'w')
        f.write(conf)
        f.close()

    def __init__(self):
        self.user = None
        self.password = None

    def collect(self):
        mode = configuration['source']
        if mode == "conf":
            self.collect_from_conf()
        elif mode == "env":
            self.collect_from_env()

    def collect_from_env(self):
        self.user = os.environ['GITHUB_ID']
        self.password = os.environ['GITHUB_PASSWORD']

    def collect_from_conf(self):
        self.user, self.password = list(configuration['github.logs'].values())

    def get_project(self, project, source, private=False, directory=None):
        if private:
            url = "https://{0}:{1}@github.com/{2}/{3}.git".format(
                self.user, self.password, project, source
            )
        else:
            url = "https://github.com/{0}/{1}.git".format(project, source)
        self.__git_clone(url, at_dir=directory)

    @classmethod
    def clone(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.__init__()
        obj.collect()
        obj.get_project(*args, **kwargs)
