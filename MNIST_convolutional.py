# -*- coding: utf-8 -*-
"""MNIST_convolutional

ГЛАВА 5: СВЕРТОЧНЫЕ НЕЙРОННЫЕ СЕТИ

ЗАГРУЗКА ВСЕХ НЕОБХОДИМЫХ МОДУЛЕЙ
"""

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
from keras.datasets import mnist
from keras.utils import to_categorical

"""СОЗДАНИЕ СВЕРТОЧНОЙ СЕТИ ДЛЯ ЗАДАЧ И MNIST"""

model = Sequential()
# принимает тензоры размером: высота, ширина, количество каналов цвета
# количество канало управляется первым аргументом - 32 или 64
# (3,3) - размер "окна" на изображении, на котором сетка ищет шаблоны (таких
# окон - много)
# (28, 28, 1) единица отвечает за количество каналов цвета (оттенки серого - 1)
model.add(Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(64, (3,3), activation='relu'))
model.add(MaxPooling2D((2,2)))
model.add(Conv2D(64, (3,3), activation='relu'))
# выходной слой имеет форму (3,3,64) 
# теперь его необходимо преобразовать в одномерный тензор и передать нескольким
# слоям Dense для классификации
model.add(Flatten())
model.add(Dense(64, activation='relu'))
# всего 10 классов изображений в MNIST -> 10 нейронов
model.add(Dense(10, activation='softmax'))
# можно заметить, что первый слой возвращает карту признаков (тензор) размер-
# ность (26, 26, 32), а принимает (28, 28, 1)
# значит, что он содержит 32е сетки размером 26 на 26 - карту ответов фильтра
# на входных данных
# каждое измерение на оси глубины - признак (или фильтр)
model.summary()
#каждый слой принимает карту признаков, отдает - карту ответов

# каждый слой MaxPooling уменьшает изображение в 2 раза, чтобы уменьшить
# количество параметров на выходе, которые будут скормлены в Dense
# MaxPooling берет окно 2 на 2 и выбирает из него самое большое значение градации
# серого и заменяет его эим значением

"""ПРЕДОБРАБОТКА ДАННЫХ"""

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# меняем форму на ту, которая указана в слое
train_images = train_images.reshape((60000, 28, 28, 1))
# преобразуем к типа float и нормализуем
train_images = train_images.astype('float32') / 255

test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255

# преобразуем метки из int (номер класса) в категориальные
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

"""КОМПИЛЯЦИЯ МОДЕЛИ"""

model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

"""ТРЕНИРОВКА МОДЕЛИ"""

model.fit(train_images, train_labels, epochs=5, batch_size=64)

"""ПРОВЕРКА ТОЧНОСТИ МОДЕЛИ"""

test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"loss is {test_loss}\naccuracy is {test_acc}")
