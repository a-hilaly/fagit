import os
import configparser
import subprocess

HOME = os.environ["HOME"]
conf_file_path = ''.join(
    os.path.abspath(os.path.dirname(__file__)).split('/')[:-1]
)
COLLECT_MODE = "conf"


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

##@@ EXPECTED ERROR

class GitCliMissing(Exception):
    pass

class GitHubLogsMissing(Exception):
    pass

class CloneError(Exception):
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

    def __init__(self):
        self.user = None
        self.password = None

    def collect(self):
        if COLLECT_MODE == "conf":
            self.collect_from_conf()
        else:
            self.collect_from_env()

    def collect_from_env(self):
        self.user = os.environ['GITHUB_ID']
        self.password = os.environ['GITHUB_PASSWORD']

    def collect_from_conf(self):
        c = configparser.ConfigParser()
        c.read(conf_file_path)
        self.user, self.password = list(c['github.logs'].values())

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
