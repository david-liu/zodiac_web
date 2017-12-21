#!.env/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import glob

import click


def convert_to_abspath(path):
    if not os.path.isabs(path):
        return os.path.abspath(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), path))

    return path


project_default_base_dir = convert_to_abspath("./test/")


def write_file_with_tokens(src_file, dest_file, tokens=None):
    with open(dest_file, "wt") as fout:
        with open(src_file, "rt") as fin:
            for line in fin:
                if tokens is None:
                    fout.write(line)
                else:
                    newline = line[:]
                    for name, value in tokens.items():
                        newline = newline.replace("{%s}" % name, value)

                    fout.write(newline)


@click.command()
@click.option('--force', is_flag=True, default=False,
              help="whether to override the existed directory or not")
@click.option('--path',
              help="directory to create the app", default=project_default_base_dir)
@click.option('--port',
              help="Port for the app", default=5000)
@click.argument('name',
                required=True)
def init(name, force, path, port):
    project_base_dir = path
    project_name = name

    if not os.path.exists(project_base_dir):
        raise ValueError("the project dir [%s] did not existed." % project_base_dir)

    os.system('./package.sh')
    whl_source_path = None
    for name in glob.glob('./dist/*.whl'):
        whl_source_path = name
        break
    parts = os.path.split(whl_source_path)
    whl_file = parts[-1]

    project_dir = os.path.abspath(os.path.join(
        project_base_dir, project_name))

    if os.path.exists(project_dir):
        if force:
            shutil.rmtree(project_dir, ignore_errors=True)
        else:
            raise ValueError("the project has existed in %s" % project_dir)

    source_dir = convert_to_abspath("./app-scaffold/")
    shutil.copytree(source_dir, project_dir + "/")

    shutil.copy(convert_to_abspath(whl_source_path), project_dir + "/" + whl_file)

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/Dockerfile"),
        dest_file=os.path.join(project_dir, "scripts/Dockerfile"),
        tokens={
            'app_name': project_name,
            'port': str(port),
            'setup_whl_file': whl_file
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/build_docker"),
        dest_file=os.path.join(project_dir, "scripts/build_docker"),
        tokens={
            'app_name': project_name
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/logging.conf"),
        dest_file=os.path.join(project_dir, "scripts/logging.conf"),
        tokens={
            'app_name': project_name
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/gunicorn.conf"),
        dest_file=os.path.join(project_dir, "scripts/gunicorn.conf"),
        tokens={
            'app_name': project_name,
            'port': str(port)
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/install_env"),
        dest_file=os.path.join(project_dir, "scripts/install_env"),
        tokens={
            'setup_whl_file': whl_file
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/scripts/service.sh"),
        dest_file=os.path.join(project_dir, "service.sh"),
        tokens={
            'app_name': project_name
        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/Makefile"),
        dest_file=os.path.join(project_dir, "Makefile"),
        tokens={
            'app_name': project_name,
            'port': str(port),

        })

    write_file_with_tokens(
        src_file=convert_to_abspath("./app-scaffold/apidoc.json"),
        dest_file=os.path.join(project_dir, "apidoc.json"),
        tokens={
            'app_name': project_name,
            'port': str(port),

        })


if __name__ == '__main__':
    init()
