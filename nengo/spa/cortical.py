import nengo
from nengo.spa.spa_ast import ConstructionContext
from nengo.spa.module import Module


class Cortical(Module):
    """A SPA module for forming connections between other modules.

    Parameters
    ----------
    actions : spa.Actions
        The actions to implement
    synapse : float
        The synaptic filter to use for the connections
    """
    def __init__(
            self, actions, synapse=0.01, label=None, seed=None,
            add_to_container=None):
        super(Cortical, self).__init__(label, seed, add_to_container)
        self.actions = actions
        self.synapse = synapse
        self.spa = None

    def on_add(self, spa):
        Module.on_add(self, spa)
        self.spa = spa

        # parse the provided class and match it up with the spa model
        self.actions.construction_context = ConstructionContext(
            spa, cortical=self)
        self.actions.process()

    def connect(self, source, target, transform):
        """Create connection.

        The connection will use the cortical synapse.
        """
        with self.spa:
            nengo.Connection(
                source, target, transform=transform, synapse=self.synapse)
