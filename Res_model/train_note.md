# **train note**

recommend use typore to view this note

| date | checkpoint        | model                                    | train                                    | loss                                     | result                                | conclusion                               |
| ---- | ----------------- | ---------------------------------------- | ---------------------------------------- | ---------------------------------------- | ------------------------------------- | ---------------------------------------- |
| 7.10 | resnet            | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning fc1, bn, fc2, no dropout, crop image, resize image to 224*112, data enhancement | AdamOptimizer, initial_learning_rate = 0.0001, ecay_rate = 0.1, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin     | step 20000, mAP 0.52                  | baseline                                 |
| 7.11 | resnet_softmax    | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), **softmax**, fine tuning fc1, bn, fc2, no dropout, crop image, resize image to 224*112, data enhancement | AdamOptimizer, initial_learning_rate = 0.0001, **decay_rate = 0.5**, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin     | output festures trend to 0            | softmax is worse                         |
| 7.11 | resnet_no_pool    | resnet50, delete **global pool**, fc, add fc1(1024), bn, relu, fc2(128), fine tuning fc1, bn, fc2, no dropout, crop image, resize image to 224*112, data enhancement | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin,    | output festures trend to 0            | delete global pool is worse              |
| 7.11 | resnet_finetuning | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning **resnet50**, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, data enhancement | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin     | step 15000, mAP 0.88                  | fine turning resnet is pefect            |
| 7.11 | resnet_finetuning | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, data enhancement | **train after resnet_finetuning step 20000**, AdamOptimizer, **initial_learning_rate = 0.000001**, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20 | **batch hardest triplet loss**, soft-margin | step 25000, mAP 0.89                  | batch hardest triplet loss seems no much help |
| 7.11 | resnet_noprecess  | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, **no data enhancement** | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin     | step 30000, mAP 0.92 (train 0.97)     | no data enhancement seems ok, maybe train data set is big enough |
| 7.12 | resnet_enhance    | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, **update data enhancement** | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20 | batch hard triplet loss, soft-margin     | **step 25000, mAP 0.92 (train 0.98)** | update data enhancement seams good       |
| 7.13 | resnet_enhance    | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, update data enhancement, **re-ranking** | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20, **change fc init**, **big valid** | batch hard triplet loss, soft-margin     | step 30000, mAP 0.89 (train 0.98)     | re-ranking is helpful                    |
| 7.14 | resnet_fc         | resnet50, delete fc, **add fc1(128)**, fine tuning resnet50, fc1, no dropout, crop image, resize image to 224*112, update data enhancement, re-ranking | AdamOptimizer, **initial_learning_rate = 1e-6**, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20, **change fc init**, big valid | batch hard triplet loss, soft-margin     | step 15000, mAP 0.78                  | one fc is not good. **fc init should small enough so loss near 0.7!!!** |
| 7.16 | resnet_IDE        | resnet50, delete fc, add fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2,  no dropout, crop image, resize image to **256*128**, update data enhancement,  **re-ranking (no bug)** | AdamOptimizer, initial_learning_rate = 0.0001, **decay_rate = 0.3**, decay_steps = 10000, return_id_num = 20, change fc init, big valid | batch hard triplet loss, soft-margin     | step 5000, mAP 0.4**????**            | big image seems not good                 |
| 7.16 | resnet_maxpool    | resnet50, delete **avg pooling**, fc, add **max pooling**, fc1(1024), bn, relu, fc2(128), fine tuning resnet50, fc1, bn, fc2, **use dropout**, crop image, resize image to 224*112, update data enhancement, re-ranking | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20, change fc init, big valid, **dropout = 0.5** | batch hard triplet loss, soft-margin     | step 30000, mAP 0.18**????**          | dropout is worse                         |
| 7.17 | resnet_256        | resnet50, delete fc, add fc1(1024), bn, relu, **fc2(256)**, fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, update data enhancement, re-ranking | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20, big valid | batch hard triplet loss, soft-margin     | step 5000, mAP 0.41**????**           | big output dim is bad                    |
| 7.18 | resnet_100        | resnet50, delete fc, add fc1(1024), bn, relu, **fc2(100)**, fine tuning resnet50, fc1, bn, fc2, no dropout, crop image, resize image to 224*112, update data enhancement, re-ranking | AdamOptimizer, initial_learning_rate = 0.0001, decay_rate = 0.5, decay_steps = 10000, return_id_num = 20, big valid | batch hard triplet loss, soft-margin     | step 40000, mAP 0.87 (train 0.988)    | dicrease output dim seems just so so     |














