#!/nix/store/9j34pp0ajq2hzb3hi7zv0l3bpszm4n43-python-2.7.18/bin/python2
# -*- coding: utf-8 -*-

# Software License Agreement (BSD License)
#
# Copyright (c) 2012, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""This file generates shell code for the setup.SHELL scripts to set environment variables."""

from __future__ import print_function

import argparse
import copy
import errno
import os
import platform
import sys

CATKIN_MARKER_FILE = '.catkin'

system = platform.system()
IS_DARWIN = (system == 'Darwin')
IS_WINDOWS = (system == 'Windows')

PATH_TO_ADD_SUFFIX = ['bin']
if IS_WINDOWS:
    # while catkin recommends putting dll's into bin, 3rd party packages often put dll's into lib
    # since Windows finds dll's via the PATH variable, prepend it with path to lib
    PATH_TO_ADD_SUFFIX.extend(['lib'])

# subfolder of workspace prepended to CMAKE_PREFIX_PATH
ENV_VAR_SUBFOLDERS = {
    'CMAKE_PREFIX_PATH': '',
    'LD_LIBRARY_PATH' if not IS_DARWIN else 'DYLD_LIBRARY_PATH': 'lib',
    'PATH': PATH_TO_ADD_SUFFIX,
    'PKG_CONFIG_PATH': os.path.join('lib', 'pkgconfig'),
    'PYTHONPATH': 'lib/python2.7/site-packages',
}


def rollback_env_variables(environ, env_var_subfolders):
    """
    Generate shell code to reset environment variables.

    by unrolling modifications based on all workspaces in CMAKE_PREFIX_PATH.
    This does not cover modifications performed by environment hooks.
    """
    lines = []
    unmodified_environ = copy.copy(environ)
    for key in sorted(env_var_subfolders.keys()):
        subfolders = env_var_subfolders[key]
        if not isinstance(subfolders, list):
            subfolders = [subfolders]
        value = _rollback_env_variable(unmodified_environ, key, subfolders)
        if value is not None:
            environ[key] = value
            lines.append(assignment(key, value))
    if lines:
        lines.insert(0, comment('reset environment variables by unrolling modifications based on all workspaces in CMAKE_PREFIX_PATH'))
    return lines


def _rollback_env_variable(environ, name, subfolders):
    """
    For each catkin workspace in CMAKE_PREFIX_PATH remove the first entry from env[NAME] matching workspace + subfolder.

    :param subfolders: list of str '' or subfoldername that may start with '/'
    :returns: the updated value of the environment variable.
    """
    value = environ[name] if name in environ else ''
    env_paths = [path for path in value.split(os.pathsep) if path]
    value_modified = False
    for subfolder in subfolders:
        if subfolder:
            if subfolder.startswith(os.path.sep) or (os.path.altsep and subfolder.startswith(os.path.altsep)):
                subfolder = subfolder[1:]
            if subfolder.endswith(os.path.sep) or (os.path.altsep and subfolder.endswith(os.path.altsep)):
                subfolder = subfolder[:-1]
        for ws_path in _get_workspaces(environ, include_fuerte=True, include_non_existing=True):
            path_to_find = os.path.join(ws_path, subfolder) if subfolder else ws_path
            path_to_remove = None
            for env_path in env_paths:
                env_path_clean = env_path[:-1] if env_path and env_path[-1] in [os.path.sep, os.path.altsep] else env_path
                if env_path_clean == path_to_find:
                    path_to_remove = env_path
                    break
            if path_to_remove:
                env_paths.remove(path_to_remove)
                value_modified = True
    new_value = os.pathsep.join(env_paths)
    return new_value if value_modified else None


def _get_workspaces(environ, include_fuerte=False, include_non_existing=False):
    """
    Based on CMAKE_PREFIX_PATH return all catkin workspaces.

    :param include_fuerte: The flag if paths starting with '/opt/ros/fuerte' should be considered workspaces, ``bool``
    """
    # get all cmake prefix paths
    env_name = 'CMAKE_PREFIX_PATH'
    value = environ[env_name] if env_name in environ else ''
    paths = [path for path in value.split(os.pathsep) if path]
    # remove non-workspace paths
    workspaces = [path for path in paths if os.path.isfile(os.path.join(path, CATKIN_MARKER_FILE)) or (include_fuerte and path.startswith('/opt/ros/fuerte')) or (include_non_existing and not os.path.exists(path))]
    return workspaces


def prepend_env_variables(environ, env_var_subfolders, workspaces):
    """Generate shell code to prepend environment variables for the all workspaces."""
    lines = []
    lines.append(comment('prepend folders of workspaces to environment variables'))

    paths = [path for path in workspaces.split(os.pathsep) if path]

    prefix = _prefix_env_variable(environ, 'CMAKE_PREFIX_PATH', paths, '')
    lines.append(prepend(environ, 'CMAKE_PREFIX_PATH', prefix))

    for key in sorted(key for key in env_var_subfolders.keys() if key != 'CMAKE_PREFIX_PATH'):
        subfolder = env_var_subfolders[key]
        prefix = _prefix_env_variable(environ, key, paths, subfolder)
        lines.append(prepend(environ, key, prefix))
    return lines


