# https://github.com/sgrvinod/a-PyTorch-Tutorial-to-Object-Detection

"""
MIT License

Copyright (c) 2019 Sagar Vinodababu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Used to train the model.
Set variables listed under 'Training parameters'
"""

import time
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data
from model import SSD300, MultiBoxLoss
from datasets import PascalVOCDataset
from obj_utils import *
import sys
import matplotlib.pyplot as plt
from evaluate import evaluate


##############################################
##### Training parameters (change these) #####
##############################################
data_folder = '/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Data_lists'     # Directory containing data lists
save_dir = '/home/chris/Documents/jackal_fyp/src/development/resources/obj_detection/Models'            # Directory to save trained model
batch_size = 6                      # batch size
iterations = 100000                 # number of iterations to train, where 1 iteration = processed 1 batch
print_freq = 1                      # print training status every __ batches
eval_freq = 1                       # evaluate accuracy on test set every __ epochs
checkpoint = None                   # path to model checkpoint, None if none

# Learning parameters
keep_difficult = True               # use objects considered difficult to detect
workers = 4                         # number of workers for loading data in the DataLoader
lr = 1e-3                           # learning rate
decay_lr_at = [80000, 100000]       # decay learning rate after these many iterations
decay_lr_to = 0.1                   # decay learning rate to this fraction of the existing learning rate
momentum = 0.9                      # momentum
weight_decay = 5e-4                 # weight decay
grad_clip = None                    # clip if gradients are exploding, which may happen at larger batch sizes (sometimes at 32) - you will recognize it by a sorting error in the MuliBox loss calculation
loss_list = []                      # list for plotting loss
acc_list = []                       # list for plotting mAP
epoch_list = []                     # corresponding epochs at which mAP is calculated
actual_iters = 0                    # actual number of iterations after rounding
best_acc = 0                        # best accuracy achieved on test set
best_epoch = 0                      # epoch where best accuracy was achieved
cudnn.benchmark = True

# Model parameters
n_classes = len(label_map)  # number of different types of objects

# Set device
if torch.cuda.is_available():
    device = torch.device("cuda")
    print("GPU found.\n")
else:
    device = torch.device("cpu")
    print("Using CPU.\n")

# Check directories
if not os.path.exists(data_folder):
    print("\n[WARNING]: Error accessing [%s]\n" % data_folder)
    sys.exit()

if not os.path.exists(save_dir):
    print("\n[WARNING]: Error accessing [%s]\n" % save_dir)
    sys.exit()

if checkpoint is not None:
    if not os.path.exists(checkpoint):
        print("\n[WARNING]: Error accessing [%s]\n" % checkpoint)
        sys.exit()


