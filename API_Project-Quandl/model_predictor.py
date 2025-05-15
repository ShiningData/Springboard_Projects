import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import classification_report, confusion_matrix
from autogluon.tabular import TabularPredictor
import matplotlib.pyplot as plt
import seaborn as sns

# Set random seed for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# 1. Load your dataset (replace with your actual data loading code)
def load_data():
    # Replace with your actual data loading code
    # For example:
    # df = pd.read_csv('your_dataset.csv')
    
    # Sample data for demonstration
    from sklearn.datasets import make_classification
    X, y = make_classification(
        n_samples=1000, 
        n_classes=4,
        n_features=20, 
        n_informative=10, 
        weights=[0.7, 0.1, 0.1, 0.1],  # Imbalanced class distribution
        random_state=42
    )
    feature_names = [f'feature_{i}' for i in range(X.shape[1])]
    df = pd.DataFrame(X, columns=feature_names)
    df['target'] = y
    return df

# 2. Data preparation function
def prepare_data(df, target_column='target', test_size=0.2):
    # Separate features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    
    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Create DataFrames for train and test data
    train_data = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    train_data[target_column] = y_train
    
    test_data = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    test_data[target_column] = y_test
    
    print(f"Training data shape: {train_data.shape}")
    print(f"Testing data shape: {test_data.shape}")
    
    # Check class distribution
    print("\nClass distribution in training data:")
    print(y_train.value_counts(normalize=True).sort_index() * 100)
    
    return train_data, test_data, target_column, scaler

# 3. Define GAN for minority class augmentation
class TabularGAN:
    def __init__(self, input_dim, latent_dim=32):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.generator = self._build_generator()
        self.discriminator = self._build_discriminator()
        self.gan = self._build_gan()
        
    def _build_generator(self):
        model = models.Sequential()
        # First hidden layer
        model.add(layers.Dense(64, input_dim=self.latent_dim))
        model.add(layers.LeakyReLU(0.2))
        model.add(layers.BatchNormalization())
        # Second hidden layer
        model.add(layers.Dense(128))
        model.add(layers.LeakyReLU(0.2))
        model.add(layers.BatchNormalization())
        # Output layer
        model.add(layers.Dense(self.input_dim, activation='tanh'))
        
        noise = layers.Input(shape=(self.latent_dim,))
        output = model(noise)
        
        return models.Model(noise, output)
        
    def _build_discriminator(self):
        model = models.Sequential()
        # First hidden layer
        model.add(layers.Dense(128, input_dim=self.input_dim))
        model.add(layers.LeakyReLU(0.2))
        model.add(layers.Dropout(0.3))
        # Second hidden layer
        model.add(layers.Dense(64))
        model.add(layers.LeakyReLU(0.2))
        model.add(layers.Dropout(0.3))
        # Output layer
        model.add(layers.Dense(1, activation='sigmoid'))
        
        features = layers.Input(shape=(self.input_dim,))
        validity = model(features)
        
        return models.Model(features, validity)
        
    def _build_gan(self):
        # For the combined model, we only train the generator
        self.discriminator.trainable = False
        
        noise = layers.Input(shape=(self.latent_dim,))
        generated_features = self.generator(noise)
        validity = self.discriminator(generated_features)
        
        return models.Model(noise, validity)
    
    def train(self, X_real, epochs=2000, batch_size=32, print_interval=200):
        # Normalize input data to range [-1, 1] if not already normalized
        X_real = np.clip(X_real, -1, 1)
        
        # Adversarial ground truths
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))
        
        d_losses, g_losses = [], []
        
        for epoch in range(epochs):
            # ---------------------
            #  Train Discriminator
            # ---------------------
            # Select a random batch of real samples
            idx = np.random.randint(0, X_real.shape[0], batch_size)
            real_samples = X_real[idx]
            
            # Generate a batch of fake samples
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            fake_samples = self.generator.predict(noise)
            
            # Train the discriminator
            d_loss_real = self.discriminator.train_on_batch(real_samples, valid)
            d_loss_fake = self.discriminator.train_on_batch(fake_samples, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)
            
            # ---------------------
            #  Train Generator
            # ---------------------
            noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            g_loss = self.gan.train_on_batch(noise, valid)
            
            d_losses.append(d_loss)
            g_losses.append(g_loss)
            
            # Print progress
            if epoch % print_interval == 0:
                print(f"Epoch {epoch}/{epochs}, [D loss: {d_loss:.4f}] [G loss: {g_loss:.4f}]")
        
        return d_losses, g_losses
    
    def generate_samples(self, n_samples):
        noise = np.random.normal(0, 1, (n_samples, self.latent_dim))
        return self.generator.predict(noise)

