import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Cargar datos MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Preprocesar datos
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

# Crear modelo CNN simple
modelo = Sequential([
    Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D(pool_size=(2,2)),
    Flatten(),
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')
])

# Compilar modelo
modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenar (solo 3 épocas para que sea rápido)
modelo.fit(x_train, y_train, epochs=3, validation_data=(x_test, y_test))

# Guardar en formato moderno recomendado
modelo.save("modelo_mnist.keras")
print("✅ Modelo guardado como modelo_mnist.keras")