def main():
    """
    Training.
    """
    global start_epoch, label_map, epoch, checkpoint, decay_lr_at, epoch_list, actual_iters, acc_list, best_acc, best_epoch

    # Initialize model or load checkpoint
    if checkpoint is None:
        start_epoch = 1
        print("Preparing model...")
        model = SSD300(n_classes=n_classes)

        # Initialize the optimizer, with twice the default learning rate for biases, as in the original Caffe repo
        biases = list()
        not_biases = list()

        for param_name, param in model.named_parameters():
            if param.requires_grad:
                if param_name.endswith('.bias'):
                    biases.append(param)
                else:
                    not_biases.append(param)
        
        print("Preparing optimizer...\n")
        optimizer = torch.optim.SGD(params=[{'params': biases, 'lr': 2 * lr}, {'params': not_biases}],
                                    lr=lr, momentum=momentum, weight_decay=weight_decay)

    else:
        checkpoint = torch.load(checkpoint)
        start_epoch = checkpoint['epoch'] + 1
        print('\nLoaded checkpoint model from epoch %d.\n' % start_epoch)
        model = checkpoint['model']
        optimizer = checkpoint['optimizer']

    # Move to default device
    model = model.to(device)
    print("Preparing loss function...\n")
    criterion = MultiBoxLoss(priors_cxcy=model.priors_cxcy).to(device)

    # Custom dataloaders
    print("\nPreparing dataloaders...\n")
    train_dataset = PascalVOCDataset(
        data_folder,
        split='train',
        keep_difficult=keep_difficult
    )

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=train_dataset.collate_fn,
        num_workers=workers,
        pin_memory=True
    )
    
    test_dataset = PascalVOCDataset(
        data_folder,
        split='test',
        keep_difficult=keep_difficult
    )

    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        collate_fn=test_dataset.collate_fn,
        num_workers=workers,
        pin_memory=True
    )

    # Calculate total number of epochs to train and the epochs to decay learning rate at (i.e. convert iterations to epochs)
    # To convert iterations to epochs, divide iterations by the number of iterations per epoch
    # The paper trains for 120,000 iterations with a batch size of 32, decays after 80,000 and 100,000 iterations
    epochs = iterations // (len(train_dataset) // batch_size)
    decay_lr_at = [it // (len(train_dataset) // batch_size) for it in decay_lr_at]
    actual_iters = epochs*(len(train_dataset) // batch_size)

    # Training loop
    print("\n***** Begin Training *****\n")
    for epoch in range(start_epoch, epochs+1):

        # Decay learning rate at particular epochs
        if epoch in decay_lr_at:
            adjust_learning_rate(optimizer, decay_lr_to)

        # One epoch's training
        train(
            train_loader=train_loader,
            model=model,
            criterion=criterion,
            optimizer=optimizer,
            epoch=epoch,
            n_epochs=epochs
        )

        # Evaluation and model saving
        if epoch % eval_freq == 0:     
            
            # Accuracy on test set
            acc = evaluate(test_loader, model)
            acc_list.append(acc)
            epoch_list.append(epoch)

            if acc > best_acc:
                best_acc = acc
                best_epoch = epoch
            
            # Print info
            print("\n***** Evaluation on Epoch %d *****" % epoch)
            print('Mean Average Precision (mAP): %.3f' % acc)
            
            # Save model
            filename = 'ssd300_epoch{}.pth.tar'.format(epoch)
            path = os.path.join(save_dir, filename)
            save_checkpoint(epoch, model, optimizer, path)
            print("Saved model: %s to %s\n" % (filename, save_dir))


def train(train_loader, model, criterion, optimizer, epoch, n_epochs):
    """
    One epoch's training.

    :param train_loader: DataLoader for training data
    :param model: model
    :param criterion: MultiBox loss
    :param optimizer: optimizer
    :param epoch: epoch number
    """
    global loss_list

    model.train()  # training mode enables dropout

    batch_time = AverageMeter()  # forward prop. + back prop. time
    data_time = AverageMeter()  # data loading time
    losses = AverageMeter()  # loss

    start = time.time()

    # Batches
    for i, (images, boxes, labels, _) in enumerate(train_loader):
        data_time.update(time.time() - start)

        # Move to default device
        images = images.to(device)  # (batch_size (N), 3, 300, 300)
        boxes = [b.to(device) for b in boxes]
        labels = [l.to(device) for l in labels]

        # Forward prop.
        predicted_locs, predicted_scores = model(images)  # (N, 8732, 4), (N, 8732, n_classes)

        # Loss
        loss = criterion(predicted_locs, predicted_scores, boxes, labels)  # scalar
        loss_list.append(loss.item())

        # Backward prop.
        optimizer.zero_grad()
        loss.backward()

        # Clip gradients, if necessary
        if grad_clip is not None:
            clip_gradient(optimizer, grad_clip)

        # Update model
        optimizer.step()

        losses.update(loss.item(), images.size(0))
        batch_time.update(time.time() - start)

        start = time.time()

        # Print status
        if i % print_freq == 0:
            print(
                '[Epoch: %d/%d]\t'
                '[Batch: %d/%d]\t'
                '[Loss (this batch): %.4f]\t'
                '[Loss (avg): %.4f]\t'
                '[Batch Time (this batch): %.4fsec]\t'
                '[Batch Time (avg): %.4fsec]\t' % (
                    epoch,
                    n_epochs,
                    i+1,
                    len(train_loader),
                    losses.val,
                    losses.avg,
                    batch_time.val,
                    batch_time.avg
                )
            )

    del predicted_locs, predicted_scores, images, boxes, labels  # free some memory since their histories may be stored


def plot():
    global actual_iters, epoch_list, loss_list, acc_list

    fig1 = plt.figure()
    plt.plot(range(1, actual_iters+1), loss_list)
    plt.xlabel('Iterations') 
    plt.ylabel('Loss') 
    plt.title('Loss vs Iterations') 
    
    fig2 = plt.figure()
    plt.plot(epoch_list, acc_list)
    plt.xlabel('Epochs') 
    plt.ylabel('mAP') 
    plt.title('mAP vs Epochs') 
    
    plt.show() 


if __name__ == '__main__':
    main()
    print("\n***** FINISHED *****")
    print("Best mAP = %.3f achieved on epoch %d" % (best_acc, best_epoch))
    plot()
