# ==============================================================================
# EvoSim
# Copyright © 2016 Elias F. Domingos. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import matplotlib.pyplot as plt
import numpy as np

plt.ion()  # Note this correction
fig = plt.figure()
plt.axis([0, 1000, 0, 1])

i = 0
x = list()
y = list()

while i < 1000:
    temp_y = np.random.random()
    x.append(i)
    y.append(temp_y)
    plt.scatter(i, temp_y)
    i += 1
    plt.show()
    plt.pause(0.0001)  # Note this correction
