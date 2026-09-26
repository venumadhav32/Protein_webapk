import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, Bidirectional, LSTM, Dense, TimeDistributed

print("Generating data and compiling model...")
# 1. Generate dummy data
X_train = np.random.randint(1, 21, size=(1500, 50))
y_train_onehot = tf.keras.utils.to_categorical(np.random.randint(0, 3, size=(1500, 50)), num_classes=3)

# 2. Build model
model = Sequential([
    Embedding(input_dim=21, output_dim=64, input_length=50),
    Bidirectional(LSTM(64, return_sequences=True)),
    TimeDistributed(Dense(3, activation='softmax'))
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 3. Train and save locally
model.fit(X_train, y_train_onehot, epochs=3, batch_size=32)
model.save('protein_model.h5')
print("\nSuccess! Local protein_model.h5 created.")