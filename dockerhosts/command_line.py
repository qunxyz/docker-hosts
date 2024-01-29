import time, argparse, docker

DOCKER_START_TAG = '# docker hosts starts'
DOCKER_END_TAG = '# docker hosts ends'

def refresh_hosts(client, hosts_file):
    containers = client.containers.list()
    docker_hosts = []
    docker_hosts_block = None
    for container in containers:
        status = container.status
        if status != 'running': continue

        name = container.name
        networks = container.attrs['NetworkSettings']['Networks']
        for network in networks:
            ip = networks[network]['IPAddress']
            if ip == '': continue
            aliases = list(set(networks[network]['Aliases']))
            for alias in aliases:
                docker_hosts.append((name, alias, ip))
                if not docker_hosts_block: docker_hosts_block = ''
                docker_hosts_block += f"{ip} {alias}\n"

    if docker_hosts_block:
        others = None
        with open(hosts_file, 'r') as f:
            lines = f.readlines()
            is_docker_host = False
            for line in lines:
                line = line.strip()
                if not others: others = ''
                if line == '':
                    if not is_docker_host:
                        others += f"{line}\n"
                    continue
                if line == DOCKER_START_TAG:
                    is_docker_host = True
                    continue
                if line == DOCKER_END_TAG:
                    is_docker_host = False
                    continue
                if not is_docker_host:
                    others += f"{line}\n"
        if others:
            with open(hosts_file, 'w+') as f:
                f.write(others)
        with open(hosts_file, 'a+') as f:
            docker_hosts_block = f"{DOCKER_START_TAG}\n{docker_hosts_block}{DOCKER_END_TAG}\n"
            f.write(docker_hosts_block)

def run():
    parser = argparse.ArgumentParser(
                        prog='docker-hosts',
                        description='Setup hosts on the host to docker containers')
    parser.add_argument('-c', '--hosts', default='/etc/hosts')
    parser.add_argument('-s', '--sock')
    args = parser.parse_args()
    while(1):
        try:
            client = None
            if not args.sock:
                client = docker.from_env()
            else:
                docker.DockerClient(base_url=args.sock)
            refresh_hosts(client, args.hosts)
            for event in client.events(decode=True):
                if event['Type'] == 'container' and event['Action'] in ['die', 'start']:
                    refresh_hosts(client, args.hosts)
        except Exception as e:
            print(e)
            print("Will try again after 5 secs")
            time.sleep(5)