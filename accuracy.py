import editdistance

def accuracy(predicted: str, target: str):
    normalizer = max(len(predicted), len(target))
    if normalizer == 0:
        return 1.0
    return 1 - editdistance.eval(predicted, target) / normalizer

def average_accuracy(net, valid_loader):
    def simplify(str_in):
        return str_in.strip().replace('  ', ' ')

    net.eval()
    
    with torch.no_grad():
        total_accuracy = 0
        num_comparisons = 0
        for i, (images, targets, lengths) in enumerate(valid_loader):
            if i > 1000: break

            images = images.to(device)
            targets = targets.to(device)
            outputs = net(images)
            
            outputs = outputs.permute(1, 0, 2)
            outs_decoded = decode_batch(outputs)
            targets_decoded = [numbers_to_text(t) for t in targets]

            for j in range(len(outs_decoded)):
                decoded_out, target_out = simplify(outs_decoded[j]), simplify(targets_decoded[j])
                total_accuracy += accuracy(decoded_out, target)

            num_comparisons += len(outs_decoded)
            
        average_accuracy = total_accuracy / num_comparisons
        return average_accuracy