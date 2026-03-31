"""
Funciones de utilidad para visualizacion de redes neuronales.
"""
import numpy as np
import matplotlib.pyplot as plt


class VisualizadorEntrenamiento:
    """
    Clase para visualizar el proceso de entrenamiento de un modelo.
    """
    
    def __init__(self, modelo, historial, X_train, y_train, X_test=None, y_test=None):
        self.modelo = modelo
        self.historial = historial
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
    
    def mostrar_todo(self, nombre_modelo='Modelo'):
        """
        Muestra todas las visualizaciones del entrenamiento.
        """
        print(f"\n{'='*60}")
        print(f"  RESULTADOS: {nombre_modelo}")
        print(f"{'='*60}\n")
        
        self._mostrar_metricas()
        
        # Figura con 4 subplots
        fig = plt.figure(figsize=(16, 10))
        
        ax1 = fig.add_subplot(2, 2, 1)
        self._plot_loss(ax1)
        
        ax2 = fig.add_subplot(2, 2, 2)
        self._plot_accuracy(ax2)
        
        ax3 = fig.add_subplot(2, 2, 3)
        self._plot_frontera(ax3)
        
        ax4 = fig.add_subplot(2, 2, 4)
        self._plot_datos(ax4)
        
        plt.suptitle(f'Analisis de Entrenamiento - {nombre_modelo}', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.show()
    
    def _mostrar_metricas(self):
        train_loss = self.historial.history['loss'][-1]
        train_acc = self.historial.history['accuracy'][-1] * 100
        print(f"Entrenamiento -> Loss: {train_loss:.4f}, Accuracy: {train_acc:.2f}%")
        
        if 'val_loss' in self.historial.history:
            val_loss = self.historial.history['val_loss'][-1]
            val_acc = self.historial.history['val_accuracy'][-1] * 100
            print(f"Validacion    -> Loss: {val_loss:.4f}, Accuracy: {val_acc:.2f}%")
        print()
    
    def _plot_loss(self, ax):
        ax.plot(self.historial.history['loss'], label='Train', color='blue', linewidth=2)
        if 'val_loss' in self.historial.history:
            ax.plot(self.historial.history['val_loss'], label='Test', color='red', linestyle='--', linewidth=2)
        ax.set_xlabel('Epoca')
        ax.set_ylabel('Loss')
        ax.set_title('Funcion de Costo')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_accuracy(self, ax):
        ax.plot(self.historial.history['accuracy'], label='Train', color='blue', linewidth=2)
        if 'val_accuracy' in self.historial.history:
            ax.plot(self.historial.history['val_accuracy'], label='Test', color='red', linestyle='--', linewidth=2)
        ax.set_xlabel('Epoca')
        ax.set_ylabel('Accuracy')
        ax.set_title('Precision')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_frontera(self, ax):
        x_min, x_max = self.X_train[:, 0].min() - 0.5, self.X_train[:, 0].max() + 0.5
        y_min, y_max = self.X_train[:, 1].min() - 0.5, self.X_train[:, 1].max() + 0.5
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                             np.linspace(y_min, y_max, 100))
        
        Z = self.modelo.predict(np.c_[xx.ravel(), yy.ravel()], verbose=0)
        Z = Z.reshape(xx.shape)
        
        ax.contourf(xx, yy, Z, levels=[0, 0.5, 1], alpha=0.3, colors=['blue', 'red'])
        ax.contour(xx, yy, Z, levels=[0.5], colors='black', linewidths=2)
        
        ax.scatter(self.X_train[self.y_train == 0, 0], self.X_train[self.y_train == 0, 1], 
                   c='blue', label='Train 0', alpha=0.7, s=40)
        ax.scatter(self.X_train[self.y_train == 1, 0], self.X_train[self.y_train == 1, 1], 
                   c='red', label='Train 1', alpha=0.7, s=40)
        
        if self.X_test is not None and self.y_test is not None:
            ax.scatter(self.X_test[self.y_test == 0, 0], self.X_test[self.y_test == 0, 1], 
                       c='blue', alpha=0.3, s=40, marker='s')
            ax.scatter(self.X_test[self.y_test == 1, 0], self.X_test[self.y_test == 1, 1], 
                       c='red', alpha=0.3, s=40, marker='s')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Frontera de Decision')
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)
    
    def _plot_datos(self, ax):
        ax.scatter(self.X_train[self.y_train == 0, 0], self.X_train[self.y_train == 0, 1], 
                   c='blue', label='Train Clase 0', alpha=0.9, s=50)
        ax.scatter(self.X_train[self.y_train == 1, 0], self.X_train[self.y_train == 1, 1], 
                   c='red', label='Train Clase 1', alpha=0.9, s=50)
        
        if self.X_test is not None and self.y_test is not None:
            ax.scatter(self.X_test[self.y_test == 0, 0], self.X_test[self.y_test == 0, 1], 
                       c='blue', label='Test Clase 0', alpha=0.3, s=50)
            ax.scatter(self.X_test[self.y_test == 1, 0], self.X_test[self.y_test == 1, 1], 
                       c='red', label='Test Clase 1', alpha=0.3, s=50)
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Datos de Entrenamiento y Prueba')
        ax.legend(loc='upper left', fontsize=8)
        ax.grid(True, alpha=0.3)


