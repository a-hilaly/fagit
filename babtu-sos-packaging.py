import os
import argparse

DEFAULT = "{0}/Desktop".format(os.environ['HOME'])

try:
    PRIVATE_OPT = True
    IALSOURCE = "github"
    _GIT_USER = os.environ['_GITHUB_USER_ID']
    _GIT_PW = os.environ['_GITHUB_PASS_WORD']
    _ORGANISATION = os.environ['_GITHUB_ORG']
except:
    PRIVATE_OPT = False
    _ORGANISATION = "iallabs"

class GitHubLogsMissing(Exception):
    pass

class WrongConfiguration(Exception):
    pass

def _make_url_from(organisation=None, repo=None, private=False):
    if not(PRIVATE_OPT) and private:
        msg = "You need to set GITHUB Logs at bash env"
        raise GitHubLogsMissing(msg)
    url_with_logs = "https://{0}:{1}@github.com/{2}/{3}"
    simple_url = "https://github.com/{0}/{1}"
    if private:
        return url_with_logs.format(_GIT_USER, _GIT_PW, organisation, repo)
    return simple_url.format(organisation, repo)

def __git_version():
    return os.system('git version')

def clone_package(repo, organisation=_ORGANISATION, private=False, directory=DEFAULT, verbose=False):
    cmd = "cd {0} && git clone {1}".format(directory, _make_url_from(organisation=organisation,
                                                                     repo=repo,
                                                                     private=private))
    x = os.system(cmd)
    if verbose:
        print('[ I ] ... Clone command completed with exit status {0}'.format(x))
    return x

def build_package(repo, build_option=None, directory=DEFAULT, verbose=False):
    repo_dir = "{0}/{1}".format(directory, repo)
    build = "{0}/build.sh".format(repo_dir)
    os.chdir(repo_dir)
    if build_option:
        cmd = "bash {0} --build --{1}".format(build, build_option)
    else:
        cmd = "bash {0} --build".format(build)
    x = os.system(cmd)
    if verbose:
        print('[ I ] ... Build command completed with exit status {0}'.format(x))
    return x

def _parse_cfg_file(directory, f):
    import configparser
    os.chdir(directory)
    config = configparser.ConfigParser()
    config.read(f)
    return config._sections

def __make_babtu_cfg(directory, target_dir=DEFAULT, verbose=False):
    data = _parse_cfg_file(directory, 'babtu.cfg')
    assert data['sos-packages']['org'] == _ORGANISATION
    for package in list(data.keys())[1::]:
        build_opt = data[package]['build']
        _private = (data[package]['private'] == 'true')
        if verbose:
            print("[ I ] ... Cloning package {0} from [{0}]".format(package, _ORGANISATION))
        x = clone_package(package,
                          organisation=_ORGANISATION,
                          directory=target_dir,
                          private=_private)
        if verbose:
            print("[ I ] ... Building package {0}".format(package))
        build_package(package,
                      build_option=build_opt,
                      directory=target_dir)




if __name__ == "__main__":

    assert __git_version() == 0
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', type=str, default=DEFAULT)
    parser.add_argument('-o', '--organisation', type=str, default=_ORGANISATION)
    parser.add_argument('-p', '--private', action="store_true", default=False)
    parser.add_argument('-v', '--verbose', action="store_true", default=False)
    parser.add_argument('-c', '--clone', type=str)
    parser.add_argument('-b', '--build', type=str)
    parser.add_argument('-bo', '--build-option', type=str, default='')
    parser.add_argument('-m', '--make', type=str)
    args = parser.parse_args()

    if args.clone:
        clone_package(args.clone,
                      organisation=args.organisation,
                      private=args.private,
                      directory=args.directory,
                      verbose=args.verbose)
    if args.build:
        build_package(args.build,
                      build_option=args.build_option,
                      directory=args.directory)
    if args.make:
        __make_babtu_cfg(args.make,
                         target_dir=args.directory,
                         verbose=args.verbose)
