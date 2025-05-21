import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Flatten, Dense # type: ignore
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau # type: ignore
import tensorflow.keras.backend as K # type: ignore
import pandas as pd

def set_seeds(seed=123):
    np.random.seed(seed)
    tf.random.set_seed(seed)
    tf.config.experimental.enable_op_determinism()

class Model:
    def __init__(self, window_size=200, step=10, seed=123):
        set_seeds(seed)
        self.window_size = window_size
        self.step = step
        self.data = None
        self.model = None

    def __build_model(self, input_shape, outputs):
        model = Sequential([
            LSTM(32, input_shape=input_shape, dropout=0.2, recurrent_dropout=0.2,
                 kernel_regularizer=tf.keras.regularizers.l2(1e-4)),
            Flatten(),
            Dense(outputs, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(1e-4))
        ])

        def sharpe_loss(_, y_pred):
            data = tf.divide(self.data, self.data[0])  # shape: (window_size, assets)
            # broadcast y_pred (1, assets) across time axis
            port_vals = tf.reduce_sum(data * y_pred[0], axis=1)

            #returns = (port_vals[1:] - port_vals[:-1]) / (port_vals[:-1] + 1e-8)
            returns = (port_vals[1:] - port_vals[:-1]) / port_vals[:-1]

            #sharpe = K.mean(returns) / (K.std(returns) + 1e-6)
            sharpe = K.mean(returns) / K.std(returns)
            return -sharpe

        model.compile(optimizer='adam', loss=sharpe_loss)
        return model

    def _make_windows(self, data_w_ret):
        X = []
        for start in range(0, len(data_w_ret) - self.window_size + 1, self.step):
            X.append(data_w_ret[start:start + self.window_size])
        return np.stack(X)  # shape: (num_windows, window_size, features)

    def fit_predict(self, price_df: pd.DataFrame):
        prices = price_df.values[1:]
        rets = price_df.pct_change().values[1:]
        data_w_ret = np.concatenate([prices, rets], axis=1)

        X = self._make_windows(data_w_ret)
        last_prices = price_df.values[-self.window_size:]
        self.data = tf.cast(tf.constant(last_prices), tf.float32)

        # dummy targets
        y = np.zeros((len(X), price_df.shape[1]))

        split = int(0.8 * len(X))
        X_train, X_val = X[:split], X[split:]
        y_train, y_val = y[:split], y[split:]

        if self.model is None:
            self.model = self.__build_model(
                input_shape=(self.window_size, X.shape[2]),
                outputs=price_df.shape[1]
            )

        early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)
        checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True, monitor='val_loss')

        self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=50,
            batch_size=1,
            shuffle=False,
            callbacks=[early_stop, reduce_lr, checkpoint]
        )

        last_window = X[-1:]
        weights = self.model.predict(last_window, batch_size=1)[0]

        # calculate return on investment
        roi = (price_df.values[-1] * weights - price_df.values[-self.window_size] * weights) / (price_df.values[-self.window_size] * weights)

        # calculate sharpe
        y_pred = tf.constant(weights[np.newaxis, :], dtype=tf.float32)
        sharpe = -self.model.loss(None, y_pred)

        return weights, roi, sharpe