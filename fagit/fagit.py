import sys
import os
import configparser
import subprocess

HOME = os.environ["HOME"]
conf_file_path = (os.path.abspath(os.path.dirname(__file__)
                                 )) + '/conf/conf.ini'

print(conf_file_path)

c = configparser.ConfigParser()
c.read(conf_file_path)
configuration=c["DEFAULT"]

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
    return _cbtr(stdout), _cbtr(stderr), p.returncode

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
    def __assert_git(verbose=False):
        out, err, exit = _subprocess_call_with_communicate('git --version')
        if exit:
            raise GitCliMissing(err)
        if verbose:
            print('[ OK ] ... Git checked')

    @staticmethod
    def __git_clone(url, at_dir=None, verbose=False):
        cmd = "git clone {0}".format(url)
        if at_dir:
            cmd += " {0}".format(at_dir)
        if verbose:
            print('[ OK ] ... Cloning {0} into {1}'.format(url, at_dir))
        out, err, exit= _subprocess_call_with_communicate(cmd)
        if exit:
            raise CloneError(err)

    @staticmethod
    def __configure(verbose=False, **kwargs):
        for k in list(kwargs.keys()):
            if not k in ['source', 'dir', 'user', 'password']:
                raise UnknownConfiguration("Conf : {0}".format(k))
        import configparser
        conf = configparser.ConfigParser()
        conf['DEFAULT'] = kwargs
        f = open(conf_file_path, 'w')
        conf.write(f)
        f.close()

    def __init__(self):
        self.user = None
        self.password = None
        self.default_directory = None
        self.default_source = None

    def _collect(self, verbose=False):
        mode = configuration['collectmode']
        if mode == "conf":
            self.user = configuration["user"]
            self.password = configuration ["password"]
            if verbose:
                print('[ OK ] ... collected ids from configuration file')
        elif mode == "env":
            self.user = os.environ['GITHUB_ID']
            self.password = os.environ['GITHUB_PASSWORD']
            if verbose:
                print('[ OK ] ... collected ids from envirenement')
        self.default_directory = configuration['dir']
        self.default_source = configuration['source']


    def get_project(self, project, source=None,
                    private=False, directory=None, verbose=False):
        if not source:
            source = self.default_source
        if not directory:
            directory = self.default_directory
        if private:
            url = "https://{0}:{1}@github.com/{2}/{3}.git".format(
                self.user, self.password, source, project
            )
        else:
            url = "https://github.com/{0}/{1}.git".format(source, project)
        self.__assert_git(verbose=verbose)
        self.__git_clone(url, at_dir=directory, verbose=verbose)
        if verbose:
            print("[ OK ] ... Cloned successfully {0} at {1}".format(project,
                                                                     directory))

    def build_project(self):
        """
        Not Implemented
        """
        pass

    @classmethod
    def clone(cls, *args, verbose=False, **kwargs):
        obj = object.__new__(cls)
        obj.__init__()
        obj._collect(verbose=verbose)
        obj.get_project(*args, **kwargs, verbose=verbose)

    @classmethod
    def configure(cls, **kwargs):
        """
        Not Implemented
        """
        pass

    @classmethod
    def build(cls, *args, **kwargs):
        """
        Not Impelemnted
        """
        pass
