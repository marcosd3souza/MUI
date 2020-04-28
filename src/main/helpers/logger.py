

def log(content, enable=True):
    if enable:
        print(content)


def mount_beauty_output(dataset_name, best_silhouette, method, best_nmi, max_nmi, best_acc, max_acc):
    print_final_results = True
    log("======================= final results =================================", print_final_results)
    log("Selection from " + method + " in dataset: " + dataset_name + " was: ", print_final_results)
    log("avg_sil = " + str(best_silhouette), print_final_results)
    log("NMI = " + str(best_nmi), print_final_results)
    log("MAX NMI = " + str(max_nmi), print_final_results)
    log("Acc = " + str(best_acc), print_final_results)
    log("MAX Acc = " + str(max_acc), print_final_results)
    log("=======================================================================", print_final_results)