def _prefix_env_variable(environ, name, paths, subfolders):
    """
    Return the prefix to prepend to the environment variable NAME.

    Adding any path in NEW_PATHS_STR without creating duplicate or empty items.
    """
    value = environ[name] if name in environ else ''
    environ_paths = [path for path in value.split(os.pathsep) if path]
    checked_paths = []
    for path in paths:
        if not isinstance(subfolders, list):
            subfolders = [subfolders]
        for subfolder in subfolders:
            path_tmp = path
            if subfolder:
                path_tmp = os.path.join(path_tmp, subfolder)
            # skip nonexistent paths
            if not os.path.exists(path_tmp):
                continue
            # exclude any path already in env and any path we already added
            if path_tmp not in environ_paths and path_tmp not in checked_paths:
                checked_paths.append(path_tmp)
    prefix_str = os.pathsep.join(checked_paths)
    if prefix_str != '' and environ_paths:
        prefix_str += os.pathsep
    return prefix_str


def assignment(key, value):
    if not IS_WINDOWS:
        return 'export %s="%s"' % (key, value)
    else:
        return 'set %s=%s' % (key, value)


def comment(msg):
    if not IS_WINDOWS:
        return '# %s' % msg
    else:
        return 'REM %s' % msg


def prepend(environ, key, prefix):
    if key not in environ or not environ[key]:
        return assignment(key, prefix)
    if not IS_WINDOWS:
        return 'export %s="%s$%s"' % (key, prefix, key)
    else:
        return 'set %s=%s%%%s%%' % (key, prefix, key)


def find_env_hooks(environ, cmake_prefix_path):
    """Generate shell code with found environment hooks for the all workspaces."""
    lines = []
    lines.append(comment('found environment hooks in workspaces'))

    generic_env_hooks = []
    generic_env_hooks_workspace = []
    specific_env_hooks = []
    specific_env_hooks_workspace = []
    generic_env_hooks_by_filename = {}
    specific_env_hooks_by_filename = {}
    generic_env_hook_ext = 'bat' if IS_WINDOWS else 'sh'
    specific_env_hook_ext = environ['CATKIN_SHELL'] if not IS_WINDOWS and 'CATKIN_SHELL' in environ and environ['CATKIN_SHELL'] else None
    # remove non-workspace paths
    workspaces = [path for path in cmake_prefix_path.split(os.pathsep) if path and os.path.isfile(os.path.join(path, CATKIN_MARKER_FILE))]
    for workspace in reversed(workspaces):
        env_hook_dir = os.path.join(workspace, 'etc', 'catkin', 'profile.d')
        if os.path.isdir(env_hook_dir):
            for filename in sorted(os.listdir(env_hook_dir)):
                if filename.endswith('.%s' % generic_env_hook_ext):
                    # remove previous env hook with same name if present
                    if filename in generic_env_hooks_by_filename:
                        i = generic_env_hooks.index(generic_env_hooks_by_filename[filename])
                        generic_env_hooks.pop(i)
                        generic_env_hooks_workspace.pop(i)
                    # append env hook
                    generic_env_hooks.append(os.path.join(env_hook_dir, filename))
                    generic_env_hooks_workspace.append(workspace)
                    generic_env_hooks_by_filename[filename] = generic_env_hooks[-1]
                elif specific_env_hook_ext is not None and filename.endswith('.%s' % specific_env_hook_ext):
                    # remove previous env hook with same name if present
                    if filename in specific_env_hooks_by_filename:
                        i = specific_env_hooks.index(specific_env_hooks_by_filename[filename])
                        specific_env_hooks.pop(i)
                        specific_env_hooks_workspace.pop(i)
                    # append env hook
                    specific_env_hooks.append(os.path.join(env_hook_dir, filename))
                    specific_env_hooks_workspace.append(workspace)
                    specific_env_hooks_by_filename[filename] = specific_env_hooks[-1]
    env_hooks = generic_env_hooks + specific_env_hooks
    env_hooks_workspace = generic_env_hooks_workspace + specific_env_hooks_workspace
    count = len(env_hooks)
    lines.append(assignment('_CATKIN_ENVIRONMENT_HOOKS_COUNT', count))
    for i in range(count):
        lines.append(assignment('_CATKIN_ENVIRONMENT_HOOKS_%d' % i, env_hooks[i]))
        lines.append(assignment('_CATKIN_ENVIRONMENT_HOOKS_%d_WORKSPACE' % i, env_hooks_workspace[i]))
    return lines


def _parse_arguments(args=None):
    parser = argparse.ArgumentParser(description='Generates code blocks for the setup.SHELL script.')
    parser.add_argument('--extend', action='store_true', help='Skip unsetting previous environment variables to extend context')
    parser.add_argument('--local', action='store_true', help='Only consider this prefix path and ignore other prefix path in the environment')
    return parser.parse_known_args(args=args)[0]


