import numpy as np
from tensorflow import keras
import tensorflow as tf
import tensorflow_addons as tfa
import matplotlib.pyplot as plt



class Train:
    def __init__(self, model):
        self.learning_rate = 0.01
        self.weight_decay = 0.000001
        self.batch_size = 64
        self.num_epochs = 50
        self.model = model
        self.run_experiment(self.model)

    def run_experiment(self, model):
        optimizer = tfa.optimizers.AdamW(
            learning_rate = self.learning_rate,
            weight_decay= self.weight_decay 
        )

        model.compile(
            optimizer=optimizer,
            loss= tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics = [
                keras.metrics.BinaryAccuracy(name="Accuracy"),
            ],
        )

        checkpoint_filepath = "/tmp/checkpoint"
        checkpoint_callback = keras.callbacks.ModelCheckpoint(
            checkpoint_filepath,
            monitor  = "val_Accuracy",
            save_best_only = True,
            save_weights_only = True
        )

        history = model.fit(
            x=np.load('X_train.npy'),
            y=np.load('y_train.npy'),
            batch_size=self.batch_size,
            epochs=self.num_epochs,
            validation_split=0.1,
            callbacks=[checkpoint_callback],
        )

        plt.plot(history.history['Accuracy'], label='accuracy')
        plt.plot(history.history['val_Accuracy'], label = 'val_accuracy')
        plt.plot(history.history['loss'], label = 'loss') 

        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.ylim([0.5, 2])
        plt.legend(loc='lower right')

        test_loss, test_acc, *is_anything_else_being_returned = model.evaluate(np.load('X_test.npy'),  np.load('y_test.npy'),  verbose=2)
        print(f"test_loss: {test_loss}")
        print(f"test_acc: {test_acc}")
        print(f"is_anything_else_being_returned: {is_anything_else_being_returned}")
        return history