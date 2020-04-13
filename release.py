from tomlkit.toml_file import TOMLFile
from git import Repo
import sys
from datetime import datetime

class PyProject:

    def __init__(self):
        self._file = TOMLFile('pyproject.toml')

    def get_version(self):
        pyproject_data = self._file.read()
        version = pyproject_data['tool']['poetry']['version']
        return version
        
    def set_version(self, version):
        pyproject_data = self._file.read()
        pyproject_data['tool']['poetry']['version'] = version
        self._file.write(pyproject_data)

class Spec:

    def __init__(self):
        self._file_path = 'ambrasdk.spec'

    def get_version(self):
        version = None
        release = None
        with open(self._file_path, 'r') as _file:
            for line in _file:
                if line.startswith('%define version'):
                    version = line.split()[-1].strip()
                if line.startswith('Release'):
                    release = line.split()[-1].strip()
        return version, release
                  
    def set_version(self, version, release):
        lines = []
        with open(self._file_path, 'r') as _file:
            for line in _file:
                if line.startswith('%define version'):
                    lines.append(
                        '%define version {version}\n'.format(version=version)
                    )
                elif line.startswith('Release'):
                    lines.append(
                        'Release: {release}\n'.format(release=release)
                    )
                else:
                    lines.append(line)

        with open(self._file_path, 'w') as _file:
            _file.writelines(lines)

class Init:

    def __init__(self):
        self._file_path = 'ambra_sdk/__init__.py'

    def get_version(self):
        version = None
        with open(self._file_path, 'r') as _file:
            for line in _file:
                if line.startswith('__version__'):
                    version = line.split("'")[-2].strip()
        return version
                  
    def set_version(self, version):
        lines = []
        with open(self._file_path, 'r') as _file:
            for line in _file:
                if line.startswith('__version__'):
                    lines.append(
                        "__version__ = '{version}'\n".format(version=version)
                    )
                else:
                    lines.append(line)

        with open(self._file_path, 'w') as _file:
            _file.writelines(lines)

def set_new_version(version, postfix, human_version):
    """Set new vesrion in files."""
    spec = Spec()
    spec.set_version(version, postfix)
    Init().set_version(human_version)
    PyProject().set_version(human_version)


def bump_release_candidate():
    """Bump release candidate.

    Run in main. 
    Change release candidate version in all files
    and git tag this release.
    """
    spec = Spec()
    ver, rel = spec.get_version()

    # Rel or rc1, rc2 or 1,2,3 (post version)
    if 'rc' in rel:
        candidate_version = int(rel[2:])
        new_candidate_version = candidate_version + 1
    else:
        rel_int = int(rel)
        if rel_int != 1:
            raise RuntimeError('You try set release candidate to post version')
        new_candidate_version = 1

    human_version = '{version}-rc.{candidate_version}'.format(
        version=ver,
        candidate_version=new_candidate_version,
    )

    set_new_version(
        ver,
        human_version,
        'rc{candidate_version}'.format(
            candidate_version=new_candidate_version,
        ),
    )

    print('New vesion:', human_version)
    repo = Repo()
    repo.git.add(u=True)
    repo.index.commit('Bump release candidate version to {version}'.format(version=human_version))
    repo.git.push()
    new_tag = repo.create_tag(human_version, message='Release candidate {version}'.format(version=human_version))
    repo.remotes.origin.push(new_tag)
    print('Git pushed with tags')

def start_release():
    """Start release.
    
    (BumpVersion analog)

    Run in main. 
    Set current release to new version in main
    Create new branch with current release name.
    Set current version (withour rc perfix)
    to all files in this new branch.
    """
    args = sys.argv
    if len(args) != 2:
        raise RuntimeError('Use start_release <new release version>')
    new_version = args[1]
    human_new_version = new_version

    msg = 'Set new version in main {version}'.format(version=human_new_version)
    print(msg)
    spec = Spec()
    current_ver, rel = spec.get_version()
    human_current_version = current_ver

    if current_ver == new_version:
        raise RuntimeError('You try to create current release')

    set_new_version(new_version, '1', human_new_version)

    repo = Repo()
    repo.git.add(u=True)
    repo.index.commit(msg)
    repo.git.push()

    date_prefix = datetime.now().strftime('%Y%m%d')
    release_branch_name = '{version}_{date_str}_PROD'.format(
        version=current_ver.replace('.', '_'),
        date_str=date_prefix,
    )
    repo.git.checkout('-b', release_branch_name)

    set_new_version(current_version, '1', human_current_version)

    repo.git.add(u=True)
    repo.index.commit(msg)
    repo.git.push('--set-upstream', 'origin', release_branch_name)
    print('New branch {branch_name} created'.format(branch_name=release_branch_name))


def bump_release():
    """Bump release.
    
    (BumpRelease analog)

    Run in release branch. 
    Set tag for current version
    Increment release version.
    """
    spec = Spec()
    current_ver, rel = spec.get_version()
    rel = int(rel)

    human_version = '{version}-{release}'.format(
        version=current_ver,
        release=rel,
    )

    repo = Repo()
    new_tag = repo.create_tag(
        human_version,
        message='Release {human_version}'.format(human_version=human_version),
    )

    repo.remotes.origin.push(new_tag)
    print('Push new tag to git:', new_tag)

    new_rel = rel + 1
    new_human_version = '{version}-{release}'.format(
        version=current_ver,
        release=new_rel,
    )

    set_new_version(current_ver, new_rel, new_human_version)

    msg ='Bumped release from {human_version} to {new_human_version}'.format(
        human_version=human_version,
        new_human_version=new_human_version,
    ) 
    repo.git.add(u=True)
    repo.index.commit(msg)
    repo.git.push()
    print(msg)
