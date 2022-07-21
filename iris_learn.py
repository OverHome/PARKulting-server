import tensorflow
from keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Dense
import os


def iris_learn():
    # Каталог с данными для обучения
    train_dir = 'Data/learn/tren'
    # Каталог с данными для проверки
    val_dir = 'Data/learn/val'
    # Каталог с данными для тестирования
    test_dir = 'Data/learn/test'
    # Размеры изображения
    img_width, img_height = 250, 250
    # Размерность тензора на основе изображения для входных данных в нейронную сеть
    # backend Tensorflow, channels_last
    input_shape = (img_width, img_height, 3)
    # Количество эпох
    epochs = 20
    # Размер мини-выборки
    batch_size = 4
    # Количество изображений для обучения
    nb_train_samples = 40 * len(os.listdir(train_dir))
    # Количество изображений для проверки
    nb_validation_samples = 4 * len(os.listdir(train_dir))
    # Количество изображений для тестирования
    nb_test_samples = 4 * len(os.listdir(train_dir))

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=input_shape))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(os.listdir(train_dir))))
    model.add(Activation('sigmoid'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    datagen = tensorflow.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

    train_generator = datagen.flow_from_directory(
        train_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')

    val_generator = datagen.flow_from_directory(
        val_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')

    test_generator = datagen.flow_from_directory(
        test_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical')

    checkpoint = ModelCheckpoint("Data/models/best.h5", monitor='val_loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]

    model.fit_generator(train_generator,
                        steps_per_epoch=nb_train_samples // batch_size,
                        epochs=epochs,
                        validation_data=val_generator,
                        validation_steps=nb_validation_samples // batch_size,
                        callbacks=callbacks_list)

    converter = tensorflow.compat.v1.lite.TFLiteConverter.from_keras_model_file('Data/models/best.h5')
    tflite_model = converter.convert()
    with open('Data/models/model.tflite', 'wb') as f:
        f.write(tflite_model)
