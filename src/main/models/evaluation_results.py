class ClusteringResults:

    def __init__(self, number_of_clusters, inertia, avg_sil, dunn, dunn2, entropy, ch, nmi, acc, corrected_rand, f_measure):
        self.number_of_clusters = number_of_clusters
        self.inertia = inertia
        self.avg_sil = avg_sil
        self.dunn = dunn
        self.dunn2 = dunn2
        self.entropy = entropy
        self.ch = ch
        self.nmi = nmi
        self.acc = acc
        self.corrected_rand = corrected_rand
        self.f_measure = f_measure
