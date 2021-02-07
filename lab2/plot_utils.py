from rbf import RBF
from dataset import SinusData
from dataset import SquareData
from rbf import CentersSampling
import matplotlib.pyplot as plt
import numpy as np

# def experiment(data, n_nodes, error, n, weight=1.0):
#     rbf_net = RBF(n=n, weight=weight)
#     _, err = rbf_net.batch_learning(
#         data.x, data.y, data.x_test, data.y_test)
#     n_nodes.append(rbf_net.n_nodes)
#     error.append(err)

# def experiment2(data, n_nodes, error, n):
#     rbf_net = RBF(n=n)
#     rbf_net.centers = np.linspace(0, 2*np.pi, n)
#     rbf_net.n_nodes = n
#     rbf_net.set_sigmas(0.5)
#     _, err = rbf_net.batch_learning(
#         data.x, data.y, data.x_test, data.y_test)
#     n_nodes.append(rbf_net.n_nodes)
#     error.append(err)

# def experiment_nodes(data):
#     error = []
#     n_nodes = []
#     for i in range(8,40):
#         # experiment(data, n_nodes, error, n=i, weight=1.0)
#         # experiment_delta(data, n_nodes, error, n=i, weight=1.0)
#         # experiment2(data, n_nodes, error, n=i)
#         experiment2_delta(data, n_nodes, error, n=i)

#     return error, n_nodes

# def experiment_delta(data, n_nodes, error, n, weight=1.0):
#     rbf_net = RBF(n=n, weight=weight)
#     _, err = rbf_net.delta_learning(
#         data.x, data.y, data.x_test, data.y_test)
#     n_nodes.append(rbf_net.n_nodes)
#     error.append(err)

# def experiment2_delta(data, n_nodes, error, n):
#     rbf_net = RBF(n=n)
#     rbf_net.centers = np.linspace(0, 2*np.pi, n)
#     rbf_net.n_nodes = n
#     rbf_net.set_sigmas(0.5)
#     _, err = rbf_net.delta_learning(
#         data.x, data.y, data.x_test, data.y_test)
#     n_nodes.append(rbf_net.n_nodes)
#     error.append(err)

# def plot_error(n_nodes, error, data):
#     plt.scatter(n_nodes, error)
#     plt.xlabel("number of hidden nodes")
#     plt.ylabel("absolute residual error")
#     plt.title("Absolute Residual Error vs number of hidden nodes")
#     plt.legend()
#     plt.savefig(f"images/3.1/{data}_error2_{len(n_nodes)}.png")
#     plt.show()

def plot_RBF_grid_search(data):
    n_nodes = [10, 15, 20, 25]
    weights = [0.6, 0.8, 1, 1.2]
    results = {}

    for n in n_nodes:
        for w in weights:
            rbf_net = RBF(CentersSampling.LINEAR, n_nodes=n, sigma=w)
            y_hat, error = rbf_net.batch_learning(data.x, data.y, data.x_test,data.y_test)
            results[(rbf_net.n_nodes, w)] = error
    
    keys = np.array(list(results.keys()))
    plt.scatter(keys[:,0], keys[:,1], c=list(results.values()), cmap='tab20b', s=200)
    plt.xlabel('units')
    plt.ylabel('width')
    plt.title('Absolute residual error for different RBF configurations')
    plt.colorbar()
    plt.show()
    return results


def error_estimate_batch(data, n_nodes=20, sigma=0.5):
    rbf_net = RBF(CentersSampling.LINEAR, n_nodes=n_nodes, sigma=0.5)
    y_hat, error = rbf_net.batch_learning(
            data.x, data.y, data.x_test, data.y_test)
    print(f'Error for batch learning: {error}')
    

def error_estimate_delta(data, n_nodes=20, sigma=0.5):
    errors = []
    for seed in range(20):
        rbf_net = RBF(CentersSampling.LINEAR, seed=seed, n_nodes=n_nodes, sigma=sigma)
        y_hat, error = rbf_net.delta_learning(
            data.x, data.y, data.x_test, data.y_test, seed=seed, max_iters=100, lr=0.1)
        errors.append(error)

    print(
        f'Error for delta rule avg: {np.mean(errors)}, variance: {np.var(errors)}')


def plot_error_delta(data, n_nodes=10, lr=0.01, max_iters=100):
    rbf_net = RBF(CentersSampling.LINEAR, n_nodes=n_nodes)
    y_hat, error = rbf_net.delta_learning(
        data.x, data.y, data.x_test, data.y_test, max_iters=max_iters, lr=lr)
    print(f'Error on the test set: {error}')
    plt.plot(rbf_net.training_errors)
    plt.xlabel("Sample number")
    plt.ylabel('absolute residual error')
    plt.title(f'Train error for delta rule with {lr} lr')
    plt.show()


def plot_estimate(data, centers_sampling=CentersSampling.LINEAR, learning_type='batch', n_nodes=20, delta_max_iters=100, sigma=0.5, delta_lr=0.01, weight=1):
    rbf_net = RBF(centers_sampling, n_nodes=n_nodes,
                  sigma=sigma, weight=weight)
    if learning_type == 'batch':
        y_hat, error = rbf_net.batch_learning(
            data.x, data.y, data.x_test, data.y_test)
    else:
        y_hat, error = rbf_net.delta_learning(
            data.x, data.y, data.x_test, data.y_test, max_iters=delta_max_iters, lr=delta_lr)
    centers, n_nodes = rbf_net.centers, rbf_net.n_nodes
    plt.plot(data.x_test, data.y_test, label="Target")
    plt.plot(data.x_test, y_hat, label="Estimate")
    plt.scatter(centers, [0]*n_nodes, c="r", label="RBF Centers")
    plt.xlabel("x")
    plt.ylabel("y")
    if sigma != 0.5:
        plt.title(
            f'{learning_type}, {n_nodes} units, {sigma} width, error= {round(error,5)}')
    else:
        plt.title(
            f'{learning_type} learning, {n_nodes} RBF units, error= {round(error,5)}')
    plt.legend()
    plt.grid(True)
    plt.show()