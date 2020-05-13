
import phate
import scprep

def run_phate(X):
    phate_op = phate.PHATE()
    data_phate = phate_op.fit_transform(X)
    scprep.plot.scatter2d(data_phate, figsize=(8,6), c=df.index,
                        filename="test.png")
    return data_phate
