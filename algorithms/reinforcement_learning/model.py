import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 32 * 32, 256)
        
        # Output layers
        self.actor_output = nn.Linear(256, 10)  # 10 classes for Actor
        self.critic_output = nn.Linear(256, 1)  # Single value for Critic
        self.predictor_output = nn.Linear(256, 10)  # 10 classes for Predictor

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)  # Flatten
        x = F.relu(self.fc1(x))
        
        # Outputs
        actor_output = self.actor_output(x)
        critic_output = self.critic_output(x)
        predictor_output = self.predictor_output(x)
        
        return actor_output, critic_output, predictor_output
    
model = CNN()
sample_input = torch.randn(1, 1, 32, 32)  # Batch size = 1, 1 channel, 32x32 height map
actor_output, critic_output, predictor_output = model(sample_input)