def visualizar_entrenamiento(modelo, historial, X_train, y_train, X_test=None, y_test=None, nombre='Modelo'):
    """
    Funcion para visualizar resultados del entrenamiento.
    
    Args:
        modelo: Modelo de Keras entrenado
        historial: Objeto History retornado por model.fit()
        X_train: Datos de entrenamiento
        y_train: Etiquetas de entrenamiento
        X_test: Datos de prueba (opcional)
        y_test: Etiquetas de prueba (opcional)
        nombre: Nombre del modelo para mostrar
    """
    viz = VisualizadorEntrenamiento(modelo, historial, X_train, y_train, X_test, y_test)
    viz.mostrar_todo(nombre_modelo=nombre)


def visualizar_multiclase(modelo, historial, X_train, y_train, X_test=None, y_test=None, nombre='Modelo', colores=None):
    """
    Funcion para visualizar resultados de clasificacion multiclase.
    
    Args:
        modelo: Modelo de Keras entrenado
        historial: Objeto History retornado por model.fit()
        X_train: Datos de entrenamiento
        y_train: Etiquetas de entrenamiento (0, 1, 2, ...)
        X_test: Datos de prueba (opcional)
        y_test: Etiquetas de prueba (opcional)
        nombre: Nombre del modelo para mostrar
        colores: Lista de colores para cada clase (opcional)
    """
    n_clases = len(np.unique(y_train))
    
    if colores is None:
        colores = ['blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 'cyan'][:n_clases]
    
    print(f"\n{'='*60}")
    print(f"  RESULTADOS: {nombre}")
    print(f"{'='*60}\n")
    
    # Metricas finales
    train_loss = historial.history['loss'][-1]
    train_acc = historial.history['accuracy'][-1] * 100
    print(f"Entrenamiento -> Loss: {train_loss:.4f}, Accuracy: {train_acc:.2f}%")
    
    if 'val_loss' in historial.history:
        val_loss = historial.history['val_loss'][-1]
        val_acc = historial.history['val_accuracy'][-1] * 100
        print(f"Validacion    -> Loss: {val_loss:.4f}, Accuracy: {val_acc:.2f}%")
    print()
    
    # Figura con 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    # Loss
    axes[0].plot(historial.history['loss'], label='Train', color='blue', linewidth=2)
    if 'val_loss' in historial.history:
        axes[0].plot(historial.history['val_loss'], label='Test', color='red', linestyle='--', linewidth=2)
    axes[0].set_xlabel('Epoca')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Funcion de Costo')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy
    axes[1].plot(historial.history['accuracy'], label='Train', color='blue', linewidth=2)
    if 'val_accuracy' in historial.history:
        axes[1].plot(historial.history['val_accuracy'], label='Test', color='red', linestyle='--', linewidth=2)
    axes[1].set_xlabel('Epoca')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Precision')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Frontera de decision multiclase
    X_all = X_train if X_test is None else np.vstack([X_train, X_test])
    h = 0.1
    x_min, x_max = X_all[:, 0].min() - 1, X_all[:, 0].max() + 1
    y_min, y_max = X_all[:, 1].min() - 1, X_all[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = modelo.predict(np.c_[xx.ravel(), yy.ravel()], verbose=0)
    Z = np.argmax(Z, axis=1).reshape(xx.shape)
    
    axes[2].contourf(xx, yy, Z, alpha=0.3, cmap='viridis')
    for i, color in enumerate(colores):
        mask_train = y_train == i
        axes[2].scatter(X_train[mask_train, 0], X_train[mask_train, 1], 
                       c=color, label=f'Clase {i}', alpha=0.7, edgecolors='k', s=40)
        if X_test is not None and y_test is not None:
            mask_test = y_test == i
            axes[2].scatter(X_test[mask_test, 0], X_test[mask_test, 1], 
                           c=color, alpha=0.3, marker='x', s=40)
    axes[2].set_xlabel('X')
    axes[2].set_ylabel('Y')
    axes[2].set_title('Frontera de Decision')
    axes[2].legend(loc='upper left', fontsize=8)
    axes[2].grid(True, alpha=0.3)
    
    plt.suptitle(f'Analisis de Entrenamiento - {nombre}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()
