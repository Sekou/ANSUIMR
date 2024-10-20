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
    model=createModel()
    model.summary()

    model.compile(optimizer='adam', loss='mae')

    X_train=[[0,0,0], [0.5, 0.5, 0.5], [1, 1, 1]]
    Y_train=[[1], [2], [3]]
    X_val=[[0.1,0.1,0.1], [0.7, 0.7, 0.7], [1.3, 1.3, 1.3]]
    Y_val=[[1.2], [2.4], [3.6]]

    losses = model.fit(X_train, Y_train,
                       validation_data=(X_val, Y_val),
                       batch_size=1,
                       epochs=15)

    result=model.predict([[0.4, 0.4, 0.4]])
    print(result)

if __name__=="__main__":
    trainNet()