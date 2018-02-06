import keras

class OutputPipe(keras.callbacks.Callback):

    def __init__(self, id, publisher, channel, epochs, model_addr, model, keras2ipfs):
        self.id = id
        self.publisher = publisher
        self.channel = channel
        self.epochs = epochs
        self.model_addr = model_addr
        self.model = model

        ## TODO -- this class and grid.py are way too tightly coupled right now
        ##         keras2ipfs & ipfs2keras should be in a lib/utils.py class
        ##         and ideally have no dependencies.  We can look into this soon.
        self.keras2ipfs = keras2ipfs

    def on_train_begin(self, logs={}):
        self.losses = []

    def on_epoch_end(self, epoch, logs={}):
        acc = logs.get('acc')
        loss = logs.get('loss')

        spec = {}
        spec['type'] = 'log'
        spec['eval_loss'] = loss
        spec['epoch_id'] = epoch
        spec['num_epochs'] = self.epochs
        spec['parent_model'] = self.model_addr
        spec['worker_id'] = self.id

        self.publisher(channel=self.channel, dict_message=spec)

    def on_train_end(self, logs={}):
        spec = {}
        spec['type'] = 'transact'
        spec['model_addr'] = self.keras2ipfs(self.model)
        spec['eval_loss'] = logs.get('loss')
        spec['parent_model'] = self.model_addr
        spec['worker_id'] = self.id

        self.publisher(channel=self.channel, dict_message=spec)
