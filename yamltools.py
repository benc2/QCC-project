import yaml

def change_link_fidelity(fidelity):
    with open("network.yaml", 'r') as file:
        yaml_dict = yaml.full_load(file.read())

    for link in yaml_dict['links']:
        link['fidelity'] = fidelity

    with open("network.yaml", 'w') as file:
        file.write(yaml.dump(yaml_dict))


def change_node_property(node_property, value, names=None):
    # optionally include list of names of nodes to change, otherwise change all
    with open("network.yaml", 'r') as file:
        yaml_dict = yaml.full_load(file.read())

    for node in yaml_dict['nodes']:
        if names is None or node['name'] in names:
            node[node_property] = value

    with open("network.yaml", 'w') as file:
        file.write(yaml.dump(yaml_dict))


def change_gate_fidelity(fidelity, names=None):
    # optionally include list of names of nodes to change, otherwise change all
    change_node_property('gate_fidelity', fidelity, names=names)

