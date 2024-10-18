import numpy as np
import tensorflow as tf


def createModel():
    model = tf.keras.Sequential([

        tf.keras.layers.Dense(units=64, activation='relu',
                              input_shape=[3]),
        tf.keras.layers.Dense(units=64, activation='relu'),
        tf.keras.layers.Dense(units=1)
    ])
    return model

def trainNet():
    model = createModel()
    model.summary()

    model.compile(optimizer='adam', loss='mae')

    with open("samples.txt", "r") as f:
        arr=np.array(eval(f.read()))
        #очень важный этап, связанный с нормализацией входных данных
        arr[:,0]/=100
        arr[:,1]/=100
        #arr[:,2]/=1
        N = len(arr)
        X=arr[:, :3]
        Y=arr[:, 3].reshape((N, 1))

    n1=int(N*0.7)

    X_train=X[:n1]
    Y_train=Y[:n1]

    X_val=X[n1:]
    Y_val=Y[n1:]

    losses = model.fit(X_train, Y_train,
                       validation_data=(X_val, Y_val),
                       batch_size=1,
                       epochs=100 )

    for x, y in zip(X_val[:5], Y_val[:5]):
        result = model.predict([x.tolist()])
        print(f"X={x}, Y={result[0]} //{y}")

    model.save_weights("net.h5")

def main():
    trainNet()