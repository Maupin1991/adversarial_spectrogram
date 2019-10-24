from decimal import Decimal

from src.audio_torch import ModelTrainer
import numpy as np
import os
import matplotlib.pyplot as plt

if __name__ == '__main__':
    model_trainer = ModelTrainer()
    accuracies = []
    models = os.listdir(model_trainer.model_dir) 
    plt.figure()
    for model in models:
        if model.endswith('.pt'):
            print("Running sec eval for model: {}".format(model))
            model_trainer.load_model(model)
            eps_values = np.arange(start=0, stop=1, step=0.05)
            eps_values /= model_trainer.train_dataset.max_value
            accs = model_trainer.security_evaluation(eps_values)
            accuracies.append(accs)
            wd = float(model.split('-')[-1][:-3])
            if wd == 0:
                label_str = "gradient_penalty = 0"
            else:
                wd = Decimal(wd)
                label_str = "gradient_penalty = {:.2E}".format(wd)
            plt.plot(eps_values, accs, label=label_str)
            plt.title("Security evaluation")
            plt.xlabel("Perturbation strength")
            plt.ylabel("Test accuracy")
    plt.legend()
    plt.savefig(os.path.join(model_trainer.plot_dir, "Security evaluation.pdf"), format='pdf')
    np.save("accuracies", np.array(accuracies))