# 4. Balance dataset using GANs
def balance_with_gan(train_data, target_column, target_count=None):
    X = train_data.drop(columns=[target_column]).values
    y = train_data[target_column].values
    
    # Get class distribution
    class_counts = pd.Series(y).value_counts().sort_index()
    classes = class_counts.index.tolist()
    
    # If target_count is not provided, use the count of the majority class
    if target_count is None:
        target_count = class_counts.max()
    
    print(f"Balancing classes to {target_count} samples each using GANs")
    
    # Initialize the balanced dataset with original samples
    X_balanced = X.copy()
    y_balanced = y.copy()
    
    # For each minority class
    for class_label in classes:
        # If this class needs augmentation
        if class_counts[class_label] < target_count:
            # Get real samples of this class
            X_class = X[y == class_label]
            
            # Calculate how many synthetic samples we need
            n_to_generate = target_count - len(X_class)
            
            print(f"Class {class_label}: Generating {n_to_generate} synthetic samples")
            
            # Train a GAN on this class
            gan = TabularGAN(input_dim=X.shape[1])
            gan.train(X_class, epochs=2000, batch_size=min(32, len(X_class)), print_interval=500)
            
            # Generate synthetic samples
            synthetic_samples = gan.generate_samples(n_to_generate)
            
            # Add synthetic samples to the balanced dataset
            X_balanced = np.vstack([X_balanced, synthetic_samples])
            y_balanced = np.append(y_balanced, [class_label] * n_to_generate)
    
    # Create a new DataFrame with the balanced data
    columns = train_data.drop(columns=[target_column]).columns
    balanced_df = pd.DataFrame(X_balanced, columns=columns)
    balanced_df[target_column] = y_balanced
    
    print("\nClass distribution after GAN balancing:")
    print(pd.Series(y_balanced).value_counts(normalize=True).sort_index() * 100)
    
    return balanced_df

# 5. Train models using AutoGluon
def train_with_autogluon(train_data, test_data, target_column, time_limit=600):
    # Initialize TabularPredictor
    predictor = TabularPredictor(
        label=target_column,
        eval_metric='balanced_accuracy',  # Good for imbalanced data
        path='agModels-GAN',  # Path to save models
    )
    
    # Fit models
    predictor.fit(
        train_data=train_data,
        time_limit=time_limit,  # in seconds
        presets='best_quality',  # You can also use 'high_quality' for faster training
        hyperparameters={
            'GBM': {'objective': 'multiclass'},  # Set for multiclass problems
            'RF': {},
            'XGB': {'objective': 'multi:softmax'},
            'CAT': {'loss_function': 'MultiClass'}
        }
    )
    
    return predictor

# 6. Evaluate model performance
def evaluate_model(predictor, test_data, target_column):
    # Generate predictions
    y_pred = predictor.predict(test_data)
    y_true = test_data[target_column]
    
    # Get feature importance
    try:
        importance = predictor.feature_importance(test_data)
        print("\nFeature Importance:")
        print(importance.head(10))  # Top 10 important features
    except:
        print("Feature importance not available for the best model")
    
    # Model performance metrics
    print("\nModel Performance Leaderboard:")
    print(predictor.leaderboard(test_data))
    
    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred))
    
    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=sorted(y_true.unique()),
                yticklabels=sorted(y_true.unique()))
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig('confusion_matrix_gan.png')
    plt.show()
    
    return y_pred

# 7. Visualize original vs generated data
def visualize_data_distribution(original_data, balanced_data, target_column, feature_pairs=None):
    """Visualize the distribution of original vs GAN-generated data"""
    # If feature pairs not specified, select first two features
    if feature_pairs is None:
        features = original_data.drop(columns=[target_column]).columns[:2]
        feature_pairs = [(features[0], features[1])]
    
    for f1, f2 in feature_pairs:
        plt.figure(figsize=(15, 6))
        
        # Original data
        plt.subplot(1, 2, 1)
        for class_label in original_data[target_column].unique():
            class_data = original_data[original_data[target_column] == class_label]
            plt.scatter(class_data[f1], class_data[f2], label=f'Class {class_label}', alpha=0.7)
        plt.title('Original Data')
        plt.xlabel(f1)
        plt.ylabel(f2)
        plt.legend()
        
        # Balanced data
        plt.subplot(1, 2, 2)
        for class_label in balanced_data[target_column].unique():
            class_data = balanced_data[balanced_data[target_column] == class_label]
            plt.scatter(class_data[f1], class_data[f2], label=f'Class {class_label}', alpha=0.7)
        plt.title('Balanced Data (with GAN-generated samples)')
        plt.xlabel(f1)
        plt.ylabel(f2)
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(f'data_distribution_{f1}_{f2}.png')
        plt.show()

# 8. Main function to orchestrate the process
def main():
    print("Loading data...")
    df = load_data()
    
    print("Preparing data...")
    train_data, test_data, target_column, scaler = prepare_data(df)
    
    # Save original training data for visualization later
    original_train_data = train_data.copy()
    
    print("Balancing data using GANs...")
    balanced_train_data = balance_with_gan(train_data, target_column)
    
    # Visualize original vs balanced data
    visualize_data_distribution(original_train_data, balanced_train_data, target_column)
    
    print("Training models with AutoGluon...")
    predictor = train_with_autogluon(balanced_train_data, test_data, target_column)
    
    print("Evaluating model performance...")
    y_pred = evaluate_model(predictor, test_data, target_column)
    
    # Save predictions to file if needed
    pd.DataFrame({
        'true': test_data[target_column],
        'pred': y_pred
    }).to_csv('predictions_gan.csv', index=False)
    
    print("Process completed successfully!")

if __name__ == "__main__":
    main()