if __name__ == '__main__':
    try:
        try:
            args = _parse_arguments()
        except Exception as e:
            print(e, file=sys.stderr)
            sys.exit(1)

        if not args.local:
            # environment at generation time
            CMAKE_PREFIX_PATH = r'/nix/store/p2np8nj9zs5dj23pxljlbv98256lb2v4-ros-env;/nix/store/jaym4sm5xfvwmzvw4hh4ywmdkrdyknmy-ignition-cmake-0.6.1;/nix/store/hni56pcvwa0w1d90srw4nllfnh6jmpa7-pkg-config-wrapper-0.29.2;/nix/store/cfvww6slpwnvz19hf169ickmjda4l6jb-patchelf-0.12;/nix/store/d2fqghv083a8q7j8sjb2m5q6i840h691-gcc-wrapper-10.2.0;/nix/store/fws5qmgl882n7zva366sw207b4rmgcyz-binutils-wrapper-2.34;/nix/store/sm6gls0p6m1ch4xqkw0ynl06v4hwfn45-glibc-locales-2.32-24;/nix/store/p2np8nj9zs5dj23pxljlbv98256lb2v4-ros-env;/nix/store/k3275xhkfygkksdf2ckvpml5q9bsh5zl-gazebo-9.16.0;/nix/store/9hsqv22xh4dp8548r40l9psirgfss9ai-freeimage-3.18.0;/nix/store/bi5lrjmrjdhw895nc8s7q9dvjgyhi7r1-boost-1.69.0-dev;/nix/store/b4xzx0x2z8wgl1d40kqfh6g0q3wbl2hg-boost-1.69.0;/nix/store/yxixzi4cmp5swd1zjyg77fpda1i6zsnf-protobuf-3.14.0;/nix/store/nhvcdx4syw4j8nvv0qjl9in2nlasy8r9-sdformat-6.2.0;/nix/store/llikrh3gzh2l84jna63vxsi8b0g259ks-ignition-math4-4.0.0;/nix/store/gbnibsb6nfy9lf426r4mgp20j7swnb6n-tinyxml-2.6.2;/nix/store/r6h1kh1ag7vvfp9y9scfb1gzxn7n8x8y-tbb-2019_U9;/nix/store/vafx0nj60997dka2706chv78wcyna16h-ogre-1.10.11;/nix/store/ppycj2c73iqrsvqcy1skpd9c0nqq0klg-ffmpeg-4.3.1-dev;/nix/store/qp9bb3bnbq0ql14j16yxxf9amvgyzb74-ffmpeg-4.3.1-bin;/nix/store/ydiq4zlqy4hq53gw9xjbnfadkgw75spc-ffmpeg-4.3.1;/nix/store/ihb53mi778g32g3xnq4v51lc5g9mi1ar-ignition-transport4-4.0.0;/nix/store/s15jmvly0yb42g6r85lliagl5564cfxa-cppzmq-4.7.1;/nix/store/jcywr9ybd82nqyhw0l5i1vhdg4b3dl20-zeromq-4.3.3;/nix/store/7dlx054v20lg620wm1s6p7m573kzgx3g-util-linux-2.36.1-dev;/nix/store/qk4awq3xrdz2ih9ch72xj4sns50inhfc-util-linux-2.36.1-bin;/nix/store/35rck1flkmw2l9xhshms6sfs2gi0gmg5-util-linux-2.36.1;/nix/store/qjp1n5zqwwlvd8xj1yhsc4agqazryvl8-ignition-msgs-1.0.0;/nix/store/2jb4c24k9psdwcpb1667n7gyvla0nzgx-ignition-fuel-tools1-1.2.0;/nix/store/z8kkzczmv6h8vn8kb1fbv11drrvd1nxb-ignition-common-1.1.1;/nix/store/kmv05r0mx3jp92n2fw9by3dwk20dng0d-gts-0.7.6-dev;/nix/store/g20ydbxyd1ybz4sw7f1h26952xzw0zxm-glib-2.66.4-dev;/nix/store/zgjx6v2skgvr8yx1b410gdq6s9diwm51-zlib-1.2.11-dev;/nix/store/nnqw9pa10j11r3jjc0fw2rwdipram6gc-zlib-1.2.11;/nix/store/wxb1awkkkbjp26jwqf854488qbzlkk25-libffi-3.3-dev;/nix/store/8b4r4lmhybjxhxx33z0si8gifhi8hfmn-libffi-3.3;/nix/store/kzwhxfzlm3s8h2yr6l315ya5p8gg4ax4-gettext-0.21;/nix/store/0pcd8lk16hmnrb8z5s2g67ajb1rkfmjy-glibc-iconv-2.32-24;/nix/store/80d7kp595vpc2plakmngsy5lk1zkfsb0-glib-2.66.4-bin;/nix/store/ah4gsslwh7sm07vflbqd4brmcjz2xdal-glib-2.66.4;/nix/store/lyj7kcrg58i93yy32x2nbp832fzks96j-gts-0.7.6-bin;/nix/store/qf9mdamzj27ni6w9cvxc8kd16c6dq4yx-gts-0.7.6;/nix/store/9zyiy3xkbgx333lxfrrwgxvjd5dx2y9l-tinyxml-2-6.0.0;/nix/store/dh6qnjpad0fjc63j01j18k58na7dzmjw-curl-7.74.0-dev;/nix/store/cdx4cxnsncg1i20kvd62nrl1w8ddlaq8-nghttp2-1.41.0-dev;/nix/store/0k52xvparksz9b84iqirrsc1v8gqb8iq-nghttp2-1.41.0-bin;/nix/store/547mh201imvskv8wq4hd0i1pdcpjqp9h-nghttp2-1.41.0-lib;/nix/store/pbw2cinmsbswwpqab7bh8xdkx93nqh6r-libkrb5-1.18-dev;/nix/store/r0zkfff12pvp12y7i1kd874fkh4yyg37-libkrb5-1.18;/nix/store/9mwb1rrrlmnlfxv7phfcw7lzph7jyi7r-openssl-1.1.1i-dev;/nix/store/lk7vzcbmgf6918si7nkhl30r6wwqhr3v-openssl-1.1.1i-bin;/nix/store/digsnjxzb85hfxfn78si8gxzscjy4c7r-openssl-1.1.1i;/nix/store/akaz1jq4bywwca11z87vvz42rp9gwla1-libssh2-1.9.0-dev;/nix/store/vi6z2a3cldayn1w7yhv0c0ndw25qlyjb-libssh2-1.9.0;/nix/store/72yb1arjflmhvh3jck8hz9xz00s3rgg1-curl-7.74.0-bin;/nix/store/795yj9pbckifps6dxgshfi4ld904lq6b-curl-7.74.0;/nix/store/dnfwwf3iy32dp14rwixhwpy9j03fgybz-jsoncpp-1.9.4-dev;/nix/store/x2g3xvxaw78xz9x0w1cd5vq3r0yd1fby-jsoncpp-1.9.4;/nix/store/b0psvg6pmkr7s4nn9xbxczgdfrxvjzw5-libyaml-0.2.5;/nix/store/y48hj09gb37yavfnb8mabxgpisrfd559-libzip-1.6.1-dev;/nix/store/y24zqcawn4vm4ki7lramnalcq214448h-libzip-1.6.1;/nix/store/bjkbc8d0m8l0gszr10dbvidcyjlq6m6z-cmake-3.19.2;/nix/store/hg4b2bbm0qlmqdxy5mv6n4408lxh5mbc-catkin-setup-hook;/nix/store/jgamvrpdpdnf90yn41h7l3l7ahlw1gmv-hook;/nix/store/90hhkgcrr71v3hmdyljl7hkfr60mrly2-hook;/nix/store/gi27nd0c0x47ka58hw7r98qllmr3hajj-hook;/nix/store/pacgk453hxff4k9i4ndrq87q9v7i8rlq-gtest-1.10.0-dev;/nix/store/x37fifc1pvd01xzi7rysch5km70b3vcb-gtest-1.10.0;/nix/store/9j34pp0ajq2hzb3hi7zv0l3bpszm4n43-python-2.7.18;/nix/store/xvxaay83vmdc6hdxd4gdxypg27daa2a5-python2.7-catkin_pkg-0.4.23;/nix/store/in9wa2n0rvp6cn1iandfadpd9q7api5l-python2.7-python-dateutil-2.8.1;/nix/store/b9y366ajdspmqpglip9w74b5amc0r9al-python2.7-six-1.15.0;/nix/store/yq9xs2nrjlxnp07cmxndvxg2valfvm3v-python2.7-setuptools_scm-4.1.2;/nix/store/167xl1gyycm29vknmdk2aa3m91d7zgi4-python2.7-docutils-0.16;/nix/store/xrsx2si4sr1gq3d2jpqnvmwbyfn6d0da-python2.7-pyparsing-2.4.7;/nix/store/5i1lbsa3xd632w09484d9pqd774hbmc6-python2.7-empy-3.3.4;/nix/store/x80j97zyfzyrplmznblqdyw74687fqvm-python2.7-nose-1.3.7;/nix/store/y9810b4j7dngkdfcjf5rk42z4rf1rv7g-python2.7-coverage-5.3;/nix/store/98cxsyzh9cn8qhc3j0l1hvl3lzj7g6m3-boost-1.69.0-dev;/nix/store/x6a252964s4aq4a98w7w6pdnyq8a31dv-boost-1.69.0;/nix/store/s7qmpksa8ib7fhy8pvf1rbqwkr7nzbb9-python2.7-rosdep-0.17.1;/nix/store/icz4m00kpi6lcv32ib6lkgyskgx7637b-python2.7-rospkg-1.1.10;/nix/store/isgp8d01g1i85284f7h9wy0gvq4wa9m8-python2.7-PyYAML-5.3.1;/nix/store/qycgm4naw2zi795gbz7p3gdbrcdd58jy-python2.7-rosdistro-0.7.5;/nix/store/3pa0c2xpqz2wwi6fr6iw2vgq5j2xm09m-python2.7-setuptools-44.0.0;/nix/store/s91vnjqbsf2vhbkv87a9hxiiqnnbb7gg-urdfdom-1.0.4;/nix/store/zncvvcf780msvvm4srgs2qvphqsvixyn-urdfdom-headers-1.0.5;/nix/store/vc3ff3smky98rxrflrj7sna2w0kiwarn-console-bridge-1.0.1;/nix/store/n0ivy2s2ij27b1mzszvb450xdpdxap3f-python2.7-numpy-1.16.6;/nix/store/yzqph8p8qp7sb4zxjc285772wvy9fjfg-graphviz-2.42.2;/nix/store/mmfc3yp52ngyrfj3dpgbl9w7vxi73chh-opencv-3.4.8;/nix/store/g0y8yyyhh1z7442maidqnv73j9cw15k4-opencv-3.4.8;/nix/store/gpca75ijm5rbjxr0krhpz5893wnqyyz0-util-linux-2.36.1-dev;/nix/store/0z9yy36np8ya0gfdzynb4kk2gwgvp6sa-util-linux-2.36.1-bin;/nix/store/pcir0csxglvif0f6hclgfxjr80aly6zz-util-linux-2.36.1;/nix/store/8jyfz10479mln95brx5bhzr3b0dwj565-apr-1.7.0-dev;/nix/store/n5386id2g8z1qpc7bjkkhx5gbr2jgb8f-apr-1.7.0;/nix/store/dw2z2q93k8dapd602xg973yqnx00hqk9-log4cxx-0.10.0;/nix/store/gbd2v04mxr08rdy6r67y56f79jjf38qm-python2.7-paramiko-2.7.1;/nix/store/r0735hxkmik8461z34jw3vly378x73ay-python2.7-bcrypt-3.1.7;/nix/store/9hfzbdffd0d0sdv4jxbkvi20pz31h0h8-python2.7-cffi-1.14.4-dev;/nix/store/lz1ydncs8lgrsnfg5xm1hy3fk0z0ynvi-python2.7-pycparser-2.20;/nix/store/yvahqwbczyvpk34lj1q8md9fpwzkax1b-python2.7-cffi-1.14.4;/nix/store/46giwbgj364ywwwf3ps3g8bxvxx8d74g-python2.7-cryptography-3.3.1-dev;/nix/store/b7imqw90hhp7czrdqjr3jypsif17lwih-python2.7-packaging-20.4;/nix/store/ll32hhy7n8xnncfmbj6jk6v3wg0w5ma6-python2.7-ipaddress-1.0.23;/nix/store/0b90b7zi80hqf1i4rqj4rp6c7qhirfja-python2.7-enum34-1.1.10;/nix/store/37y3vx63rqqcp5a9ffc8bqb5rqrc4fsz-python2.7-cryptography-3.3.1;/nix/store/3skmrm8vy2zb1xiwhxyax2dqxsh5hzs5-python2.7-pynacl-1.4.0;/nix/store/f9xg5qfvshcj24i301gmpjyfmibvp8vi-python2.7-pyasn1-0.4.8;/nix/store/hrffhnd21k0vhjrijf4vvyjfqmfn7b1g-python2.7-netifaces-0.10.9;/nix/store/4skfq4jbxcv96nxh3wxwq2k85qjml9ik-libyaml-cpp-0.6.3;/nix/store/jf52mpi7nlh530ay2fm0nrq9bafy5ccv-python2.7-wxPython-3.0.2.0;/nix/store/hwc5p91pdp80mnxzf9m5qb7h1nff13rf-python2.7-defusedxml-0.6.0;/nix/store/lbfzn4zj61lafr1wxki7hqy3ajdg82m6-poco-1.10.1-dev;/nix/store/hgxpbh5589qax4hqvz40vfln8clrk9cl-pcre-8.44-dev;/nix/store/hrl5wmbi9ba5spz67jxgj426n6kvrpfq-pcre-8.44-bin;/nix/store/v3aw5ip513vsh6r36fs07niv0b3f7f8l-pcre-8.44;/nix/store/g41fvyjaas2b5yb2lz8h1gy5pivh20ci-expat-2.2.10-dev;/nix/store/lyfq32jhpbw2ppq7s7m312df0z8sxa7c-expat-2.2.10;/nix/store/jrsffa62cng6wr28y79q72ck54x4wlh7-sqlite-3.34.0-dev;/nix/store/bysxhfhcrs40xzxpzdsp9frrkjxfjiim-sqlite-3.34.0-bin;/nix/store/gk764kygqrz9nzyxqnplns008kcflpii-sqlite-3.34.0;/nix/store/pq1zgy10mswfjh8xbz8kd9pv26m3n6wd-poco-1.10.1;/nix/store/jifkb4yhg2ly26mf7z2jiagrcx5jl7pq-python2.7-pycryptodomex-3.9.9;/nix/store/nwcamwwpwj63f4f7x8l22hahxl4jfi9c-python2.7-python-gnupg-0.4.6;/nix/store/6qq7pzrs6204aifj4hq3xhb6144q5v10-bzip2-1.0.6.0.1-dev;/nix/store/c5jgwpwxc1nxl9gzd9m4wlalrw7sr0z7-bzip2-1.0.6.0.1-bin;/nix/store/7l68hmbqhmxib2wlmwyd5ib5czfyb25g-bzip2-1.0.6.0.1;/nix/store/3fyw7ybrpf4g6cxa96pqjy5mx5pw1rgi-gpgme-1.15.0-dev;/nix/store/b9cxf2hg5hzff31npfammvzpgz8f1dil-libgpg-error-1.38-dev;/nix/store/k4k6k8rydpidjnck44lh0fvkhana2jqj-libgpg-error-1.38;/nix/store/dxb5wrk9wm40rhwglgzdm4jbzdf4bxxf-libassuan-2.5.4-dev;/nix/store/8nma2gl2hgaz50gs25gzayc9w9fyihxs-libassuan-2.5.4;/nix/store/isd2gkz5sls4yxxm1s9r80c09vyn9cv4-pth-2.0.7;/nix/store/7y3b1rkmqwq5dy9inxh32qffkxs4adkb-gpgme-1.15.0;/nix/store/cmxl5f8ay629ghwk8ha54mhlw2fg4d1a-lz4-1.9.3-dev;/nix/store/86rh3v9psg7d9bhl6fqfdnh6kmd7imng-lz4-1.9.3-bin;/nix/store/f8idbr4dlm1h8cl3fgk35lg6m7h07gxc-lz4-1.9.3;/nix/store/jaym4sm5xfvwmzvw4hh4ywmdkrdyknmy-ignition-cmake-0.6.1;/nix/store/hni56pcvwa0w1d90srw4nllfnh6jmpa7-pkg-config-wrapper-0.29.2;/nix/store/cfvww6slpwnvz19hf169ickmjda4l6jb-patchelf-0.12;/nix/store/d2fqghv083a8q7j8sjb2m5q6i840h691-gcc-wrapper-10.2.0;/nix/store/fws5qmgl882n7zva366sw207b4rmgcyz-binutils-wrapper-2.34;/nix/store/sm6gls0p6m1ch4xqkw0ynl06v4hwfn45-glibc-locales-2.32-24;/nix/store/p2np8nj9zs5dj23pxljlbv98256lb2v4-ros-env;/nix/store/k3275xhkfygkksdf2ckvpml5q9bsh5zl-gazebo-9.16.0;/nix/store/9hsqv22xh4dp8548r40l9psirgfss9ai-freeimage-3.18.0;/nix/store/bi5lrjmrjdhw895nc8s7q9dvjgyhi7r1-boost-1.69.0-dev;/nix/store/b4xzx0x2z8wgl1d40kqfh6g0q3wbl2hg-boost-1.69.0;/nix/store/yxixzi4cmp5swd1zjyg77fpda1i6zsnf-protobuf-3.14.0;/nix/store/nhvcdx4syw4j8nvv0qjl9in2nlasy8r9-sdformat-6.2.0;/nix/store/llikrh3gzh2l84jna63vxsi8b0g259ks-ignition-math4-4.0.0;/nix/store/gbnibsb6nfy9lf426r4mgp20j7swnb6n-tinyxml-2.6.2;/nix/store/r6h1kh1ag7vvfp9y9scfb1gzxn7n8x8y-tbb-2019_U9;/nix/store/vafx0nj60997dka2706chv78wcyna16h-ogre-1.10.11;/nix/store/ppycj2c73iqrsvqcy1skpd9c0nqq0klg-ffmpeg-4.3.1-dev;/nix/store/qp9bb3bnbq0ql14j16yxxf9amvgyzb74-ffmpeg-4.3.1-bin;/nix/store/ydiq4zlqy4hq53gw9xjbnfadkgw75spc-ffmpeg-4.3.1;/nix/store/ihb53mi778g32g3xnq4v51lc5g9mi1ar-ignition-transport4-4.0.0;/nix/store/s15jmvly0yb42g6r85lliagl5564cfxa-cppzmq-4.7.1;/nix/store/jcywr9ybd82nqyhw0l5i1vhdg4b3dl20-zeromq-4.3.3;/nix/store/7dlx054v20lg620wm1s6p7m573kzgx3g-util-linux-2.36.1-dev;/nix/store/qk4awq3xrdz2ih9ch72xj4sns50inhfc-util-linux-2.36.1-bin;/nix/store/35rck1flkmw2l9xhshms6sfs2gi0gmg5-util-linux-2.36.1;/nix/store/qjp1n5zqwwlvd8xj1yhsc4agqazryvl8-ignition-msgs-1.0.0;/nix/store/2jb4c24k9psdwcpb1667n7gyvla0nzgx-ignition-fuel-tools1-1.2.0;/nix/store/z8kkzczmv6h8vn8kb1fbv11drrvd1nxb-ignition-common-1.1.1;/nix/store/kmv05r0mx3jp92n2fw9by3dwk20dng0d-gts-0.7.6-dev;/nix/store/g20ydbxyd1ybz4sw7f1h26952xzw0zxm-glib-2.66.4-dev;/nix/store/zgjx6v2skgvr8yx1b410gdq6s9diwm51-zlib-1.2.11-dev;/nix/store/nnqw9pa10j11r3jjc0fw2rwdipram6gc-zlib-1.2.11;/nix/store/wxb1awkkkbjp26jwqf854488qbzlkk25-libffi-3.3-dev;/nix/store/8b4r4lmhybjxhxx33z0si8gifhi8hfmn-libffi-3.3;/nix/store/kzwhxfzlm3s8h2yr6l315ya5p8gg4ax4-gettext-0.21;/nix/store/0pcd8lk16hmnrb8z5s2g67ajb1rkfmjy-glibc-iconv-2.32-24;/nix/store/80d7kp595vpc2plakmngsy5lk1zkfsb0-glib-2.66.4-bin;/nix/store/ah4gsslwh7sm07vflbqd4brmcjz2xdal-glib-2.66.4;/nix/store/lyj7kcrg58i93yy32x2nbp832fzks96j-gts-0.7.6-bin;/nix/store/qf9mdamzj27ni6w9cvxc8kd16c6dq4yx-gts-0.7.6;/nix/store/9zyiy3xkbgx333lxfrrwgxvjd5dx2y9l-tinyxml-2-6.0.0;/nix/store/dh6qnjpad0fjc63j01j18k58na7dzmjw-curl-7.74.0-dev;/nix/store/cdx4cxnsncg1i20kvd62nrl1w8ddlaq8-nghttp2-1.41.0-dev;/nix/store/0k52xvparksz9b84iqirrsc1v8gqb8iq-nghttp2-1.41.0-bin;/nix/store/547mh201imvskv8wq4hd0i1pdcpjqp9h-nghttp2-1.41.0-lib;/nix/store/pbw2cinmsbswwpqab7bh8xdkx93nqh6r-libkrb5-1.18-dev;/nix/store/r0zkfff12pvp12y7i1kd874fkh4yyg37-libkrb5-1.18;/nix/store/9mwb1rrrlmnlfxv7phfcw7lzph7jyi7r-openssl-1.1.1i-dev;/nix/store/lk7vzcbmgf6918si7nkhl30r6wwqhr3v-openssl-1.1.1i-bin;/nix/store/digsnjxzb85hfxfn78si8gxzscjy4c7r-openssl-1.1.1i;/nix/store/akaz1jq4bywwca11z87vvz42rp9gwla1-libssh2-1.9.0-dev;/nix/store/vi6z2a3cldayn1w7yhv0c0ndw25qlyjb-libssh2-1.9.0;/nix/store/72yb1arjflmhvh3jck8hz9xz00s3rgg1-curl-7.74.0-bin;/nix/store/795yj9pbckifps6dxgshfi4ld904lq6b-curl-7.74.0;/nix/store/dnfwwf3iy32dp14rwixhwpy9j03fgybz-jsoncpp-1.9.4-dev;/nix/store/x2g3xvxaw78xz9x0w1cd5vq3r0yd1fby-jsoncpp-1.9.4;/nix/store/b0psvg6pmkr7s4nn9xbxczgdfrxvjzw5-libyaml-0.2.5;/nix/store/y48hj09gb37yavfnb8mabxgpisrfd559-libzip-1.6.1-dev;/nix/store/y24zqcawn4vm4ki7lramnalcq214448h-libzip-1.6.1;/nix/store/bjkbc8d0m8l0gszr10dbvidcyjlq6m6z-cmake-3.19.2;/nix/store/hg4b2bbm0qlmqdxy5mv6n4408lxh5mbc-catkin-setup-hook;/nix/store/jgamvrpdpdnf90yn41h7l3l7ahlw1gmv-hook;/nix/store/90hhkgcrr71v3hmdyljl7hkfr60mrly2-hook;/nix/store/gi27nd0c0x47ka58hw7r98qllmr3hajj-hook;/nix/store/pacgk453hxff4k9i4ndrq87q9v7i8rlq-gtest-1.10.0-dev;/nix/store/x37fifc1pvd01xzi7rysch5km70b3vcb-gtest-1.10.0;/nix/store/9j34pp0ajq2hzb3hi7zv0l3bpszm4n43-python-2.7.18;/nix/store/xvxaay83vmdc6hdxd4gdxypg27daa2a5-python2.7-catkin_pkg-0.4.23;/nix/store/in9wa2n0rvp6cn1iandfadpd9q7api5l-python2.7-python-dateutil-2.8.1;/nix/store/b9y366ajdspmqpglip9w74b5amc0r9al-python2.7-six-1.15.0;/nix/store/yq9xs2nrjlxnp07cmxndvxg2valfvm3v-python2.7-setuptools_scm-4.1.2;/nix/store/167xl1gyycm29vknmdk2aa3m91d7zgi4-python2.7-docutils-0.16;/nix/store/xrsx2si4sr1gq3d2jpqnvmwbyfn6d0da-python2.7-pyparsing-2.4.7;/nix/store/5i1lbsa3xd632w09484d9pqd774hbmc6-python2.7-empy-3.3.4;/nix/store/x80j97zyfzyrplmznblqdyw74687fqvm-python2.7-nose-1.3.7;/nix/store/y9810b4j7dngkdfcjf5rk42z4rf1rv7g-python2.7-coverage-5.3;/nix/store/98cxsyzh9cn8qhc3j0l1hvl3lzj7g6m3-boost-1.69.0-dev;/nix/store/x6a252964s4aq4a98w7w6pdnyq8a31dv-boost-1.69.0;/nix/store/s7qmpksa8ib7fhy8pvf1rbqwkr7nzbb9-python2.7-rosdep-0.17.1;/nix/store/icz4m00kpi6lcv32ib6lkgyskgx7637b-python2.7-rospkg-1.1.10;/nix/store/isgp8d01g1i85284f7h9wy0gvq4wa9m8-python2.7-PyYAML-5.3.1;/nix/store/qycgm4naw2zi795gbz7p3gdbrcdd58jy-python2.7-rosdistro-0.7.5;/nix/store/3pa0c2xpqz2wwi6fr6iw2vgq5j2xm09m-python2.7-setuptools-44.0.0;/nix/store/s91vnjqbsf2vhbkv87a9hxiiqnnbb7gg-urdfdom-1.0.4;/nix/store/zncvvcf780msvvm4srgs2qvphqsvixyn-urdfdom-headers-1.0.5;/nix/store/vc3ff3smky98rxrflrj7sna2w0kiwarn-console-bridge-1.0.1;/nix/store/n0ivy2s2ij27b1mzszvb450xdpdxap3f-python2.7-numpy-1.16.6;/nix/store/yzqph8p8qp7sb4zxjc285772wvy9fjfg-graphviz-2.42.2;/nix/store/mmfc3yp52ngyrfj3dpgbl9w7vxi73chh-opencv-3.4.8;/nix/store/g0y8yyyhh1z7442maidqnv73j9cw15k4-opencv-3.4.8;/nix/store/gpca75ijm5rbjxr0krhpz5893wnqyyz0-util-linux-2.36.1-dev;/nix/store/0z9yy36np8ya0gfdzynb4kk2gwgvp6sa-util-linux-2.36.1-bin;/nix/store/pcir0csxglvif0f6hclgfxjr80aly6zz-util-linux-2.36.1;/nix/store/8jyfz10479mln95brx5bhzr3b0dwj565-apr-1.7.0-dev;/nix/store/n5386id2g8z1qpc7bjkkhx5gbr2jgb8f-apr-1.7.0;/nix/store/dw2z2q93k8dapd602xg973yqnx00hqk9-log4cxx-0.10.0;/nix/store/gbd2v04mxr08rdy6r67y56f79jjf38qm-python2.7-paramiko-2.7.1;/nix/store/r0735hxkmik8461z34jw3vly378x73ay-python2.7-bcrypt-3.1.7;/nix/store/9hfzbdffd0d0sdv4jxbkvi20pz31h0h8-python2.7-cffi-1.14.4-dev;/nix/store/lz1ydncs8lgrsnfg5xm1hy3fk0z0ynvi-python2.7-pycparser-2.20;/nix/store/yvahqwbczyvpk34lj1q8md9fpwzkax1b-python2.7-cffi-1.14.4;/nix/store/46giwbgj364ywwwf3ps3g8bxvxx8d74g-python2.7-cryptography-3.3.1-dev;/nix/store/b7imqw90hhp7czrdqjr3jypsif17lwih-python2.7-packaging-20.4;/nix/store/ll32hhy7n8xnncfmbj6jk6v3wg0w5ma6-python2.7-ipaddress-1.0.23;/nix/store/0b90b7zi80hqf1i4rqj4rp6c7qhirfja-python2.7-enum34-1.1.10;/nix/store/37y3vx63rqqcp5a9ffc8bqb5rqrc4fsz-python2.7-cryptography-3.3.1;/nix/store/3skmrm8vy2zb1xiwhxyax2dqxsh5hzs5-python2.7-pynacl-1.4.0;/nix/store/f9xg5qfvshcj24i301gmpjyfmibvp8vi-python2.7-pyasn1-0.4.8;/nix/store/hrffhnd21k0vhjrijf4vvyjfqmfn7b1g-python2.7-netifaces-0.10.9;/nix/store/4skfq4jbxcv96nxh3wxwq2k85qjml9ik-libyaml-cpp-0.6.3;/nix/store/jf52mpi7nlh530ay2fm0nrq9bafy5ccv-python2.7-wxPython-3.0.2.0;/nix/store/hwc5p91pdp80mnxzf9m5qb7h1nff13rf-python2.7-defusedxml-0.6.0;/nix/store/lbfzn4zj61lafr1wxki7hqy3ajdg82m6-poco-1.10.1-dev;/nix/store/hgxpbh5589qax4hqvz40vfln8clrk9cl-pcre-8.44-dev;/nix/store/hrl5wmbi9ba5spz67jxgj426n6kvrpfq-pcre-8.44-bin;/nix/store/v3aw5ip513vsh6r36fs07niv0b3f7f8l-pcre-8.44;/nix/store/g41fvyjaas2b5yb2lz8h1gy5pivh20ci-expat-2.2.10-dev;/nix/store/lyfq32jhpbw2ppq7s7m312df0z8sxa7c-expat-2.2.10;/nix/store/jrsffa62cng6wr28y79q72ck54x4wlh7-sqlite-3.34.0-dev;/nix/store/bysxhfhcrs40xzxpzdsp9frrkjxfjiim-sqlite-3.34.0-bin;/nix/store/gk764kygqrz9nzyxqnplns008kcflpii-sqlite-3.34.0;/nix/store/pq1zgy10mswfjh8xbz8kd9pv26m3n6wd-poco-1.10.1;/nix/store/jifkb4yhg2ly26mf7z2jiagrcx5jl7pq-python2.7-pycryptodomex-3.9.9;/nix/store/nwcamwwpwj63f4f7x8l22hahxl4jfi9c-python2.7-python-gnupg-0.4.6;/nix/store/6qq7pzrs6204aifj4hq3xhb6144q5v10-bzip2-1.0.6.0.1-dev;/nix/store/c5jgwpwxc1nxl9gzd9m4wlalrw7sr0z7-bzip2-1.0.6.0.1-bin;/nix/store/7l68hmbqhmxib2wlmwyd5ib5czfyb25g-bzip2-1.0.6.0.1;/nix/store/3fyw7ybrpf4g6cxa96pqjy5mx5pw1rgi-gpgme-1.15.0-dev;/nix/store/b9cxf2hg5hzff31npfammvzpgz8f1dil-libgpg-error-1.38-dev;/nix/store/k4k6k8rydpidjnck44lh0fvkhana2jqj-libgpg-error-1.38;/nix/store/dxb5wrk9wm40rhwglgzdm4jbzdf4bxxf-libassuan-2.5.4-dev;/nix/store/8nma2gl2hgaz50gs25gzayc9w9fyihxs-libassuan-2.5.4;/nix/store/isd2gkz5sls4yxxm1s9r80c09vyn9cv4-pth-2.0.7;/nix/store/7y3b1rkmqwq5dy9inxh32qffkxs4adkb-gpgme-1.15.0;/nix/store/cmxl5f8ay629ghwk8ha54mhlw2fg4d1a-lz4-1.9.3-dev;/nix/store/86rh3v9psg7d9bhl6fqfdnh6kmd7imng-lz4-1.9.3-bin;/nix/store/f8idbr4dlm1h8cl3fgk35lg6m7h07gxc-lz4-1.9.3'.split(';')
        else:
            # don't consider any other prefix path than this one
            CMAKE_PREFIX_PATH = []
        # prepend current workspace if not already part of CPP
        base_path = os.path.dirname(__file__)
        # CMAKE_PREFIX_PATH uses forward slash on all platforms, but __file__ is platform dependent
        # base_path on Windows contains backward slashes, need to be converted to forward slashes before comparison
        if os.path.sep != '/':
            base_path = base_path.replace(os.path.sep, '/')

        if base_path not in CMAKE_PREFIX_PATH:
            CMAKE_PREFIX_PATH.insert(0, base_path)
        CMAKE_PREFIX_PATH = os.pathsep.join(CMAKE_PREFIX_PATH)

        environ = dict(os.environ)
        lines = []
        if not args.extend:
            lines += rollback_env_variables(environ, ENV_VAR_SUBFOLDERS)
        lines += prepend_env_variables(environ, ENV_VAR_SUBFOLDERS, CMAKE_PREFIX_PATH)
        lines += find_env_hooks(environ, CMAKE_PREFIX_PATH)
        print('\n'.join(lines))

        # need to explicitly flush the output
        sys.stdout.flush()
    except IOError as e:
        # and catch potential "broken pipe" if stdout is not writable
        # which can happen when piping the output to a file but the disk is full
        if e.errno == errno.EPIPE:
            print(e, file=sys.stderr)
            sys.exit(2)
        raise

    sys.exit(0)
