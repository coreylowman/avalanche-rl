from avalanche_rl.training.strategies import A2CStrategy
from avalanche_rl.models.actor_critic import ActorCriticMLP
from torch.optim import Adam
from avalanche_rl.benchmarks.generators.rl_benchmark_generators import gym_benchmark_generator
import torch


if __name__ == "__main__":
    device = torch.device('cpu')

    scenario = gym_benchmark_generator(
        ['CartPole-v1'],
        n_parallel_envs=1, eval_envs=['CartPole-v1'], n_experiences=1)

    # CartPole setting
    model = ActorCriticMLP(4, 2, 1024, 1024)
    print("Model", model)

    # A2C learning rate
    optimizer = Adam(model.parameters(), lr=1e-4)

    strategy = A2CStrategy(
        model, optimizer, per_experience_steps=10000, max_steps_per_rollout=5,
        device=device, eval_every=1000, eval_episodes=10)

    # TRAINING LOOP
    print('Starting experiment...')
    for experience in scenario.train_stream:
        print("Start of experience ", experience.current_experience)
        print("Current Env ", experience.env)
        print("Current Task", experience.task_label, type(experience.task_label))
        strategy.train(experience, scenario.test_stream)

    print('Training completed')
    eval_episodes = 100
    print(f"\nEvaluating on {eval_episodes} episodes!")
    print(strategy.eval(scenario.test_stream))
