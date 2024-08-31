import pickle

def load_model_components(model_path='Models/churn_model_components.pkl'):
    """Loading model components from a pickle file."""
    with open(model_path, 'rb') as file:
        components = pickle.load(file)
    return components['preprocessing']['preprocessor'], components['tuned_models']